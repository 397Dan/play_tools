#!usr/bin/python
#coding=utf-8

import json
import os
import re
import time

pyPath = os.path.dirname(os.path.realpath(__file__))
# wsPath = os.path.dirname(pyPath)
# csPath = os.path.dirname(wsPath)
from paly_tools.ximalaya.tools.XimaTools import XimaTools

payRankUrl = 'https://www.ximalaya.com/revision/rank/v1/album/getRankAlbum?rankIds=62&pageNum=1&pageSize=100'

translateDictFile = ''.join([pyPath,'/translateDict.json'])

class XimaMain(XimaTools):
	def __init__(self):
		self.translateDict = self.readFile(translateDictFile)

	def getRankInfo(self,url):
		resultList = []
		translateDict = json.loads(self.translateDict)
		pageDict = self.getPageDict(url)
		if pageDict.has_key('data') and pageDict['data'].has_key('albumRankPageList'):
			dataList = pageDict['data']['albumRankPageList']
			print time.time(),'strat loop'
			for d in dataList:
				if d.has_key('albums'):
					for c,a in enumerate(d['albums']):
						dataInfo = {}
						dataInfo['_id'] = a['id'] if a.has_key('id') else '' #作品的id
						dataInfo['title'] = a['albumTitle'] if a.has_key('albumTitle') else '' #作品名称
						dataInfo['anchorName'] = a['anchorName'] if a.has_key('anchorName') else '' #作品作者名
						dataInfo['urlId'] = str(a['albumUrl']).lstrip('/') if a.has_key('albumUrl') else '' #作品url
						if dataInfo['urlId'] != '':
							pageUrl = 'https://www.ximalaya.com/%s' % dataInfo['urlId']
							urlTag = dataInfo['urlId'].split('/')[0]   # 链接上回分大类  例如 陈果的幸福哲学课->人文
							if translateDict.has_key(urlTag):
								urlTag = translateDict[urlTag]
							else:
								# translateDict 里没有tag时 进到专辑页面内用正则获取tag  并存入全局变量translateDict中
								urlTag = self.getTag(pageUrl,urlTag,translateDict)
						else:
							pageUrl = ''
							urlTag = ''
						dataInfo['PageUrl'] = pageUrl
						dataInfo['urlTag'] = urlTag
						dataInfo['anchorUrl'] = 'https://www.ximalaya.com/%s'%str(a['anchorUrl']).lstrip('/') if a.has_key('anchorUrl') else '' #作者主页链接
						dataInfo['playCount'] = a['playCount'] if a.has_key('anchorName') else 0 #作品作者名
						dataInfo['trackCount'] = a['trackCount'] if a.has_key('trackCount') else 0 #专辑集数
						dataInfo['description'] = a['description'] if a.has_key('description') else '' #专辑描述
						dataInfo['isPaid'] = a['isPaid'] if a.has_key('isPaid') else 0 #是否付费
						dataInfo['price'] = a['price'] if a.has_key('price') else 0 #售价
						dataInfo['index'] = c+1
						resultList.append(dataInfo)
			print time.time(),'end loop'
		return resultList

	def getTag(self,url,sTag,translateDict):
		tag = ''
		content = self.getPageContent(url)
		pTag = re.compile(r'class="cate NQi" title="(.+?)"')
		mTag = pTag.search(content)
		if mTag:
			tag = str(mTag.group(1))
			translateDict[sTag] = tag
			self.writeFile(translateDictFile,json.dumps(translateDict))
		return tag

	def getFileName(self,name,date=''):
		if date == '':
			date = self.getTodayTimeStr() # 2019-01-19
		fileName = ''.join([pyPath,name,'_',date,'.json'])
		return fileName

	def Main(self):
		payRankList = json.dumps(self.getRankInfo(payRankUrl))
		fileName = self.getFileName('/dataDir/payRnak')
		self.writeFile(fileName,payRankList)

if __name__ == '__main__':
	XimaMain().Main()