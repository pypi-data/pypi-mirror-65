#!/usr/bin/env python

import time
import json
from vmwvro2.workflow import Workflow, WorkflowRun, MultiRun
from vmwvro2.parameters import WorkflowParameter
from vmwvro2.sessions import Session, SessionList
from vmwvro2.utils import format_url, safeget


sl = SessionList()
sl.load()




##########################################################
wf = Workflow()
wf.id = "92bffd10-ea48-43e7-8970-b5dd6e577f5f"
wf.name = "test"
wf.param(name="s1", value="my value")

mt = MultiRun()
mt.add(wf,sl,"dev")
mt.run()
mt.wait()


##########################################################
wf = Workflow()
wf.id = "2294b1f0-46de-47dc-b740-f17d5d857502"
wf.name = "cramer Get info for an IP"

wf.param(name="ipAddress",value="10.10.10.10")
wf.param(name="ipSubnetName",value="*")
wf.param(name="ipRangeName",value="*")
wf.param(name="spaceName",value="*")


mt = MultiRun()
mt.add(wf,sl,"dev")
mt.add(wf,sl,"prod1-de")
mt.run()
mt.wait()


##########################################################
wf = Workflow()
wf.id = "e6458f98-e092-4f18-98b6-abb2d79d362a"
wf.name = "Cramer, Does IPSubnet Exist?"

wf.param(name="ipSubnetName",value="*")
wf.param(name="ipRangeName",value="10.105.0.0/16")
wf.param(name="spaceName",value="*")


mt = MultiRun()
mt.add(wf,sl)
mt.run()
mt.wait()
