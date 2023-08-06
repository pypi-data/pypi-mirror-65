#!/usr/bin/env python

import json
import unittest
from vmwvro2.sessions import Session, SessionList




class Test_Session(unittest.TestCase):


    #####################
    def test_basic_sesion(self):

        login = 'login'
        password = 'password'
        proxies = dict(https='socks5://127.0.0.1:8888')


        s1 =    Session(url="host", 
                        username=login, 
                        password=password,
                        proxies=proxies,
                        alias="dev-de",
                        tags=['dev', 'rat'])

        self.assertIsNotNone(s1)
        self.assertEqual(s1.username, "login")
        self.assertIsNotNone(s1.basic_auth)
        self.assertEqual(s1.url, "https://host:8281")
        self.assertTrue('dev' in s1.tags)


    #####################
    def test_sesion_list(self):
        sl = SessionList()
        sl.load()
        self.assertIsNotNone(sl)

        s1 =sl.list['dev-it']
        self.assertIsNotNone(s1)
        self.assertRegex(s1.url, r'^https://ciit.*:8281$')
        self.assertRegex(s1.username, r'^vf.*@.*com$')


class Alias(unittest.TestCase):


    def test_getById(self):
        sl = SessionList()
        sl.load()
    
        s1 =sl.getSession('dev-de')
        self.assertIsNotNone(s1)

        s2 =sl.getSession('dev-es')
        self.assertIsNone(s2)
        
        
    def test_getByAlias(self):
        sl = SessionList()
        sl.load()

        s1 =sl.getSession('ciitdevvro11')
        self.assertIsNotNone(s1)
        self.assertRegex(s1.url, r'^https://ciit.*:8281$')

        s2 =sl.getSession('ciesdevvro11')
        self.assertIsNone(s2)

        
        
if __name__ == '__main__':
    unittest.main()
