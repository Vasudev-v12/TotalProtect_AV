import hashlib
import os
import requests
# import json


def generate_md5(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        return "File not found."


def scan_folder_and_generate_md5(folder_path):
    md5_hashes = {}
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            md5_hashes[file_path] = generate_md5(file_path)
    return md5_hashes


def virusScan(item):
    url = "https://www.virustotal.com/api/v3/files/"+item
    headers = {'accept': 'application/json', 'x-apikey': 'a9594ba3487ed4bc176060925bfda31d65a80f6482414a7eba7d3e2f7eca60bd'}
    response = requests.get(url, headers=headers)
    try:
        data = response.json()

        print("Virus Name: " +data['data']['attributes']['meaningful_name'])
        print("Threat category: "+data['data']['attributes']['popular_threat_classification']['popular_threat_category'][0]['value'])
        print("Links : "+ data['data']['links']['self'])
        print(" ")
    finally:
        print("Item is not recognized as a virus or has no associated data")


def getResult(folder_path = "",hashMD5 = ""):
    if folder_path == "":
        print("Enter a valid path !!")
        return
    if hashMD5 == "":
        md5_hashes = scan_folder_and_generate_md5(folder_path)
        for file_path, md5 in md5_hashes.items():
            print("Scanning file: "+file_path)
            virusScan(md5)
    else:
        print("Cheching for the given hash: "+hashMD5)
        virusScan(hashMD5)
    print("Cloud Scanning completed")
        
if __name__ == "__main__":
    #getResult(hashMD5 = "2d75cc1bf8e57872781f9cd04a529256")
    #getResult(folder_path = "D:\\WEB development\\test website")
    getResult("D:\\WEB development\\test website","")
