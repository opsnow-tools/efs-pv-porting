import os
import sys
import getopt
from subprocess import Popen, PIPE, STDOUT
import subprocess

def help():
    print("print help usage")
    return

def export(args):
    ## export PVs to yaml files
    exportCmd="kubectl get pv"
    p1 = Popen(exportCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    cmd_export = p1.stdout.read()
    print(cmd_export.decode('utf-8'.split()))

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"he:i:", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(1)


    for opt,args in opts:
        if ( opt == "-e" ) or ( opt == "--export" ):
            print("export directory = "+args)
            export(args)
        elif ( opt == "-i" ) or ( opt == "--import" ):
            print("Importing PV... "+args)
        elif ( opt == "-h" ) or ( opt == "--help" ):
            help()

    return

if __name__ == "__main__":
    main()