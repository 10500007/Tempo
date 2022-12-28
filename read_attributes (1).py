""" This script read values through the PI Web API.

    This python script requires some pre-requisites:
        1.  A back-end server with PI WEB API with CORS enabled.
"""

import json
from os import PRIO_PGRP
import requests
from urllib.parse import urlparse
from funcoesgerais.constantes import *
from funcoesgerais.Funcoespi import call_security_method

OSI_AF_ATTRIBUTE_TAG = 'Montante'
OSI_AF_DATABASE = 'Controle Hidraulico'
OSI_AF_ELEMENT = 'ULAJ'


def call_headers(include_content_type):
    """ Create API call headers
        @includeContentType boolean: Flag determines whether or not the
        content-type header is included
    """
    if include_content_type is True:
        header = {
            'content-type': 'application/json',
            'X-Requested-With': 'XmlHttpRequest'
        }
    else:
        header = {
            'X-Requested-With': 'XmlHttpRequest'
        }

    return header



def read_attribute_snapshot(piwebapi_url, asset_server, user_name, user_password,
                            piwebapi_security_method, verify_ssl):
    """ Read a single value
        @param piwebapi_url string: The URL of the PI Web API
        @param asset_server string: Name of the Asset Server
        @param user_name string: The user's credentials name
        @param user_password string: The user's credentials password
        @param piwebapi_security_method string: Security method: basic or kerberos
        @param verify_ssl: If certificate verification will be performed
    """
    # print('antes')
    # request_url = "https://sts.edp.pt/adfs/oauth2/authorize?response_type=code&client_id=claimsxrayclient&resource=urn:microsoft:adfs:claimsxray&redirect_uri=https://adfshelp.microsoft.com/ClaimsXray/TokenResponse"  
    # print(requests.get(request_url).text)
    # return str(requests.get(request_url).text)
    #  create security method - basic or kerberos
    security_method = call_security_method(
        piwebapi_security_method, user_name, user_password)
    
    print('apos autentificacao')

    #  Get the sample tag
    request_url = '{}/attributes?path=\\\\{}\\{}\\{}|{}'.format(
        piwebapi_url, asset_server, OSI_AF_DATABASE, OSI_AF_ELEMENT, OSI_AF_ATTRIBUTE_TAG)
    print(request_url)
    response = requests.get(request_url, auth=security_method, verify=verify_ssl)
    print('response:')
    print(response)
    #  Only continue if the first request was successful
    if response.status_code == 200:
        print(response.text)
        #  Deserialize the JSON Response
        data = json.loads(response.text)

        url = urlparse(piwebapi_url + '/streams/' + data['WebId'] + '/value')
        # Validate URL
        assert url.scheme == 'https'
        assert url.geturl().startswith(piwebapi_url)

        #  Read the single stream value
        response = requests.get(url.geturl(),
                                auth=security_method, verify=verify_ssl)

        if response.status_code == 200:
            print('{} Snapshot Value'.format(OSI_AF_ATTRIBUTE_TAG))
            print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))
        else:
            print(response.status_code, response.reason, response.text)
    else:
        print(response.status_code, response.reason, response.text)
    return str(response.status_code)


def read_attribute_stream(piwebapi_url, asset_server, user_name, user_password,
                          piwebapi_security_method, verify_ssl):
    """ Read a set of values
        @param piwebapi_url string: The URL of the PI Web API
        @param asset_server string: Name of the Asset Server
        @param user_name string: The user's credentials name
        @param user_password string: The user's credentials password
        @param piwebapi_security_method string: Security method: basic or kerberos
        @param verify_ssl: If certificate verification will be performed
    """
    print('readAttributeStream')

    #  create security method - basic or kerberos
    security_method = call_security_method(
        piwebapi_security_method, user_name, user_password)

    #  Get the sample tag
    request_url = '{}/attributes?path=\\\\{}\\{}\\{}|{}'.format(
        piwebapi_url, asset_server, OSI_AF_DATABASE, OSI_AF_ELEMENT, OSI_AF_ATTRIBUTE_TAG)

    url = urlparse(request_url)
    # Validate URL
    assert url.scheme == 'https'
    assert url.geturl().startswith(piwebapi_url)

    response = requests.get(url.geturl(), auth=security_method, verify=verify_ssl)

    #  Only continue if the first request was successful
    if response.status_code == 200:
        #  Deserialize the JSON Response
        data = json.loads(response.text)

        url = urlparse(piwebapi_url + '/streams/' + data['WebId'] +
                       '/recorded?startTime=*-2d')
        # Validate URL
        assert url.scheme == 'https'
        assert url.geturl().startswith(piwebapi_url)

        #  Read the set of values
        response = requests.get(
            url.geturl(), auth=security_method, verify=verify_ssl)

        if response.status_code == 200:
            print('{} Values'.format(OSI_AF_ATTRIBUTE_TAG))
            print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))
        else:
            print(response.status_code, response.reason, response.text)
    else:
        print(response.status_code, response.reason, response.text)
    return response.status_code


def read_attribute_selected_fields(piwebapi_url, asset_server, user_name, user_password,
                                   piwebapi_security_method, verify_ssl):
    """ Read sampleTag values with selected fields to reduce payload size
        @param piwebapi_url string: The URL of the PI Web API
        @param asset_server string: Name of the Asset Server
        @param user_name string: The user's credentials name
        @param user_password string: The user's credentials password
        @param piwebapi_security_method string: Security method: basic or kerberos
        @param verify_ssl: If certificate verification will be performed
    """
    print('readAttributeSelectedFields')

    #  create security method - basic or kerberos
    security_method = call_security_method(
        piwebapi_security_method, user_name, user_password)

    #  Get the sample tag
    request_url = '{}/attributes?path=\\\\{}\\{}\\{}|{}'.format(
        piwebapi_url, asset_server, OSI_AF_DATABASE, OSI_AF_ELEMENT, OSI_AF_ATTRIBUTE_TAG)
    response = requests.get(request_url,
                            auth=security_method, verify=verify_ssl)

    #  Only continue if the first request was successful
    if response.status_code == 200:
        #  Deserialize the JSON Response
        data = json.loads(response.text)

        url = urlparse(piwebapi_url + '/streams/' + data['WebId'] +
                       '/recorded?startTime=*-2d&selectedFields=Items.Timestamp;Items.Value')
        # Validate URL
        assert url.scheme == 'https'
        assert url.geturl().startswith(piwebapi_url)

        #  Read a set of values and return only the specified columns
        response = requests.get(url.geturl(),
                                auth=security_method, verify=verify_ssl)
        if response.status_code == 200:
            print('SampleTag Values with Selected Fields')
            print(json.dumps(json.loads(response.text), indent=4, sort_keys=True))
        else:
            print(response.status_code, response.reason, response.text)
    else:
        print(response.status_code, response.reason, response.text)
    return response.status_code


def pesquisarpai():
    
    """ Main method. Receive user input and call the write value methods """
    piwebapi_url = "https://piwebapi.edpbr.com.br/piwebapi"
    af_server_name = "EDPBR339"
    piwebapi_user = "10500089"
    piwebapi_password = ""
    piwebapi_security_method = "basic"
    piwebapi_security_method = piwebapi_security_method.lower()
    verify_ssl_string = "N"
    
    if (verify_ssl_string.upper() == "N"):
        print('Not verifying certificates poses a security risk and is not recommended')
        verify_ssl = False
    else:
        verify_ssl = True

    return read_attribute_snapshot(piwebapi_url, af_server_name, piwebapi_user, piwebapi_password,
                            piwebapi_security_method, verify_ssl)
    #read_attribute_stream(piwebapi_url, af_server_name, piwebapi_user, piwebapi_password,
    #                      piwebapi_security_method, verify_ssl)
    #read_attribute_selected_fields(piwebapi_url, af_server_name, piwebapi_user, piwebapi_password,
    #                               piwebapi_security_method, verify_ssl)
