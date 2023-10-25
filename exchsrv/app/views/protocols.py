#!python
#cython: language_level=3, always_allow_keywords=True
from . import database_engine
from app.views.files import filelog_add
from app.utils.file_fixer import (xmlfile_nzap_adder, xmlfile_pers_adder, xmlfile_pers_remover, xmlfile_nzap_remover,
                                  xmlerror_parser)

from flask import current_app, render_template, flash, request, send_from_directory, url_for, Blueprint
from flask_login import login_required, current_user
from pathlib import Path
from hashlib import md5
from datetime import datetime
from shutil import copyfile
from zipfile import ZipFile
import lxml.etree as et
import os
import sqlalchemy as db

protocols_handler = Blueprint('protocols', __name__)


@login_required
@protocols_handler.route('/transaction/<path:transaction_id>/protocol/<path:protocol_name>/show', methods=['GET'])
def file_protocol_show(transaction_id, protocol_name):
    login = ''
    file_path = Path(protocol_name)
    if current_user.is_authenticated:
        login = current_user.name
    try:
        file_xml = os.path.join(os.path.join(current_app.root_path, str(file_path.parent)[4:]), file_path.name)
        file_xsl = os.path.join(os.path.join(current_app.root_path, 'opt', 'templates', 'xsl'), 'FLK_XSL.xsl')
        dom = et.parse(file_xml)
        xslt = et.parse(file_xsl)
        transform = et.XSLT(xslt)
        newdom = transform(dom)
        return render_template('protocol.html', protocol_data=newdom, login=login, transaction_id=transaction_id,
                               protocolname=protocol_name)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@protocols_handler.route('/transaction/<path:transaction_id>/protocol/<path:protocol_name>/records/delete',
                         methods=['GET'])
def transaction_error_edit(transaction_id, protocol_name):
    login = ''
    file_path = Path(protocol_name)
    if current_user.is_authenticated:
        login = current_user.name
    try:
        file_xml = os.path.join(os.path.join(current_app.root_path, str(file_path.parent)[4:]), file_path.name)
        file_xsl = os.path.join(os.path.join(current_app.root_path, 'opt', 'templates', 'xsl'), 'FLK_XSL_edit.xsl')
        dom = et.parse(file_xml)
        xslt = et.parse(file_xsl)
        transform = et.XSLT(xslt)
        newdom = transform(dom)
        return render_template('protocol_error.html', protocol_data=newdom, login=login, transaction_id=transaction_id,
                               protocol_name=protocol_name)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@protocols_handler.route('/transaction/<path:transaction_id>/protocol/records/processing', methods=['POST'])
def transaction_error_processing(transaction_id):
    try:
        form_args = request.form.to_dict()
        excluded_list = []
        file_processing_log = ''
        file_processing_status = ''
        for key, value in form_args.items():
            if key.startswith('N_ZAP') and value == 'on':
                excluded_list.append(key.split('###')[1])
        hm_file = ''
        lm_file = ''
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT file_name FROM file_processing WHERE trans_id=:trans_id'),
                                  trans_id=transaction_id)
        for file in result:
            if Path(file[0]).name.startswith('HM'):
                hm_file = file[0]
            if Path(file[0]).name.startswith('LM'):
                lm_file = file[0]
        new_session_id = md5(datetime.now().strftime('%d.%m.%Y %H:%M:%S').encode('utf-8')).hexdigest()
        new_session_dir = os.path.join(current_app.config['TRANS_OUT_FOLDER'], new_session_id)
        Path(new_session_dir).mkdir(parents=True, exist_ok=True)
        new_hm_file = os.path.join(new_session_dir, Path(hm_file).name)
        new_lm_file = os.path.join(new_session_dir, Path(lm_file).name)
        if os.path.exists(new_session_dir):
            copyfile(hm_file, new_hm_file)
            copyfile(lm_file, new_lm_file)
            files_list = [new_hm_file, new_lm_file]
            lm_count = xmlfile_pers_remover(new_hm_file, new_lm_file, excluded_list)
            hm_count = xmlfile_nzap_remover(new_hm_file, excluded_list)
            file_transaction_dict_list = []
            for new_file in files_list:
                file_path = Path(new_file)
                if file_path.name.startswith('HM'):
                    if hm_count != -1:
                        file_processing_log = f'Изменено записей: {hm_count}'
                        file_processing_status = 'Ошибок нет'
                    else:
                        file_processing_log = f''
                        file_processing_status = 'Ошибка обработки'
                elif file_path.name.startswith('LM'):
                    if hm_count != -1:
                        file_processing_log = f'Изменено записей: {lm_count}'
                        file_processing_status = 'Ошибок нет'
                    else:
                        file_processing_log = f''
                        file_processing_status = 'Ошибка обработки'
                file_transaction_dict = {'file_name': new_file, 'file_size': file_path.stat().st_size,
                                         'file_create': datetime.fromtimestamp(file_path.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                                         'file_status': file_processing_status, 'file_log': file_processing_log,
                                         'trans_id': new_session_id}
                filelog_add(file_transaction_dict)
                file_transaction_dict_list.append(file_transaction_dict)
            login = ''
            result_list = []
            result_header = ['Имя файла', 'Размер', 'Дата создания', 'Статус', 'Лог обработки']
            if current_user.is_authenticated:
                login = current_user.name
            for file_dict in file_transaction_dict_list:
                edit_url = f"""<div class="col">{Path(file_dict['file_name']).name}<a href="{url_for("transactions.file_processing_edit", transaction_id=new_session_id, file_name=file_dict['file_name'])}" 
                               alt="Показать протокол" style="float: right;"><i class="bi bi-pencil-square btn-outline-danger" 
                               style="font-size: 12pt; padding: 5px; border-radius: 4px;"></i></a></div>""" if Path(file_dict['file_name']).name.startswith('HM') else Path(file_dict['file_name']).name
                result_list.append([edit_url, f'{file_dict["file_size"] / 1024:.2f} кБ', file_dict['file_create'], file_dict['file_status'], file_dict['file_log']])
            return render_template('processing.html', login=login, session_id=new_session_id,
                                   trans_parent=transaction_id, file_contents=result_list,
                                   file_contents_header=result_header)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@protocols_handler.route('/transaction/<path:transaction_id>/protocol/records/errors/get', methods=['POST'])
def transaction_error_get(transaction_id):
    try:
        form_args = request.form.to_dict()
        included_list = []
        for key, value in form_args.items():
            if key.startswith('N_ZAP') and value == 'on':
                included_list.append(key.split('###')[1])
        hm_file = ''
        lm_file = ''
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT file_name FROM file_processing WHERE trans_id=:trans_id'),
                                  trans_id=transaction_id)
        for file in result:
            if Path(file[0]).name.startswith('HM'):
                hm_file = file[0]
            elif Path(file[0]).name.startswith('LM'):
                lm_file = file[0]
        hm_file_tmp = xmlfile_nzap_adder(hm_file, included_list)
        lm_file_tmp = xmlfile_pers_adder(hm_file, lm_file, included_list)
        files_list = [hm_file_tmp, lm_file_tmp]
        dir_name = os.path.join(current_app.root_path, str(Path(hm_file).parent)[4:])
        zip_name = Path(hm_file).name[:-4] + '_из_протокола_ошибок.zip'
        with ZipFile(os.path.join(dir_name, zip_name), 'w') as zipObj:
            for file in files_list:
                zipObj.write(file, arcname=os.path.basename(file[:-4]))
        return send_from_directory(dir_name, zip_name, as_attachment=True)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@protocols_handler.route('/transaction/<path:transaction_id>/protocol/<path:protocol_name>/records/xlsx/download',
                     methods=['GET'])
def transaction_protocol_xlsx_get(transaction_id, protocol_name):
    try:
        hm_file = ''
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT file_name FROM file_processing WHERE trans_id=:trans_id'),
                                  trans_id=transaction_id)
        for file in result:
            if Path(file[0]).name.startswith('HM'):
                hm_file = file[0]
        xlsx_file = xmlerror_parser(protocol_name, hm_file)
        return send_from_directory(os.path.join(current_app.root_path, str(Path(protocol_name).parent)[4:]), xlsx_file,
                                   as_attachment=True)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')
