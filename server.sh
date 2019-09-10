#! /bin/bash

dpkg --add-architecture i386
apt-get update && apt-get -y upgrade

apt-get install -y \
sudo \
build-essential \
gcc-multilib \
g++-multilib \
python-dev \
python-pip \
python3-pip \
ipython \
default-jdk \
net-tools \
nasm \
vim \
tmux \
git \
autoconf \
socat \
netcat \
nmap \
wget \
tcpdump \
libimage-exiftool-perl \
squashfs-tools \
unzip \
man-db \
manpages-dev \
libtool-bin \
bison \
libini-config-dev \
libssl-dev \
libffi-dev \
libglib2.0-dev \
libc6:i386 \
libncurses5:i386 \
libstdc++6:i386 \
zsh

cd ~ && \
git clone https://github.com/pullp/.tmux.git && \
ln -s -f .tmux/.tmux.conf && \
cp .tmux/.tmux.conf.local .

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

apt-get -y autoremove
apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

python3 -m pip install setuptools
python3 -m pip install ipython
python3 -m pip install ropgadget

pip install \
python-constraint

git clone git://github.com/wting/autojump.git && \
cd autojump && \
./install.py
echo "[[ -s /home/pu1p/.autojump/etc/profile.d/autojump.sh ]] && source /home/pu1p/.autojump/etc/profile.d/autojump.sh" >> ~/.zshrc
echo "[[ -s /home/pu1p/.autojump/etc/profile.d/autojump.sh ]] && source /home/pu1p/.autojump/etc/profile.d/autojump.sh" >> ~/.bashrc

apt-get remove docker docker-engine docker.io containerd runc

apt-get install \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt-get update

apt-get install docker-ce docker-ce-cli containerd.io

# docker run -e PASSWORD=greed_1s_g00d@greed_1s_g00d -p445:8388 -p445:8388/udp -d shadowsocks/shadowsocks-libev