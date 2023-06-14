# winrm-shell
Interactive Shell for WinRM from a Linux machine

## Installation

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
sudo ln -s $(pwd)/winrm-shell.py /usr/bin/winrm
```

## Usage

```bash
python winrm-shell.py -s 192.168.1.20 -u admin -p SuperPassword123 -d test.local
```
