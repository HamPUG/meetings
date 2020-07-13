# Paramiko

During the June 2020 Waikato Linux Group meeting Ian delivered a [presentation](https://github.com/WLUG/meetings/tree/master/2020/2020-06-22/last) 
on the Linux utility **last**. In his presentation he introduced the use of the Python module **Paramiko**.

This presentation is a more in-depth review of the Paramiko module.

Paramiko is a Python (3.4+) implementation of the SSHv2 protocol, providing both client and server functionality. 
While it leverages a Python C extension for low level cryptography (Cryptography), Paramiko itself is a pure 
Python interface around SSH networking concepts.

For more information:

https://www.paramiko.org/

http://docs.paramiko.org/en/stable/

## Installation

For installation of paramiko using apt.
```
$ sudo apt install python3-paramiko
```
Paramiko is also available from PyPI, https://pypi.org/project/paramiko/ and may be installed with:
```
$ pip3 install paramiko
```

## GUI Application

This GUI based demonstration of Paramiko highlights its ability to:

* Copy files from and to a remote computer.
* Execute commands on a remote computer.

To run the demonstration code download the files:

* paramiko_demo.py
* paramiko_demo_local_file_to_put_on_remote_computer


## Security Considerations

On launching this application four options are available for the remote computers
access details. This is retrieving what would normally be considered to be
confidential data. Thus it is not ideal to have this data embedded in the program 
or left in the command line history. However as this is a demonstration code, 
then you may consider this to be acceptable.

The four options used are:

### 1.

At the top of this program edit in values for 
```
SERVER = ""
PORT = 22
USERNAME = ""
PASSWORD = ""
```
...to be something like this...
```
SERVER = "1.2.3.4"
PORT = 22
USERNAME = "admin"
PASSWORD = "my_password"
```

### 2. 

Launch this program with the command line option `--make-b64`. E.g.
```
$ paramiko_demo.py --make-b64
```

When prompted enter something like this for the remote computer:
```
SERVER = "1.2.3.4", PORT = 22, USERNAME = "admin", PASSWORD = "my_password"
```
Restart the application normally. E.g. `$ paramiko_demo.py` 
A file named b64.data will now be read to retrieve these remote 
server details. The contents of the b64.data file is something like this:
`0gIjIxOS44OS4yMDUuMTAwIixQT1JUID0gMjAyMixVU0VSTkFNRSA9ICJpImRlY3RoYWlsYW5kIg==`

### 3.

Run the application with `--help` option and observe the command line options 
available. E.g.
```
$ paramiko_demo.py --help

usage: paramiko_demo.py [-h] [-s SERVER] [-p PORT] [-u USERNAME] [-w PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Server domain name or IP address string.
  -p PORT, --port PORT  Port number for ssh
  -u USERNAME, --username USERNAME
                        Account name on remote server .
  -w PASSWORD, --password PASSWORD
                        Password to Account on remote server.
```

Start the application with something like this:
```
$ python paramiko_demo.py -s 1.2.3.4 -p 22 -u admin -w my_password
```

### 4.

Start without preforming any of the above and the application will prompt 
you to enter the remote computers details. E.g.

```
$ python paramiko_demo.py
b64.data file not found. Continuing...

Enter the name or ip address of the server: 1.2.3.4
Enter the ssh port number: 22
Enter the Account name on the remote server: admin
Enter the password for the account on the remote server: my_password
```

## Screenshot

<img src="https://github.com/irsbugs/paramiko/blob/master/sreenshot.png">


Ian Stewart - 2020-07-08

