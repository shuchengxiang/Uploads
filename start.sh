#!/bin/bash
set -e
data_path=$1
port=$2

if [ -z ${data_path} ];then
    echo "使用方法: ./start.sh [数据目录的绝对路径] [端口号(可选，默认8080)]，"
    echo "如: ./start.sh /data/data_dir"
    exit 1
fi

if [ -z ${port} ];then
    port=8080
fi

sudo docker run --pull always --rm -p ${port}:5000 -v ${data_path}:/app/uploads ampregistry:5000/hw/file-server