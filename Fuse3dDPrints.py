import PySimpleGUI as gui
import os.path
from GMFil import f3dp
gui.theme("DarkRed1")
GetFolder=[
    [
        gui.Text("Folder with Gcode files")
    ], 
    [
        gui.Text("Folder:"),
        gui.In(size=(25,1),enable_events=True,key="-FOLDER-"),
        gui.FolderBrowse()
    ],
    [
        gui.Listbox(values=[],enable_events=True, size=(43,20),key="-FILE LIST-")
    ]
]
GetFilename=[
    [
        gui.Text("Files to combine")
    ],
    [
        gui.Text("Path to file:"),
        gui.In(size=(34,1),enable_events=True,key="-FILENAME-"),
        gui.FileBrowse()
    ],
    [
        gui.Listbox(values=[],enable_events=True,size=(43,20),key="-CHSN FILE LIST-")
    ],
    [
        gui.Button("↑",key="-MV UP-"),
        gui.Button("↓",key="-MV DOWN-"),
        gui.Button("-",key="-RM-"),
        gui.Button("+",key="-ADD-")
    ]
]
GetOffsetFC=[
    [
        gui.Text("Offset and Filamentchange for each gcode file")
    ],
    [
        gui.Text(size=(40,1),key="-SELECT FILE-")
    ],
    [
        gui.Text("Offset:"),
        gui.In(size=(35,1),enable_events=True,key="-OFFSET-")

    ],
    [
        gui.Checkbox(text="Change Filament before file",enable_events=True,key="-CHANGE FILAMENT-")
    ]
]
layout=[
    [
        gui.Text("Fuse 3D Prints")
    ],
    [
        gui.Column(GetFolder),
        gui.VSeperator(),
        gui.Column(GetFilename),
        gui.VSeperator(),
        gui.Column(GetOffsetFC)
    ],
    [
        gui.Button("Stop"),

        gui.Button("Combine"),
        gui.Text(size=(100,1),key="-OUTPUT-")
    ]


]
window=gui.Window("Fuse3DPrints",layout)

files=[]
name=""

def NamesFromFiles(files):
    return [p[0].split("/")[-1] for p in files]

def ProcessEvent(event,values):
    global files
    global name
    if event=="-FOLDER-":
        folder=values["-FOLDER-"]
        try:
            file_list=os.listdir(folder)
        except:
            file_list=[]
        fnames=[
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder,f))
            and f.lower().endswith(".gcode")
            and not f==".gcode"
        ]
        window["-FILE LIST-"].update(fnames)

    elif event=="-FILE LIST-":
        if len(values["-FILE LIST-"])>0:
            f=values["-FILE LIST-"][0]
            files.append([os.path.join(values["-FOLDER-"],values["-FILE LIST-"][0]),0,False])
            window["-CHSN FILE LIST-"].update(NamesFromFiles(files))
        
    elif event=="-ADD-":
        if os.path.isfile(values["-FILENAME-"]):
            files.append([values["-FILENAME-"],0,False])
            window["-CHSN FILE LIST-"].update(NamesFromFiles(files))
    
    elif event=="-RM-":
        el=window["-CHSN FILE LIST-"].get_indexes()
        for e in reversed(el):
            files.pop(e)
        files[0][1]=0
        files[0][2]=False
        window["-CHSN FILE LIST-"].update(NamesFromFiles(files))

    elif event=="-MV UP-":
        el=window["-CHSN FILE LIST-"].get_indexes()
        for e in el:
            if e>0:
                p=files.pop(e)
                files.insert(e-1,p)
        files[0][1]=0
        files[0][2]=False
        window["-CHSN FILE LIST-"].update(NamesFromFiles(files))

    elif event=="-MV DOWN-":
        el=window["-CHSN FILE LIST-"].get_indexes()
        for e in reversed(el):
            if e<len(files):
                p=files.pop(e)
                files.insert(e+1,p)
        files[0][1]=0
        files[0][2]=False
        window["-CHSN FILE LIST-"].update(NamesFromFiles(files))

    elif event=="-CHSN FILE LIST-":
        el=window["-CHSN FILE LIST-"].get_indexes()
        s=""
        l=NamesFromFiles(files)
        for e in el:
            if s!="":
                s+=", "
            s+=l[e]
        window["-SELECT FILE-"].update(s)
        window["-OFFSET-"].update(files[el[0]][1])
        window["-CHANGE FILAMENT-"].update(files[el[0]][2])
        if el[0]==0:
            window["-OFFSET-"].update(disabled=True)
            window["-CHANGE FILAMENT-"].update(disabled=True)
        else:
            window["-OFFSET-"].update(disabled=False)
            window["-CHANGE FILAMENT-"].update(disabled=False)

    elif event=="-OFFSET-":
        el=window["-CHSN FILE LIST-"].get_indexes()
        for e in el:
            try:
                files[e][1]=float(values["-OFFSET-"])
            except:
                window["-OFFSET-"].update("")

    elif event=="-CHANGE FILAMENT-":
        el=window["-CHSN FILE LIST-"].get_indexes()
        for e in el:
            if e>0:
                files[e][2]=values["-CHANGE FILAMENT-"]
            else:
                window["-CHANGE FILAMENT-"].update(False)

    elif event=="Combine":
        print(files)
        window["-OUTPUT-"].update("Saved as: "+f3dp(paths=[f[0] for f in files],offset=[f[1] for f in files],matchnge=[f[2] for f in files],name=NamesFromFiles(files)[0]))

while True:
    event, values=window.read()
    ProcessEvent(event,values)
    if event=="Stop" or event==gui.WIN_CLOSED:
        break
window.close()
