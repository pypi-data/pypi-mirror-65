#!/usr/bin/env python

import json
from vmwvro2.parameters import WorkflowParameter


import unittest


with open('./sample-json/exeDetail2.json', 'r') as myfile:
    data=myfile.read()
jData = json.loads(data)

with open('./sample-json/exeDetail3.json', 'r') as myfile:
    data=myfile.read()
jData3 = json.loads(data)



class Test_Parameters(unittest.TestCase):


    #####################
    def test_json_string(self):

        #print jData['output-parameters'][0]

        p1 = WorkflowParameter()
        p1.from_json(jData['output-parameters'][0])
        tmp = str(p1)
        tmp = p1.to_json()
        self.assertIsNotNone(tmp)
        self.assertEqual( "o1", p1.name)
        self.assertEqual( "abcd abcd", p1.value)


    #####################
    def test_json_number(self):

        p1 = WorkflowParameter()
        p1.from_json(jData['output-parameters'][1])
        tmp = str(p1)
        tmp = p1.to_json()
        self.assertIsNotNone(tmp)
        self.assertEqual( "o2", p1.name)
        self.assertEqual( 51234, p1.value)


    #####################
    def test_json_null_number(self):

        p1 = WorkflowParameter()
        p1.from_json(jData['input-parameters'][2])
        tmp = str(p1)
        tmp = p1.to_json()
        self.assertIsNotNone(tmp)
        self.assertEqual( "n1", p1.name)
        self.assertIsNone(p1.value)
        
    #####################
    def test_json_array(self):

        p1 = WorkflowParameter()
        p1.from_json(jData['output-parameters'][2])
        tmp = str(p1)
        tmp = p1.to_json()
        self.assertIsNotNone(tmp)

    #####################
    def test_json_boolean(self):

        p1 = WorkflowParameter()
        p1.from_json(jData3['output-parameters'][0])
        tmp = str(p1)
        tmp = p1.to_json()
        self.assertIsNotNone(tmp)
        self.assertEqual( "statusCode", p1.name)
        self.assertEqual( "boolean", p1.type)
        self.assertEqual( True, p1.value)





    #####################
    def test_string_array(self):

        v = [ "aa", "bb", "cc", "dd" ]
        p1 = WorkflowParameter(name = "mio", _type = "Array/string", value = v )
        tmp = str(p1)
        tmp = p1.to_json()
        self.assertIsNotNone(tmp)




if __name__ == '__main__':
    unittest.main()
