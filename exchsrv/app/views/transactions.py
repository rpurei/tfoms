#!python
#cython: language_level=3, always_allow_keywords=True
from . import database_engine
from app.config import ROWS_PER_PAGE, APP_VER, TRANS_OUT_FOLDER
from app.utils.hm_xlsx_converter import xml_hm_parser
from app.tasks.tfoms_statuses import *

from flask import request, current_app, url_for, render_template, redirect, flash, send_from_directory, Blueprint
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_parameter
from app.models.transactions import TransActions, TransActionsLog
from app.models.db import db_exchsrv
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from dict2xml import dict2xml
from shutil import rmtree
from zipfile import ZipFile
from decimal import Decimal
import lxml.etree as et
from sqlalchemy import text
import os

trans_handler = Blueprint('transactions', __name__)


def dct_one_level(dct):
    dct_name = ''
    res_dict = OrderedDict()
    dct_lst = []
    for key, value in dct.items():
        key_lst = key.split('###')
        dct_key = key_lst[1].split('---')[0]
        if dct_name != key_lst[0]:
            if dct_lst:
                res_dict[dct_name] = OrderedDict(dct_lst)
            dct_lst = []
            dct_name = key_lst[0]
            if value:
                dct_lst.append((dct_key, value))
        else:
            if value:
                dct_lst.append((dct_key, value))
        if key == list(dct.items())[-1][0]:
            res_dict[dct_name] = OrderedDict(dct_lst)
    for key, value in res_dict.items():
        print(f'Key: {key} Value: {value}')
    return res_dict


def element_counter(dct, element_name):
    counter = 0
    for key, value in dct.items():
        if key.startswith(element_name):
            counter += 1
    return counter


def lek_pr_getter(dct, lekpr_id):
    lek_pr = []
    converted_dict = dct
    lek_count = element_counter(converted_dict, 'LEK_PR%%%' + str(lekpr_id))
    lek_count_list = list(range(1, lek_count + 1))
    lek_counter = 0
    for key, value in dct.items():
        if value and key == f'LEK_PR%%%{lekpr_id}$$${lek_count_list[lek_counter]}':
            lek_dose = []
            lek_pr_dict = converted_dict[f'LEK_PR%%%{str(lekpr_id)}$$${str(lek_count_list[lek_counter])}']
            dose_count = element_counter(converted_dict, f'LEK_DOSE%%%{str(lekpr_id)}$$${str(lek_count_list[lek_counter])}')
            for dose in range(1, dose_count + 1):
                lek_dose_dict = converted_dict[f'LEK_DOSE%%%{str(lekpr_id)}$$${str(lek_count_list[lek_counter])}***{str(dose)}']
                lek_dose.append(lek_dose_dict)
            if lek_dose:
                lek_pr_dict['LEK_DOSE'] = lek_dose
            lek_pr.append(lek_pr_dict)
            if lek_counter + 1 < len(lek_count_list):
                lek_counter += 1
    return lek_pr


def ds2_getter(dct, sl_id):
    ds2 = []
    ds2_count = element_counter(dct, f'SL%%%{sl_id}###DS2---')
    for ds2_id in range(1, ds2_count + 1):
        ds2.append(dct[f'SL%%%{sl_id}###DS2---{str(ds2_id)}'])
    return ds2


def hm_form_processor(result_items, file_name):
    if Path(result_items.get('filename')).name.startswith('HM'):
        ord_dict = OrderedDict(result_items)
        del (ord_dict['filename'])
        del (ord_dict['transid'])
        #pprint.pprint(ord_dict)
        zap_counter = int(ord_dict['ZGLV###SD_Z'])
        converted_dict = dct_one_level(ord_dict)
        result_xml_dict = OrderedDict()
        result_xml_dict['ZGLV'] = converted_dict['ZGLV']
        result_xml_dict['SCHET'] = converted_dict['SCHET']
        zap_list = []
        for tail in range(1, zap_counter + 1):
            zap_dict = converted_dict['ZAP%%%' + str(tail)]
            zap_dict['PACIENT'] = converted_dict['PACIENT%%%' + str(tail)]
            zap_dict['Z_SL'] = converted_dict['Z_SL%%%' + str(tail)]
            for key, value in zap_dict['Z_SL'].items():
                if key == 'ISHOD':
                    zap_dict['Z_SL']['SL'] = converted_dict['SL%%%' + str(tail)]
                    break
            for key, value in zap_dict['Z_SL']['SL'].items():
                if converted_dict.get(f'KSG_KPG%%%{str(tail)}'):
                    zap_dict['Z_SL']['SL']['KSG_KPG'] = converted_dict[f'KSG_KPG%%%{str(tail)}']
                    ds2_list = ds2_getter(ord_dict, tail)
                    if ds2_list:
                        zap_dict['Z_SL']['SL']['DS2'] = ds2_list
                    break
            if converted_dict.get('LEK_PR%%%' + str(tail) + '$$$1'):
                for key, value in zap_dict['Z_SL']['SL'].items():
                    if key == 'SUM_M' and converted_dict.get('LEK_PR%%%' + str(tail) + '$$$1'):
                        zap_dict['Z_SL']['SL']['LEK_PR'] = lek_pr_getter(converted_dict, tail)
                        break
            if converted_dict.get(f'USL%%%{str(tail)}+++1'):
                for key, value in zap_dict['Z_SL']['SL'].items():
                    if key == 'SUM_M' and converted_dict.get(f'USL%%%{str(tail)}+++1'):
                        usl_count = element_counter(converted_dict, f'USL%%%{str(tail)}+++')
                        usl_list = []
                        for usl_id in range(1, usl_count + 1):
                            usl_dict = converted_dict[f'USL%%%{str(tail)}+++{str(usl_id)}']
                            usl_dict['MR_USL_N'] = converted_dict[f'MR_USL_N%%%{str(tail)}+++{str(usl_id)}']
                            usl_list.append(usl_dict)
                        zap_dict['Z_SL']['SL']['USL'] = usl_list
                        break
            if converted_dict.get(f'SL_KOEF%%%{str(tail)}+++1'):
                slkoef_count = element_counter(converted_dict, f'SL_KOEF%%%{str(tail)}+++')
                slkoef_list = []
                for slkoef_id in range(1, slkoef_count + 1):
                    slkoef_dict = converted_dict[f'SL_KOEF%%%{str(tail)}+++{str(slkoef_id)}']
                    slkoef_list.append(slkoef_dict)
                zap_dict['Z_SL']['SL']['KSG_KPG']['SL_KOEF'] = slkoef_list
            zap_dict['Z_SL'].move_to_end('IDSP')
            zap_dict['Z_SL'].move_to_end('SUMV')
            zap_dict['Z_SL']['SL'].move_to_end('PRVS')
            zap_dict['Z_SL']['SL'].move_to_end('VERS_SPEC')
            zap_dict['Z_SL']['SL'].move_to_end('IDDOKT')
            zap_dict['Z_SL']['SL'].move_to_end('ED_COL')
            zap_dict['Z_SL']['SL'].move_to_end('TARIF')
            zap_dict['Z_SL']['SL'].move_to_end('SUM_M')
            if converted_dict.get('LEK_PR%%%' + str(tail) + '$$$1'):
                zap_dict['Z_SL']['SL'].move_to_end('LEK_PR')
            if converted_dict.get(f'USL%%%{str(tail)}+++1'):
                zap_dict['Z_SL']['SL'].move_to_end('USL')
            if zap_dict['Z_SL']['SL'].get('COMENTSL'):
                zap_dict['Z_SL']['SL'].move_to_end('COMENTSL')
            zap_list.append(zap_dict)
        result_xml_dict['ZAP'] = zap_list
        xml = dict2xml(result_xml_dict, wrap='ZL_LIST', indent="  ")
        new_sum = Decimal('0.00')
        tree = et.ElementTree(et.fromstring(xml))
        tree_root = tree.getroot()
        for zap_item in tree_root.findall('ZAP'):
            zsl_sum = zap_item.find('Z_SL/SUMV')
            new_sum += Decimal(zsl_sum.text)
        schet_item = tree_root.find('SCHET/SUMMAV')
        schet_item.text = str(new_sum)
        tree.write(file_name, encoding='WINDOWS-1251', xml_declaration=True)
        flash(f'Файл {Path(file_name).name} успешно сохранен', 'success')
    elif Path(result_items.get('filename')).name.startswith('LM'):
        flash(f'Редактирование данного файла пока не поддерживается', 'warning')
    else:
        flash(f'Редактирование данного файла пока не поддерживается', 'warning')


def xml_to_dom_processor(file_name):
    xslt = ''
    dom = et.parse(file_name)
    if Path(file_name).name.startswith('HM'):
        xslt = et.parse(os.path.join(os.path.join(current_app.root_path, 'opt', 'templates', 'xsl'), 'HM_XSL.xsl'))
    elif Path(file_name).name.startswith('LM'):
        xslt = et.parse(os.path.join(os.path.join(current_app.root_path, 'opt', 'templates', 'xsl'), 'LM_XSL.xsl'))
    transform = et.XSLT(xslt)
    return transform(dom)


@trans_handler.route('/')
def index_show():
    if current_user.is_authenticated:
        login = current_user.name
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start_at = (page - 1) * ROWS_PER_PAGE
        files_list = []
        files_list_header = ['', 'Имя файла', 'Размер', 'Дата создания']
        result_header = ['', 'Статус', 'Дата', 'Примечание', 'Протокол', 'Пользователь', 'Контур']
        try:
            session_files = os.listdir(current_app.config['UPLOAD_FOLDER'])
            for file in session_files:
                temp = (file,
                        f'<span>{file}</span>',
                        f'{os.path.getsize(os.path.join(current_app.config["UPLOAD_FOLDER"], file)) / 1024:.2f} кБ',
                        str(datetime.fromtimestamp(
                            os.path.getctime(os.path.join(current_app.config['UPLOAD_FOLDER'], file))).strftime(
                            '%d.%m.%Y %H:%M:%S')))
                files_list.append(temp)
            with database_engine.connect() as conn:
                result_count = conn.execute(text(f'SELECT COUNT(*) FROM transactions'))
                for row_count in result_count:
                    count = int(row_count[0])
                result = conn.execute(text(f"""SELECT trans_id,trans_status,trans_date,note,trans_protocol,
                                                         user_name,trans_addr 
                                               FROM transactions 
                                               ORDER BY trans_date DESC LIMIT :limit OFFSET :offset"""),
                                      limit=ROWS_PER_PAGE, offset=start_at)
                pagination = Pagination(page=page, total=count, search=False, record_name='transactions',
                                        per_page=ROWS_PER_PAGE, css_framework='bootstrap4', prev_label='<',
                                        next_label='>', display_msg='')
                result_list = []
                for row in result:
                    result_list.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
        except Exception as err:
            current_app.logger.critical(str(err))
            flash(f'Ошибка: {str(err)}', 'danger')
            return render_template('500.html')
        return render_template('index.html', files_list=files_list, files_list_header=files_list_header, login=login,
                               result_data=result_list, result_header=result_header, pagination=pagination,
                               app_ver=APP_VER)
    else:
        return redirect(url_for('users.auth_login'))


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/processing')
def file_processing(transaction_id):
    login = ''
    result_list = []
    result_header = ['Имя файла', 'Размер', 'Дата создания', 'Статус', 'Лог обработки']
    if current_user.is_authenticated:
        login = current_user.name
    try:
        with database_engine.connect() as conn:
            result = conn.execute(text(f"""SELECT file_name,file_size,file_create,file_status,log 
                                           FROM file_processing 
                                           WHERE trans_id=:trans_id"""), trans_id=transaction_id)
            for row in result:
                edit_url = f"""<div class="col">{Path(row[0]).name}<a href="{url_for("transactions.file_processing_edit", transaction_id=transaction_id, file_name=row[0])}" 
                                                    alt="Показать протокол" style="float: right;"><i class="bi bi-pencil-square btn-outline-danger" 
                                                    style="font-size: 12pt; padding: 5px; border-radius: 4px;"></i></a></div>""" if Path(row[0]).name.startswith('HM') else Path(row[0]).name
                result_list.append([edit_url, f'{row[1] / 1024:.2f} кБ', row[2], row[3], row[4]])
        return render_template('processing.html', login=login, session_id=transaction_id, file_contents=result_list,
                               file_contents_header=result_header)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/printform', methods=['GET'])
def file_printform_show(transaction_id):
    login = ''
    hm_file = ''
    lm_file = ''
    try:
        if current_user.is_authenticated:
            login = current_user.name
        with database_engine.connect() as conn:
            result = conn.execute(text(f"""SELECT file_name,file_size,file_create,file_status,log 
                                           FROM file_processing 
                                           WHERE trans_id=:trans_id"""), trans_id=transaction_id)
            for row in result:
                path = Path(row[0])
                if path.name.startswith('HM'):
                    hm_file = row[0]
                if path.name.startswith('LM'):
                    lm_file = row[0]
            xls_dir = os.path.join(current_app.root_path, 'opt', 'templates', 'xlsx')
            print_form = xml_hm_parser(hm_file, lm_file, xls_dir, path.parent)
            return send_from_directory(os.path.join(current_app.root_path, str(path.parent)[4:]), print_form,
                                       as_attachment=True)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/delete', methods=['POST'])
def transaction_delete(transaction_id):
    try:
        with database_engine.connect() as conn:
            conn.execute(text(f'DELETE FROM transactions WHERE trans_id=:trans_id'), trans_id=transaction_id)
            result_files = conn.execute(text(f'SELECT file_name FROM file_processing WHERE trans_id=:trans_id'),
                                        trans_id=transaction_id)
            delete_path = os.path.join(TRANS_OUT_FOLDER, transaction_id)
            if os.path.exists(delete_path):
                rmtree(delete_path)
            for file_delete in result_files:
                if os.path.exists(file_delete[0]):
                    os.remove(file_delete[0])
            conn.execute(text(f'DELETE FROM file_processing WHERE trans_id=:trans_id'), trans_id=transaction_id)
            conn.execute(text(f'DELETE FROM transactions_logs WHERE trans_id=:trans_id'), trans_id=transaction_id)
        flash(f'Транзакция {transaction_id} и ее файлы удалены', 'success')
        return redirect(url_for('transactions.index_show'))
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/detail', methods=['GET'])
def transaction_detail(transaction_id):
    login = ''
    parent_trans = ''
    result_list_log = []
    result_list_files = []
    result_list_trans = []
    result_header = ['ID', 'Дата', 'Операция']
    result_header_files = ['Имя файла', 'Размер', 'Дата создания', 'Статус', 'Лог обработки']
    result_header_log = ['ИД', 'Статус', 'Дата', 'Примечание', 'Контур', 'Пользователь']
    protocol_url = ''
    protocol_id = ''
    main_tfoms_send_button = ''
    records_edit_button = ''
    out_data = ''
    if current_user.is_authenticated:
        login = current_user.name
    try:
        result = db_exchsrv.session.query(TransActionsLog).filter_by(trans_id=transaction_id)
        for row in result:
            result_list_log.append([row.id, row.trans_date, row.log])
        with database_engine.connect() as conn:
            result = conn.execute(text("""SELECT file_name,file_size,file_create,file_status,log 
                                          FROM file_processing 
                                          WHERE trans_id=:trans_id"""), trans_id=transaction_id)
            for row in result:
                download_url = url_for('files.file_protocol_download', protocol_name=Path(row[0]))
                edit_url = url_for('transactions.file_transaction_edit', transaction_id=transaction_id, file_name=row[0])
                if Path(row[0]).name.startswith('HM'):
                    printform_url = url_for('transactions.file_printform_show', transaction_id=transaction_id)
                else:
                    printform_url = ''
                result_list_files.append([Path(row[0]).name, download_url, edit_url, printform_url,
                                          f'{row[1] / 1024:.2f} кБ', row[2], row[3], row[4]])
        result = db_exchsrv.session.query(TransActions).filter_by(trans_id=transaction_id)
        for row in result:
            protocol_url = row.trans_protocol
            protocol_id = row.protocol_id
            result_list_trans.append([row.trans_id, row.trans_status, row.trans_date, row.note, row.trans_addr,
                                      row.user_name])
            out_data = row.out_data
            parent_trans = row.trans_parent
            if row.trans_status == 'Предварительный МЭК пройден. Получен ответ' or row.trans_status == 'Не удалось выгрузить территориальный счет, он не найден на сервере. Статус его обработки: Предварительный МЭК пройден':
                main_tfoms_send_button = transaction_id
            elif row.trans_status == 'Предварительный МЭК не пройден. Получен протокол ошибок.' or (row.trans_status == TFOMS_FLK_FAIL_STATUS and protocol_url):
                records_edit_button = f'<a class="btn btn-outline-warning" href="{url_for("protocols.transaction_error_edit", transaction_id=transaction_id, protocol_name=protocol_url)}" role="button" style="margin-right: 20px;"><i class="bi bi-filetype-xml"></i> Работа с записями</a>'
        return render_template('trans_detail.html',
                               login=login, result_data=result_list_log,
                               result_header=result_header,
                               result_data_files=result_list_files, result_header_files=result_header_files,
                               result_data_trans=result_list_trans, result_header_trans=result_header_log,
                               protocol_url=protocol_url, send_button=main_tfoms_send_button,
                               records_edit_button=records_edit_button, parent_trans=parent_trans,
                               transaction_id=transaction_id, out_data=out_data, protocol_id=protocol_id)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/send', methods=['GET'])
def transaction_send(transaction_id):
    with database_engine.connect() as conn:
        conn.execute(text(f"""UPDATE transactions SET trans_status=:tr_st,
                                                      trans_addr=:tr_addr,
                                                      protocol_id=:pr_id,
                                                      trans_protocol=:tr_pr 
                              WHERE trans_id=:trans_id"""),
                     tr_st=TFOMS_MAIN_SEND_READY, tr_addr=TFOMS_MAIN_ADDRESS, pr_id='', tr_pr='',
                     trans_id=transaction_id)
    flash(f'Транзакция поставлена в очередь на ОСНОВНОЙ КОНТУР ТФОМС', 'success')
    return redirect(url_for('transactions.transaction_detail', transaction_id=transaction_id))


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/processing/<path:file_name>/edit', methods=['GET'])
def file_processing_edit(transaction_id, file_name):
    login = ''
    if current_user.is_authenticated:
        login = current_user.name
    try:
        newdom = xml_to_dom_processor(file_name)
        return render_template('processing_file_edit.html', login=login, form_data=newdom, trans_id=transaction_id,
                               file_name=file_name)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/file/<path:file_name>/edit', methods=['GET'])
def file_transaction_edit(transaction_id, file_name):
    login = ''
    if current_user.is_authenticated:
        login = current_user.name
    try:
        newdom = xml_to_dom_processor(file_name)
        return render_template('trans_file_edit.html', login=login, form_data=newdom, trans_id=transaction_id,
                               file_name=file_name)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/processing/<path:file_name>/save', methods=['POST'])
def file_processing_save(transaction_id, file_name):
    try:
        result_items = request.form.to_dict()
        hm_form_processor(result_items, file_name)
        return redirect(url_for('transactions.file_processing', transaction_id=transaction_id))
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/file/<path:file_name>/save', methods=['POST'])
def file_transaction_save(transaction_id, file_name):
    try:
        result_items = request.form.to_dict()
        hm_form_processor(result_items, file_name)
        files_list = []
        with database_engine.connect() as conn:
            result = conn.execute(text(f"""SELECT in_data FROM transactions WHERE trans_id=:trans_id"""),
                                  trans_id=transaction_id)
            for row in result:
                zip_file_name = row[0]
            result = conn.execute(text("""SELECT file_name FROM file_processing WHERE trans_id=:trans_id"""),
                                  trans_id=transaction_id)
            for row in result:
                files_list.append(row[0])
            with ZipFile(zip_file_name, 'w') as zipObj:
                for file in files_list:
                    zipObj.write(file, arcname=os.path.basename(file))
        return redirect(url_for('transactions.transaction_detail', transaction_id=transaction_id))
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/status/check', methods=['POST'])
def transaction_status_check(transaction_id):
    try:
        with database_engine.connect() as conn:
            conn.execute(text(f"""UPDATE transactions 
                                  SET trans_status=:tr_st
                                  WHERE trans_id=:trans_id"""), trans_id=transaction_id, tr_st='Запрос статуса')
        flash('Транзакция поставлена в очередь на запрос статуса', 'info')
        return redirect(url_for('transactions.transaction_detail', transaction_id=transaction_id))
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/resend', methods=['POST'])
def transaction_resend(transaction_id):
    try:
        with database_engine.connect() as conn:
            result = conn.execute(text(f"""SELECT trans_addr FROM transactions WHERE trans_id=:trans_id"""),
                                  trans_id=transaction_id)
            for row in result:
                if row[0] == TFOMS_MAIN_ADDRESS:
                    trans_status = TFOMS_MAIN_SEND_READY
                else:
                    trans_status = TFOMS_TEST_SEND_READY
            conn.execute(text(f"""UPDATE transactions 
                                  SET trans_status=:tr_st,protocol_id=:pr_id,trans_protocol=:tr_pr
                                  WHERE trans_id=:trans_id"""), trans_id=transaction_id, tr_st=trans_status,
                                                                   pr_id='', tr_pr='')
        flash('Транзакция поставлена в очередь на повторную отправку', 'info')
        return redirect(url_for('transactions.transaction_detail', transaction_id=transaction_id))
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@trans_handler.route('/transaction/<path:transaction_id>/stop', methods=['POST'])
def transaction_stop(transaction_id):
    try:
        with database_engine.connect() as conn:
            conn.execute(text(f"""UPDATE transactions 
                                  SET trans_status=:tr_st
                                  WHERE trans_id=:trans_id"""), trans_id=transaction_id,
                                                                tr_st='Остановлена пользователем')
        flash('Обработка транзакции остановлена пользователем', 'info')
        return redirect(url_for('transactions.transaction_detail', transaction_id=transaction_id))
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')
