import argparse
import os
import glob
import re
import subprocess
import shutil
import pathlib

parser = argparse.ArgumentParser(
    prog = "Bin/Cue to CHD",
    description = "Batch converts bin/cues to CHD."
)

parser.add_argument('path')
parser.add_argument('-r', '--recursive', action = 'store_true')
parser.add_argument('-w', '--windows', action = 'store_true', help = "Specifies if you are running on Windows or Other.")
args = parser.parse_args()

WINDOWS_CHDMAN = ".\chdman.exe"
LINUX_CHDMAN = "chdman"
target_chdman = ""
bad_files = []

if(args.windows):
    target_chdman = WINDOWS_CHDMAN
else:
    target_chdman = LINUX_CHDMAN

def parse_directory(directory_base, files):
    bad_files = []
    for file in files:
        if(".cue" in file):
            disc_tag = re.search("\(Disc.*\)", file)
            if(disc_tag is not None):
                # CHD in place, remove .bin/.cues
                filestem = file[0:file.find(".cue")]
                infile = directory_base / pathlib.Path(file) 
                outfile = directory_base / pathlib.Path( filestem + ".chd" )
                print(f"Converting {infile} to {outfile}")
                subprocess.run([target_chdman, "createcd", "-i", infile, "-o", outfile ])
                target_bins = pathlib.Path.glob( directory_base, (filestem + "*.bin") ) 
                for bin in target_bins:
                    os.remove(bin)
                os.remove(directory_base / pathlib.Path(filestem + ".cue"))

            else:
                # CHD, move up directory, remove directory with .bin/.cue
                outfile = file[0:file.find(".cue")]
                filestem = file[0:file.find(".cue")]
                infile = directory_base / pathlib.Path(file) 
                outfile = directory_base / pathlib.Path( filestem + ".chd" )
                print(f"Converting {infile} to {outfile}")
                subprocess.run([target_chdman, "createcd", "-i", infile, "-o", outfile ])
                shutil.move( outfile, (directory_base / pathlib.Path("../")) )
                shutil.rmtree(directory_base)

for root, dirs, files in os.walk(args.path):
    target_dir = ""
    if(files is not []):
        if(not args.recursive):
            print("Only operating on root directory")
            parse_directory(pathlib.Path(root), files)
            break
        else:
            # FIXME: We will recursively walk through all of the directories we make in this process as well.
            # It's not the end of the world, because we check for a 7z extension, but it would be good to fix this.
            parse_directory(pathlib.Path(root), files)

if(bad_files is not []):
    print(f"Failed to extract {bad_files}")