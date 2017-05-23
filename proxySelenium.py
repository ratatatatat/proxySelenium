########### Additional Imports ############
import csv
import random
import time
import urllib2
import sys
import os
import datetime
from bs4 import BeautifulSoup
import json

########### Importing Selenium ############
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumProxy(object):

	def __init__(self):
		self.logFile = './SeleniumProxyLog.txt'
		self.setActiveProxy()
		print self.proxyObj
		self.testDriver()

	def setActiveProxy(self):
		proxyObj = self.getActiveProxies()
		if(proxyObj != None):
			self.proxyObj = proxyObj
			return
		else:
			self.writeLogMsg("Could Not Set A Proxy")
			return

	def testDriver(self):
		# addrArg = '--proxy='+self.proxyObj['ip']+':' + self.proxyObj['port']
		# print addrArg
		# typeArg = '--proxy-type=' + self.proxyObj['type'].lower()
		# print typeArg
		addrArg = '--proxy='+'70.35.197.74'+':' + '80'
		typeArg = '--proxy-type=' + 'https'
		service_args = [
			addrArg,
			typeArg,
	    ]
		print service_args
		driver = webdriver.PhantomJS(service_args=service_args)
		driver.get("http://icanhazip.com/")
		print driver.page_source
		driver.close()

	def getActiveProxies(self):
		## For Now Grab from One Source:
		## IMPLEMENT ADDTIONAL SOURCES HERE
		apiEndpoint = 'http://proxy.tekbreak.com/best/json'
		response = self.getRequest(apiEndpoint)
		if( response['status'] == 'success' ):
			proxyJson = json.loads(response['payload'])[0]
			return proxyJson
		else:
			self.writeLogMsg("Could not get a Proxy")
			return None


	def getRequest(self,url):
		returnObj = {}
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			req = urllib2.Request(url, None, headers)
			htmlText = urllib2.urlopen(req,timeout=10).read()
			self.writeLogMsg("Successfully Got Response from: " + url)
			returnObj['status'] = 'success'
			returnObj['payload'] = htmlText
			return returnObj
		except:
			e = sys.exc_info()[0]
			self.writeLogMsg("Error could not get Response from: " + url + '\n' + str(e))
			returnObj['status'] = 'failure'
			returnObj['payload'] = None
			return returnObj

	def getTimeStamp(self):
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	def writeLogMsg(self,msg):
		fileTarget = open(self.logFile,'a')
		msg = msg + ' ' + self.getTimeStamp() + '\n'
		fileTarget.write(msg)
		fileTarget.close()
		return



def main():
	selProxy = SeleniumProxy()

if __name__ == '__main__':
	main()