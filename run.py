#!/usr/bin/python

import os
import sys
import getopt
from subprocess import Popen, PIPE, STDOUT
import subprocess
import yaml
import shutil
from os.path import expanduser

home=expanduser('~')


def help():
    print("print help usage")
    print("-t / --init option : Must place in cluster directory. And It can find right place of .output directoires")
    return
    
def mod_file(args):
    file_name="test/"+args+".yaml"
    output = []
    with open(file_name,'r+t') as f:
        for lines in f:
            # if not 'uid' in lines:
            #     print('here')
            #     output.append(lines)
            if ('status' in lines) or ('uid' in lines) or ('creationTimestamp' in lines) or ('selfLink' in lines) or ('phase' in lines):
                continue
            output.append(lines)
            
    f=open(file_name,'w')
    f.writelines(output)
    f.close()

def export_pv_yaml(arg_pv, arg_file):
    # print("args = "+arg_pv.replace('\n','').replace('"',''))
    
    arg_pv=arg_pv.replace('\n','').replace('"','')
    arg_file=arg_file.replace('\n','').replace('"','')

    # genFileCmd = "kubectl get pv -oyaml "+arg_pv+" > ./test/"+arg_file+".yaml"
    f=open("test/"+arg_file+".yaml", 'w')
    out=subprocess.check_output("kubectl get pv -oyaml "+arg_pv, shell=True)
    f.write(out)
    f.close()
    mod_file(arg_file)

def export_pv(args):
    # check directory & make directory
    if os.path.exists(args):
        print("Temp directory already exists")
    else:
        os.mkdir(args)
        print("Temp directory create")

    # export PVs to yaml files

    statusCmd="kubectl get pv -ojson | jq '.items[].status.phase'"
    statusRes = Popen(statusCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    #parsing_pv, parsing_file = [], []
    #parsing_export, parsing_export_pv, parsing_export_file = dict(), dict(), dict()
    cnt = 0
    while True:
        cmd_status = statusRes.stdout.readline()
        cmd_status = cmd_status.encode('ascii').replace('\n','').replace('"','')
        if not cmd_status:
            break
        elif 'Available' == cmd_status:
            cnt+=1
            continue
        elif 'Bound' == cmd_status:
            # pv_name is a base of yaml file.
            # claimRef name use for making file name
            pvNameCmd = "kubectl get pv -ojson | jq '.items["+str(cnt)+"].metadata.name'"
            pvNameRes = Popen(pvNameCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

            fileNameCmd = "kubectl get pv -ojson | jq '.items["+str(cnt)+"].spec.claimRef.name'"
            fileNameRes = Popen(fileNameCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

            export_pv_yaml(pvNameRes.stdout.read(), fileNameRes.stdout.read())
            cnt+=1
        else:
            break

def import_pv():
    findGenFileCmd = "ls -al test | awk '{print $9}' | sed '1,3d'"
    findGenFileRes = Popen(findGenFileCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    while True:
        genFileName = findGenFileRes.stdout.readline()
        genFileName = genFileName.encode('ascii').replace('\n','').replace('"','')
        if not genFileName:
            break
        else:
            applyPvCmd = "kubectl apply -f "+genFileName
            applyPvRes = Popen(applyPvCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            applyPvRes.stdout.read()

def check_dir(arg_dir):
    if os.path.exists(arg_dir):
        pass
    else:
        os.mkdir(arg_dir)

def init_context(args):
    # declare variables
    clusters, contexts, users = [], [], []
    new_config = {}
    new_config_file = 'key/new-kube-config.yaml'
    arg_dir = 'key'

    check_dir(arg_dir)
    for params in os.listdir("../"+args):
        print(params)
    #     findDirCmd = "find -name '"+params.encode('utf-8')+"'"
    #     findDirRes = Popen(findDirCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    #     findDir = findDirRes.stdout.read()
    #     shutil.copy2(findDir+'infra/.output/kube-config.yaml',arg_dir+'/'+params+'-kube-config.yaml')
   
    # if os.path.exists(new_config_file):
    #     os.remove(new_config_file)
    # else:
    #     pass

    # file_names = os.listdir(arg_dir)
    # for file_name in file_names:
    #     f = open(arg_dir + "/"+ file_name)
    #     dataMap = yaml.safe_load(f)
    #     clusters.append(dataMap['clusters'][0])
    #     contexts.append(dataMap['contexts'][0])
    #     users.append(dataMap['users'][0])
    #     current_ctx = dataMap['current-context']
    #     f.close()
    # print(clusters)
    # print("==================================================================\n")
    # print(contexts)
    # print("==================================================================\n")
    # print(users)
    # print("==================================================================\n")
    # new_config = {'kind': 'Config', 'preferences': {}, 'current-context':current_ctx, 
    #         'clusters': clusters, 'contexts': contexts, 'users': users}
    
    # with open(new_config_file, 'w') as yaml_file:
    #     yaml.dump(new_config, yaml_file, default_flow_style=False)
    # shutil.copy2(new_config_file, home+'/.kube/config')

    
def switch_context():

    return

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:e:i:t:")
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(1)

    for opt,args in opts:
        #result=args.split(',')
        if ( opt == "-e" ) or ( opt == "--export" ):
            print("export directory = "+args)
            export_pv(args)
        elif ( opt == "-i" ) or ( opt == "--import" ):
            print("Importing PV... "+args)
        elif ( opt == "-s" ) or ( opt == "--switch" ):
            switch_context()
        elif ( opt == "-t" ) or ( opt == "--init" ):
            print(len(args))
            if len(args) > 0:
                init_context(args)
            else:
                print('Wrong argument... Please check help for using it 1')
        elif ( opt == "-h" ) or ( opt == "--help" ):
            help()
    return

if __name__ == "__main__":
    main()