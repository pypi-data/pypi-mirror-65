# Project description
A REST API library to execute 'Worflows' on VMware vRealize Orchestrator (vRO).


# Features
What you can do with vmwvro:

* Support for a list of vRO endpoints
* Concurrent executions
* Support of input and output paramenters
* Supported socks proxy 
* Download of Workflow log

# Basic usage
```python
#!/usr/bin/env python
from vmwvro2.workflow import Workflow, MultiRun
from vmwvro2.sessions import SessionList


sl = SessionList()
sl.load()



##########################################################
wf = Workflow()
wf.id = "338beefa-9fff-469b-89d4-914031ffbfb6"
wf.name = "IP update"

wf.param(name="ipAddress",value="10.10.10.10")
wf.param(name="newStatus",value="In Service")


mt = MultiRun()
mt.add(wf,sl,"dev")
mt.run()
mt.wait()
mt.getLogs()

for alias in mt.list:
    print("****************")
    print(alias)
    print(mt.list[alias].name)
    mt.list[alias].print_parameters())
    print(mt.list[alias].log)


````

# Licence
MIT

NOTE: Based and some parts copied from "vmwvro" (c) Lior P. Abitbol

