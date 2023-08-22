# Any2MicronConverter
This program converts any text/markup document into the micron format, which can then be used by a reticlum page server/node.

At the moment only the DokuWiki format is supported. It is only a very rudimentary functionality, which will be further developed in the future. It is not guaranteed that all formatting will be converted properly. 


### Features
- Compatible with all Reticulum apps which can display micron pages.
- Compatible with the following source file formats:
  - DokuWiki
  - ...
- Relatively easy to extend to convert additional file formats


## Current Status
It should currently be considered beta software and still work in progress.

All core features are implemented and functioning, but additions will probably occur as real-world use is explored.

There may be errors or the compatibility after an update is no longer guaranteed.

The full documentation is not yet available. Due to lack of time I can also not say when this will be further processed.


## Installation manual

### Linux

Download the file `any2micronconverter-x.x.x-py3-none-any.whl`.

Install the dependencies. (CentOS)
```
yum -y install epel-release.noarch
yum -y install python3-pip
pip3 install pip --upgrade
pip3 install wheel --upgrade
```

Install the dependencies. (Debian/Mint/Raspi OS/Ubuntu)
```
apt install python3-pip
pip3 install pip --upgrade
```

Install the dependencies. (Fedora)
```
yum -y install make gcc
yum -y install python3-pip
pip3 install pip --upgrade
pip3 install wheel --upgrade
```

Install the dependencies. (Manjaro)
```
pacman -Sy python-pip
pip3 install pip --upgrade
```

Install the dependencies. (openSUSE)
```
zypper install python310 python310-pip
pip3 install pip --upgrade
```

Install the application.
`pip3 install any2micronconverter-x.x.x-py3-none-any.whl`

Done. Launch the application (as user).
`any2micronconverter`
or in case of an error
`./local/bin/any2micronconverter`

### Windows
Download the file `any2micronconverter-x.x.x.exe`.

Launch it.

### Startup parameters:
```bash
usage: main.py [-h] [-m MODE] [-s SRC] [-d DST] [-l LOGLEVEL] [-t] [--link_root LINK_ROOT] [--header HEADER]
               [--footer FOOTER]

Any2MicronConverter - Convert any text/makrup document to micron format

options:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Mode or type of source data for conversion (Folder name with the command files)
  -s SRC, --src SRC     Path to source directory (All subfolders are included)
  -d DST, --dst DST     Path to destination directory (Folder is overwritten/deleted)
  -l LOGLEVEL, --loglevel LOGLEVEL
  -t, --test            Running in test mode (No files are deleted or overwritten)
  --link_root LINK_ROOT
                        Root path of the links (Internal links in the documents)
  --header HEADER       Header string which will be added on all pages
  --footer FOOTER       Footer string which will be added on all pages
```

### Example:
The following command converts all files from the source folder `/root/wiki` to the destination folder `/root/.rns_server_page/pages/wiki`.
The source file format is `dw2mu`.
Internal links start with the text `619d97957a863c8e9d29e2449925fb7c:/page/wiki` to ensure accessibility of the links.
  ```bash
  any2micronconverter -m dw2mu -s /root/wiki -d /root/.rns_server_page/pages/wiki --link_root 619d97957a863c8e9d29e2449925fb7c:/page/wiki
  ```


## Support / Donations
You can help support the continued development by donating via one of the following channels:

- PayPal: https://paypal.me/SebastianObi
- Liberapay: https://liberapay.com/SebastianObi/donate


## Support in another way?
You are welcome to participate in the development. Just create a pull request. Or just contact me for further clarifications.


## Do you need a special function or customization?
Then feel free to contact me. Customizations or tools developed specifically for you can be realized.


## FAQ

### How do I start with the software?
You should read the `Installation manual` section. There everything is explained briefly. Just work through everything from top to bottom :)