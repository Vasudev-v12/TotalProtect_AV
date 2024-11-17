import os
import sys
import random
from hashlib import md5
#-----------------------------------------------------------------------
class CBasicFuzzer:
 def __init__(self, file_in, folder_out, cmd):
    """ Set the directories and the OS command to run after mutating."""
    self.folder_out = folder_out
    self.file_in = file_in
    self.cmd = cmd

def mutate(self, buf):
    tmp = bytearray(buf)
    # Calculate the total number of changes to made to the buffer
    total_changes = random.randint(1, len(tmp))
    for i in range(total_changes):
    # Select a random position in the file
        pos = random.randint(0, len(tmp)-1)
        # Select a random character to replace
        char = chr(random.randint(0, 255))
        # Finally, replace the content at the selected position with the
        # new randomly selected character
        tmp[pos] = char
        return str(tmp)
    
def fuzz(self):
    orig_buf = open(self.file_in, "rb").read()
    # Create 255 mutations of the input file
    for i in range(255):
        buf = self.mutate(orig_buf)
        md5_hash = md5(buf).hexdigest()
        print("[+] Writing mutated file %s" % repr(md5_hash))
        filename = os.path.join(self.folder_out, md5_hash)
        with open(filename, "wb") as f:
            f.write(buf)
            # Run the operating system command to scan the directory with the av
            cmd = "%s %s" % (self.cmd, self.folder_out)
            os.system(cmd)
#-----------------------------------------------------------------------
def usage():
    print("Usage:", sys.argv[0], "<filename> <output directory> " + "<av scan command>")
#-----------------------------------------------------------------------
def main(file_in, folder_out, cmd):
 fuzzer = CBasicFuzzer(file_in, folder_out, cmd)
 fuzzer.fuzz()
if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
