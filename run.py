#!/usr/bin/python

import os
import sys
import getopt
from subprocess import Popen, PIPE, STDOUT
import subprocess

def help():
    print("print help usage")
    return
    
def mod_file(args):
    file_name="test/"+args+".yaml"
    output = []
    with open(file_name,'r+t') as f:
        for lines in f:
            if not 'uid' or 'status' in lines:
                output.append(lines)
            
    f=open(file_name,'w')
    f.writelines(output)
    f.close()

def export_pv_yaml(arg_pv, arg_file):
    print("args = "+arg_pv.replace('\n','').replace('"',''))
    
    arg_pv=arg_pv.replace('\n','').replace('"','')
    arg_file=arg_file.replace('\n','').replace('"','')

    # genFileCmd = "kubectl get pv -oyaml "+arg_pv+" > ./test/"+arg_file+".yaml"
    f=open("test/"+arg_file+".yaml", 'w')
    out=subprocess.check_output("kubectl get pv -oyaml "+arg_pv, shell=True)
    f.write(out)
    f.close()
    mod_file(arg_file)

def export(args):
    # check directory & make directory
    if os.path.exists(args):
        print("Temp directory already exists")
    else:
        os.mkdir(args)
        print("Temp directory create")

    # export PVs to yaml files

    statusCmd="kubectl get pv -ojson | jq '.items[].status.phase'"
    p1 = Popen(statusCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    #parsing_pv, parsing_file = [], []
    #parsing_export, parsing_export_pv, parsing_export_file = dict(), dict(), dict()
    cnt = 0
    while True:
        cmd_status = p1.stdout.readline()
        if not cmd_status:
            break
        cmd_status = cmd_status.encode('ascii').replace('\n','').replace('"','')

        if 'Available' == cmd_status:
            cnt+=1
            continue
        elif 'Bound' == cmd_status:
            # pv_name is a base of yaml file.
            # claimRef name use for making file name
            pvNameCmd = "kubectl get pv -ojson | jq '.items["+str(cnt)+"].metadata.name'"
            p2 = Popen(pvNameCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

            fileNameCmd = "kubectl get pv -ojson | jq '.items["+str(cnt)+"].spec.claimRef.name'"
            p3 = Popen(fileNameCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

            export_pv_yaml(p2.stdout.read(), p3.stdout.read())
            cnt+=1
        else:
            break
        

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