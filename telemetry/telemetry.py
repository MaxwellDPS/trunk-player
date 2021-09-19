from datetime import datetime
from radio.models import System
from telemetry.models import Call, Freq, Source, SystemStatus

class source:
    def __init__(self, json):
        self.json = json
        self.source = int(json["source"])
        self.position = int(float(json["position"]))
        self.time = datetime.fromtimestamp(int(json["time"]))
        self.signal_system = json["signal_system"]

        if json["emergency"] == "false":
            self.emergency = False
        else:
            self.emergency = True

class freq:
    def __init__(self, json):
        self.json = json
        self.freq = int(float(json["freq"]))
        self.spikes = int(float(json["spikes"]))
        self.errors = int(float(json["errors"]))
        self.position = int(float(json["position"]))
        self.length = int(float(json["length"]))

        self.time = datetime.fromtimestamp(int(json["time"]))

class call:
    def __init__(self, json):
        self.json = json

        self.id = json["id"]
        self.freq = int(json["freq"])
        self.sysNum = int(json["sysNum"])
        self.shortName = json["shortName"]
        self.talkgroup = int(json["talkgroup"])
        self.talkgrouptag = json["talkgrouptag"]
        self.elasped = int(json["elasped"])
        self.length = int(float(json["length"]))
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

def get_or_create_Source(sourcex:source):
    if Source.objects.filter(source = sourcex.source,
                position = sourcex.position,
                time = sourcex.time,
                signal_system = sourcex.signal_system,
                emergency = sourcex.emergency):
        return Source.objects.get(source = sourcex.source,
                position = sourcex.position,
                time = sourcex.time,
                signal_system = sourcex.signal_system,
                emergency = sourcex.emergency)
    else:
        sourceX = Source(
                source = sourcex.source,
                position = sourcex.position,
                time = sourcex.time,
                signal_system = sourcex.signal_system,
                emergency = sourcex.emergency            
            )
        sourceX.save()
        return sourceX

def get_or_create_Freq(freqx:freq):
    if Freq.objects.filter(freq = freqx.freq,
                spikes = freqx.spikes,
                time = freqx.time,
                errors = freqx.errors,
                position = freqx.position,
                length = freqx.length):
        return Freq.objects.get(freq = freqx.freq,
                spikes = freqx.spikes,
                time = freqx.time,
                errors = freqx.errors,
                position = freqx.position,
                length = freqx.length)
    else:
        FreqX = Freq(freq = freqx.freq,
                spikes = freqx.spikes,
                time = freqx.time,
                errors = freqx.errors,
                position = freqx.position,
                length = freqx.length)
        FreqX.save()
        return FreqX

def createCall(Callx:call):
    callObject = Call(
        call_id = Callx.id,
        freq = Callx.freq,
        sysNum = Callx.sysNum,
        shortName = Callx.shortName,
        talkgroup = Callx.talkgroup,
        talkgrouptag = Callx.talkgrouptag,
        elasped = Callx.elasped,
        length = Callx.length,
        state = Callx.state,
        recNum = Callx.recNum,
        srcNum = Callx.srcNum,
        recState = Callx.recState,
        sigmffilename = Callx.sigmffilename,
        debugfilename = Callx.debugfilename,
        filename = Callx.filename,
        statusfilename = Callx.statusfilename,
        startTime = Callx.startTime,
        stopTime = Callx.stopTime,
        phase2 = Callx.phase2,
        conventional = Callx.conventional,
        encrypted = Callx.encrypted,
        emergency = Callx.emergency,
        analog = Callx.analog
    )
    callObject.save()

    for sourcex in Callx.sourceList:
        sourcex:source
        callObject.sourceList.add(
            get_or_create_Source(sourcex)
        )
    callObject.save()

    for freqx in Callx.freqList:
        freqx:freq
        callObject.freqList.add(
            get_or_create_Freq(freqx)
        )
    callObject.save()
    return callObject

def endCall(Callx:call):
    callObject:Call = Call.objects.get(call_id=Callx.id)
    callObject.stopTime = Callx.stopTime

    callObject.sourceList.clear()
    callObject.freqList.clear()

    for sourcex in Callx.sourceList:
        sourcex:source
        callObject.sourceList.add(
           get_or_create_Source(sourcex)
        )
    callObject.save()

    for freqx in Callx.freqList:
        freqx:freq
        callObject.freqList.add(
            get_or_create_Freq(freqx)
        )
    callObject.save()
    return callObject

def GetSystemStatus(system:System):
    if SystemStatus.objects.filter(system=system):
        return SystemStatus.objects.get(system=system)
    else:
        systemX = SystemStatus(system=system)
        systemX.save()
        return systemX

def handleMessage(message, type, uuid):
    system = System.objects.get(recorder_uuid=uuid)
    SystemObject = GetSystemStatus(system)

    if type == "call_start":
        callX = call(message["call"])
        SystemObject.activeCalls.add(createCall(callX))
    elif type == "call_end":
        callX = call(message["call"])
        SystemObject.activeCalls.remove(endCall(callX))
    elif type == "calls_active":
        callIDs = []
        for callX in message["calls"]:
            callIDs.append(callX["id"])
        for active in SystemObject.activeCalls.all():
            if not active.call_id in callIDs:
                SystemObject.activeCalls.remove(active)            
    elif type == "rates":
        if len(message["rates"]) == 1:            
            SystemObject.decoderate = int(float(message["rates"][0]["decoderate"]))
            
        else:
            for rate in message["rates"]:
                try:
                    system = System.objects.get(system_id=rate["id"])
                    SystemObject = GetSystemStatus(system)
                    SystemObject.decoderate = int(float(rate["decoderate"]))
                except: pass
    SystemObject.save()