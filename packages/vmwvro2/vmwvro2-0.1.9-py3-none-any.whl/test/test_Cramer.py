#!/usr/bin/env python
import unittest

from vmwvro2.workflow import Workflow,WorkflowRun
from vmwvro2.sessions import SessionList

    
sl = SessionList()
s = sl.getSession()
print(s.alias)

class UpdateAnIPManualy(unittest.TestCase):

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
        cls.wfr.getLogs("./sample-json/exeDetail4.json")
        cls.wfr.print_workflow()



    def test_run(self): 
        state = self.wfr.state        
        self.assertEqual(state, "completed")


    def test_out(self): 
        out = self.wfr.out
        self.assertEqual(out("o1"), "abcd abcd")
        self.assertEqual(out("o2"), 51234)


    def test_log(self):
        log = self.wfr.log

        self.assertRegex(log, "Duplicated", "Duplicated IP was not detected")
        self.assertRegex(log, "Cramer, Update OK", "Cramer update not OK ")


    def test_SendMail(self):
        log = self.wfr.log

        self.assertNotRegex(log, "-InternalError:",  "Generic Internal error")
        self.assertNotRegex(log, "-Cannot send mail", "Mail error")

    def test_Other(self):
        raise unittest.SkipTest("Not performed")
        

        
        
            
if __name__ == '__main__':
    unittest.main()

