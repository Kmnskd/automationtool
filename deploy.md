#### 脚本使用方法说明
先登录服务器
- 10.180.98.114 root/Ali$%Uhome>!@489 

执行脚本
- python3 deploy.py code_type, branch, tag
- 参数说明
    - code_type: 部署cloud或fronetnd
    - branch： 基于那个分支的部署
    - tag：部署的tag号

例子
- 如果要部署基于integration_4.1.0分支tag号为4.1.0.2.2021111167前端的代码，则命令为python3 deploy.py frontend integration_4.1.0 4.1.0.2.2021111167

    