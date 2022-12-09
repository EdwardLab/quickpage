# QuickPage
Quickly create and share HTML pages, support Bootstrap 5. Generate your own URLs for quick page sharing  
Click STAR to support our development  
Sponsor us: [Patreon](https://www.patreon.com/xingyujie)  [PayPal](https://paypal.me/xingyujie50)
## Get community support
[Telegram](https://t.me/digitalplatdev)  
[Discord](https://discord.gg/xhZhjcZd)  
[Follow us on Twitter for the latest news and updates](https://twitter.com/digitalplatdev)  
Our official website: https://www.digitalplat.org   
# Quick start
Demo: https://quickpage.digitalplat.org  
System Requirements: Linux, Windows or Unix-like System  
Python requirements: Python 3.7+  
## Install Python
### On Linux systems:
Debian-like system: `apt update & apt install python3 python3-pip -y`  
CentOS-like system: `yum update & yum install -y python3 python3-pip`  
For other Linux distributions, please Google :D
### On Microsoft Windows
Go to https://www.python.org/downloads/ to download the latest Python releases  
In the first installation interface, be sure to check `Add Python3.xx to PATH`
## Install library
Enter Linux BASH or Windows CMD  
If you have Git, you can use `git clone https://github.com/xingyujie/quickpage.git`  
If you don't have Git, click `Code -> Download ZIP` in the Github repository and unzip it  
Change to the working directory, e.g. `cd quickpage-main`
Check if you are in the root directory of the quickpage source and use `pip install -r requirements.txt` and wait for installation  
## Start server
If everything is in order, then you can start the server...  
Make sure you are still in the working directory  
### Change the gevent configuration file start.py to configure the listening address and port 
Open the `start.py` file (in the working root directory) with any editor such as `vim`, `mousepad`, `vscode`, and you will see the following code  
```
from gevent.pywsgi import WSGIServer
from main import app

http_server = WSGIServer(("0.0.0.0", 5400), app)
http_server.serve_forever()
```
`0.0.0.0` is the listening address, `5400` is the listening port, usually we only need to change the listening port  
Type `python start.py` to start the server. Open any browser and enter the address `http://{your_server_ip}:5400` to see the login interface
### Bind a domain name through a reverse proxy
You can point Nginx and Apache to your server IP through a reverse proxy, and you can bind domain names and SSL through Nginx or Apache. As an additional option, you can consult the Apache or Nginx documentation to implement it  
# File tree
```
├───static -- static resource file
│   ├───css
│   ├───js
│   └───res
│       └───img
├───templates -- HTML template file
├───users
│   ├───admin
│   └───...... --User folder, where HTML pages are stored
└───__pycache__ -- PyCache
```
# Database
QuickPage uses Sqlite database to store user name and password, etc., and performs hash encryption through `werkzeug.security`  
We created a test user `admin` with password `123456` by default. You can delete it by reading the database  
# Open Source License
Bootstrap 5 -- [Bootstrap License](https://getbootstrap.com/docs/5.0/about/license/)  
Python 3 -- [Python License](https://docs.python.org/3/license.html)  
Flask -- [BSD-3-Clause](https://flask.palletsprojects.com/en/2.2.x/license/)  
