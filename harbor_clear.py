#!/usr/bin/env python
# -*- coding:utf-8  -*-

import requests


baseline_service = [
            "baseline-frontend",
            "baseline-auth",
            "baseline-project",
            "baseline-version",
            "devp-client-integration",
            "devp-user-center",
            "devp-api-gateway",
            "baseline-board",
        ]

env = ["baseline-dev", "baseline-test", "baseline-prd"]


def get_images_sha256(current_env):
    headers = {"Content-Type": "application/json"}
    for service_name in baseline_service:
        get_url = "https://10.180.98.106:30033/api/v2.0/projects/%s/repositories/%s/artifacts" \
              "?with_tag=true&with_scan_overview=true&with_label=true&page_size=30" % (current_env, service_name)
        res = requests.get(headers=headers, url=get_url, verify=False)
        # print(dir(res))
        # print(res.json())
        data = res.json()
        l = []
        # print(service_name)
        for i in data:
            # print(i.get("digest"), i.get("extra_attrs").get("created"))
            l.append(i.get("digest"))

        # print(l[10:])
        for sha256 in l[10:]:
            delete_url = "https://10.180.98.106:30033/api/v2.0/projects/%s/repositories/%s/artifacts" \
                  "/%s" % (current_env, service_name, sha256)
            res = requests.delete(url=delete_url, auth=('admin', 'Harbor12345'), verify=False)
            if res.status_code == 200:
                print("delete %s ok." % sha256)
            else:
                print("delete %s failed." % sha256)


def delete_imagse():
    for current_env in env:
        get_images_sha256(current_env)


delete_imagse()


# def get_images_sha256(current_tag, service_name):
#     headers = {"Content-Type": "application/json"}
#     get_url = "https://10.180.98.106:30033/api/v2.0/projects/baseline-prd/repositories/%s/artifacts" \
#               "?with_tag=true&with_scan_overview=true&with_label=true&page_size=1" % service_name
#     res = requests.get(headers=headers, url=get_url, verify=False)
#     data = res.json()
#     print(data)
#     print(service_name)
#     for i in data:
#         tag_name = i.get("tags")[0].get("name")
#         print(tag_name)
#         if tag_name == current_tag:
#             return i.get("digest")
#
#
# current_tag = "6.6.6"
# for i in baseline_service:
#     print(get_images_sha256(current_tag, i))
