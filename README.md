# dialogue-nav
A voice navigation system that integrates multiple rounds of dialogue to confirm the destination for the visually impaired.

Build snowboy
---
https://github.com/pmec-home/snowboy-aarch64
https://www.cnblogs.com/lly277365/p/12348583.html
```
mkdir snowboy
cd snowboy
wget http://downloads.sourceforge.net/swig/swig-3.0.10.tar.gz &&
tar -xvzf swig-3.0.10.tar.gz &&
cd swig-3.0.10/ &&   
./configure --prefix=/usr                  \
       --without-clisp                    \
       --without-maximum-compile-warnings &&
make &&
make install &&
install -v -m755 -d/usr/share/doc/swig-3.0.10 &&
cp -v -R Doc/* /usr/share/doc/swig-3.0.10 &&
cd ..

git clone https://github.com/Kitt-AI/snowboy && cd snowboy/swig/Python3 && make
```
#### Note 1:
If it occurs python3-config command does not found error, check the python3-config path in user mode (not root), and do make again. Append the path to $PATH.
```
export PATH=/home/nvidia/archiconda3/bin:$PATH
```

#### Note 2:
```
[before]
SNOWBOYDETECTLIBFILE := $(TOPDIR)/lib/ubuntu64/libsnowboy-detect.a

[after]
SNOWBOYDETECTLIBFILE := $(TOPDIR)/lib/aarch64-ubuntu1604/libsnowboy-detect.a
```
