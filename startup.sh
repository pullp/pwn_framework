#! /bin/bash


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
ipython \
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
zsh

cd ~ && \
git clone https://github.com/pullp/.tmux.git && \
ln -s -f .tmux/.tmux.conf && \
cp .tmux/.tmux.conf.local .

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

apt-get -y autoremove
apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
# echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc && \
# echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc


python3 -m pip install setuptools
python3 -m pip install ipython
python3 -m pip install ropgadget

pip install \
pycipher \
uncompyle \
ropgadget \
distorm3 \
filebytes \
r2pipe \
scapy \
python-constraint

# virtualenvwrapper
pip install virtualenvwrapper -i https://pypi.douban.com/simple/
source /usr/local/bin/virtualenvwrapper.sh
echo "source /usr/local/bin/virtualenvwrapper.sh" >> .bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> .zshrc


# bash -c 'source /etc/bash_completion.d/virtualenvwrapper && \
# mkvirtualenv angr && \
# pip install angr && \
# deactivate'


pip install --upgrade pwntools

pip install docopt

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


git clone https://github.com/niklasb/libc-database /opt/libc-database

git clone https://github.com/pwndbg/pwndbg.git /opt/pwndbg && \
cd /opt/pwndbg && \
./setup.sh

gem install one_gadget

git clone git://github.com/wting/autojump.git && \
cd autojump && \
./install.py
echo "[[ -s /home/pu1p/.autojump/etc/profile.d/autojump.sh ]] && source /home/pu1p/.autojump/etc/profile.d/autojump.sh" >> ~/.zshrc
echo "[[ -s /home/pu1p/.autojump/etc/profile.d/autojump.sh ]] && source /home/pu1p/.autojump/etc/profile.d/autojump.sh" >> ~/.bashrc

# disable ASLR
bash -c 'echo "kernel.randomize_va_space = 0" > /etc/sysctl.d/01-disable-aslr.conf'

# install libc sourc for gdb
apt-get install glibc-source && \
cd /usr/src/glibc && \
tar xvf ./glibc-2.23.tar.xz
bash -c 'echo "dir /usr/src/glibc/glibc-2.23/malloc" >> ~/.gdbinit'