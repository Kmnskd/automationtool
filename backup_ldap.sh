#!/usr/bin/env bash

LDAPBK=ldap-$(date +%Y%m%d-%H).ldif

BACKUP_DIR=/data/ldap_backups

BACKUP_EXEC=`which slapcat`


checkdir() {
	if [ ! -d "$BACKUP_DIR" ]; then
	  mkdir -p ${BACKUP_DIR}
	fi
}

backuping() {
	echo "Backup Ldap Start...."
	BACKUP_FILE=${LDAPBK}
	echo ""
	${BACKUP_EXEC} -v -l ${BACKUP_DIR}/${BACKUP_FILE} > /dev/null 2>&1
}

rsync_data() {
  scp ${BACKUP_DIR}/${BACKUP_FILE} root@10.180.98.114:${BACKUP_DIR}
  find ${BACKUP_DIR} -type f -name "*.ldif" -mtime +7 -exec rm -rf {} \;
  ssh root@10.180.98.114 'find ${BACKUP_DIR} -type f -name "*.ldif" -mtime +7 -exec rm -rf {} \;'
  echo "Backup Ldap end...."
}

main() {
  checkdir
  backuping
  rsync_data
}

main

#清空openldap

ldapdelete -x -w 'password'  -D'cn=Manager,dc=ldap,dc=xxxxx,dc=net' -r 'dc=ldap,dc=xxxxx,dc=net'

#停止openldap服务

/etc/init.d/slapd  stop

#导入数据，启动服务

slapadd   -l  backup.ldif

chown -R ldap.ldap /var/lib/ldap  /etc/openldap

/etc/init.d/slapd  start