#!/usr/bin/env python
import unittest

from vmwvro2.workflow import Workflow,WorkflowRun
from vmwvro2.sessions import SessionList

    
sl = SessionList()
s = sl.getSession()
print(s.alias)

class getPriceList(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        WF: "Price, get price list"
        """
        
        wf = Workflow()
        wf.id = "a8ec5e2e-dba7-4825-9d97-6a32701dffed"
        wf.name = "getPrice"

        wf.param(name="operatingsystem", value="RHEL")
        wf.param(name="tshirtSize", value="")
        wf.param(name="extraDiskSize", value=20, _type="number")
        wf.param(name="independentDiskSize", value=1, _type="number")

        cls.wfr = WorkflowRun(wf,s)
        cls.wfr.from_file("./sample-json/exeOutPropertiesArray.json")
        cls.wfr.run()
        cls.wfr.wait()
        cls.wfr.print_workflow()



    def test_run(self): 
        state = self.wfr.state        
        self.assertEqual(state, "completed")


    def test_out(self): 
        out = self.wfr.out
        #self.assertEqual(out("o1"), "abcd abcd")
        #self.assertEqual(out("o2"), 51234)



        
        
            
if __name__ == '__main__':
    unittest.main()

