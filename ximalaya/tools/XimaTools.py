#!usr/bin/python
#coding=utf-8

import urllib2
import json
import os
import datetime
import time

pyPath = os.path.dirname(os.path.realpath(__file__ ))
wsPath = os.path.dirname(pyPath)

header = {
	'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
	# 'Accept':'*/*' ,
	# 'Accept-Language':'zh,en-US;q=0.7,en;q=0.3',
	# 'Referer':'https://www.ximalaya.com/top/premium/' ,
	# 'content-type':'application/x-www-form-urlencoded;charset=UTF-8' ,
	# 'origin':'https://www.ximalaya.com' ,
	# 'Cookie':'_xmLog=xm_1529911840494_jity0b8uwjj218; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1547804000,1547804189,1547809435,1547810814; _ga=GA1.2.678741676.1529911841; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; device_id=xm_1547803999270_jr1ujdbautcf00; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1547810835' ,
	# 'Connection':'keep-alive'
}

class XimaTools(object):

	def getPageContent(self,url):
		Request = urllib2.Request(url,headers=header)
		response = urllib2.urlopen(Request)
		content = response.read()
		return content

	def getPageDict(self,url):
		try:
			pageDict = json.loads(self.getPageContent(url))
		except:
			pageDict = {}
		return pageDict

	def readFile(self,filePath):
		with open(filePath,'r') as f:
			return f.read()

	def isExistsFile(self,fileName):
		print fileName
		if os.path.exists(fileName):
			pass
		else:
			os.mknod(fileName)

	def writeFile(self,filePath,content):
		self.isExistsFile(filePath)
		with open(filePath,'w') as f:
			f.write(content)

	def getTodayTimeStr(self):
		return datetime.date.fromtimestamp(time.time()).strftime("%Y-%m-%d")

	def getFileName(self,name,date='',suf='.json'):
		if date == '':
			date = self.getTodayTimeStr() # eg:2019-01-19
		fileName = ''.join([wsPath,name,'_',date,suf])
		return fileName
