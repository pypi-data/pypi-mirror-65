#!/usr/bin/env python

#import time
#import json
#from vmwvro2.workflow import Workflow, WorkflowRun, MultiRun
#from vmwvro2.parameters import WorkflowParameter
#from vmwvro2.sessions import Session, SessionList
#from vmwvro2.utils import format_url,safeget
#import vmwvro2
from vmwvro2.workflow import Workflow, MultiRun
from vmwvro2.sessions import SessionList


sl = SessionList()
sl.load()


##########################################################
wf = Workflow()
wf.id = "e6458f98-e092-4f18-98b6-abb2d79d362a"
wf.name = "Cramer, Does IPSubnet Exist?"

wf.param(name="ipSubnetName",value="*")
wf.param(name="ipRangeName",value="10.105.0.0/16")
wf.param(name="spaceName",value="*")


mt = MultiRun()
mt.add(wf,sl)
#mt.run("./sample-json/exeDetail2.json")
mt.run()
mt.wait()

for alias in mt.list:
    print(mt.list[alias])
    #print(mt.list[alias].print_paramenters())
    
