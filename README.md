# dialogue-nav
A voice navigation system that integrates multiple rounds of dialogue to confirm the destination for the visually impaired.

Build snowboy
---
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
