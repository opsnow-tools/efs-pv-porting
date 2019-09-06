import os
import sys
import getopt
from subprocess import Popen, PIPE, STDOUT
import subprocess

def help():
    print("print help usage")
    return

def export_pv_yaml(args):
    for arg in {k : v for k,v in args.iteritems() if 'pv-name-' in k}.values():


        #exportFileCmd = "kubectl get pv "+arg_pv+" -oyaml > "+arg_file+".yaml"
        #p2 = Popen(exporFileCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        #cmd_exportFile=p2.stdout.read()

def export(args):
    ## check directory & make directory
    if os.path.exists(args):
        print("Temp directory already exists")
    else:
        os.mkdir(args)
        print("Temp directory create")

    ## export PVs to yaml files

    exportCmd="kubectl get pv"
    p1 = Popen(exportCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    parsing_pv, parsing_file = [], []
    parsing_export, parsing_export_pv, parsing_export_file = dict(), dict(), dict()
    cnt = 0
    while True:
        cmd_export = p1.stdout.readline()
        if not cmd_export:
            break
        cmd_export = cmd_export.encode('ascii')

        if 'Available' in cmd_export or 'NAME' in cmd_export:
            continue
        else:
            prs_ex = cmd_export.split()
            key_pv_name, value_pv_name = 'pv-name-'+str(cnt), prs_ex[0]
            key_file_name, value_file_name = 'file-name-'+str(cnt), prs_ex[5].split('/')[1]
            parsing_export_pv[key_pv_name] = value_pv_name
            parsing_export_file[key_file_name] = value_file_name
            parsing_export.update(parsing_export_pv)
            parsing_export.update(parsing_export_file)
            cnt=cnt+1


    ################################################################
    export_pv_yaml(parsing_export)

#def under_construction_file(args):

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