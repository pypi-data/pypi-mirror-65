#!/usr/bin/env python
from vmwvro2.workflow import Workflow, MultiRun
from vmwvro2.sessions import SessionList
import re


sl = SessionList()
sl.load()


##########################################################
wf = Workflow()
wf.id = "e6458f98-e092-4f18-98b6-abb2d79d362a"
wf.name = "Cramer, Does IPSubnet Exist?"

wf.param(name="ipSubnetName",value="*")
wf.param(name="ipRangeName",value="10.105.0.0/16")
wf.param(name="spaceName",value="*")

##########################################################
wf = Workflow()
wf.id = "338beefa-9f7f-469b-89d4-914031ffbfb6"
wf.name = "Cramer, update an IP Manualy"

wf.param(name="ipAddress",value="10.10.10.10")
wf.param(name="newStatus",value="In Service")
wf.param(name="description",value="TestingCramer")
wf.param(name="mailAddressList",value="")


mt = MultiRun()
mt.add(wf,sl,"dev")
mt.run("./sample-json/exeDetail2.json")
#mt.run()
mt.wait()
mt.getLogs("./sample-json/exeDetail4.json")
#mt.getLogs()

for alias in mt.list:
    mt.list[alias].print_workflow()

    if re.search("Duplicated", mt.list[alias].log):
        print("found in log")
