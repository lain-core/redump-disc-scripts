import argparse
import os
import py7zr
import re
import pathlib

# TODO: Python will handle my garbage paths for NT/POSIX for now, but in the future this should really use Pathlib.

parser = argparse.ArgumentParser(
    prog = "Redump/No-Intro Extraction Tool",
    description = "Unpacks .7z files into directories for disc based games",
)

parser.add_argument('-r', '--recursive', action = 'store_true')
parser.add_argument('path')
args = parser.parse_args()



def parse_directory(directory_base, files):
    bad_files = []
    target_dir = ""
    for file in files:
        if(".7z" in file):
            disc_tag = re.search("\(Disc.*\)", file)
            rev_tag = re.search("\(Rev.*\)", file)
            if(disc_tag is not None):
                print(f"Found multidisc: {file}")
                # Create a directory from the stub of this and then find all other games with this name.
                target_dir = directory_base / pathlib.Path( file[0 : disc_tag.start() - 1] )# disc_tag.start() - 1 will remove the trailing space.

                # If the directory doesn't exist, see if there is a directory with the revision name instead.
                if not os.path.exists( target_dir ) and rev_tag is not None:
                    target_dir = directory_base / ( pathlib.Path( file[0: disc_tag.start() - 1] + " " + rev_tag.group(0) ))
                    if(not os.path.exists( target_dir )):
                        os.mkdir(target_dir)
                elif(not os.path.exists(target_dir)):
                    os.mkdir(target_dir)
            else:
                print(f"found single disc: {file}")
                # Extract in place.
                target_dir = directory_base / pathlib.Path( file[0:(file.find(".7z"))] )
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)
            
            # Check if this has already been handled previously
            cue_name = file[0:file.find(".7z")] + ".cue"
            print(f"File stem: {cue_name}")
            cue_file = target_dir / pathlib.Path( cue_name )
            print(f"Target cue file is: {cue_file}")
            if(not os.path.exists( cue_file )):
                print(f"Extracting {file} to {target_dir}")
                try:
                    with py7zr.SevenZipFile(directory_base / pathlib.Path(file), 'r') as archive:
                        archive.extractall(path = target_dir)
                except:
                    print(f"Failed to extract {file}")
                    bad_files.append(file)
                     
            else:
                print(f"{file} has already been extracted. Skipping...")

for root, dirs, files in os.walk(args.path):
    bad_files = []
    target_dir = ""
    if(not args.recursive):
        print("Only operating on root directory")
        parse_directory(pathlib.Path(root), files)
        break
    else:
        # FIXME: We will recursively walk through all of the directories we make in this process as well.
        # It's not the end of the world, because we check for a 7z extension, but it would be good to fix this.
        if(files is not []):
            parse_directory(pathlib.Path(root), files)
print(f"Failed to extract {bad_files}")
