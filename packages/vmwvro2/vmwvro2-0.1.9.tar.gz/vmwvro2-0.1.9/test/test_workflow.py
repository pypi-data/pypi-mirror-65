#!/usr/bin/env python


import time
import re
import json
import unittest

from vmwvro2.workflow import Workflow, WorkflowRun, MultiRun
from vmwvro2.parameters import WorkflowParameter
from vmwvro2.sessions import Session, SessionList
from vmwvro2.utils import format_url,safeget




class Test_Workflow(unittest.TestCase):


    #####################
    def test_workflow_multiRun(self):

        sl = SessionList()
        sl.load()

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
        #mt.getLogs("./sample-json/exeDetail3.json")

        for alias in mt.list:
            wfRun = mt.list[alias]
            #wfRun.print_parameters()
            #print mt.list[alias].output_parameters['o1']

            self.assertEqual( wfRun.state , "completed")
            self.assertEqual( wfRun.output_parameters['o1'].value , "abcd abcd")
            self.assertEqual( wfRun.output_parameters['o2'].value , 51234 )

if __name__ == '__main__':
    unittest.main()
