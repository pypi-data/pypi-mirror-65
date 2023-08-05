#!/usr/bin/env python
import unittest
from parameterized import parameterized


from vmwvro2.workflow import Workflow, MultiRun
from vmwvro2.sessions import SessionList


sl = SessionList()
sl.load()
vro = sl.getAlias("dev")
 
class UpdateAnIPManualy(unittest.TestCase):

    mt = MultiRun()

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

        cls.mt.add(wf,sl,"dev")
        cls.mt.run("./sample-json/exeDetail2.json")
        cls.mt.wait()
        cls.mt.getLogs("./sample-json/exeDetail4.json")
        
        for alias in cls.mt.list:
            cls.mt.list[alias].print_workflow()




    @parameterized.expand(vro)
    def test_state(self,alias): 
        
        state = self.mt.state(alias)
        if not state:
            raise unittest.SkipTest("Not performed")
        
        self.assertEqual(state, "completed")


    @parameterized.expand(vro)
    def test_out(self,alias): 

        if not self.mt.state(alias):
            raise unittest.SkipTest("Not performed")
        
        self.assertEqual(self.mt.out(alias, "o1"), "abcd abcd")
        self.assertEqual(self.mt.out(alias, "o2"), 51234)


    @parameterized.expand(vro)
    def test_logs(self,alias):

        if not self.mt.state(alias):
            raise unittest.SkipTest("Not performed")

        log = self.mt.log(alias)
        if not log:
            raise unittest.SkipTest("Log was not found")


        self.assertRegex(log, "Duplicated", "Duplicated IP was not detected")
        self.assertRegex(log, "Cramer, Update OK", "Cramer update not OK ")

        self.assertNotRegex(log, "-InternalError:",  "Generic Internal error")
        self.assertNotRegex(log, "-Cannot send mail", "Mail error")
        
        
            
if __name__ == '__main__':
    #unittest.main(testRunner=HTMLTestRunner(output='example_dir'))
    unittest.main()

