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

#!/bin/bash

############# SET VARIABLES #############

# Env Variables
BACKUPSERVER="101.200.146.218" # Backup Server Ip
BACKUPDIR=/var/backup/mysql
BACKUPREMOTEDIR="/data/backup/kubernetes/"
NOW="$(date +"%Y-%m-%d")"
STARTTIME=$(date +"%s")


############# BUILD ENVIROMENT #############
# Check if temp Backup Directory is empty
mkdir $BACKUPDIR

if [ "$(ls -A $BACKUPDIR)" ]; then
    echo "Take action $BACKUPDIR is not Empty"
    rm -f $BACKUPDIR/*.gz
    rm -f $BACKUPDIR/*.mysql
else
    echo "$BACKUPDIR is Empty"
fi

############# BACKUP SQL DATABASES #############
for DB in $(mysql -u$USER -p$PASS -h $HOST -e 'show databases' -s --skip-column-names); do
    mysqldump -u$USER -p$PASS -h $HOST --lock-tables=false $DB > "$BACKUPDIR/$DB.sql";
done

############# ZIP BACKUP #############
cd $BACKUPDIR
tar -zcvf backup-${NOW}.tar.gz *.sql

############# MOVE BACKUP TO REMOTE #############
scp $BACKUPDIR/backup-${NOW}.tar.gz root@$BACKUPSERVER:$BACKUPREMOTEDIR

# done