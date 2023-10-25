#!python
#cython: language_level=3, always_allow_keywords=True
from . import database_engine
from app.tasks.tfoms_statuses import *
from app.config import SEND_FILES
from app.models.db import db_exchsrv
from app.models.files import FileProcessing
from app.models.transactions import TransActions
from app.utils.file_fixer import xml_fixer

from flask import current_app, request, flash, redirect, render_template, url_for, send_from_directory, Blueprint
from flask_login import login_required, current_user
from hashlib import md5
from os import remove, listdir
from os.path import exists, join, isfile, basename
from datetime import datetime
from werkzeug.utils import secure_filename
from pathlib import Path
from zipfile import ZipFile
import sqlalchemy as db
from shutil import move


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def filelog_add(filedata_dict):
    file_add = FileProcessing(filedata_dict['trans_id'], filedata_dict['file_name'], filedata_dict['file_size'],
                              filedata_dict['file_create'], filedata_dict['file_status'], filedata_dict['file_log'],
                              filedata_dict['file_flags'])
    db_exchsrv.session.add(file_add)
    db_exchsrv.session.commit()


def transaction_add(transaction_dict):
    trans_action = TransActions(transaction_dict['trans_id'], transaction_dict['trans_status'],
                                transaction_dict['in_data'], transaction_dict['note'], transaction_dict['user_name'],
                                transaction_dict['trans_addr'], transaction_dict['trans_parent'])
    db_exchsrv.session.add(trans_action)
    db_exchsrv.session.commit()


files_handler = Blueprint('files', __name__)


@login_required
@files_handler.route('/files/upload', methods=['POST', 'GET'])
def upload_file():
    file_list_converted = []
    if request.method == 'POST':
        try:
            uploaded_files = request.files.getlist("files[]")
            session_id = md5(datetime.now().strftime('%d.%m.%Y %H:%M:%S').encode('utf-8')).hexdigest()
            existing_files = [f for f in listdir(current_app.config['UPLOAD_FOLDER']) if
                              isfile(join(current_app.config['UPLOAD_FOLDER'], f))]
            for file in existing_files:
                if exists(file):
                    remove(file)
            if len(uploaded_files) == 1:
                for file in uploaded_files:
                    if file and allowed_file(file.filename):
                        filename = join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                        if exists(filename):
                            remove(filename)
                        file.save(filename)
                        if filename.endswith('.zip'):
                            with ZipFile(filename, 'r') as zipObj:
                                zipObj.extractall(current_app.config['UPLOAD_FOLDER'])
                            if exists(filename):
                                remove(filename)
                    else:
                        flash('При загрузке 1 файла - он должен быть в формате ZIP', 'danger')
                        return redirect(url_for('transactions.index_show'))
            elif len(uploaded_files) == SEND_FILES:
                for file in uploaded_files:
                    if file and allowed_file(file.filename):
                        filename = join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                        if exists(filename):
                            remove(filename)
                        file.save(filename)
                    else:
                        flash('Ошибка загрузки, выбран неподдерживаемый тип файла', 'danger')
                        return redirect(url_for('transactions.index_show'))
            else:
                flash(f'Количество отправляемых файлов должно быть: {SEND_FILES} файла XML, либо 1 файл ZIP', 'danger')
                return render_template('index.html')
            xml_files = [join(current_app.config['UPLOAD_FOLDER'], f) for f in
                         listdir(current_app.config['UPLOAD_FOLDER'])
                         if isfile(join(current_app.config['UPLOAD_FOLDER'], f))]
            xml_counter = 0
            for f in xml_files:
                if f.endswith('.xml'):
                    xml_counter += 1
            if xml_counter != 2:
                flash(f'Количество отправляемых файлов должно быть: {SEND_FILES} файла XML', 'danger')
                return render_template('index.html')
            else:
                for filename in xml_files:
                    conversion_result = xml_fixer(filename)
                    conversion_result['trans_id'] = session_id
                    file_list_converted.append(filename)
                    filelog_add(conversion_result)
            return redirect(url_for('transactions.file_processing', transaction_id=session_id))
        except Exception as err:
            current_app.logger.critical(str(err))
            flash(f'Ошибка: {str(err)}', 'danger')
            return render_template('500.html')
    elif request.method == 'GET':
        return redirect(url_for('transactions.index_show'))


@login_required
@files_handler.route('/files/send', methods=['POST'])
def file_send():
    session_id = request.form.get('session_id')
    file_note = request.form.get('file_note')
    parent_id = request.form.get('trans_parent')
    trans_dict = dict()
    trans_dict['trans_id'] = session_id
    trans_dict['trans_status'] = TFOMS_TEST_SEND_READY
    trans_dict['note'] = file_note
    if current_user.is_authenticated:
        trans_dict['user_name'] = current_user.name
    trans_dict['trans_addr'] = TFOMS_TEST_ADDRESS
    trans_dict['trans_parent'] = parent_id
    result = db_exchsrv.session.query(TransActions).filter_by(trans_id=session_id)
    counter = 0
    for _ in result:
        counter += 1
    if counter == 0 and session_id:
        try:
            Path(join(current_app.config['TRANS_OUT_FOLDER'], session_id)).mkdir(parents=True, exist_ok=True)
            with database_engine.connect() as conn:
                result = conn.execute(db.text(f'SELECT * FROM file_processing WHERE trans_id=:session_id'),
                                      session_id=session_id)
                files_list = []
                zipfile_name = ''
                for row in result:
                    new_dir = join(current_app.config['TRANS_OUT_FOLDER'], session_id)
                    files_list.append(join(new_dir, Path(row[2]).name))
                    if not zipfile_name.startswith('HM'):
                        zipfile_name = Path(row[2]).name[:-4] if Path(row[2]).name.startswith('HM') else session_id
                    if exists(new_dir):
                        move(row[2], join(new_dir, Path(row[2]).name))
                        conn.execute(db.text(f"""UPDATE file_processing 
                                                 SET file_name=:new_file_name 
                                                 WHERE trans_id=:session_id AND file_name=:old_file_name"""),
                                     new_file_name=join(new_dir, Path(row[2]).name), old_file_name=row[2],
                                     session_id=session_id)
                new_filename = join(new_dir, f'{zipfile_name}.zip')
                with ZipFile(new_filename, 'w') as zipObj:
                    for file in files_list:
                        zipObj.write(file, arcname=basename(file))
            if exists(new_filename):
                trans_dict['in_data'] = new_filename
                transaction_add(trans_dict)
                flash(f'Транзакция {session_id} поставлена в очередь отправки', 'success')
                current_app.logger.info(f'Транзакция {session_id} поставлена в очередь отправки')
        except Exception as err:
            current_app.logger.critical(str(err))
            flash(f'Ошибка: {str(err)}', 'danger')
            return render_template('500.html')
    elif counter > 0:
        current_app.logger.critical('Данный файл уже был обработан')
        flash('Данный файл уже был обработан', 'danger')
    return redirect(url_for('transactions.index_show'))


@login_required
@files_handler.route('/files/delete', methods=['POST'])
def file_delete():
    file_delete_list = request.form.getlist('file_delete')
    try:
        for file in file_delete_list:
            delete_filename = join(current_app.config['UPLOAD_FOLDER'], file)
            if exists(delete_filename):
                remove(delete_filename)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(str(err), 'danger')
    return redirect(url_for('transactions.index_show'))


@login_required
@files_handler.route('/files/<path:name>/download', methods=['GET'])
def file_download(name):
    safe_path = join(current_app.root_path, 'uploads')
    try:
        return send_from_directory(safe_path, name, as_attachment=True)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@files_handler.route('/files/protocol/<path:protocol_name>/download', methods=['GET'])
def file_protocol_download(protocol_name):
    file_path = Path(protocol_name)
    try:
        return send_from_directory(join(current_app.root_path, str(file_path.parent)[4:]),
                                   file_path.name, as_attachment=True)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@files_handler.route('/files/transaction/<path:transaction_id>/zip/download', methods=['POST'])
def file_zip_download(transaction_id):
    try:
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT * FROM file_processing WHERE trans_id=:session_id'),
                                  session_id=transaction_id)
            files_list = []
            zipfile_name = ''
            for row in result:
                current_dir = join(current_app.config['TRANS_OUT_FOLDER'], transaction_id)
                files_list.append(join(current_dir, Path(row[2]).name))
                if not zipfile_name.startswith('HM'):
                    zipfile_name = Path(row[2]).name[:-4] if Path(row[2]).name.startswith('HM') else transaction_id
            new_filename = join(current_dir, f'{zipfile_name}.zip')
            with ZipFile(new_filename, 'w') as zipObj:
                for file in files_list:
                    zipObj.write(file, arcname=basename(file))
            return send_from_directory(join(current_app.root_path, str(current_dir)[4:]),
                                       Path(new_filename).name, as_attachment=True)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')
