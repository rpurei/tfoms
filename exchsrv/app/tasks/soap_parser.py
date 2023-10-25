#!python
#cython: language_level=3, always_allow_keywords=True
from app.config import TRANS_IN_FOLDER

from requests import post
from bs4 import BeautifulSoup
from base64 import b64encode, decodebytes
from random import choices
from string import ascii_uppercase, digits
from os.path import join, exists
from os import listdir, remove
from zipfile import ZipFile
from xmltodict3 import XmlTextToDict
from shutil import rmtree
from pathlib import Path


def b64_encoder(file_name):
    result = {}
    try:
        with open(file_name, 'rb') as f:
            data = f.read()
            result['data'] = b64encode(data).decode('ascii')
    except Exception as err:
        result['error'] = str(err)
    return result


def unzip_attachment(file_name):
    dir_name = file_name[:-4]
    result = {}
    try:
        with ZipFile(file_name, 'r') as zipObj:
            zipObj.extractall(dir_name)
        session_files = listdir(dir_name)
        for file in session_files:
            xml_file = join(dir_name, file)
            with open(xml_file, 'r', encoding='cp1251') as f:
                result['zip'] = file_name
                result[file] = XmlTextToDict(f.read(), ignore_namespace=True).get_dict()
                result['path'] = join(file_name[:-4], file)
            if file == 'ProtocolStatus.xml' or file == 'ProtocolDeliveredToServer.xml':
                if exists(dir_name):
                    rmtree(dir_name)
            if exists(file_name):
                remove(file_name)
    except Exception as err:
        result['file_error'] = str(err)
    return result


def soap_parser(req_data, parse_fields_dict, transid_folder):
    result = {}
    try:
        response = post(req_data['service'], data=req_data['request'].encode('utf8'), headers=req_data['headers'])
        parser = BeautifulSoup(response.content.decode('utf8'), 'lxml')
        for field, record_type in parse_fields_dict.items():
            if record_type == 'string':
                if parser.find(field):
                    result[field] = parser.find(field).string
            elif record_type == 'file':
                if parser.find(field):
                    dir_name = join(TRANS_IN_FOLDER, transid_folder)
                    Path(dir_name).mkdir(exist_ok=True)
                    file_name = join(dir_name, ''.join(choices(ascii_uppercase + digits, k=8)) + '.zip')
                    with open(file_name, 'wb') as f:
                        f.write(decodebytes(parser.find(field).string.encode('utf8')))
                    result = unzip_attachment(file_name)
    except Exception as err:
        result['SOAP_error'] = str(err)
    return result
