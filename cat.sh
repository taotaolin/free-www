#!/bin/bash

echo  "更新源"
apt-get update
apt-get install curl wget -y
echo  "安装docker"
apt-get install docker.io -y

VERSION=$(curl --silent https://api.github.com/repos/docker/compose/releases/latest | grep -Po '"tag_name": "\K.*\d')

DESTINATION=/usr/local/bin/docker-compose
curl -L https://github.com/docker/compose/releases/download/${VERSION}/docker-compose-$(uname -s)-$(uname -m) -o $DESTINATION
chmod 755 $DESTINATION

echo  "安装node"
apt-get install npm -y
npm install n -g
n stable
npm i -g yarn


echo  "拉取cat库"
git clone https://github.com/CATProtocol/cat-token-box


echo  "安装cat库"
cd cat-token-box
yarn install && yarn build

# 定义要写入的内容
script_content='#!/bin/bash

command="sudo yarn cli mint -i 45ee725c2c5993b3e4d308842d87e973bf1951f5f7a804b21e4dd964ecd12d6b_0 5"

while true; do
    $command

    if [ $? -ne 0 ]; then
        echo "命令执行失败，退出循环"
        exit 1
    fi

    sleep 15
done
'

# 将内容写入到 s.sh 文件
echo "$script_content" > s.sh

# 为 s.sh 添加执行权限
chmod +x s.sh


sed -i 's/"maxFeeRate":.*/"maxFeeRate": 500,/' /root/cat-token-box/packages/cli/config.json