# gns3 安装使用

## gns3 IOU for linux 安装

* `fedora 29`

    ```sh
    sudo dnf install git bison flex gcc make openssl-libs:i686 libgcc:i686
    git clone http://github.com/ndevilla/iniparser.git
    cd iniparser
    make
    sudo cp libiniparser.* /usr/lib/
    sudo cp src/iniparser.h /usr/local/include
    sudo cp src/dictionary.h /usr/local/include
    cd ..

    git clone https://github.com/GNS3/iouyap.git
    cd iouyap
    make
    sudo make install
    ```