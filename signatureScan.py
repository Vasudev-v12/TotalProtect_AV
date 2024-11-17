import os
import hashlib
import csv

# Example virus signatures (hexadecimal byte patterns)
VIRUS_SIGNATURES = {
    "YARA":{
    1:"1e03444e8954f8bc34882dc780ceb2e4e3426d22", #SHA1
    2:"707b752f6bd89d4f97d08602d0546a56d27acfe00e6d5df2a2cb67c5e2eeee30", # SHA256
    3:"8fe7bfef6ebc53e9047561d35555cd24" #MD5
    },
    "RemcosRAT":{
    1:"21cf02ec5fa8d8f4bc97803e02c3e638d51b69bd",
    2:"a9d403efd3d1d5740a5b1d8a0d691422b4cede106265437f533523f2d7bac16e",
    3:"ae75577913968ec41742093de9a8f00d"
    }
}

malwareDB = "malwareHashes.csv"

malHashList = []

def printVirusHashes():
    for virus in VIRUS_SIGNATURES:
        print(virus,end="\n")
        for i in range(1,5):
            print(VIRUS_SIGNATURES.get(virus).get(i))


def list_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def calculate_hashes(file_path):    
    sha256_hash = hashlib.sha256()
    sha1_hash = hashlib.sha1()
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                sha256_hash.update(chunk)
                sha1_hash.update(chunk)
                md5_hash.update(chunk)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    return [sha1_hash.hexdigest(),sha256_hash.hexdigest(),md5_hash.hexdigest()]


def print_hashes(hashes):
    if not hashes:
        return
    
    print("Hash Values:")
    print(f"  SHA1: {hashes[1]}")
    print(f"  SHA256: {hashes[2]}")
    print(f"  MD5: {hashes[3]}")


def scan_file(file_path):
    # try:
    for malware in malHashList:
        hashes = calculate_hashes(file_path)
        i = -1
        if (malware[1] in hashes[0]):
            i=1
        elif(malware[2] in hashes[1]):
            i=2
        elif(malware[3] in hashes[2]):
            i=3
        if(i != -1):
            print(f"Malware signature found in {file_path}\nName of malware: {malware[0]}\nsignature detected: {malware[i]}")
            return True
    return False
    # except Exception as e:
    #     print(f"Error scanning: {e}")
    # return False


def scan_directory(directory):
    with open(malwareDB, "r") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        for line in reader:
            malHashList.append(line)
    
    print("STARTED SCANNING THE DIRECTORY "+directory)
    for root,_, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Scanning {file_path}...")
            flag = scan_file(file_path)
            if flag == False:
                print("No viruses were found")


if __name__ == "__main__":
    directory_to_scan = "D:\\WEB development\\test website"#input("Enter the directory to scan: ") #Enter the path of the directory to be scanned

    files = list_files(directory_to_scan)
    # printVirusHashes()
    # for file in files:
    #     hashes = calculate_hashes(file)
    #     print("\n")
    #     print_hashes(hashes)
    #     scan_file(file)

    #print(type(VIRUS_SIGNATURES.get("YARA").get(1)))
    scan_directory(directory_to_scan)
