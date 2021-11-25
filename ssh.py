import sys
import paramiko

def ssh_hd(code_type, branch, tag):
    print(code_type, branch, tag)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('10.180.98.114', 22, 'root', 'Ali$%Uhome>!@489')
    #stdin, stdout, stderr = ssh.exec_command('python3 deploy.py %s %s %s' % (code_type, branch, tag))
    stdin, stdout, stderr = ssh.exec_command('sh fcl.sh %s %s %s' % (code_type, branch, tag))
    print(stdout.read())

if __name__ == '__main__':
    code_type = sys.argv[1]
    branch = sys.argv[2]
    tag = sys.argv[3]
    ssh_hd(code_type, branch, tag)

