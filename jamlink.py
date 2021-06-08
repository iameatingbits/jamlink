#!/usr/bin/env python3

import subprocess
import time
import os
import shutil
import sys


def print_help():
    help_str = \
        "////////////////////////////////////////////\n\r"  \
        "{} help:\n\r"                                      \
        "* to restart terminal -- hit Ctrl+C one time\n\r"  \
        "* to exit -- hit Ctrl+C twice\n\r"                 \
        "////////////////////////////////////////////"
    print(help_str.format(os.path.basename(__file__)))

def check_tool(tool):
    if shutil.which(tool) is None:
        print("No {} tool is installed".format(tool))
        sys.exit(1)

def args_supplier(cmd, args):
    args_list = [f'{cmd}']

    [args_list.extend([k, v]) for (k, v) in zip(args.keys(), args.values())]

    return args_list

def jlink_exe():
    jlink_exe_cmd = "JLinkExe"
    # if you have to use blank option (w/o argument) just leave the value empty as blank string ""
    jlink_exe_args = {
        "-RTTTelnetPort":"19021",
        "-device":"NRF52832_XXAA",
        "-if":"swd",
        "-speed":"4000",
        "-autoconnect":"1"
    }

    check_tool(jlink_exe_cmd)
    cmd = args_supplier(jlink_exe_cmd, jlink_exe_args)

    return subprocess.Popen(cmd, shell=False, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def telnet_exe():
    telnet_exe_cmd = "telnet"
    telnet_exe_args = {
        "localhost":"19021"
    }

    check_tool(telnet_exe_cmd)
    cmd = args_supplier(telnet_exe_cmd, telnet_exe_args)
    subprocess.run(cmd, shell=False)

def main(argv = None):
    while True:
        print_help()
        jlink_proc = jlink_exe()
        time.sleep(1)

        try:
            telnet_exe()
        except KeyboardInterrupt:
            print("\n\rRestarting terminal")
            jlink_proc.kill()

if __name__ == "__main__":
    main(sys.argv)
