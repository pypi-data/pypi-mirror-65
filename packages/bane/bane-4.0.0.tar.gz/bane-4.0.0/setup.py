#for windows you need to download: winpcap: http://www.win10pcap.org/download/
import sys,setuptools,os
with open("README.md", "r") as fh:
    long_description = fh.read()
termux=False
if os.path.isdir('/home/')==True:
 os.system('sudo apt install sshpass -y')
 os.system('sudo apt install nodejs -y')
adr=False
if os.path.isdir('/data/data')==True:
    adr=True
if os.path.isdir('/data/data/com.termux/')==True:
    termux=True
if termux==False:
   if  sys.version_info < (3,0):
    os.system('pip uninstall dnspython -y')
    os.system('pip install dnspython')
   else:
    os.system('pip3 uninstall dnspython -y')
    os.system('pip3 install dnspython')
if  sys.version_info < (3,0):
 req=["xtelnet","protobuf==3.6.1","requests","PySocks","bs4","mysql-connector","scapy","stem","cfscrape","python-whois","google","colorama","dnspython"]
 if adr==True:
    req=["xtelnet","protobuf==3.6.1","requests","PySocks","bs4","mysql-connector","cfscrape","scapy","python-whois","google","colorama","dnspython"]
 if termux==True:
    req=["xtelnet","protobuf==3.6.1","requests","PySocks","bs4","mysql-connector","scapy","cfscrape","python-whois","google","colorama","dnspython"]
else:
 req=["xtelnet","requests","protobuf==3.6.1","PySocks","bs4","mysql-connector","kamene","stem","cfscrape","python-whois","google","colorama","dnspython"]
 if adr==True:
    req=["xtelnet","requests","protobuf==3.6.1","PySocks","bs4","mysql-connector","cfscrape","kamene","python-whois","google","colorama","dnspython"]
 if termux==True:
    req=["xtelnet","requests","protobuf==3.6.1","PySocks","bs4","mysql-connector","kamene","cfscrape","python-whois","google","colorama","dnspython"]
if (sys.platform == "win32") or( sys.platform == "win64"):
 req+=["win_inet_pton"]
if termux==True:
 os.system('pkg install openssh -y')
 os.system('pkg install sshpass -y')
 os.system('pkg install nodejs -y')
setuptools.setup(
    name="bane",
    version="4.0.0",
    author="AlaBouali",
    author_email="trap.leader.123@gmail.com",
    description="cyber security library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlaBouali/bane",
    python_requires=">=2.7",
    install_requires=req,
    packages=["bane"],
    license="MIT License",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License ",
    ],
)
