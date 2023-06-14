#!/usr/bin/env python

import argparse
import winrm
import sys
from code import InteractiveConsole
import readline

class WinRMConsole():
    def __init__(self, winrm_session, username, server):
        self.winrm_session = winrm_session
        self.username = username
        self.server = server

        #Get Initial Directory
        result = self.winrm_session.run_ps("pwd")
        if not result.status_code:
            self.dir = result.std_out.decode().split("Path")[-1].split("\r\n")[2]
        self.prompt = f"{args.username}@{args.server}# {self.dir}$ "

        #History File Definition
        self.history_file = ".winrm_history"
        readline.set_history_length(1000)
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass

    def push(self, line):
        """
        Send Command to Remote Host via WinRM
        """
        delimiter = "coojohCaivay3lu"
        result = self.winrm_session.run_ps(f"cd {self.dir}; {line}; echo {delimiter} $(pwd).Path")
        if not result.status_code:
            sys.stdout.write(str(result.std_out.decode().split(delimiter)[0]))
            sys.stdout.write("\n")
            self.dir = result.std_out.decode().split(delimiter)[-1].replace("\r\n","")
        else:
            sys.stdout.write(str(result.std_err.decode()))
            sys.stdout.write("\n")

        readline.add_history(line)
        self.prompt = f"{args.username}@{args.server}# {self.dir}$ "
    
    def __del__(self):
        readline.write_history_file(self.history_file)

    def interact(self):
        """"
        Interactive Shell
        """
        while True:
            try:
                line = input(self.prompt)
                self.push(line)
            except KeyboardInterrupt:
                sys.stdout.write("\nExiting...\n")
                sys.exit(0)
            except EOFError:
                sys.stdout.write("\nExiting...\n")
                sys.exit(0)
        return 0
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WinRM Shell')
    parser.add_argument('-s', '--server', action="store", dest="server", help="server", required=True)
    parser.add_argument('-d', '--domain', action="store", dest="domain", help="Domain")
    parser.add_argument('-u', '--username', action="store", dest="username", help="Username", required=True)
    parser.add_argument('-p', '--password', action="store", dest="password", help="Password", required=True)
    parser.add_argument('-c', '--cmd', action="store", dest="command", help="Command")
    args = parser.parse_args()

    username = args.username if not args.domain else f"{args.domain}\\{args.username}"
    session = winrm.Session(args.server, auth=(username, args.password))

    if args.command:
        result = session.run_ps(args.command)
        if not result.status_code:
            sys.stdout.write(str(result.std_out.decode()))
            sys.stdout.write("\n")
        else:
            sys.stdout.write(str(result.std_err.decode()))
            sys.stdout.write("\n")
    else:
        winrm_console = WinRMConsole(session, username, args.server)
        winrm_console.interact()
