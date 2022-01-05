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
        gui.Text("Filename of gcode files")
    ],
    [
        gui.Text("Filename:"),
        gui.In(size=(34,1),enable_events=True,key="-FILENAME-")
    ],
    [
        gui.Listbox(values=[],enable_events=True,size=(43,20),key="-CHSN FILE LIST-")
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
filenumber=0
nfiles=0
name=""
offsets=[]
filChanges=[]
def ProcessEvent(event,values):
    global filenumber
    global nfiles 
    global name
    global offsets
    global filChanges
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
            f=f[:-6]
            while f[-1].isnumeric():
                f=f[:-1]
            window["-FILENAME-"].update(f)
            values["-FILENAME-"]=f
            ProcessEvent("-FILENAME-",values)
        
    elif event=="-FILENAME-":
        folder=values["-FOLDER-"]
        try:
            file_list=os.listdir(folder)
        except:
            file_list=[]
        fnames=[]
        offsets=[]
        filChanges=[]
        nfiles=0
        name=""
        while True:
            if os.path.isfile(os.path.join(folder,values["-FILENAME-"]+str(nfiles)+".gcode")):
                name=os.path.join(folder,values["-FILENAME-"])
                fnames.append(values["-FILENAME-"]+str(nfiles)+".gcode")
                nfiles+=1
                offsets.append(float(0))
                filChanges.append(False)
            else:
                break

        window["-CHSN FILE LIST-"].update(fnames)
        filenumber=0 
        if nfiles>0:
            window["-CHSN FILE LIST-"].update(set_to_index=[0])  
            window["-SELECT FILE-"].update(values["-FILENAME-"]+"0.gcode")
            window["-OFFSET-"].update("")
            window["-CHANGE FILAMENT-"].update(False)
            window["-OFFSET-"].update(disabled=True)
            window["-CHANGE FILAMENT-"].update(disabled=True)

    elif event=="-CHSN FILE LIST-":
        if nfiles>0:
            window["-SELECT FILE-"].update(values["-CHSN FILE LIST-"][0])
            filenumber=int(values["-CHSN FILE LIST-"][0][len(values["-FILENAME-"]):-6])
            window["-OFFSET-"].update(offsets[filenumber])
            window["-CHANGE FILAMENT-"].update(filChanges[filenumber])
            if filenumber==0:
                window["-OFFSET-"].update(disabled=True)
                window["-CHANGE FILAMENT-"].update(disabled=True)
            else:
                window["-OFFSET-"].update(disabled=False)
                window["-CHANGE FILAMENT-"].update(disabled=False)

    elif event=="-OFFSET-":
        try:
            offsets[filenumber]=float(values["-OFFSET-"])
        except:
            window["-OFFSET-"].update("")

    elif event=="-CHANGE FILAMENT-":
        if filenumber>0:
            filChanges[filenumber]=values["-CHANGE FILAMENT-"]
        else:
            window["-CHANGE FILAMENT-"].update(False)

    elif event=="Combine":
        print(name)
        print(nfiles)
        print(offsets)
        print(filChanges)
        if nfiles>0:
            window["-OUTPUT-"].update("Saved as: "+f3dp(name,nfiles,offsets,filChanges))
        else:
            window["-OUTPUT-"].update("No files selected")

while True:
    event, values=window.read()
    ProcessEvent(event,values)
    if event=="Stop" or event==gui.WIN_CLOSED:
        break
window.close()
