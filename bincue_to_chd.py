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
parser.add_argument('-nr', '--non-recursive', action = 'store_true')
parser.add_argument('-y', '--skip-check', action='store_true')
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

def parse_file(file):
    disc_tag = re.search("\s\(Disc.*\)", file.name)
    chd_file = file.stem + ".chd"
    target_dir = pathlib.Path(file.parent)

    if(disc_tag is not None):
        # CHD in place, update the .m3u, and remove the .bin/.cues.
        playlist_file = pathlib.Path( file.name[0:disc_tag.start()] + ".m3u" )
        print(f"Playlist file: {playlist_file}")
        
        # If this is the first disc, blow up the existing .m3u file.
        if "1" in disc_tag.string:
            os.remove(pathlib.Path(target_dir, playlist_file))
        
        with open(pathlib.Path(target_dir, playlist_file), "a") as multidisc_tracks:
            multidisc_tracks.write(str(chd_file) + "\n")
        
        print(f"Converting {file.name} to {chd_file}")
        outfile = pathlib.Path(target_dir, chd_file)

        subprocess.run([target_chdman, "createcd", "-i", file, "-o", outfile])
        target_bins = pathlib.Path.glob(target_dir, file.stem + "*.bin")
        for bin in target_bins:
            os.remove(bin)
        os.remove(file)
    
    else:
        # Create CHD up one level, and then delete this directory.
        print(f"File: {file} Target_Dir: {target_dir}")
        outfile = pathlib.Path(target_dir.parent, chd_file)
        subprocess.run([target_chdman, "createcd", "-i", file, "-o", outfile])
        shutil.rmtree(target_dir)


# Iterate through the paths the user pointed to and construct a list of paths.
def assemble_archives():
    files_to_parse = []

    filepath = pathlib.Path(args.path)
    if args.non_recursive:
        for file in sorted(list(pathlib.Path(args.path).glob("*.cue"))):
            files_to_parse.append(file)
    
    else:
        for file in sorted(list(filepath.rglob("*.cue"))):
            files_to_parse.append(file)

    return files_to_parse

def parse(files):
    for index, file in enumerate(files):
        print(f"Processing {file}: {index+1}/{files.__len__()}")
        parse_file(file)

bad_files = []
print("Will operate on: ")
files_to_parse = assemble_archives()
for file in files_to_parse:
    print(str(file))

if(not args.skip_check):
    user_checked = input("Does this look correct (Y/n)?: ")
    if user_checked != "n" and user_checked != "N":
        print("OK")
        parse(files_to_parse)
        # do stuff
    else:
        print("Cancelling.")
else:
    # do stuff
    print("OK")