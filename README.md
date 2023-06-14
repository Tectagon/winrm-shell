# winrm-shell
Interactive Shell for WinRM from a Linux machine

## Installation

```bash
pip install -r requirements.txt
sudo ln -s $(pwd)/winrm-shell.py /usr/bin/winrm
```

## Usage

```bash
winrm -s 192.168.1.20 -u admin -p SuperPassword123 -d test.local
```
