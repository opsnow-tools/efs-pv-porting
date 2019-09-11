# EFS-PV-PORTING script

 `efs-pv-porting` can export current cluster PV(Persistent Volume) and import new cluster.

## Use case
You should install python2.7.

```
$ ./run.py -h
-----------------------------------------
|            efs-pv-porting             |
-----------------------------------------
Available OPTIONS:
    -e / --export       Exporting PV in old cluster
                        ex) ./run.py -e export_file   // ./run.py --export export_file
    -i / --import       Importing PV in new cluster
    -t / --init         Initializing Kubeconfig file. Must place with cluster directory. And It can find right place of .output directoires
                        ex) ./run.py -t key  // ./run.py --init key
    -s / --switch       Switching context cluster
    -h / --help         help
Usage: ./run.py [OPTIONS] [ARGS]

Sequences:
    ./run.py -t                 --> Initializing
    ./run.py -s                 --> Setting old cluster
    ./run.py -e export_file     --> Export
    ./run.py -i                 --> Import
```
