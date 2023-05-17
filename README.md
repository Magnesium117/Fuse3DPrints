# Fuse3DPrints
A Python script to print one gcode file on top of another with or without z offset and Filament change. 

ONLY WORKS WHITH EDITS TO THE START AND END GCODE: 
- at the end of Start G-code add: "; Start Gcode done"
- at the begining of End G-code add: "; begin End Gcode"

ONLY TESTED FOR PRUSASLICER

IT IS ADVISED TO LOOK AT THE PRODUCED GCODE AFTER THE FIRST APPLICATION TO SPOT ANY MISTAKES THE SOFTWARE MADE.
The script removes part of the gcode(like auto homeing for the second file or the purge line for any file but the first one) 
Additionaly the script adds, if wished a z-offset to any file but the first one
