#!python
#cython: language_level=3, always_allow_keywords=True
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as et
from flask import current_app
from decimal import *
from os import remove
from os.path import exists, join
from csv import writer
from pandas import read_csv
from collections import Counter
from copy import deepcopy

move_elements_list = ['PRVS', 'CODE_MD']
tail_12 = '\n            '
tail_8 = '\n        '


def xmlfile_ver_mr_fixer(file_name):
    counter = 0
    try:
        tree = et.parse(file_name)
        tree_root = tree.getroot()
        data_item = tree_root.find('ZGLV/DATA')
        if data_item.text.startswith('2022') or data_item.text.startswith('2023'):
            version_item = tree_root.find('ZGLV/VERSION')
            if version_item.text != '3.2':
                counter += 1
                version_item.text = '3.2'
        for item in tree_root.findall('ZAP/Z_SL/SL'):
            zsl_ds1 = item.find('DS1')
            if zsl_ds1.text == 'U07.1' or zsl_ds1.text == 'U07.2':
                if item.find('WEI') is None:
                    counter += 1
                    if item.find('KD'):
                        target_element = item.find('KD')
                        insert_index = list(item).index(target_element) + 1
                    else:
                        target_element = item.find('DATE_2')
                        insert_index = list(item).index(target_element) + 1
                    target_element = None
                    wei_el = et.Element('WEI')
                    wei_el.tail = tail_8
                    item.insert(insert_index, wei_el)
        for item in tree_root.findall('ZAP/Z_SL/SL/USL'):
            if not item.find('MR_USL_N'):
                counter += 1
                sub_el = et.SubElement(item, 'MR_USL_N')
                sub_el.text = tail_12
                sub_el.tail = tail_8
                subsub_el_mr = et.SubElement(sub_el, 'MR_N')
                subsub_el_mr.text = '1'
                subsub_el_mr.tail = tail_12
                for element in move_elements_list:
                    subsub_el = et.SubElement(sub_el, element)
                    subsub_el.tail = tail_12 if element != 'CODE_MD' else tail_8 + '  '
                    subsub_el.text = item.find(element).text
                for element in move_elements_list:
                    el_rem = item.find(element)
                    item.remove(el_rem)
        tree.write(file_name, encoding='WINDOWS-1251', xml_declaration=True)
    except Exception as err:
        counter = -1
        current_app.logger.critical(f'IN FUNCTION xmlfile_ver_mr_fixer() ERROR: {str(err)}')
    return counter


def xmlfile_flags_analyzer(file_name):
    result_flags = ''
    try:
        tree = et.parse(file_name)
        tree_root = tree.getroot()
        for item in tree_root.findall('ZAP/Z_SL'):
            usl_ok = item.find('USL_OK')
            if usl_ok:
                if usl_ok.text == '1':
                    zsl_ds1 = item.find('SL/DS1')
                    if zsl_ds1:
                        if zsl_ds1.text == 'U07.1' or zsl_ds1.text == 'U07.2':
                            result_flags += 'covid_19;'
        tree.write(file_name, encoding='WINDOWS-1251', xml_declaration=True)
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION xmlfile_flags_analyzer() ERROR: {str(err)}')
    return result_flags


def xmlfile_usl_covid_fixer(file_name):
    counter = 0
    try:
        tree = et.parse(file_name)
        tree_root = tree.getroot()
        for item_sl in tree_root.findall('ZAP/Z_SL/SL'):
            for item_usl in item_sl.findall('USL'):
                if item_usl.find('CODE_USL').text == 'A26.08.027.001':
                    counter += 1
                    item_usl_copy = deepcopy(item_usl)
                    item_usl_copy.find('IDSERV').text = hex(int(item_usl.find('IDSERV').text,
                                                                16) + 1).upper()[2:].zfill(32)
                    item_usl_copy.find('CODE_USL').text = 'A26.08.046.001'
                    item_usl_copy.find('TARIF').text = '0'
                    item_usl_copy.find('SUMV_USL').text = '0'
                    item_sl.insert(list(item_sl).index(item_usl) + 1, item_usl_copy)
                    new_col = float(item_sl.find('ED_COL').text) + 1
                    item_sl.find('ED_COL').text = str(round(new_col, 2))
        tree.write(file_name, encoding='WINDOWS-1251', xml_declaration=True)
    except Exception as err:
        counter = -1
        current_app.logger.critical(f'IN FUNCTION xmlfile_usl_covid_fixer() ERROR: {str(err)}')
    return counter


def xml_fixer(file_name_input):
    try:
        file_path = Path(file_name_input)
        # file_ext = file_path.suffix
        # file_name = file_path.stem
        # file_dir = file_path.parent
        file_log = ''
        file_status = ''
        file_name = file_name_input
        file_size = file_path.stat().st_size
        file_create = datetime.fromtimestamp(file_path.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        file_flags = xmlfile_flags_analyzer(file_name_input)
        rows_count_mr = xmlfile_ver_mr_fixer(file_name_input)
        rows_count_usl_covid = xmlfile_usl_covid_fixer(file_name_input)
        if rows_count_mr != -1 and rows_count_usl_covid != -1:
            file_log = f'Изменено записей: {rows_count_mr + rows_count_usl_covid}'
            file_status = 'Ошибок нет'
        elif rows_count_mr == -1 or rows_count_usl_covid == -1:
            file_log = f''
            file_status = 'Ошибка обработки'
        result_dict = {'file_name': file_name, 'file_size': file_size, 'file_create': file_create,
                       'file_status': file_status, 'file_log': file_log, 'file_flags': file_flags}
        return result_dict
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION xml_fixer() ERROR: {str(err)}')


def xmlfile_nzap_remover(file_name_protocol, nzap_list):
    counter = 0
    try:
        tree = et.parse(file_name_protocol)
        tree_root = tree.getroot()
        for zap_item in tree_root.findall('ZAP'):
            nzap = zap_item.find('N_ZAP')
            if nzap.text in nzap_list:
                tree_root.remove(zap_item)
                counter += 1
        new_counter = 1
        new_sum = Decimal('0.00')
        for zap_item in tree_root.findall('ZAP'):
            nzap = zap_item.find('N_ZAP')
            nzap.text = str(new_counter)
            new_counter += 1
            zsl_sum = zap_item.find('Z_SL/SUMV')
            new_sum += Decimal(zsl_sum.text)
        zglv_item = tree_root.find('ZGLV/SD_Z')
        zglv_item.text = str(new_counter - 1)
        schet_item = tree_root.find('SCHET/SUMMAV')
        schet_item.text = str(new_sum)
        tree.write(file_name_protocol, encoding='WINDOWS-1251', xml_declaration=True)
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION xmlfile_nzap_remover() ERROR: {str(err)}')
        counter = -1
    return counter


def xmlfile_pers_remover(hm_file_name, lm_file_name, nzap_list):
    counter = 0
    try:
        remove_pers_list = []
        zap_to_delete_dict = {}
        zap_all_dict = {}
        tree_hm = et.parse(hm_file_name)
        tree_hm_root = tree_hm.getroot()
        for zap_item in tree_hm_root.findall('ZAP'):
            nzap = zap_item.find('N_ZAP')
            id_pac = zap_item.find('PACIENT/ID_PAC')
            zap_all_dict[nzap.text] = id_pac.text
            if nzap.text in nzap_list:
                zap_to_delete_dict[nzap.text] = id_pac.text
        all_dict_count = Counter(zap_all_dict.values())
        delete_dict_count = Counter(zap_to_delete_dict.values())
        for ipac, count in delete_dict_count.items():
            if all_dict_count[ipac] == count:
                remove_pers_list.append(ipac)
        tree_lm = et.parse(lm_file_name)
        tree_lm_root = tree_lm.getroot()
        for pers_item in tree_lm_root.findall('PERS'):
            id_pac = pers_item.find('ID_PAC')
            if id_pac.text in remove_pers_list:
                tree_lm_root.remove(pers_item)
                counter += 1
        tree_lm.write(lm_file_name, encoding='WINDOWS-1251', xml_declaration=True)
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION zap_pd_analyzer() ERROR: {str(err)}')
        counter = -1
    return counter


def xmlfile_nzap_adder(file_name_protocol, nzap_list):
    try:
        tree = et.parse(file_name_protocol)
        tree_root = tree.getroot()
        new_tree = et.Element('ZL_LIST')
        new_tree.text = '\n  '
        new_zglv = tree_root.find('ZGLV')
        new_tree.append(new_zglv)
        schet_item = tree_root.find('SCHET')
        new_tree.append(schet_item)
        for zap_item in tree_root.findall('ZAP'):
            nzap = zap_item.find('N_ZAP')
            if nzap.text in nzap_list:
                new_tree.append(zap_item)
        new_counter = 1
        new_sum = Decimal('0.00')
        for zap_item in new_tree.findall('ZAP'):
            nzap = zap_item.find('N_ZAP')
            nzap.text = str(new_counter)
            new_counter += 1
            zsl_sum = zap_item.find('Z_SL/SUMV')
            new_sum += Decimal(zsl_sum.text)
        zglv_item = new_tree.find('ZGLV/SD_Z')
        zglv_item.text = str(new_counter - 1)
        schet_item = new_tree.find('SCHET/SUMMAV')
        schet_item.text = str(new_sum)
        tree_root = et.ElementTree(new_tree)
        new_path = file_name_protocol + '_TMP'
        tree_root.write(new_path, encoding='WINDOWS-1251', xml_declaration=True)
        return new_path
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION xmlfile_nzap_adder() ERROR: {str(err)}')
        counter = -1
    return counter


def xmlfile_pers_adder(hm_file_name, lm_file_name, nzap_list):
    try:
        add_pers_list = []
        tree_hm = et.parse(hm_file_name)
        tree_hm_root = tree_hm.getroot()
        for zap_item in tree_hm_root.findall('ZAP'):
            nzap = zap_item.find('N_ZAP')
            id_pac = zap_item.find('PACIENT/ID_PAC')
            if nzap.text in nzap_list:
                add_pers_list.append(id_pac.text)
        tree_lm = et.parse(lm_file_name)
        tree_lm_root = tree_lm.getroot()
        new_tree = et.Element('PERS_LIST')
        new_tree.text = '\n  '
        new_zglv = tree_lm_root.find('ZGLV')
        new_tree.append(new_zglv)
        for pers_item in tree_lm_root.findall('PERS'):
            id_pac = pers_item.find('ID_PAC')
            if id_pac.text in add_pers_list:
                new_tree.append(pers_item)
        new_tree_root = et.ElementTree(new_tree)
        new_path = lm_file_name + '_TMP'
        new_tree_root.write(new_path, encoding='WINDOWS-1251', xml_declaration=True)
        return new_path
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION zap_pd_analyzer() ERROR: {str(err)}')


def xmlerror_parser(file_error_protocol, file_xml_protocol):
    counter = 0
    try:
        protocol_dir = Path(file_error_protocol).parent
        tree = et.parse(file_error_protocol)
        tree_root = tree.getroot()
        tree_in = et.parse(file_xml_protocol)
        tree_root_in = tree_in.getroot()
        for item in tree_root.findall('PR'):
            sub_el = et.SubElement(item, 'IB')
            sub = item.find('SL_ID')
            for ib_item in tree_root_in.findall('ZAP/Z_SL/SL'):
                search_item = ib_item.find('SL_ID')
                if search_item.text == sub.text:
                    counter += 1
                    nhistory = ib_item.find('NHISTORY')
                    sub_el.text = nhistory.text
        filename_csv = join(protocol_dir, tree_root.find('FNAME').text + '.csv')
        with open(filename_csv, 'w', encoding='cp1251') as csvfile:
            csvfile_writer = writer(csvfile, dialect='excel', delimiter=';')
            csvfile_writer.writerow(['OSHIB', 'NSCHET', 'BAS_EL', 'N_ZAP', 'ID_PAC', 'IDCASE', 'SL_ID', 'COMMENT',
                                     'IB'])
            for row in tree_root.findall('PR'):
                if row:
                    oshib = row.find('OSHIB')
                    nschet = row.find('NSCHET')
                    bas_el = row.find('BAS_EL')
                    n_zap = row.find('N_ZAP')
                    id_pac = row.find('ID_PAC')
                    idcase = row.find('IDCASE')
                    sl_id = row.find('SL_ID')
                    comment = row.find('COMMENT')
                    ib = row.find('IB')
                    csvfile_writer.writerow([oshib.text, nschet.text, bas_el.text, n_zap.text, id_pac.text,
                                             idcase.text, sl_id.text, comment.text, ib.text])
        read_file = read_csv(filename_csv, encoding='cp1251', delimiter=';')
        filename_xlsx = filename_csv[:-4] + '.xlsx'
        read_file.to_excel(filename_xlsx, index=False, header=True)
        if exists(filename_csv):
            remove(filename_csv)
        return Path(filename_xlsx).name
    except Exception as err:
        current_app.logger.critical(f'IN FUNCTION xmlerror_parser() ERROR: {str(err)}')
        counter = -1
    return counter
