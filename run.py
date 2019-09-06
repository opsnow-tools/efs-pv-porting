import os
import sys
import getopt

def help():
    print("print help usage")
    return

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"he:i", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(1)


    for opt,args in opts:
        if ( opt == "-e" ) or ( opt == "--export" ):
            print("export directory = "+args)
        elif ( opt == "-i" ) or ( opt == "--import" ):
            print("Importing PV... "+args)
        elif ( opt == "-h" ) or ( opt == "--help" ):
            help()

    return

if __name__ == "__main__":
    main()