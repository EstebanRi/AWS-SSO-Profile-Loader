#!/usr/bin/env python3
import boto3
import json, webbrowser, socket
import operator
import os

from pathlib import Path
from configparser import ConfigParser

AWS_DEFAULT_REGION = 'us-east-1'
AWS_CREDENTIAL_PATH = os.path.join(Path.home(),'.aws','credentials')
print(AWS_CREDENTIAL_PATH)
sso_start_url = 'https://cloud-uala.awsapps.com/start#/'
client = boto3.client('sso-oidc')
sso_client = boto3.client('sso')

def read_config(path):
    config = ConfigParser()
    config.read(path)
    return config

def write_config(path, config):
    with open(path, "w") as destination:
        config.write(destination)

def device_registration(client_name, client_type):
    try:
        response_client_registration = client.register_client(
            clientName= client_name,
            clientType= client_type,
        )
        return response_client_registration['clientId'], response_client_registration['clientSecret']
    except Exception as e:
        return e

def get_auth_device(id, secret, start_url):
    try:
        response_device_authorization = client.start_device_authorization(
            clientId=id,
            clientSecret=secret,
            startUrl=start_url
        )
        return response_device_authorization['verificationUriComplete'], response_device_authorization['deviceCode'], response_device_authorization['userCode']
    except Exception as e:
        return e

def get_token(id, secret, device_code, user_code):
    try:
        response_token_creation = client.create_token(
            clientId= id,
            clientSecret= secret,
            grantType='urn:ietf:params:oauth:grant-type:device_code', #review
            deviceCode= device_code,
            code= user_code
        )
        return response_token_creation['accessToken']
    except Exception as e:
        return e

def get_list_accounts(token):
    try:
        response_list_accounts = sso_client.list_accounts(
            # nextToken='string',
            maxResults=123,
            accessToken=token
        )
        accounts = response_list_accounts['accountList']
        accounts.sort(key=operator.itemgetter('accountName'))
        return accounts
    except Exception as e:
        return e

def get_roles_account(token, accountid):
    try:
        response_account_roles = sso_client.list_account_roles(
            # nextToken='string',
            maxResults=123,
            accessToken=token,
            accountId=accountid
        )
        roles = response_account_roles['roleList']
        roles.sort(key = operator.itemgetter('roleName'))
        return roles
    except Exception as e:
        return e

def get_roles_credentials(rolename, accountid, token):
    try:
        response_role_credentials = sso_client.get_role_credentials(
            roleName=rolename,
            accountId=accountid,
            accessToken=token
        )
        return response_role_credentials['roleCredentials']
    except Exception as e:
        return e

def update_aws_credentials(account, profile, credentials):
    profile_id = account + '-_-' + profile
    print('Creando perfil:', profile_id)
    region = AWS_DEFAULT_REGION
    config = read_config(AWS_CREDENTIAL_PATH)
    if account == 'uala-arg-operaciones-prod':
        account = 'uala-operaciones'
    if config.has_section(profile_id):
        config.remove_section(profile_id)
    config.add_section(profile_id)
    config.set(profile_id, "region", region)
    config.set(profile_id, "aws_access_key_id", credentials["accessKeyId"])
    config.set(profile_id, "aws_secret_access_key ", credentials["secretAccessKey"])
    config.set(profile_id, "aws_session_token", credentials["sessionToken"])
    write_config(AWS_CREDENTIAL_PATH, config)

def main():
    clientId, clientSecrets = device_registration(socket.gethostname(), 'public')
    url, deviceCode, userCode = get_auth_device(clientId, clientSecrets, sso_start_url)
    try:
        print(url)
        webbrowser.open(url)
    except:
        print("Please manual login: %s \n" % (url))

    input("After login, press Enter to continue...")
    token = get_token(clientId, clientSecrets, deviceCode, userCode)
    accounts_list = get_list_accounts(token)

    for account in accounts_list:
        account_id = account['accountId']
        account_name = account['accountName']
        role_name_data = get_roles_account(token, account_id)
        for roleName in role_name_data:
            role_name = roleName ['roleName']
            account = roleName['accountId']
            temp_credentials = get_roles_credentials(role_name, account, token)
            update_aws_credentials(account_name, role_name, temp_credentials)
