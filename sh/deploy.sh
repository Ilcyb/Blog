#!/bin/bash

if [ -z ${MYSQL_DOCKER_USERNAME} ]; then
echo 'enter your mysql user'
read MYSQL_DOCKER_USERNAME
export MYSQL_DOCKER_USERNAME=${MYSQL_DOCKER_USERNAME}
fi

if [ -z ${MYSQL_DOCKER_PASSWORD} ]; then
echo 'enter your mysql password'
read MYSQL_DOCKER_PASSWORD
export MYSQL_DOCKER_PASSWORD=${MYSQL_DOCKER_PASSWORD}
fi

# 获取代码路径
cd ../../
CODE_PATH=`pwd`
export BLOG_PATH="${CODE_PATH}"

# 启动docker
cd Blog/docker
docker-compose up -d

# 执行sql脚本
cd ../
mysql -u${MYSQL_DOCKER_USERNAME} -p${MYSQL_DOCKER_PASSWORD} -h 127.0.0.1 < blog.sql
cd docker/
docker-compose logs -f