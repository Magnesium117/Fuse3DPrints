#Written by Marcel Gansfusz
def f3dp(paths,offset,matchnge,name):
    files=[]
    for path in paths:
        with open(path,"r") as f:
            files.append(f.readlines())
    for filenr,file in enumerate(files):
        dellines=[]
        delmvmt=False
        section="s"     #s...stsart, g...general, e...end
        for n,line in enumerate(file):
            if section=="s" and filenr==0:
                section="g"
#<start Gcode>
            if section=="s":
                if "G28" in line or "G29" in line:
                    dellines.append(n)
                    delmvmt=True
                if delmvmt and ("G1" in line or "G0" in line):
                    dellines.append(n)
                if delmvmt and "; Start Gcode done" in line:
                    delmvmt=False
                    section="g"
#</Start Gcode>
#<Genderal Gcode>
            if offset[filenr]>0 and section=="g":
                if "G1" in line and "Z" in line:
                    i=line.find("Z")
                    pre=line[:i+1]
                    post=line[i+1:].split(" ",1)
                    post[0]=str(float(post[0])+offset[filenr])
                    files[filenr][n]=pre+post[0]+" "+post[1]
            if section=="g" and "; begin End Gcode" in line:
                section="e"
#</General Gcode>
#<End Gcode>
            if section=="e" and filenr<len(paths)-1:
                if "M140" in line or "M104" in line or "M107" in line or "M84" in line:
                    dellines.append(n);
                    if "M84" in line:
                        delmvmt=True
                elif delmvmt:
                    dellines.append(n)

#</End Gcode>
        for line in reversed(dellines):
            files[filenr].pop(line)

    with open(name,"w") as f:
        for n,fle in enumerate(files):
            if matchnge[n]:
                f.write("M600\n")            
            for line in fle:
                f.write(line)            
    print("Files combined as "+str(name))
    return str(name)

def isfloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def main():
    paths=[]
    offsets=[]
    matchnge=[]
    name=""
    print("input filenames (when finished enter nothing)")
    while True:
        name=input("Filename: ")
        if name=="":
            break
        paths.append(name)
        offset=input("Offset for this file: ")
        if isfloat(offset):
            offsets.append(offset)
        else:
            offsets.append(0)
        mat=input("Change material before file[t/f]: ")
        if mat=="t":
            matchnge.append(True)
        else:
            matchnge.append(False)
    name=input("Enter the name of the final gcode file: ")
    f3dp(paths,offset,matchnge,name)


if __name__=="__main__":
    main()
