#!/usr/bin/env python
import unittest
import logging

from vmwvro2.workflow import Workflow,WorkflowRun
from vmwvro2.sessions import SessionList


logging.basicConfig(level=logging.DEBUG)


sl = SessionList()
s = sl.getSession()
print(s.alias)

class GetLogs_noRunId(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        WF: "Cramer, update an IP Manualy"
        """
        
        wf = Workflow()
        wf.id = "338beefa-9f7f-469b-89d4-914031ffbfb6"
        wf.name = "Cramer, update an IP Manualy"

        wf.param(name="ipAddress", value="10.10.10.10")
        wf.param(name="newStatus", value="In Service")
        wf.param(name="description", value="TestingCramer")
        wf.param(name="mailAddressList", value="")

        cls.wfr = WorkflowRun(wf,s)
        cls.wfr.from_file("./sample-json/exeDetail2.json")
        cls.wfr.run()
        cls.wfr.wait()
        cls.wfr.id = None
        cls.wfr.getLogs("./sample-json/exeDetail4.json")
        cls.wfr.print_workflow()



    def test_run(self): 
        state = self.wfr.state        
        self.assertEqual(state, "completed")

    def test_log(self):
        log = self.wfr.log

        self.assertIsNone(log, "No detected RunId is null")



class Exe(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        WF: "Cramer, update an IP Manualy"
        """
        
        wf = Workflow()
        wf.id = "338beefa-9f7f-469b-89d4-914031ffbfb6"
        wf.name = "Cramer, update an IP Manualy"

        wf.param(name="ipAddress", value="10.10.10.10")
        wf.param(name="newStatus", value="In Service")
        wf.param(name="description", value="TestingCramer")
        wf.param(name="mailAddressList", value="")

        cls.wfr = WorkflowRun(wf,s)
        cls.wfr.from_file("./sample-json/exeDetail2.json")
        cls.wfr.exe()


    def test_run(self): 
        state = self.wfr.state        
        self.assertEqual(state, "completed")

    def test_out(self): 
        out = self.wfr.out
        self.assertEqual(out("o1"), "abcd abcd")
        self.assertEqual(out("o2"), 51234)



class search_wfid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        WF: "Cramer, update an IP Manualy"
        """

        cls.wf = Workflow(name = "getPrice")
        cls.wf.param(name="ipAddress", value="10.10.10.10")
        cls.wf.param(name="newStatus", value="In Service")


    def test_wfid(self): 
        id = self.wf.id       
        self.assertEqual(id, "a8ec5e2e-dba7-4825-9d97-6a32701dffed")



        
            
if __name__ == '__main__':
    unittest.main()

