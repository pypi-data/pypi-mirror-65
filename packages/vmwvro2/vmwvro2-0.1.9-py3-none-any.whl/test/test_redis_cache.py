#!/usr/bin/env python
import unittest
import logging

from vmwvro2.workflow import Workflow,WorkflowRun
from vmwvro2.sessions import SessionList
import json

logging.basicConfig(level=logging.DEBUG)


sl = SessionList()
s = sl.getSession()



class RedisCache(unittest.TestCase):

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

    def test_calculate_hash(self):
        hash = self.wfr.calculate_hash()
        print(hash)

    def test_cache_check(self):
        self.wfr.cache_check()

    def test_cache_write(self):

        path = "./sample-json/exeDetail2.json"
        with open(path, 'r') as myfile:
            data=myfile.read()
        jData = json.loads(data)

        self.wfr.calculate_hash()
        self.wfr.cache_write(jData)


    def test_run(self): 
        state = self.wfr.state        
        self.assertEqual(state, "completed")




        
            
if __name__ == '__main__':
    unittest.main()

