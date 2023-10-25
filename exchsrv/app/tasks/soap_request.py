#!python
#cython: language_level=3, always_allow_keywords=True

getservicetoken_fields = {'a:expireddate': 'string', 'a:token': 'string', 'exception': 'string'}
getserviceuserprofile_fields = {'getserviceuserprofileresult': 'file', 'exception': 'string'}
sendprotocolmo_fields = {'sendprotocolmoresult': 'file', 'exception': 'string'}
getprotocolstatusmo_fields = {'getprotocolstatusmoresult': 'file', 'exception': 'string'}
getprotocolerrorsmo_fields = {'getprotocolerrorsmoresult': 'file', 'exception': 'string'}
getprotocolformo_fields = {'getprotocolformoresult': 'file', 'exception': 'string'}


def authservice_getservicetoken(user_login, user_password):
    return {'service': 'http://tfoms2020.vipnet:1900/AuthService',
            'request': f"""
                        <s11:Envelope xmlns:s11='http://schemas.xmlsoap.org/soap/envelope/'>
                          <s11:Body>
                            <ns1:GetServiceToken xmlns:ns1='http://tempuri.org/'>
                              <ns1:login>{user_login}</ns1:login>
                              <ns1:psw>{user_password}</ns1:psw>
                              <ns1:orgType>MO</ns1:orgType>
                            </ns1:GetServiceToken>
                          </s11:Body>
                        </s11:Envelope>
                      """,
            'headers': {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': 'http://tempuri.org/IAuthContract/GetServiceToken'}}


def authservice_getserviceuserprofile(token):
    return {'service': 'http://tfoms2020.vipnet:1900/AuthService',
            'request': f"""
                            <s11:Envelope xmlns:s11='http://schemas.xmlsoap.org/soap/envelope/'>
                              <s11:Body>
                                <ns1:GetServiceUserProfile xmlns:ns1='http://tempuri.org/'>
                                  <ns1:serviceToken>{token}</ns1:serviceToken>
                                </ns1:GetServiceUserProfile>
                              </s11:Body>
                            </s11:Envelope>
                        """,
            'headers': {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': 'http://tempuri.org/IAuthContract/GetServiceUserProfile'}}


def authservice_getlogs(key, date_from, date_to):
    return {'service': 'http://tfoms2020.vipnet:1900/AuthService',
            'request': f"""
                        <s11:Envelope xmlns:s11='http://schemas.xmlsoap.org/soap/envelope/'>
                          <s11:Body>
                            <ns1:GetLogs xmlns:ns1='http://tempuri.org/'>
                              <ns1:key>{key}</ns1:key>
                              <ns1:dateFrom>{date_from}</ns1:dateFrom>
                              <ns1:dateTo>{date_to}</ns1:dateTo>
                            </ns1:GetLogs>
                          </s11:Body>
                        </s11:Envelope>
                                    """,
            'headers': {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': 'http://tempuri.org/IAuthContract/GetLogs'}}


def protservice_sendprotocolmo(token, mocode, file, contur=447):
    return {'service': f'http://tfoms2020.vipnet:{contur}/ProtService',
            'request': f"""
                        <s11:Envelope xmlns:s11='http://schemas.xmlsoap.org/soap/envelope/'>
                          <s11:Body>
                            <ns1:SendProtocolMO xmlns:ns1='http://tempuri.org/'>
                              <ns1:token>{token}</ns1:token>
                              <ns1:MOCode>{mocode}</ns1:MOCode>
                              <ns1:data>{file}</ns1:data>
                            </ns1:SendProtocolMO>
                          </s11:Body>
                        </s11:Envelope>
                                    """,
            'headers': {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': 'http://tempuri.org/IProtContract/SendProtocolMO'}}


def protservice_getprotocolstatusmo(token, mocode, protocol_id, contur=447):
    return {'service': f'http://tfoms2020.vipnet:{contur}/ProtService',
            'request': f"""
                            <s11:Envelope xmlns:s11='http://schemas.xmlsoap.org/soap/envelope/'>
                              <s11:Body>
                                <ns1:GetProtocolStatusMO xmlns:ns1='http://tempuri.org/'>
                                  <ns1:token>{token}</ns1:token>
                                  <ns1:MOCode>{mocode}</ns1:MOCode>
                                  <ns1:protUNID>{protocol_id}</ns1:protUNID>
                                </ns1:GetProtocolStatusMO>
                              </s11:Body>
                            </s11:Envelope>
                                        """,
            'headers': {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': 'http://tempuri.org/IProtContract/GetProtocolStatusMO'}}


def protservice_getprotocolerrormo(token, mocode, protocol_id, contur=447):
    return {'service': f'http://tfoms2020.vipnet:{contur}/ProtService',
            'request': f"""
                            <s11:Envelope xmlns:s11='http://schemas.xmlsoap.org/soap/envelope/'>
                              <s11:Body>
                                <ns1:GetProtocolErrorsMO xmlns:ns1='http://tempuri.org/'>
                                  <ns1:token>{token}</ns1:token>
                                  <ns1:MOCode>{mocode}</ns1:MOCode>
                                  <ns1:protUNID>{protocol_id}</ns1:protUNID>
                                </ns1:GetProtocolErrorsMO>
                              </s11:Body>
                            </s11:Envelope>
                                            """,
            'headers': {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': 'http://tempuri.org/IProtContract/GetProtocolErrorsMO'}}


def protservice_getprotocolformo(token, mocode, protocol_id, contur=447):
    return {'service': f'http://tfoms2020.vipnet:{contur}/ProtService',
            'request': f"""
                            <s11:Envelope xmlns:s11='http://schemas.xmlsoap.org/soap/envelope/'>
                              <s11:Body>
                                <ns1:GetProtocolForMO xmlns:ns1='http://tempuri.org/'>
                                  <ns1:token>{token}</ns1:token>
                                  <ns1:MOCode>{mocode}</ns1:MOCode>
                                  <ns1:protUNID>{protocol_id}</ns1:protUNID>
                                </ns1:GetProtocolForMO>
                              </s11:Body>
                            </s11:Envelope>
                                            """,
            'headers': {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': 'http://tempuri.org/IProtContract/GetProtocolForMO'}}
