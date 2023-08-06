"""
VMware vRealize Workflow implementation and supporting objects.

Copyright (c) 2018, Jose Ibanez

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import re
import logging
import requests
import time
import json
import hashlib
import yaml
import redis


from .config import URL_RUN_WORKFLOW_BY_ID, FINISHED_STATES, WORKFLOW_GETFWLOGS_ID
from .utils import format_url, safeget
from .parameters import WorkflowParameter
from .settings import ConfigVMWvro

class WorkflowError(Exception):
    """Parameters Exception."""
    pass

class WorkflowRunError(Exception):
    """Run Exception."""
    pass




class Workflow:
    """
    Workflow object, contain:
     - an id 
     - a name
     - list of input paramenters

    You can:
     - add paramenters
     - convert to json object
    """


    def __init__(self, id=None, name=None, logger=None):
        """
        Returns a new Workflow instance.
        """
        self.id = id
        self.name = name
        self.input_parameters = dict()

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(self.__class__.__name__)

        if not id and name:
            self.search_wfid()


    def search_wfid(self, target_name=None, path=None):

        if not target_name:
            target_name = self.name

        # get list of known workflows ids
        config = ConfigVMWvro.config.get("workflowsIds") or []

        for item in config:

            name = item.get('name')
            id = item.get('id')

            if name == target_name:
                self.logger.debug("Workflow name: %s, id:%s",target_name,id)
                self.id = id
                return id

        self.logger.warning("Workflow id not found for name %s",target_name)
        return None





    def param(self, name=None, value=None, _type="string", param=None):
        if param:
            name = param.name
            p = param
        else:
            p = WorkflowParameter(name=name, value=value, _type=_type)

        self.input_parameters[name] = p


    def to_json(self):
        self.body = {"parameters": []}

        for name in self.input_parameters:
            param = self.input_parameters[name].to_json()
            self.logger.debug("WF:{}, in-param:{}".format(self.name,self.input_parameters[name]))
            self.body['parameters'].append(param)

        return self.body






class WorkflowRun:
    """
    Workflow object to contain execution object
    """

    def __init__(self, wf, session=None):
        """
        Returns a new Workflow instance.
        """
        self.id = None
        self.name = wf.name
        self.version = None
        self.workflowId = wf.id
        self.reqBody = wf.to_json()
        self.vro = session.alias
        self.startUrl = None
        self.href = None
        self.state = None
        self.exception = None
        self.input_parameters = dict()
        self.output_parameters = dict()
        self.session = session
        self.logger = wf.logger
        self.log = None
        self.hash = None


    def __str__(self):
        return self.session.alias+"/"+str(self.name)+": "+str(self.state)+" "+str(self.exception)

    def calculate_hash(self):
        """
        Calculate hash of workflow request
        """

        master = {
            "body": self.reqBody,
            "workflowId": self.workflowId,
            "vro": self.vro
        }
        master_str =  json.dumps(master, sort_keys=True)
        self.hash = str(hashlib.md5(master_str.encode("utf-8")).hexdigest())
        self.logger.debug("WF Hash: %s",self.hash)
        return self.hash



    def cache_check(self):
        """
        Check if current query is in cache
        """
        self.calculate_hash()

        redisConfig = safeget(ConfigVMWvro.config,"cache","redis")

        try:
            redisClient = redis.StrictRedis(host=redisConfig.get("host"), port=redisConfig.get("port"), db=redisConfig.get("db"))
            value = redisClient.hget(self.hash, "out")
        except Exception as e:
            self.logger.warning("Redis not ready. %s",e)
            return None

        if not value:
            self.logger.debug("Answer not found in cache, hash:%s",self.hash)
            return None
        
        self.logger.debug("Answer found in cache, hash:%s",self.hash)        

        #update wfr with cache value
        self.from_json(json.loads(value))

        return value

        


    def cache_write(self, data):
        """
        Save answer to cache
        """
        if not self.hash:
            self.logger.debug("Cache disabled for this WF")
            return None

        redisConfig = safeget(ConfigVMWvro.config,"cache","redis")

        try:
            redisClient = redis.StrictRedis(host=redisConfig.get("host"), port=redisConfig.get("port"), db=redisConfig.get("db"))
            redisClient.hset(self.hash, "out", data)
            redisClient.expire(self.hash, 300)
        except Exception as e:
            self.logger.warning("Redis not ready. %s",e)
            return None

        self.logger.debug("Write answer to cache, hash:%s",self.hash)


        return True


    def from_json(self, data):
        """
        load the object from json object or file
        """
        self.answerBody = data
        self.description = data.get("description")
        self.name = data.get("name")
        self.href = data.get("href")
        self.id = data.get("id")
        self.version = data.get("version")
        self.state = data.get("state")
        self.exception = data.get("content-exception")

        self.output_parameters = dict()
        for jParam in data.get('output-parameters') or []:
            p = WorkflowParameter()
            p.from_json(jParam)
            self.output_parameters[p.name] = p


        self.input_parameters = dict()
        for jParam in data.get('input-parameters') or []:
            p = WorkflowParameter()
            p.from_json(jParam)
            self.input_parameters[p.name] = p


    def print_workflow(self):
        print("***********")
        print("vRO: "+str(self.vro))
        print("Name: "+str(self.name))
        print("Result: "+str(self.state))
        print("Exeption: "+str(self.exception))
        self.print_parameters()
        self.logger.debug("Log:")
        #print self.log.encode('utf-8')
        self.logger.debug(self.log)

    def print_parameters(self):
        for name in self.input_parameters:
            print("IN:  " + str(self.input_parameters.get(name)))
        for name in self.output_parameters:
            print("OUT: " + str(self.output_parameters.get(name)))
            
            
    def run(self, session=None, cache=False):
        """
        Starts the Workflow on vRO server defined in Sesion parameter
        """

        self.logger.info("vRO Calling WF:{}".format(self.name))

        # Check cache
        if cache:
            self.cache_check()

        # Check if already executed or cache found
        if self.state in FINISHED_STATES:
            return 0

        # check if specific session
        if session is not None:
            self.session = session

        if self.session is None:
            self.state = "failed"
            self.exception = "No vRO session defined"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
		
        url = format_url(URL_RUN_WORKFLOW_BY_ID,
                         base_url=self.session.url,
                         id=self.workflowId)

        body = json.dumps(self.reqBody)

        try:
            r = requests.post(url,
                          auth=self.session.basic_auth,
                          verify=self.session.verify_ssl,
                          headers=headers,
                          #proxies=self.session.proxies,
                          data=body)

            status_code = r.status_code
            retText = r.text

        except requests.exceptions.RequestException as e:
            status_code = 999
            retText = e
            print(e)


        if status_code < 200 or status_code > 299:
            self.state = "failed"
            self.exception = "Wrong HTTP code received: "+str(status_code)
            self.logger.error("Exception: %s",self.exception)
            self.logger.error(retText)
            return

        if status_code != 202:
            self.logger.warning("vRO status code {}, expected 202".format(status_code))

        self.href = r.headers.get("Location")
        #print("Location: "+self.href)
        if not self.href:
            self.state = "failed"
            self.exception = "Not location/href in headers"
            self.logger.error("Exception: %s",self.exception)
            return

        return 0



    def update(self):
        """
        Update the state, logs and content of this Workflow Run.
        """

        if self.state in FINISHED_STATES:
            return

        if self.href is None:
            self.state = "failed"
            return

        headers = {"Content-Type": "application/json"}
        
        
        # Perform the REST query
        try:
            r = requests.get(self.href,
                         auth=self.session.basic_auth,
                         verify=self.session.verify_ssl,
                         #proxies=self.session.proxies,
                         headers=headers)

            status_code = r.status_code

        except requests.exceptions.RequestException as e:
            status_code = 999
            self.state = "failed"
            self.exception = e
            self.logger.error("vRO request error")
            self.logger.error(e)
            print(e)
            return

        # Save the answer to file
        m = re.search(r'^http.*/vco/api/.*executions/([\w-]+)/', self.href)
	    #print self.href
        runId = m.group(1)

        with open(os.path.join('/tmp/', runId), "w") as file1:
            #file1.write(r.text.encode('utf-8'))
            file1.write(r.text)

        if status_code < 200 or status_code > 299:
            self.state = "failed"
            self.exception = "Wrong HTTP code received: "+str(status_code)
            self.logger.error("Exception:'{}', url:'{}'".format(self.exception,self.href))
            self.logger.error(r.text)
            return

        self.cache_write(r.text)
        #print("---------------------")
        #print(r.text)
        #print("---------------------")
        #print(json.dumps(r.json()))
        self.from_json(r.json())
        return 0
        

        
    def wait(self):
        """
        Wait for execution finished
        """
        secToWait = [ 1, 1, 2, 3, 5, 8, 13, 21, 34, 34, 34, 34, 34, 34, 34, 55, 55, 55, 55, 89, 144 ]
        
        for t in secToWait:

            self.update()
            if self.state in FINISHED_STATES:
                self.logger.info("WF:'{}' execution finished, Result:{}.".format(self.name,self.state))        
                break
                
            self.logger.debug("Waiting for WF:'{}', {} sec.".format(self.name, t))
            time.sleep(t)



    def from_file(self, path):
        """
        Load answer from file, used in testing
        """

        with open(path, 'r') as myfile:
            data=myfile.read()
        jData = json.loads(data)
        self.from_json(jData)


    def out(self, name):
        """
        Safe waw of 
        Return output parameter for a workflow excution on a vRO
        """

        try:
            out = self.output_parameters.get(name).value
        except:
            out = None
        
        return out



    def getLogs(self, path=None):

        if not self.id or len(self.id)<12:
            print("RunID is wrong")
            self.log = None
            return
            
        wfLog = Workflow()
        wfLog.id = WORKFLOW_GETFWLOGS_ID
        wfLog.name = "Get log of other WF"
        wfLog.param(name="runId", value=self.id)

        self.wfrLog=WorkflowRun(wfLog,self.session)

        if path:
            self.wfrLog.from_file(path)

        self.wfrLog.run()
        self.wfrLog.wait()

        try:
            self.log = self.wfrLog.out('log')
            #print self.log
        except:
            pass

    def exe(self):
        self.run()
        self.wait()
        self.getLogs()
        self.print_workflow()



class MultiRun:
    """
    Manage a list of executions
    """

    def __init__(self):
        self.list = dict()
        self.logList  = dict()


    def add(self, wf, sessionList, filter="*"):
        """
        To create a list of WF executions with a list of sessions (vRO servers)
         - wf: Workflow 
         - sessionList: SessionList
         - filter: string

        The same workflow will executed in several vRO's hosts
        """

        for alias in sessionList.list:
            s = sessionList.list.get(alias)

            if filter not in s.tags and filter != alias and filter != "*":
                continue

            self.list[alias] = WorkflowRun(wf,s)


    def run(self, path=None, _type=None):
        """
        To start the those list of WF/vRO servers

        If a path is provied, no executions will perfomed, a file will be used as REST answer, used in testing
        """

        runList = self.list
        if _type == "Log":
            runList = self.logList


        for alias in runList:

            if path is None:
                runList[alias].run()
            else:
                print("Path: "+path)
                runList[alias].from_file(path)
            

            print("vRO: "+alias+", Started WorkFlow: "+str(runList[alias].name))




    def wait(self, _type=None):
        """
        Wait for all list finished
        """

        secToWait = [ 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 ]
        

        runList = self.list
        if _type == "Log":
            runList = self.logList


        for t in secToWait:

            nRunning = 0

            for alias in runList:
                runList[alias].update()
                if runList[alias].state not in FINISHED_STATES:
                    print("vRO: "+alias+", State:"+runList[alias].state)
                    nRunning += 1
            
            if nRunning == 0:
                break

            print("Waiting " + str(t) + " Sec.")
            time.sleep(t)


        print("Result:")
        for alias in runList:
            print("vRO:"+alias+", WF:"+str(runList[alias].name)+", Result:"+runList[alias].state)



    def getLogs(self, path=None):

        for alias in self.list:
            
            wfLog = Workflow()
            wfLog.id = WORKFLOW_GETFWLOGS_ID
            wfLog.name = "Get log of other WF"
            wfLog.param(name="runId", value=self.list[alias].id)

            self.logList[alias]=WorkflowRun(wfLog,self.list[alias].session)

        self.run(_type="Log", path=path)
        self.wait(_type="Log")

        for alias in self.list:
            #print "alias: "+alias
            #self.log[alias].print_workflow()
            try:
                log = self.logList[alias].output_parameters.get('log').value
                #print alias
                #print log
                self.list[alias].log = log
            except:
                pass


    def state(self, alias):
        """
        Safe way of
        Return execution final state for a workflow on a vRO
        """

        try:
            state = self.list[alias].state
        except:
            state = None
        
        return state



    def log(self, alias):
        """
        Safe way of
        Return log for a workflow excution on a vRO
        """

        try:
            log = self.list[alias].log
        except:
            log = None
        
        return log


    def out(self, alias, name):
        """
        Safe waw of 
        Return output parameter for a workflow excution on a vRO
        """

        try:
            out = self.list[alias].output_parameters.get(name).value
        except:
            out = None
        
        return out
