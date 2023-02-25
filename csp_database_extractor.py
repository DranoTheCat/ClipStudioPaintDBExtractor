#!/usr/bin/env python

import PySimpleGUI as sg
import os
import pathlib
import sqlite3
import bitstring

valid_extensions = [ ".clip", ".csp" ]

l = [ [sg.Text("Clip Studio Paint Sqlite3 Database Extractor.\n\nChoose the top-level folder.  This tool will recursively scan all subfolders.")],
      [sg.HorizontalSeparator()],
      [sg.Text("Choose folder: "), sg.Input(key="_FileBrowse_", enable_events=True, visible=False), sg.FolderBrowse("Select Folder", target="_FileBrowse_"), sg.Text("", key="_FolderName_")],
      [sg.Multiline("[Event Log]", auto_refresh = True, size=(150, 15),  autoscroll = True, horizontal_scroll = True, background_color='white', text_color='black',
            enable_events=True, key="_LogBox_")],
      [sg.Button("Process Folder", key="_ProcessFolder_", disabled = True),
       sg.Checkbox("Overwrite existing Sqlite3 Databases", default=-False, key="_Overwrite_", tooltip="Checking this will force overwriting of all existing PNG files."),
       sg.Push(),
       sg.Button("Exit")]
    ]

window = sg.Window(title="CSP Sqlite3 Database Extractor", icon="icons/favicon.ico", layout=l, margins=(50, 20))
textbox = window['_LogBox_']

def logline(msg):
    textbox.update(textbox.get()+"\n"+msg)

def processFolder(folder):
    logline("Processing top-level folder: "+folder)
    for path, _directories, files in os.walk(folder):
        for file in files:
            if pathlib.Path(file).suffix in valid_extensions:
                f = os.path.join(path, file)
                logline("Found CSP file: "+f)
                stem = pathlib.Path(file).stem
                db_file = os.path.join(path, stem + ".sqlite")
                if os.path.exists(db_file):
                    logline("Found existing extracted DB file: " + db_file)
                    if values['_Overwrite_'] == True:
                        logline("Overwriting file...")
                        processFile(f, db_file)
                else:
                    processFile(f, db_file)

def processFile(file, db_file):
    logline("Processing file " + file)
    with open(file, mode="rb") as f:
        rawdata = f.read()
        s = bitstring.ConstBitStream(rawdata)
        found = s.find(b'SQLite format 3\000', bytealigned=True)
        if not found:
            logline("File does not seem to be a valid Clip Studio Paint file.")
            return
        logline("--> File seems to be valid!  SQLlite3 Header found at {} {}".format(found, s.bytepos))
        f.seek(s.bytepos)
        sql_data = f.read()
        with open(db_file, mode="wb") as w:
            w.write(sql_data)
        w.close()

# Entry point
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "_FileBrowse_":
        folder = values['_FileBrowse_']
        logline("Found "+folder+" as a valid folder.")
        window['_FolderName_'].update(folder)
        if os.path.exists(folder):
            window['_ProcessFolder_'].update(disabled=False)
    elif event == "_ProcessFolder_":
        window['_ProcessFolder_'].update(disabled=True)
        logline("[ Starting processing... ]")
        processFolder(folder)
        if os.path.exists("temp.db"):
            os.remove("temp.db")
        logline("[ Processing Complete. ]")
        logline("")
        window['_ProcessFolder_'].update(disabled=False)

window.close()