# Scripts
A dumping ground for misc scripts I am writing to save myself the hassle

## Redump.py
Recursively extracts Redump games into folders labelled with their name, unpacking multi-disc games into a single folder with no disc label.

### Caveats
* Dependent on `py7zr`
* I am using `os.walk()` to traverse the directories, but it will traverse through the directories that get made in the extracting process. This is fine for small use cases, but will blow up quickly. **I would not recommend running this script on an entire console library directory.** I may or may not fix this later.
