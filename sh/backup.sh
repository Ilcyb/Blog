#!/bin/bash

CURDIR=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
source $(dirname ${CURDIR})/.env

TOP_PATH=$(dirname $(dirname ${CURDIR}))
cd ${TOP_PATH}

# 不存在备份git文件夹则需要克隆
if [ ! -d "${TOP_PATH}/${BACKUP_FOLDER}" ]; then
git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@${GIT_REPO_ADDR}
cd ${TOP_PATH}/${BACKUP_FOLDER}
git config user.email "${GIT_EMAIL}"
git config user.name "${GIT_USERNAME}"
git remote add origin https://${GIT_USERNAME}:${GIT_PASSWORD}@${GIT_REPO_ADDR}
fi

# 进入备份文件夹
cd ${TOP_PATH}/${BACKUP_FOLDER}
MYSQL_DUMP_PATH=${TOP_PATH}/${BACKUP_FOLDER}/blog_dump.sql

# 备份
mysqldump -u${MYSQL_USERNAME} -p${MYSQL_PASSWORD} -h127.0.0.1 --databases blog > ${MYSQL_DUMP_PATH}
git add .
git commit -m "mysql data backup"
git push -u origin master
echo "mysql backup down!"