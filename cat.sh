#!/bin/bash

check_root
echo  "upgrade"
sudo apt update && sudo apt upgrade -y
sudo apt install curl tar wget clang pkg-config libssl-dev jq build-essential git make ncdu unzip zip docker.io -y
echo  "install docker"
VERSION=$(curl --silent https://api.github.com/repos/docker/compose/releases/latest | grep -Po '"tag_name": "\K.*\d')
DESTINATION=/usr/local/bin/docker-compose
curl -L https://github.com/docker/compose/releases/download/${VERSION}/docker-compose-$(uname -s)-$(uname -m) -o $DESTINATION
chmod 755 $DESTINATION
echo  "install node"
apt-get install npm -y
npm install n -g
n stable
npm i -g yarn

echo  "pull cat-git"
git clone https://github.com/CATProtocol/cat-token-box
cd cat-token-box
yarn install
yarn build

cd /root/cat-token-box/packages/tracker/
chmod 777 docker/data
chmod 777 docker/pgdata
docker-compose up -d

cd ../../
docker build -t tracker:latest .
docker run -d \
    --name tracker \
    --add-host="host.docker.internal:host-gateway" \
    -e DATABASE_HOST="host.docker.internal" \
    -e RPC_HOST="host.docker.internal" \
    -p 3000:3000 \
    tracker:latest


#创建快速重启tracker
cat >"/root/cat-token-box/packages/cli/mint.sh"<<EOF
#!/bin/bash
while true; do
  gas=$(curl -s https://explorer.unisat.io/fractal-mainnet/api/bitcoin-info/fee | jq -r '.data.halfHourFee')
  if [[ $gas -lt 300 ]]; then
    sudo yarn cli mint -i 45ee725c2c5993b3e4d308842d87e973bf1951f5f7a804b21e4dd964ecd12d6b_0 5 --max-fee-rate=$gas
  else
    echo "当前gas：$gas,不执行，继续等待....."
  fi
  sleep 10
done
EOF
chmod +x /root/cat-token-box/packages/cli/mint.sh

#创建快速重启tracker
cat >"/usr/local/bin/retracker"<<EOF
#!/bin/bash
dockerid=`docker ps -a | grep tracker:latest | awk '{print $1}'`
docker restart $dockerid
echo "重启tracker.."
EOF
chmod +x /usr/local/bin/retracker


#创建快速查吨高度
cat >"/usr/local/bin/getbl0ck"<<EOF
#!/bin/bash
curl 127.0.0.1:3000/api
EOF
chmod +x /usr/local/bin/getbl0ck






