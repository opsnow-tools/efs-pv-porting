#!/usr/bin/python

import os
import sys
import getopt
from subprocess import Popen, PIPE, STDOUT
import subprocess

def help():
    print("print help usage")
    return
    
def export_pv_yaml(args):
    print("args = "+args.replace('\n',''))
    return

def export(args):
    # check directory & make directory
    if os.path.exists(args):
        print("Temp directory already exists")
    else:
        os.mkdir(args)
        print("Temp directory create")

    # export PVs to yaml files

    statusCmd="kubectl get pv -ojson | jq '.items[].status'"
    p1 = Popen(statusCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    #parsing_pv, parsing_file = [], []
    #parsing_export, parsing_export_pv, parsing_export_file = dict(), dict(), dict()
    cnt = 0
    while True:
        cmd_status = p1.stdout.readline()
        if not cmd_status:
            break
        cmd_status = cmd_status.encode('ascii')
        print(cmd_status)

        if 'Available' in cmd_status:
            continue
        elif 'Bound' in cmd_status:
            # pv_name is a base of yaml file.
            # claimRef name use for making file name
            pvNameCmd = "kubectl get pv -ojson | jq '.items["+str(cnt)+"].metadata.name'"
            p2 = Popen(pvNameCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

            export_pv_yaml(p2.stdout.read())
            fileNameCmd = "kubectl get pv -ojson | jq '.items["+str(cnt)+"].spec.claimRef.name'"
            p3 = Popen(fileNameCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        #else:
        #    break
        cnt+=1

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:i:", ["help"])
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