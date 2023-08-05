#!/usr/bin/env python
import unittest
import json

#from vmwvro2.workflow import Workflow,WorkflowRun
#from vmwvro2.sessions import SessionList
from vmwvro2.parameters import parse_value
from vmwvro2.utils import safeget

#sl = SessionList()
#s = sl.getSession()
#print(s.alias)

class ParseValue(unittest.TestCase):


    def test_parse_value_01(self):

        path = "./sample-json/exeOutPropertiesArray.json"

        with open(path, 'r') as myfile:
            data=myfile.read()
        jData = json.loads(data)

        o1 = safeget(jData, "output-parameters")[0]
        #print(o1) 

        result = parse_value(o1.get('value'))
        #print(result)


        self.assertEqual( 1.0, result[0]['qty'])
        self.assertEqual( '00001', result[0]['id'])

        self.assertEqual( 20.0 , result[1]['qty'])




    def test_parse_value_02(self):

        path = "./sample-json/exeOutPropertiesArray.json"
        with open(path, 'r') as myfile:
            data=myfile.read()
        jData = json.loads(data)


        i1 = safeget(jData, "input-parameters")[0]
        #print("\n-i1")
        #print(i1) 
        result = parse_value(i1.get('value'))
        #print(result)
        self.assertEqual( "RHEL", result)


        i2 = safeget(jData, "input-parameters")[3]
        #print("\n-i2")
        #print(i2) 
        result = parse_value(i2.get('value'))
        #print(result)
        self.assertEqual( 20, result)



    def test_parse_value_03(self):

        path = "./sample-json/exeDetail2.json"
        with open(path, 'r') as myfile:
            data=myfile.read()
        jData = json.loads(data)

        o1 = safeget(jData, "output-parameters")[2]
        #print("\n-o2")
        #print(o1) 

        result = parse_value(o1.get('value'))
        #print(result)
        self.assertEqual( "string1", result[0])
        self.assertEqual( "string2", result[1])



        
            
if __name__ == '__main__':
    unittest.main()

