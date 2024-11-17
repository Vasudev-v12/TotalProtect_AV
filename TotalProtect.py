from signatureScan import *
#from dynamicAnalysis import *
from VDBapi import *
from fuzzyHashing import *

def menu():
    print("===========================DASHBOARD============================\n")
    print("1.Quick Scan\n2.Fuzzy Scan\n3.Cloud Scan\n4.Exit")
    print("\n================================================================")

def main():
    menu()
    while(True):
        Input = input()
        if Input == "1":
            print("===========================QUICK SCAN===========================")
            path = input("Enter directory or File path to be scanned: ")
            scan_directory(path)
            print("Scan completed\n")
            print("================================================================")
        elif Input == "2":
            print("===========================FUZZY SCAN===========================")
            path = input("Enter directory or File path to be scanned: ")
            scanFile(path)
            print("Scan completed\n")
            print("================================================================")
        elif Input == "3":
            print("===========================CLOUD SCAN===========================")
            path = input("Enter directory or File path to be scanned: ")
            getResult(path)
            print("================================================================")
        elif Input == "4":
            print("\n>>>>>>>>>>>>>>>>>>>>>>>>>> EXITING <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            return


if __name__ == "__main__":
    print("=========================TOTAL PROTECT==========================")
    main()
    
