#!python
#cython: language_level=3, always_allow_keywords=True
from .soap_request import (authservice_getservicetoken, getservicetoken_fields,
                           protservice_sendprotocolmo, sendprotocolmo_fields,
                           protservice_getprotocolstatusmo, getprotocolstatusmo_fields,
                           protservice_getprotocolformo, getprotocolformo_fields,
                           protservice_getprotocolerrormo, getprotocolerrorsmo_fields)
from .soap_parser import soap_parser, b64_encoder
from app.config import LOCAL_DATABASE_URI, TFOMS_LOGIN, TFOMS_PASSWORD, TFOMS_UNID
from .tfoms_statuses import *

from datetime import datetime, timezone, timedelta
from flask import current_app
import sqlalchemy as db
from flask_crontab import Crontab

crontab = Crontab()

database_engine = db.create_engine(LOCAL_DATABASE_URI, echo=True)
tzinfo = timezone(timedelta(hours=3.0))


def get_token(transaction_row_id):
    current_token = ''
    try:
        with database_engine.connect() as conn:
            result = conn.execute(db.text("""SELECT token,token_date,trans_id FROM transactions WHERE id=:tr_row_id"""),
                                  tr_row_id=transaction_row_id)
            for row in result:
                try:
                    transaction_id = row[2]
                    db_token = row[0]
                    dt = datetime.fromisoformat(str(row[1])) if row[1] else ''
                    if row[0] == '' or dt == '' or (datetime.now() - dt) > timedelta(minutes=19):
                        request_token = authservice_getservicetoken(TFOMS_LOGIN, TFOMS_PASSWORD)
                        response_data = soap_parser(request_token, getservicetoken_fields, transaction_id)
                        if not response_data.get('error'):
                            current_app.logger.info(f'GET_TOKEN TRID {transaction_id} RESPONSE: {response_data}')
                            current_token = response_data.get('a:token')
                            date_field = response_data.get('a:expireddate').split('T')
                            token_date = date_field[0] + ' ' + date_field[1].split('.')[0]
                            conn.execute(db.text("""UPDATE transactions 
                                                    SET token=:tok_cur,token_date=:tok_dt 
                                                    WHERE id=:tr_rw_id"""),
                                         tok_cur=current_token, tok_dt=token_date, tr_rw_id=transaction_row_id)
                            conn.execute(db.text(f"""INSERT INTO transactions_logs (trans_id,trans_date,log) 
                                                     VALUES ('{transaction_id}','{datetime.now(tzinfo)}',
                                        'Запрошен новый токен, истекает: {token_date}')"""))
                        elif response_data.get('exception') or response_data.get('SOAP_error'):
                            exchange_error_message = 'Ошибка:' + (str(response_data.get('exception') or '') + ' ' +
                                                                  str(response_data.get('SOAP_error') or ''))
                            conn.execute(db.text(f"""UPDATE transactions 
                                                     SET trans_status='Ошибка',out_data='{exchange_error_message}' 
                                                     WHERE id={transaction_id}"""))
                            conn.execute(db.text(f"""INSERT INTO transactions_logs (trans_id,trans_date,log) 
                                                     VALUES ('{transaction_id}','{datetime.now(tzinfo)}','{exchange_error_message}')"""))
                            current_app.logger.critical(
                                f'ERROR PROCESSING TRID {transaction_id}: {exchange_error_message}')
                    elif db_token != '' and (datetime.now() - dt) < timedelta(minutes=19):
                        current_token = db_token
                        current_app.logger.info(f'USING OLD TOKEN TRID {transaction_id}')
                except Exception as err:
                    current_app.logger.critical(f'IN FUNCTION get_token() for TRID {transaction_id} ERROR: {str(err)}')
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION get_token() ERROR: {str(err)}')
    return current_token


def send_protocol_test():
    try:
        log_prefix = 'ТСТ'
        with database_engine.connect() as conn:
            result = conn.execute(db.text("""SELECT * FROM transactions 
                                             WHERE trans_status=:tr_st AND trans_addr=:tr_addr"""),
                                  tr_st=TFOMS_TEST_SEND_READY, tr_addr=TFOMS_TEST_ADDRESS)
            for row in result:
                try:
                    transaction_id = row[1]
                    current_token = get_token(row[0])
                    if current_token:
                        file_base64 = b64_encoder(row[6])
                        if file_base64.get('error'):
                            current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} FILE: {file_base64.get("error")}')
                        else:
                            request_send = protservice_sendprotocolmo(current_token, TFOMS_UNID, file_base64.get('data'))
                            protocol_response = soap_parser(request_send, sendprotocolmo_fields, transaction_id)
                            conn.execute(db.text(f"""INSERT INTO transactions_logs (trans_id,trans_date,log) 
                                                     VALUES ('{transaction_id}','{datetime.now(tzinfo)}','{log_prefix} Протокол отправлен')"""))
                            current_app.logger.info(f'SEND PROTOCOL TRID {transaction_id} RESPONSE: {protocol_response}')
                            if protocol_response.get('ProtocolDeliveredToServer.xml'):
                                protocol_id = protocol_response['ProtocolDeliveredToServer.xml']['Answer']['ProtocolUNID']
                                protocol_info = protocol_response['ProtocolDeliveredToServer.xml']['Answer']['Information']
                                conn.execute(db.text(f'UPDATE transactions SET protocol_id="{protocol_id}",trans_status="{protocol_info}",out_data="{protocol_response["ProtocolDeliveredToServer.xml"]}" WHERE id={row[0]}'))
                                conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","{log_prefix} Протокол получен ТФОМС, ответ: {protocol_response["ProtocolDeliveredToServer.xml"]}")'))
                            else:
                                exchange_error_message = 'Ошибка:' + (str(protocol_response.get('exception') or '') + ' ' + str(protocol_response.get('SOAP_error') or ''))
                                conn.execute(db.text(f"""UPDATE transactions 
                                                         SET trans_status='{exchange_error_message}' 
                                                         WHERE id={row[0]}"""))
                                conn.execute(db.text(f"""INSERT INTO transactions_logs (trans_id,trans_date,log) 
                                                         VALUES ('{transaction_id}',{datetime.now(tzinfo)},'{log_prefix} {exchange_error_message}')"""))
                                current_app.logger.critical(f'PROTOCOL STSTUS TRID {transaction_id} ERROR: {exchange_error_message}')
                    else:
                        current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} - NO TOKEN')
                except Exception as err:
                    current_app.logger.critical(f'IN FUNCTION send_protocol_test() for TRID {transaction_id} ERROR: {str(err)}')
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION send_protocol_test() ERROR: {str(err)}')


def get_protocol_status_test():
    try:
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT * FROM transactions WHERE (trans_status LIKE "{TFOMS_BILL_REG_FLK_STATUS}" OR trans_status LIKE "{TFOMS_FLK_FAIL_STATUS}" OR trans_status LIKE "{TFOMS_BILL_WAIT_STATUS}" OR trans_status LIKE "{TFOMS_FLK_SUCCESS_STATUS}" OR trans_status LIKE "%{TFOMS_PRE_MEK_SUCCESS_STATUS}" OR trans_status LIKE "{TFOMS_PRE_MEK_FAIL_STATUS}") AND trans_addr="{TFOMS_TEST_ADDRESS}"'))
            for row in result:
                try:
                    transaction_id = row[1]
                    current_token = get_token(row[0])
                    protocol_id = row[8]
                    if current_token:
                        if protocol_id:
                            request_get_protocolstatus = protservice_getprotocolstatusmo(current_token, TFOMS_UNID,
                                                                                         protocol_id)
                            protocol_status_response = soap_parser(request_get_protocolstatus,
                                                                   getprotocolstatusmo_fields,
                                                                   transaction_id)
                            conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ТСТ Запрос статуса протокола №{protocol_id} отправлен")'))
                            current_app.logger.info(f'GET_PROTOCOL_STATUS RESPONSE TRID {transaction_id}: {protocol_status_response}')
                            if protocol_status_response.get('ProtocolStatus.xml'):
                                protocol_status = protocol_status_response['ProtocolStatus.xml']['PROTOCOL_STATUS']['NAME']
                                conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}" WHERE id={row[0]}'))
                                conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ТСТ Получен статус протокола №{protocol_id}: {protocol_status}")'))
                                if protocol_status == 'Счет ожидает обработки' or protocol_status == 'ФЛК пройден':
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}"')
                                elif protocol_status == TFOMS_FLK_FAIL_STATUS:
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}"')
                                    request_get_protocolerrorstatus = protservice_getprotocolerrormo(current_token,
                                                                                                     TFOMS_UNID,
                                                                                                     protocol_id)
                                    protocol_error_response = soap_parser(request_get_protocolerrorstatus,
                                                                          getprotocolerrorsmo_fields, transaction_id)
                                    current_app.logger.info(f'PROTOCOL ERROR FLK TRID {transaction_id}: {protocol_error_response}')
                                    if protocol_error_response:
                                        conn.execute(db.text(f'UPDATE transactions SET trans_status="{TFOMS_FLK_FAIL_STATUS}. Получен протокол ошибок", out_data="",trans_protocol="{protocol_error_response["path"]}" WHERE id={row[0]}'))
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ТСТ Получен протокол ошибок: {protocol_error_response["path"]}")'))
                                elif protocol_status == 'Предварительный МЭК не пройден':
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}"')
                                    request_get_protocol = protservice_getprotocolformo(current_token, TFOMS_UNID,
                                                                                        protocol_id)
                                    protocol_response = soap_parser(request_get_protocol, getprotocolformo_fields,
                                                                    transaction_id)
                                    current_app.logger.info(f'PROTOCOL ERROR MEK TRID {transaction_id}: {protocol_response}')
                                    err_protocol = protocol_response.get('PreliminaryMekErrors.xml')
                                    if err_protocol:
                                        conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}. Получен протокол ошибок.",out_data="",trans_protocol="{protocol_response.get("path")}" WHERE id={row[0]}'))
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ТСТ Получен протокол: {protocol_response.get("path")}")'))
                                    elif protocol_response.get('exception') or protocol_response.get('SOAP_error'):
                                        conn.execute(db.text(f'UPDATE transactions SET out_data="Ошибка: {str(protocol_response.get("exception") or "") + " " + str(protocol_response.get("SOAP_error") or "")}" WHERE id={row[0]}'))
                                elif protocol_status == 'Предварительный МЭК пройден':
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}"')
                                    request_get_protocol = protservice_getprotocolformo(current_token, TFOMS_UNID,
                                                                                        protocol_id)
                                    protocol_response = soap_parser(request_get_protocol, getprotocolformo_fields,
                                                                    transaction_id)
                                    current_app.logger.info(f'GET PROTOCOL MEK TRID {transaction_id}: {protocol_response}')
                                    prot_path = protocol_response.get('path')
                                    if prot_path:
                                        conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}. Получен ответ",out_data="",trans_protocol="{prot_path}" WHERE id={row[0]}'))
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ТСТ Получен ответ: {prot_path}")'))
                                    elif protocol_response.get('exception') or protocol_response.get('SOAP_error'):
                                        conn.execute(db.text(f'UPDATE transactions SET trans_status="{str(protocol_response.get("exception") or "")}",out_data="{str(protocol_response.get("exception") or "") + " " + str(protocol_response.get("SOAP_error") or "")}" WHERE id={row[0]}'))
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ТСТ Получен ответ: {str(protocol_response.get("exception") or "") + " " + str(protocol_response.get("SOAP_error") or "")}")'))
                                    else:
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ТСТ Получен ответ: {protocol_response}")'))
                                else:
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}" ANSWER: {protocol_response}')
                                    conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}",out_data="{protocol_response}" WHERE id={row[0]}'))
                                    conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ТСТ Получен ответ: {protocol_response}")'))
                            elif protocol_status_response.get('exception') or protocol_status_response.get('SOAP_error'):
                                conn.execute(db.text(f'UPDATE transactions SET out_data="Ошибка: {str(protocol_status_response.get("exception") or "") + " " + str(protocol_status_response.get("SOAP_error") or "")}" WHERE id={row[0]}'))
                        else:
                            current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} - NO TOKEN')
                except Exception as err:
                    current_app.logger.critical(f'IN FUNCTION get_protocol_status_test() for TRID {transaction_id} ERROR : {str(err)}')
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION get_protocol_status_test() ERROR TRID {transaction_id}: {str(err)}')


def send_protocol_combat():
    try:
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT * FROM transactions WHERE trans_status="{TFOMS_MAIN_SEND_READY}" AND trans_addr="{TFOMS_MAIN_ADDRESS}"'))
            for row in result:
                try:
                    transaction_id = row[1]
                    current_token = get_token(row[0])
                    if current_token:
                        file_base64 = b64_encoder(row[6])
                        if file_base64.get('error'):
                            current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} FILE: {file_base64.get("error")}')
                        else:
                            request_send_protocolmo = protservice_sendprotocolmo(current_token, TFOMS_UNID,
                                                                                 file_base64.get('data'), contur=446)
                            protocol_response = soap_parser(request_send_protocolmo, sendprotocolmo_fields, transaction_id)
                            conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Протокол отправлен")'))
                            current_app.logger.info(f'SEND PROTOCOL RESPONSE: {protocol_response}')
                            if protocol_response.get('ProtocolDeliveredToServer.xml'):
                                protocol_id = protocol_response['ProtocolDeliveredToServer.xml']['Answer']['ProtocolUNID']
                                protocol_info = protocol_response['ProtocolDeliveredToServer.xml']['Answer']['Information']
                                conn.execute(db.text(f'UPDATE transactions SET protocol_id="{protocol_id}",trans_status="{protocol_info}",out_data="{protocol_response["ProtocolDeliveredToServer.xml"]}" WHERE id={row[0]}'))
                                conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Протокол получен ТФОМС, получен ответ: {protocol_response["ProtocolDeliveredToServer.xml"]}")'))
                            else:
                                conn.execute(db.text(f'UPDATE transactions SET trans_status="{str(protocol_response.get("exception") or "") + " " + str(protocol_response.get("SOAP_error") or "")}" WHERE id={row[0]}'))
                                conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Ошибка: {str(protocol_response.get("exception") or "") + " " + str(protocol_response.get("SOAP_error") or "")}")'))
                                current_app.logger.critical(f'GET PROTOCOL STATUS ERROR: {str(protocol_response.get("exception")) + " " + str(protocol_response.get("SOAP_error"))}"')
                    else:
                        current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} - NO TOKEN')
                except Exception as err:
                    current_app.logger.critical(f'IN FUNCTION send_protocol_combat() for for TRID {transaction_id} ERROR: {str(err)}')
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION send_protocol_combat() ERROR: {str(err)}')


def get_protocol_status_combat():
    try:
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT * FROM transactions WHERE (trans_status LIKE "{TFOMS_BILL_REG_FLK_STATUS}" OR trans_status LIKE "{TFOMS_FLK_FAIL_STATUS}" OR trans_status LIKE "Счет ожидает обработки" OR trans_status LIKE "ФЛК пройден" OR trans_status LIKE "Предварительный МЭК пройден" OR trans_status LIKE "Предварительный МЭК не пройден") AND trans_addr="{TFOMS_MAIN_ADDRESS}"'))
            for row in result:
                try:
                    transaction_id = row[1]
                    current_token = get_token(row[0])
                    protocol_id = row[8]
                    if current_token:
                        if protocol_id:
                            request_get_protocolstatus = protservice_getprotocolstatusmo(current_token, TFOMS_UNID,
                                                                                         protocol_id,
                                                                                         contur=446)
                            protocol_status_response = soap_parser(request_get_protocolstatus,
                                                                   getprotocolstatusmo_fields,
                                                                   transaction_id)
                            conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Запрос статуса протокола №{protocol_id} отправлен")'))
                            current_app.logger.info(f'GET_PROTOCOL_STATUS RESPONSE TRID {transaction_id}: {protocol_status_response}')
                            if protocol_status_response.get('ProtocolStatus.xml'):
                                protocol_status = protocol_status_response['ProtocolStatus.xml']['PROTOCOL_STATUS']['NAME']
                                conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}" WHERE id={row[0]}'))
                                conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Получен статус протокола №{protocol_id}: {protocol_status}")'))
                                if protocol_status == 'Счет ожидает обработки' or protocol_status == 'ФЛК пройден':
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}"')
                                elif protocol_status == TFOMS_FLK_FAIL_STATUS:
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}"')
                                    request_get_protocolerrorstatus = protservice_getprotocolerrormo(current_token,
                                                                                                     TFOMS_UNID,
                                                                                                     protocol_id,
                                                                                                     contur=446)
                                    protocol_error_response = soap_parser(request_get_protocolerrorstatus,
                                                                          getprotocolerrorsmo_fields, transaction_id)
                                    current_app.logger.info(f'PROTOCOL ERROR FLK TRID {transaction_id}: {protocol_error_response}')
                                    if protocol_error_response:
                                        conn.execute(db.text(f'UPDATE transactions SET trans_status="{TFOMS_FLK_FAIL_STATUS}. Получен протокол ошибок",out_data="",trans_protocol="{protocol_error_response["path"]}" WHERE id={row[0]}'))
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Получен протокол ошибок: {protocol_error_response["path"]}")'))
                                elif protocol_status == 'Предварительный МЭК не пройден':
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}"')
                                    request_get_protocol = protservice_getprotocolformo(current_token, TFOMS_UNID,
                                                                                        protocol_id,
                                                                                        contur=446)
                                    protocol_response = soap_parser(request_get_protocol, getprotocolformo_fields,
                                                                    transaction_id)
                                    current_app.logger.info(f'PROTOCOL ERROR MEK TRID {transaction_id}: {protocol_response}')
                                    err_protocol = protocol_response.get('PreliminaryMekErrors.xml')
                                    if err_protocol:
                                        conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}. Получен протокол ошибок.",out_data="",trans_protocol="{protocol_response.get("path")}" WHERE id={row[0]}'))
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Получен протокол: {protocol_response.get("path")}")'))
                                    elif protocol_response.get('exception') or protocol_response.get('SOAP_error'):
                                        conn.execute(db.text(f'UPDATE transactions SET out_data="Ошибка: {str(protocol_response.get("exception") or "") + " " + str(protocol_response.get("SOAP_error") or "")}" WHERE id={row[0]}'))
                                elif protocol_status == 'Предварительный МЭК пройден':
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}"')
                                    request_get_protocol = protservice_getprotocolformo(current_token, TFOMS_UNID,
                                                                                        protocol_id,
                                                                                        contur=446)
                                    protocol_response = soap_parser(request_get_protocol, getprotocolformo_fields,
                                                                    transaction_id)
                                    current_app.logger.info(f'GET PROTOCOL MEK TRID {transaction_id}: {protocol_response}')
                                    prot_path = protocol_response.get('path')
                                    if prot_path:
                                        conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}. Получен ответ",out_data="",trans_protocol="{prot_path}" WHERE id={row[0]}'))
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Получен ответ: {prot_path}")'))
                                    elif protocol_response.get('exception') or protocol_response.get('SOAP_error'):
                                        conn.execute(db.text(f'UPDATE transactions SET trans_status="{str(protocol_response.get("exception") or "")}",out_data="{str(protocol_response.get("exception") or "") + " " + str(protocol_response.get("SOAP_error") or "")}" WHERE id={row[0]}'))
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Получен ответ: {str(protocol_response.get("exception") or "") + " " + str(protocol_response.get("SOAP_error") or "")}")'))
                                    else:
                                        conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Получен ответ: {protocol_response}")'))
                                else:
                                    current_app.logger.info(f'PROTOCOL STATUS TRID {transaction_id}: "{protocol_status}" ANSWER: {protocol_response}')
                                    conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}",out_data="{protocol_response}" WHERE id={row[0]}'))
                                    conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","ОСН Получен ответ: {protocol_response}")'))
                            elif protocol_status_response.get('exception') or protocol_status_response.get('SOAP_error'):
                                conn.execute(db.text(f'UPDATE transactions SET out_data="Ошибка: {str(protocol_status_response.get("exception") or "") + " " + str(protocol_status_response.get("SOAP_error") or "")}" WHERE id={row[0]}'))
                        else:
                            current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} - NO TOKEN')
                except Exception as err:
                    current_app.logger.critical(
                        f'IN FUNCTION get_protocol_status_test() for TRID {transaction_id} ERROR: {str(err)}')
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION get_protocol_status_test() ERROR TRID {transaction_id}: {str(err)}')


def get_transaction_status():
    try:
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT * FROM transactions WHERE trans_status LIKE "Запрос статуса"'))
            contur = 447
            contur_prefix = 'ТСТ'
            for row in result:
                try:
                    transaction_id = row[1]
                    current_token = get_token(row[0])
                    protocol_id = row[8]
                    if current_token:
                        if protocol_id:
                            if row[12] == TFOMS_MAIN_ADDRESS:
                                contur = 446
                                contur_prefix = 'ОСН'
                            request_get_protocolstatus = protservice_getprotocolstatusmo(current_token, TFOMS_UNID,
                                                                                         protocol_id, contur)
                            protocol_status_response = soap_parser(request_get_protocolstatus,
                                                                   getprotocolstatusmo_fields, transaction_id)
                            current_app.logger.info(f'PROCESSING TRID {transaction_id} TFOMS RESPONSE: {protocol_status_response}')
                            if protocol_status_response.get('ProtocolStatus.xml'):
                                protocol_status = protocol_status_response['ProtocolStatus.xml']['PROTOCOL_STATUS']['NAME']
                                conn.execute(db.text(f'UPDATE transactions SET trans_status="{protocol_status}" WHERE id={row[0]}'))
                                conn.execute(db.text(f'INSERT INTO transactions_logs (trans_id,trans_date,log) VALUES ("{transaction_id}","{datetime.now(tzinfo)}","{contur_prefix} Получен статус протокола №{protocol_id}: {protocol_status}")'))
                            elif protocol_status_response.get('exception') or protocol_status_response.get('SOAP_error'):
                                conn.execute(db.text(f'UPDATE transactions SET out_data="Ошибка: {str(protocol_status_response.get("exception") or "") + " " + str(protocol_status_response.get("SOAP_error") or "")}" WHERE id={row[0]}'))
                        else:
                            current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} - NO PROTOCOL ID')
                    else:
                        current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} - NO TOKEN')
                except Exception as err:
                    current_app.logger.critical(f'IN FUNCTION get_transaction_status() for TRID {transaction_id} ERROR: {str(err)}')
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION get_transaction_status() ERROR TRID {transaction_id}: {str(err)}')


def get_mek_passed_protocol():
    try:
        with database_engine.connect() as conn:
            result = conn.execute(db.text(f'SELECT * FROM transactions WHERE trans_status LIKE "Запрос статуса"'))
            for row in result:
                transaction_id = row[1]
                current_token = get_token(row[0])
                protocol_id = row[8]
                if current_token:
                    if protocol_id:
                        request_get_protocol = protservice_getprotocolformo(current_token, TFOMS_UNID, protocol_id,
                                                                            contur=446)
                        protocol_response = soap_parser(request_get_protocol, getprotocolformo_fields, transaction_id)
                        current_app.logger.info(f'PROTOCOL ERROR MEK TRID {transaction_id}: {protocol_response}')
                    else:
                        current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} - NO PROTOCOL ID')
                else:
                    current_app.logger.critical(f'ERROR PROCESSING TRID {transaction_id} - NO TOKEN')
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION get_mek_passed_protocol() ERROR TRID {transaction_id}: {str(err)}')


@crontab.job(minute='*/5')
def check_transactions_test():
    send_protocol_test()
    get_protocol_status_test()


@crontab.job(minute='*/7')
def check_transactions_combat():
    send_protocol_combat()
    get_protocol_status_combat()


@crontab.job(minute='*/3')
def check_transactions_manual():
    get_transaction_status()
