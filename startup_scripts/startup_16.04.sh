#! /bin/bash

cp /etc/apt/sources.list /etc/apt/sources.list.bak
echo """deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse""" > /etc/apt/sources.list
dpkg --add-architecture i386
apt-get update 

apt-get install -y \
sudo \
build-essential \
gcc-multilib \
g++-multilib \
gdb \
gdb-multiarch \
net-tools \
nasm \
cmake \
ruby \
vim \
tmux \
git \
binwalk \
strace \
ltrace \
autoconf \
socat \
netcat \
nmap \
wget \
tcpdump \
libimage-exiftool-perl \
squashfs-tools \
unzip \
upx-ucl \
man-db \
manpages-dev \
libtool-bin \
bison \
libc6:i386 \
libncurses5:i386 \
libstdc++6:i386 \
lib32z1 \
xinetd \
curl \
zsh \
openssh-server

apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
apt-get -y autoremove

/etc/init.d/ssh restart

# install .tmux
cd ~ && \
git clone https://github.com/gpakosz/.tmux && \
ln -s -f .tmux/.tmux.conf && \
cp .tmux/.tmux.conf.local .

# install ohmyzsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# # install ruby first
# gem install one_gadget
# gem install seccomp-tools


# # python 相关建议使用 conda 安装
# pip install ipython
# 
# git clone https://github.com/sashs/Ropper.git /opt/ropper && \
# cd /opt/ropper && \
# pip install -r requirements.txt
# python setup.py install

rm -rf /opt/ropper

# 
# git clone https://github.com/niklasb/libc-database /opt/libc-database

# git clone https://github.com/pwndbg/pwndbg.git /opt/pwndbg && \
# cd /opt/pwndbg && \
# ./setup.sh

git clone git://github.com/wting/autojump.git && \
cd autojump && \
./install.py
echo "[[ -s ~/.autojump/etc/profile.d/autojump.sh ]] && source ~/.autojump/etc/profile.d/autojump.sh" >> ~/.zshrc
echo "[[ -s ~/.autojump/etc/profile.d/autojump.sh ]] && source ~/.autojump/etc/profile.d/autojump.sh" >> ~/.bashrc

# disable ASLR
bash -c 'echo "kernel.randomize_va_space = 0" > /etc/sysctl.d/01-disable-aslr.conf'

# # install libc sourc for gdb
# apt-get install glibc-source && \
# cd /usr/src/glibc && \
# tar xvf ./glibc-2.23.tar.xz
# bash -c 'echo "dir /usr/src/glibc/glibc-2.23/malloc" >> ~/.gdbinit'