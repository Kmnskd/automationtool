#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import subprocess
import os

test_gateway_server = "REACT_APP_BASE_URL=http://10.180.98.106:30910"
dev_gateway_server = "REACT_APP_BASE_URL=http://10.180.98.106:30911"
prd_gateway_server = "REACT_APP_BASE_URL=http://10.180.98.106:30912"
npm_cmd = ' CI=false /usr/local/bin/npm run build'


def build(branch, tag):
    cwd = os.getcwd()

    clone_code = "git clone -b %s git@git.haier.net:uplus/buildsystem/baseline_frontend.git" % branch

    path = cwd + "/baseline_frontend/"
    npm_install = "npm install"
    current = tag.split(".")[-2]
    if len(tag.split(".")) == 3:
        npm_run = prd_gateway_server + npm_cmd
    elif current == 1:
        npm_run = test_gateway_server + npm_cmd
    elif current == 2:
        npm_run = dev_gateway_server + npm_cmd

    nginx = "sed -i 's/gateway_port/30911/g' deploy/nginx.conf"
    docker_build = "docker build -f deploy/Dockerfile -t baseline-frontend:%s ." % tag
    docker_tag = "docker tag baseline-frontend:%s 10.180.98.106:30033/baseline-test/baseline-frontend:%s" % (tag, tag)
    docker_push = "docker push 10.180.98.106:30033/baseline-test/baseline-frontend:%s" % tag
    "sed -i -e 's/current-env/dev/g' -e 's/tag-name/${current_tag}/g' -e 's/frontend-port/30906/g' deploy/baseline-frontend.yaml"



def run_cmd(cmd):
    """ 执行sh命令 """
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding="utf-8")
    status = ret.returncode
    if status == 0:
        print("run cmd: %s. success status: %s " % (cmd, status))
        return status, ret.stdout
    else:
        print(
            "run cmd: %s, status: %s, error: %s " %
            (cmd, status, ret.stderr))
        if "cp" not in cmd:
            sys.exit(1)


if __name__ == '__main__':
    "integration_4.1.0"
    auto = AutomationDeploy()
    tag = sys.argv[1]
    auto.auto_build(tag)
