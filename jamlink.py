#!/usr/bin/env python3

import subprocess
import time
import os

def print_help():
    help_str = "////////////////////////////////////////////\n\r" \
        "{} help:\n\r" \
        "* to restart terminal -- hit Ctrl+C one time\n\r" \
        "* to exit -- hit Ctrl+C twice\n\r" \
        "////////////////////////////////////////////"
    print(help_str.format(os.path.basename(__file__)))

def args_supplier(cmd, args):
    args_list = [f'{cmd}']
    complete_cmd = []

    for k, v in zip(args.keys(), args.values()):
        args_list.extend([k, v])

    complete_cmd.extend(args_list)

    return complete_cmd

def jlink_exe():
    jlink_exe_cmd = "JLinkExe"
    jlink_exe_args = {
        "-RTTTelnetPort":"19021",
        "-device":"NRF52832_XXAA",
        "-if":"swd",
        "-speed":"4000",
        "-autoconnect":"1"
    }

    cmd = args_supplier(jlink_exe_cmd, jlink_exe_args)
    return subprocess.Popen(cmd, shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def telnet_exe():
    telnet_exe_cmd = "telnet"
    telnet_exe_args = {
        "localhost":"19021"
    }

    cmd = args_supplier(telnet_exe_cmd, telnet_exe_args)
    subprocess.run(cmd, shell=False)

while True:
    print_help()
    jlink_proc = jlink_exe()
    time.sleep(1)

    try:
        telnet_exe()
    except KeyboardInterrupt:
        print("\n\rRestarting terminal")
        jlink_proc.kill()
