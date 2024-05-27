# Scripts
A dumping ground for misc scripts I am writing to save myself the hassle

## Redump.py
Recursively extracts Redump games into folders labelled with their name, unpacking multi-disc games into a single folder with no disc label, and a populated .m3u file.

For Example:
```
/ExampleDir
├── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1).7z
├── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2).7z
├── Klonoa - Door to Phantomile (USA).7z
├── Mega Man X6 (USA) (Rev 1).7z
└── RPGs
    ├── Chrono Cross (USA) (Disc 1).7z
    ├── Chrono Cross (USA) (Disc 2).7z
    ├── Final Fantasy IX (USA) (Disc 1) (Rev 1).7z
    ├── Final Fantasy IX (USA) (Disc 2) (Rev 1).7z
    ├── Final Fantasy IX (USA) (Disc 3) (Rev 1).7z
    └── Final Fantasy IX (USA) (Disc 4) (Rev 1).7z
```

Will Become:
```
/ExampleDir
├── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1)
│   ├── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1).bin
│   └── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1).cue
├── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1).7z
├── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2)
│   ├── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2).bin
│   └── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2).cue
├── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2).7z
├── Klonoa - Door to Phantomile (USA)
│   ├── Klonoa - Door to Phantomile (USA).bin
│   └── Klonoa - Door to Phantomile (USA).cue
├── Klonoa - Door to Phantomile (USA).7z
├── Mega Man X6 (USA) (Rev 1)
│   ├── Mega Man X6 (USA) (Rev 1).bin
│   └── Mega Man X6 (USA) (Rev 1).cue
├── Mega Man X6 (USA) (Rev 1).7z
└── RPGs
    ├── Chrono Cross (USA) 
    │   ├── Chrono Cross (USA) (Disc 1).bin
    │   ├── Chrono Cross (USA) (Disc 1).cue
    │   ├── Chrono Cross (USA) (Disc 2).bin
    │   ├── Chrono Cross (USA) (Disc 2).cue
    |   └── Chrono Cross (USA).m3u
    ├── Chrono Cross (USA) (Disc 1).7z
    ├── Chrono Cross (USA) (Disc 2).7z
    ├── Final Fantasy IX (USA) (Disc 1) (Rev 1).7z
    ├── Final Fantasy IX (USA) (Disc 2) (Rev 1).7z
    ├── Final Fantasy IX (USA) (Disc 3) (Rev 1).7z
    ├── Final Fantasy IX (USA) (Disc 4) (Rev 1).7z
    └── Final Fantasy IX (USA) (Rev 1)
        ├── Final Fantasy IX (USA) (Disc 1) (Rev 1).bin
        ├── Final Fantasy IX (USA) (Disc 1) (Rev 1).cue
        ├── Final Fantasy IX (USA) (Disc 2) (Rev 1).bin
        ├── Final Fantasy IX (USA) (Disc 2) (Rev 1).cue
        ├── Final Fantasy IX (USA) (Disc 3) (Rev 1).bin
        ├── Final Fantasy IX (USA) (Disc 3) (Rev 1).cue
        ├── Final Fantasy IX (USA) (Disc 4) (Rev 1).bin
        ├── Final Fantasy IX (USA) (Disc 4) (Rev 1).cue
        └── Final Fantasy IX (USA).m3u
```

### Usage
`python redump.py /path/to/root [-r]`
Use `-r` to specify recursive extraction, otherwise only files on the root directory will be managed.

### Caveats
* Dependent on `py7zr`

## bincue_to_chd
Take a directory of bin/cues and convert them the the MAME CHD format, correcting .m3us where necessary. If they are single-disc games, remove the containing folder as they now exist in only one file.

For Example:
```
/ExampleDir
├── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1)
│   ├── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1).bin
│   └── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1).cue
├── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2)
│   ├── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2).bin
│   └── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2).cue
├── Klonoa - Door to Phantomile (USA)
│   ├── Klonoa - Door to Phantomile (USA).bin
│   └── Klonoa - Door to Phantomile (USA).cue
├── Mega Man X6 (USA) (Rev 1)
│   ├── Mega Man X6 (USA) (Rev 1).bin
│   └── Mega Man X6 (USA) (Rev 1).cue
└── RPGs
    ├── Chrono Cross (USA) 
    │   ├── Chrono Cross (USA) (Disc 1).bin
    │   ├── Chrono Cross (USA) (Disc 1).cue
    │   ├── Chrono Cross (USA) (Disc 2).bin
    │   ├── Chrono Cross (USA) (Disc 2).cue
    |   └── Chrono Cross (USA).m3u
    └── Final Fantasy IX (USA) (Rev 1)
        ├── Final Fantasy IX (USA) (Disc 1) (Rev 1).bin
        ├── Final Fantasy IX (USA) (Disc 1) (Rev 1).cue
        ├── Final Fantasy IX (USA) (Disc 2) (Rev 1).bin
        ├── Final Fantasy IX (USA) (Disc 2) (Rev 1).cue
        ├── Final Fantasy IX (USA) (Disc 3) (Rev 1).bin
        ├── Final Fantasy IX (USA) (Disc 3) (Rev 1).cue
        ├── Final Fantasy IX (USA) (Disc 4) (Rev 1).bin
        ├── Final Fantasy IX (USA) (Disc 4) (Rev 1).cue
        └── Final Fantasy IX (USA).m3u
```

Will become:
```
/ExampleDir
├── Gran Turismo 2 (USA) (Arcade Mode) (Rev 1).chd
├── Gran Turismo 2 (USA) (Simulation Mode) (Rev 2).chd
├── Klonoa - Door to Phantomile (USA).chd
├── Mega Man X6 (USA) (Rev 1).chd
└── RPGs
    ├── Chrono Cross (USA) 
    │   ├── Chrono Cross (USA) (Disc 1).chd
    │   ├── Chrono Cross (USA) (Disc 2).chd
    |   └── Chrono Cross (USA).m3u
    └── Final Fantasy IX (USA) (Rev 1)
        ├── Final Fantasy IX (USA) (Disc 1) (Rev 1).chd
        ├── Final Fantasy IX (USA) (Disc 2) (Rev 1).chd
        ├── Final Fantasy IX (USA) (Disc 3) (Rev 1).chd
        ├── Final Fantasy IX (USA) (Disc 4) (Rev 1).chd
        └── Final Fantasy IX (USA).m3u
```

## Usage
`python bincue_to_chd.py /path/to/root [-r]`
Use `-r` to specify recursive traversal otherwise only files on the root directory will be managed.

### Caveats
* `chdman` must be installed. On Ubuntu/Debian, this is included in the `mame-tools` package.
* Multi-disc games are left in a containing folder, individual disc games have their folders and contents deleted after being made.
* **Be careful** when applying this to a large directory, as it **will** delete the bin/cues when it is finished compressing.
