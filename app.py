# -*- coding: utf-8 -*-

'wang xue liang'

import logging; logging.basicConfig(level=logging.INFO)

import copy
from urllib.request import urlopen
from bs4 import BeautifulSoup
import asyncio,os,json,time
from datetime import datetime
from urllib.parse import parse_qs 
from aiohttp import web

def get(path):
	'''
	define decorator @get('/path')
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__ = 'GET'
		wrapper.__rout__ = path
		return wrapper
	return decorator	
	
def reqJin10(request):
	query_params = parse_qs(request.query_string)
	if query_params:
		if query_params['date']:
			logging.info('request jin10 data of : %s' % query_params['date'][0])
			jin10data = 'http://rili.jin10.com/' + query_params['date'][0]
			html = urlopen(jin10data)
			soup = BeautifulSoup(html,'lxml')
			dataTable = soup.find('table')
			tb_ths = soup.thead.tr.contents
			print('----------过滤前----------')
			print(len(tb_ths))
			#print(tb_ths)
			delIndexs = []
			#用下面的循环删除替换该算法
			for t in range(len(tb_ths)):
				if tb_ths[t] == '\n':
					delIndexs.append(int(t)) #记录要删除的位置
					#tb_ths.pop(int(t))
			for dt in tb_ths:
				if dt == '\n':
					tb_ths.remove(dt)
			print('----------过滤后----------')
			#print(tb_ths)
			#print(delIndexs)
			rst = BeautifulSoup('<html><head><meta charset="UTF-8"></head><body><table><thead><tr></tr></thead></table></body></html>','lxml')
			n = 0 
			#过滤表格头
			while n < len(tb_ths)-4:
				#下面的语句不能使用rst.tr.append(tb_ths[n]),tb_ths中的元素执行了pop操作，所以要先复制Tag，然后append
				temp = copy.copy(tb_ths[n])
				if n != 2:
					temp['width'] = '20%'
				rst.tr.append(temp)
				n = n + 1
			#过滤表格头
			tbd = rst.new_tag('tbody')
			rst.table.append(tbd)
			#print(rst.prettify())
			tb_tr = soup.tbody.contents
			for tt in tb_tr:
				if tt == '\n':
					tb_tr.remove(tt)
			tr_index = 0
			while tr_index < len(tb_tr):
				m = 0
				tr = rst.new_tag('tr')
				tds = tb_tr[tr_index].contents
				for dd in tds:re
					if dd == '\n':
						tds.remove(dd)
				while m < len(tds)-4:
					#print('tb_tr[%s]:%s' % (tr_index,tb_tr[tr_index].contents))
					tr.append(copy.copy(tds[m]))
					m = m + 1
				tr_index = tr_index + 1
				rst.tbody.append(tr)

			
			logging.info('用户查询了财经日历：%s' % query_params['date'])
			#print(rst.prettify())
			return web.Response(body=b'%s' % rst.encode('gbk'))
	
@asyncio.coroutine
def init(loop):
	app = web.Application(loop=loop)
	app.router.add_route('GET','/caijing',reqJin10)
	srv = yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
	logging.info('server started at http://127.0.0.1:9000...')
	return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()