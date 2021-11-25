#!/usr/bin/env python3

import requests
from jira import JIRA

white_list = ["jirahicadmin", "jirasystem", "vcrash", "admin", "yindeshuai", "yinfei", "liudi"]

deleted_user_list = []


class JiraClearException(Exception):
    """Base exception class for JiraClearException."""


def login_jira():
    """ login jira"""
    url = 'https://uh.haier.net:8443/jira/'
    auth = {
        "os_username": "likunkun",
        "os_password": "633153@LBLMwoaini",
        "os_cookie": "true",
        "os_captcha": ""
    }
    session = requests.session()
    session.post(url, auth)
    return session


def get_day14_user():
    """select 14 day not login user"""
    session = login_jira()
    body = {'searchString': '', 'daysSinceLastLogin': '14d', 'activeUsers': True,
            'inActiveUsers': True, 'application': 'jira-software', 'pageSize': -1, 'offSet': -1}
    uri = "https://uh.haier.net:8443/jira/rest/jirauserexport/1.0/search"
    headers = {"Content-Type": "application/json"}
    try:
        rep = session.post(uri, headers=headers, json=body)
        if rep.status_code == 200:
            data_list = rep.json()
            print(data_list)
            delete_user(data_list, session)
        else:
            raise JiraClearException("get 14d not login user failed, error_code: %s" % rep.status_code)
    except Exception as e:
        print(e)


def delete_user(data, session):
    for i in data.get("users"):
        day_14_not_login = i.get("name")
        print(day_14_not_login)
        if day_14_not_login in white_list:
            continue
        delete_uri = "https://uh.haier.net:8443/jira/rest/internal/2/viewuser/application/jira-software?username=%s" % day_14_not_login
        res = session.delete(delete_uri)
        # res = session.post(delete_uri)
        if res.status_code != 200:
            raise JiraClearException("delete %s user failed, error_code: %s" % (day_14_not_login, res.status_code))
        else:
            deleted_user_list.append(day_14_not_login)


get_day14_user()
