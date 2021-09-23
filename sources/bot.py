# from sources.telega import Settings
import callUtils

Settings = None

def init():
    if Settings != None:
        callUtils.rootPassword = Settings['rootPassword']
        callUtils.utilsPath = Settings['UtilsPath']
        callUtils.bitmobileHost = Settings['bitmobileHost']

def glic(sn, sp=None):
    if sp == None:
        sp = callUtils.getSP(sn)
    if sp != None:
        UtilsOutput = str(callUtils.getLics(sn, sp))        
        if UtilsOutput.find('Invalid')==-1:
            return UtilsOutput.replace("b'{", '').replace("}\\r\\n\'", '')        
        else:
            return "not found"
    else:
        return "not found"    


def slic(sn):
    sp = callUtils.getSP(sn)
    if sp != None:
       UtilsOutput = str(callUtils.getLics(sn, sp))
       if UtilsOutput.find('Invalid')==-1:
            TotalLicenses = UtilsOutput.split(',')
            licCount = int(TotalLicenses[0][TotalLicenses[0].find(":")+1:]) 
            callUtils.slic(sn, licCount)
            return glic(sn, sp)
       else:
            return "not found"
    else:
        return "not found"

 
       
