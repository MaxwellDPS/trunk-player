from datetime import datetime

class source:
    def __init__(self, json):
        self.json = json
        self.source = int(json["source"])
        self.position = int(json["position"])
        self.time = datetime.fromtimestamp(int(json["time"]))
        self.signal_system = json["source"]

        if json["emergency"] == "false":
            self.emergency = False
        else:
            self.emergency = True

class freq:
    def __init__(self, json):
        self.json = json
        self.freq = int(json["freq"])
        self.spikes = int(json["spikes"])
        self.errors = int(json["errors"])
        self.position = int(json["position"])
        self.length = int(json["length"])

        self.time = datetime.fromtimestamp(int(json["time"]))


class call:
    def __init__(self, json):
        self.json = json

        self.id = int(json["id"])
        self.freq = int(json["freq"])
        self.sysNum = int(json["sysNum"])
        self.shortName = json["shortName"]
        self.talkgroup = int(json["talkgroup"])
        self.talkgrouptag = json["talkgrouptag"]
        self.elasped = int(json["elasped"])
        self.length = int(json["length"])
        self.state = int(json["state"])
        self.recNum = int(json["recNum"])
        self.srcNum = int(json["srcNum"])
        self.recState = int(json["recState"])
        self.sigmffilename = json["sigmffilename"]
        self.debugfilename = json["debugfilename"]
        self.filename = json["filename"]
        self.statusfilename = json["statusfilename"]
        self.startTime = datetime.fromtimestamp(int(json["startTime"]))
        self.stopTime = datetime.fromtimestamp(int(json["stopTime"]))


        if json["phase2"] == "false":
            self.phase2 = False
        else:
            self.phase2 = True

        if json["conventional"] == "false":
            self.conventional = False
        else:
            self.conventional = True

        if json["encrypted"] == "false":
            self.encrypted = False
        else:
            self.encrypted = True

        if json["emergency"] == "false":
            self.emergency = False
        else:
            self.emergency = True

        if json["analog"] == "false":
            self.analog = False
        else:
            self.analog = True

        self.sourceList = []
        for src in json["sourceList"]:
            self.sourceList.append(source(src)) 

        self.freqList = []
        for freqx in json["freqList"]:
            self.freqList.append(freq(freqx)) 

def createCall(Callx):
    pass

def endCall(Callx):
    pass


def handleMessage(message, type):
    if type == "call_start":
        callX = call(message["call"])
        createCall(callX)
    elif type == "call_end":
        callX = call(message["call"])
        endCall(callX)
    elif type == "calls_active":
        pass