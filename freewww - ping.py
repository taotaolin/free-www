#coding=utf8
import requests,re,time,os

username = '面板用户'
password = '面板密码' 
ID = '机器ID'
ip = '检测机器IP'
check = 'vm'
restart = 'vm.restart'


checkurl = 'http://kvm.free-www.ru:1500/vmmgr?out=xml&authinfo={0}:{1}&func={2}&elid={3}'.format(username,password,check,ID)
keepurl = 'http://kvm.free-www.ru:1500/vmmgr?out=xml&authinfo={0}:{1}&func={2}&elid={3}'.format(username,password,restart,ID)
list1 = [('ok', 'vm.restart')]


def check(url = checkurl):
	try:
		s = requests.Session()
		r = s.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except Exception as e:
		print(e)

def restart(url = keepurl):
	try:
		s = requests.Session()
		r = s.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		khtml = r.text
		result = re.findall(r'><(.*)/><tparams><elid>237</elid><out>xml</out><func>(.*)</func>',khtml)
		if list1 == result:
			print("Success Runing!")
		else:
			print("Error")
	except Exception as e:
		print(e)	

def main():
	if(os.system('ping -c 5 -w 5 %s'%ip) == 0):
		print("Free-www is Running")
	else:
		rhtml = check()
		state = re.findall(r'<vmstatus>(.*)</vmstatus>',rhtml)
		if "running" in state:
			print("Free-www is Running")
		else:
			restart()

if __name__ == '__main__':
	while True:
		main()
		time.sleep(300)
