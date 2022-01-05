#Written by Marcel Gansfusz
def f3dp(name,nfiles,offset,matchnge):
    #name=str(input("Path to Gcode files \n[Gcodes/Part0.gcode->enter Gcodes/Part]: "))
    #nfiles=int(input("Number of gcode files: "))
    files=[]
    #offset=[]
    #matchnge=[]
    startposz=[]
    startpose=[]
    #offset.append(0)
    #matchnge.append(False)
    startposz.append(0)
    startpose.append(0)
    for n in range(nfiles):
        with open(name+str(n)+".gcode","r") as f:
            files.append(f.readlines())
        if n>0:
            #offset.append(float(input("Input offset of "+name+str(n)+".gcode to the Buidlplate: ")))
            #if input("Change the filament between "+name+str(n-1)+".gcode and "+name+str(n)+".gcode [Y;N]: ").upper()=="Y":
            #    matchnge.append(True)
            #else:
            #    matchnge.append(False)
            startposz.append(0)
            startpose.append(0)
    n=0
    dellines=False
    for file in files:
        nl=0
        for line in file:
            if n!=0:
                if line[:3]=="G28" or line[:3]=="G29":
                    dellines=True
                #if line[:6]==";LAYER":
                #    dellines=False
                #if line==";LAYER:0\n":
                #    dellines=True
                if line[:5]==";MESH":
                    dellines=False
                if dellines:
                    numberize=False
                    number=""
                    for c in line:
                        if c==";":
                            break
                        if numberize and c!="." and c!="0" and c!="1" and c!="2" and c!="3" and c!="4" and c!="5" and c!="6" and c!="7" and c!="8" and c!="9":
                            numberize=False
                        if numberize:
                            number+=c
                        if c=="Z":
                            numberize=True
                    if number!="":
                        startposz[n]=float(number)+offset[n]
                    numberize=False
                    number=""
                    for c in line:
                        if c==";":
                            break
                        if numberize and c!="." and c!="0" and c!="1" and c!="2" and c!="3" and c!="4" and c!="5" and c!="6" and c!="7" and c!="8" and c!="9":
                            numberize=False
                        if numberize:
                            number+=c
                        if c=="E":
                            numberize=True
                    if number!="":
                        startpose[n]=float(number)
                    files[n][nl]=""
            if n!=nfiles-1:
                if line[:7]=="M104 S0":
                    files[n][nl]=""
                if line[:9]=="M84 X Y E":
                    files[n][nl]=""
            if offset[n]!=0 and not dellines:        
                numberize=False
                number=""
                i=0
                posa=0
                pose=0
                for c in line:
                    if c==";":
                        break
                    if numberize and c!="." and c!="0" and c!="1" and c!="2" and c!="3" and c!="4" and c!="5" and c!="6" and c!="7" and c!="8" and c!="9":
                        numberize=False
                    if numberize:
                        pose=i+1
                        number+=c
                    if c=="Z":
                        posa=i
                        numberize=True
                    i+=1
                if number!="":
                    num=float(number)
                    num+=offset[n]
                    number=str(num)
                    files[n][nl]=line[:posa+1]+number+line[pose:]
            nl+=1
        n+=1
    with open(name+".gcode","w") as f:
        n=0
        for fle in files:
            npting=True
            if matchnge[n]:
                f.write("M600\n")            
            for line in fle:
                if n>0 and npting and line[:2]=="G1":
                    f.write("G0 Z"+str(startposz[n])+"\n")
                    if not matchnge[n]:
                        f.write("G1 F1500 E4\n")
                    f.write("G92 E"+str(startpose[n])+"\n")
                    npting=False
                f.write(line)            
            n+=1
    print("Files combined as "+str(name)+".gcode")
    return str(name)+".gcode"

def main():
    name=str(input("Path to Gcode files \n[Gcodes/Part0.gcode->enter Gcodes/Part]: "))
    nfiles=int(input("Number of gcode files: "))
    offset=[]
    matchnge=[]
    offset.append(0)
    matchnge.append(False)
    for n in range(nfiles):
        if n>0:
            offset.append(float(input("Input offset of "+name+str(n)+".gcode to the Buidlplate: ")))
            if input("Change the filament between "+name+str(n-1)+".gcode and "+name+str(n)+".gcode [Y;N]: ").upper()=="Y":
                matchnge.append(True)
            else:
                matchnge.append(False)
    f3dp(name,nfiles,offset,matchnge)


if __name__=="__main__":
    main()
