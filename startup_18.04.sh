#! /bin/bash

cp /etc/apt/sources.list /etc/apt/sources.list.bak
echo """# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse""" > /etc/apt/sources.list

dpkg --add-architecture i386
apt-get update && apt-get -y upgrade

apt-get install -y \
sudo \
build-essential \
gcc-multilib \
g++-multilib \
gdb \
gdb-multiarch \
python-dev \
python-pip \
python3-pip \
default-jdk \
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
libini-config-dev \
libssl-dev \
libffi-dev \
libglib2.0-dev \
libc6:i386 \
libncurses5:i386 \
libstdc++6:i386 \
lib32z1 \
xinetd \
curl \
ipython \
zsh \
openssh-server

apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
apt-get -y autoremove

/etc/init.d/ssh restart

cd ~ && \
git clone https://github.com/pullp/.tmux.git && \
ln -s -f .tmux/.tmux.conf && \
cp .tmux/.tmux.conf.local .

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"


# git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
# echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc && \
# echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc

python -m pip install \
pycipher \
uncompyle \
ropgadget \
distorm3 \
filebytes \
r2pipe \
scapy \
python-constraint

python -m pip install --upgrade pwntools

# python -m pip install docopt

python3 -m pip install setuptools \
ipython

mv /usr/local/bin/ipython /usr/local/bin/ipython3

# # virtualenvwrapper
# pip install virtualenvwrapper -i https://pypi.douban.com/simple/
# source /usr/local/bin/virtualenvwrapper.sh
# echo "source /usr/local/bin/virtualenvwrapper.sh" >> .bashrc
# echo "source /usr/local/bin/virtualenvwrapper.sh" >> .zshrc


# bash -c 'source /etc/bash_completion.d/virtualenvwrapper && \
# mkvirtualenv angr && \
# pip install angr && \
# deactivate'



gem install one_gadget

# git clone https://github.com/aquynh/capstone.git /opt/capstone && \
# cd /opt/capstone && \
# ./make.sh && \
# ./make.sh install  && \
# cd bindings/python && \
# make install && \
# make install3

# git clone https://gist.github.com/47e3a5ac99867e7f4e0d.git /opt/binstall && \
# cd /opt/binstall && \
# chmod 755 binstall.sh && \
# ./binstall.sh amd64 && \
# ./binstall.sh i386

git clone https://github.com/sashs/Ropper.git /opt/ropper && \
cd /opt/ropper && \
python3 setup.py install

rm -rf /opt/ropper

# git clone https://github.com/niklasb/libc-database /opt/libc-database

git clone https://github.com/pwndbg/pwndbg.git /opt/pwndbg && \
cd /opt/pwndbg && \
./setup.sh

git clone git://github.com/wting/autojump.git && \
cd autojump && \
./install.py
echo "[[ -s /home/wxk/.autojump/etc/profile.d/autojump.sh ]] && source /home/wxk/.autojump/etc/profile.d/autojump.sh" >> ~/.zshrc
echo "[[ -s /home/wxk/.autojump/etc/profile.d/autojump.sh ]] && source /home/wxk/.autojump/etc/profile.d/autojump.sh" >> ~/.bashrc

# disable ASLR
bash -c 'echo "kernel.randomize_va_space = 0" > /etc/sysctl.d/01-disable-aslr.conf'

# # install libc sourc for gdb
# apt-get install glibc-source && \
# cd /usr/src/glibc && \
# tar xvf ./glibc-2.23.tar.xz
# bash -c 'echo "dir /usr/src/glibc/glibc-2.23/malloc" >> ~/.gdbinit'