#!/bin/bash

if [ -z "$1" ]
then
    echo "please input a valid path"
    exit
fi

CURDIR=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )

MYSQL_VOLUME_PATH=$(dirname ${CURDIR})/docker/mysql

cd ${MYSQL_VOLUME_PATH}

tar -Jcvf mysql-data-backup.tar.xz mysql-data

cp mysql-data-backup.tar.xz $1/

cd $1

git add .
git commit -m "mysql data backup"
git push

echo "mysql backup down!"