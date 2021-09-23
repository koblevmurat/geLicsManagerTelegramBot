import subprocess

utilsPath = ''
rootPassword = ''
bitmobileHost = ''

def getSP(sn):
    sp = None
    try:
        cmd = utilsPath 
        args = f' -sgp -host {bitmobileHost} -p {rootPassword} -sn {sn}'
        output = subprocess.run(cmd + args, capture_output=True)
        sp = str(output.stdout.decode().replace("\r\n",''))
    except:
        print("io error")
    finally:
        return sp


def getLics(sn, sp):
    output = ""
    try:
        cmd = utilsPath
        args = f' -glicc -host {bitmobileHost} -sp {sp} -sn {sn}'
        output = subprocess.run(cmd + args, capture_output=True)
        output = output.stdout
    except:
        print("io error")
    finally:
        return output

def slic(sn, licNum):
    output = ""
    try:
        cmd = utilsPath
        args = f' -slic -host {bitmobileHost} -p {rootPassword} -sn {sn} -slic {licNum}'
        output = subprocess.run(cmd + args, capture_output=True) 
        output = output.stdout 
    except:
        print("io error")  
    finally:
        return output

if __name__ == '__main__':
    #print(getSP('demo'))