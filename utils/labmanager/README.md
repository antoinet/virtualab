# labmanager.py

Use this script to provision connections and users for your lab boxes on the jumphost.

## Installation

Setup the required python dependencies using a [virtual environment](https://docs.python.org/3/library/venv.html):

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```


## Usage

This command will automatically provision users and connections on guacamole according to the configuration values from `config.yaml` in the root folder.

```bash
$ python3 labmanager.py map automap
```
