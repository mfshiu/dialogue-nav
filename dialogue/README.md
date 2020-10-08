# dialogue-nav
A voice navigation system that integrates multiple rounds of dialogue to confirm the destination for the visually impaired.

Helping the visually impaired to walk and guiding him to the destination is a challenging task. The difficulty is to use natural language as the only communication method and assist the visually impaired to see the road and environment in front of him. We have developed a voice navigation system that integrates multiple rounds of dialogue to confirm the destination for the visually impaired. Besides, we also use image interpretation technology based on the RNN neural network to describe the scene in front of the user. Finally, in terms of hardware, we use a low-cost, low-power embedded hardware that integrates cameras, Wi-Fi, and microphones to implement this application.

Install dialogue-sys (vin)
       sudo apt-get install portaudio19-dev
       sudo apt-get install python-pyaudio python3-pyaudio sox
       sudo apt-get install swig3.0
       sudo apt-get install libatlas-base-dev
       sudo apt-get install libpython3.7
       sudo apt-get install python3-gi
       sudo apt-get install pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev
    
    sudo apt-get install ffmpeg
    --sudo apt_get install libgazebo9-dev
    sudo rm /usr/lib/aarch64-linux-gnu/libdrm.so.2
    sudo -H ln -s /usr/lib/aarch64-linux-gnu/libdrm.so.2.4.0 /usr/lib/aarch64-linux-gnu/libdrm.so.2
    
    pip install pyaudio
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
    Note 1:
    If it occurs python3-config command does not found error, check the python3-config path in user mode (not root), and do make again. Append the path to $PATH.
    ex: export PATH=/home/nvidia/archiconda3/bin:$PATH
    
    Note 2:
    [before]
    SNOWBOYDETECTLIBFILE := $(TOPDIR)/lib/ubuntu64/libsnowboy-detect.a
    [after]
    SNOWBOYDETECTLIBFILE := $(TOPDIR)/lib/aarch64-ubuntu1604/libsnowboy-detect.a
    
    
    pip install dialogflow
    pip install googlemaps
    pip install playsound
    pip install google-cloud-texttospeech
    --pip install pyobjc
    pip install pydub
    pip install gobject PyGObject






