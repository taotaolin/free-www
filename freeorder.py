#coding=utf8
import requests,re
import time
import datetime

username = '用户名'
password = '密码' 
order_url = 'https://my.free-www.ru/billmgr?out=xml&func=vds.order'
ID = 319

def Login():
	url = 'https://my.free-www.ru/'
	playlod = {
			'username':username,
			'password':password,
			'lang':'ru',
			'forget':'on',
			'func':'auth',
		}
	r = s.post(url,data = playlod,verify=False)
	r = s.get('https://my.free-www.ru/billmgr?out=xml&func=vds.order',verify=False)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	html = r.text
	state = re.findall(r'</error>',html)
	if '</error>' in state:
		print('Fail Login')
	else:
		print("Cookie Get!")
'''
def Find(url = order_url):
	r = s.get('https://my.free-www.ru/billmgr?out=xml&func=vds.order',verify=False)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	html = r.text
	ID = re.findall(r'<pricelist>(\d+)</pricelist>',html)
	desc = re.findall(r'<desc>(.+?)</desc>',html)
	if 'kvm0' in desc:
		return ID[desc.index('kvm0')]
	else:
		pass
'''

def Find(url = order_url):
	r = s.get('https://my.free-www.ru/billmgr?out=xml&func=vds.order',verify=False)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	html = r.text
	ID = re.findall(r'<pricelist>319</pricelist>',html)
	if ID:
		print("毛子哥上架啦")
		return 1
	else:
		print("已售完")
		return 0

def addCar():
	url = 'https://my.free-www.ru/billmgr'
	t = time.time()
	playlod = {
				'func':'vds.order.pricelist',
				'elid':'',
				'datacenter':'1',
				'snext':'ok',
				'skipbasket':'',
				'newbasket':'',
				'stylesheet':'',
				'itemtype':'3',
				'period':'1',
				'pricelist':ID,
				'clicked_button':'order',
				'progressid':'false',
				'sok':'ok',
				'sfrom':'ajax',
				'operafake':int(round(t * 1000)),
		}

	playlod2 = {
				'func':'vds.order.param',
				'elid':'',
				'autoprolong':'1',
				'datacenter':'1',
				'itemtype':'3',
				'newbasket':'',
				'period':'1',
				'pricelist':ID,
				'skipbasket':'',
				'stylesheet':'',
				'domain':'',
				'ostempl':'ISPsystem__Debian-7-amd64',
				'clicked_button':'finish',
				'progressid':'false',
				'sok':'ok',
				'sfrom':'ajax',
				'operafake':int(round(t * 1000)),
		}
	r = s.post(url,data = playlod,verify=False)
	time.sleep(1)
	r = s.post(url,data = playlod2,verify=False)
	print(r.text)

if __name__ == '__main__':
	with requests.Session() as s:
		s.headers = {
			'DNT':'1',
			'Host':'my.free-www.ru',
			'ISP-Client':'Web-interface',
			'Origin':'https://my.free-www.ru',
			'Referer':'https://my.free-www.ru/billmgr',
			'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
			'X-Requested-With':'XMLHttpRequest',
		}
		Login()
		while True:
			if Find():
				addCar()
			time.sleep(5)
