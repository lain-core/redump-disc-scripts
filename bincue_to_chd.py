import argparse
import os
import glob
import re
import subprocess
import shutil

parser = argparse.ArgumentParser(
    prog = "Bin/Cue to CHD",
    description = "Batch converts bin/cues to CHD."
)

parser.add_argument('path')
parser.add_argument('-r', '--recursive', action = 'store_true')
args = parser.parse_args()

def parse_directory(directory_base, files):
    bad_files = []
    for file in files:
        if(".cue" in file):
            disc_tag = re.search("\(Disc.*\)", file)
            if(disc_tag is not None):
                # CHD in place, remove .bin/.cues
                print(directory_base)
                filestem = file[0:file.find(".cue")]
                infile = directory_base + "/" + file 
                outfile = directory_base + "/" + filestem + ".chd"
                subprocess.run(["chdman", "createcd", "-i", infile, "-o", outfile ])
                target_bins = glob.glob(directory_base + "/" + filestem + "*.bin")
                for bin in target_bins:
                    os.remove(bin)
                os.remove(directory_base + "/" + filestem + ".cue")

            else:
                # CHD, move up directory, remove directory with .bin/.cue
                print(directory_base)
                outfile = file[0:file.find(".cue")]
                print(outfile)
                print(f"Will write to {directory_base}/../")
                infile = directory_base + "/" + file 
                outfile = directory_base + "/" + file[0:file.find(".cue")] + ".chd"
                subprocess.run(["chdman", "createcd", "-i", infile, "-o", outfile ])
                shutil.move( outfile, (directory_base + "/../"))
                shutil.rmtree(directory_base)

for root, dirs, files in os.walk(args.path):
    bad_files = []
    target_dir = ""
    if(files is not []):
        if(not args.recursive):
            print("Only operating on root directory")
            parse_directory(root, files)
            break
        else:
            # FIXME: We will recursively walk through all of the directories we make in this process as well.
            # It's not the end of the world, because we check for a 7z extension, but it would be good to fix this.
            parse_directory(root, files)

print(f"Failed to extract {bad_files}")