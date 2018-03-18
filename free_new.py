#coding=utf8
import requests,re,json,os
import time,subprocess
import datetime

username = '' #用户名
password = '' #密码
systems = 'linux'#linux  windows   win下若linux不能正常运行请选择windows

def Login():
	url = 'https://my.free-www.ru/'
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
	state = re.findall(r'vds.order.pricelist',html)
	if 'vds.order.pricelist' in state:
		print('Cookie Get!')
		return True
	else:
		print("Fail Login")
		return False

def getID():
	t = time.time()
	time13 = int(round(t * 1000))
	url = 'https://my.free-www.ru/billmgr?func=dashboard.items&p_num=1&dashboard=items&p_cnt=5&sfrom=ajax&operafake={0}'.format(time13)
	r = s.get(url ,verify=False)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	html = r.text
	return html

def edgaJson(dic):
	jsGet = getID()
	jsonTemp = json.loads(jsGet)
	jsonInfo = jsonTemp['content']
	for x in range(len(jsonInfo)):
		if 'example.com' in jsonInfo[x]['name']['v']:
			id_result = re.findall(r'#(\d+)',jsonInfo[x]['name']['v'])
			ip_result = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',jsonInfo[x]['name']['v'])
			dic.append([id_result,ip_result])
	#print(len(dic))
	print("共发现%s台主机"%len(dic))
	return dic

def restart(ID):
	t = time.time()
	time13 = int(round(t * 1000))
	url1 = 'https://my.free-www.ru/billmgr?func=service.reboot&elid={2}&plid=&progressid=_rebootlist{0}&sfrom=ajax&operafake={1}'.format(time13,time13,ID)
	url2 = 'https://my.free-www.ru/billmgr?elid=_rebootlist{0}&func=progress.get&sfrom=ajax&operafake={1}'.format(time13,time13)
	h = s.get(url1, verify=False)
	time.sleep(1)
	h1 = s.get(url2, verify=False)
	if '"ok" : true,"start"' in h1.text:
		print("Success reboot")
	#print(url1,url2)

def main():
	result_dic = []
	if Login():
		time.sleep(1)
		edgaJson(result_dic)
		for x in range(len(result_dic)):
			if 'linux' in systems:
				if(os.system('ping -c 5 -w 5 %s'%result_dic[x][1]) == 0):
					print("The %d Free-www is running!"%(x+1))
				else:
					print("The %d Server is not running!"%(x+1))
					restart(result_dic[x][0][0])
			elif 'windows' in systems:
				p = subprocess.Popen(["ping.exe ", result_dic[x][1]],stdin = subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)
				out = p.stdout.read()
				out_dc = out.decode('gbk')
				ping = re.findall(r'(100% 丢失)',out_dc)
				if ping:
					print("The %d Server is not running!"%(x+1))
					restart(result_dic[x][0][0])				
				else:
					print("The %d Server is running!"%(x+1))

if __name__ == '__main__':
	while True:
		with requests.Session() as s:
			s.headers = {
				'DNT':'1',
				'Host':'my.free-www.ru',
				'ISP-Client':'Web-interface',
				'Origin':'https://my.free-www.ru',
				'Referer':'https://my.free-www.ru/billmgr',
				'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
				'X-Requested-With':'XMLHttpRequest',
				'Connection':'keep-alive',
				'Upgrade-Insecure-Requests':'1'
			}
			main()
			time.sleep(3600)
			