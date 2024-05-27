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
parser.add_argument('-y', '--skip-check', action='store_true')
parser.add_argument('path')
args = parser.parse_args()


def parse_file(file):
    # Fetch relevant details about this title.
    disc_tag = re.search("\s\(Disc.*?\)", file.name)
    cue_name = file.stem + ".cue"
    cue_file = pathlib.Path( cue_name )
    target_dir = pathlib.Path(file.parent, file.stem)
    # print(f"Cue file is {cue_file}")


    if(disc_tag is not None):
        #print(f"Found multidisc game!")
        # Create a directory from the stub of this and then find all other games with this name.
        # This works because the Disc tag is always the last one in the name, so this will capture all revisions neatly.
        #print(f"Game name is {file.name[0:disc_tag.start()]}")
        playlist_file = pathlib.Path( file.name[0:disc_tag.start()] + ".m3u")

        target_dir = pathlib.Path( file.parent, file.name[0:disc_tag.start()] )

        # If this is Disc 1 of a game, check if there is already an m3u and delete if so.
        if("1" in disc_tag.string):
            if os.path.exists(target_dir):
                if os.path.isfile(pathlib.Path(target_dir, playlist_file)):
                    os.remove(pathlib.Path(target_dir, playlist_file))

        # If the directory doesn't exist, make it.
        if(not os.path.exists( target_dir )):
            os.mkdir(target_dir)

        # Append this file's .cue into the .m3u for a multidisc game.
        with open (pathlib.Path(target_dir, playlist_file), "a") as multidisc_tracks:
            multidisc_tracks.write(str(cue_file) + "\n")

    else:
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
    
    # Check if this has already been handled previously
    print(f"Extracting {file} to {target_dir}")
    try:
        with py7zr.SevenZipFile(pathlib.Path(file), 'r') as archive:
            archive.extractall(path = target_dir)
    
    except KeyboardInterrupt:
        print("Cancelled operation.")
        os.remove(target_dir)
        exit(0)
    
    except:
        print(f"Failed to extract {file}")
        bad_files.append(file)

# Iterate through the paths the user pointed to and construct a list of paths.
def assemble_archives():
    files_to_parse = []

    filepath = pathlib.Path(args.path)
    if args.recursive: 
        for file in sorted(list(filepath.rglob("*.7z"))):
            files_to_parse.append(file)
    
    else:
        for file in sorted(list(pathlib.Path(args.path).glob("*.7z"))):
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


# if(bad_files is not []):
#     print(f"Failed to extract {bad_files}")
