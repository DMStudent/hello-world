# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from sogou_util import *
import os,sys
import math

__all__ = ['WordSegmentor']

class WordSegmentor:
    def __init__(self):
        os.putenv('LD_LIBRARY_PATH', './libs')
        self.p = Popen('bin/segmenttest', stdin=PIPE, stdout=PIPE)
    def simpleseg(self, val, flag=0):
	val = val.replace(' ', '')
        val = val.replace('\n', ' ')
        if len(val) < 2 or len(val) >= 65536/2:
            return []
        self.p.stdin.write(val)
        self.p.stdin.write('\n')
        self.p.stdin.flush()
        line = chomp(self.p.stdout.readline())
        res = [x for x in line.split('\t') if x]
        return res
    def close(self):
        self.p.stdin.close()
        os.waitpid(self.p.pid, 0)
        

if __name__ == '__main__':
	
	segmentor = WordSegmentor()
	for line_u in sys.stdin:
		line=line_u.strip().decode('utf-8').encode('gb18030')
		if line=='':
			continue
		items = line.split("\t")
		if len(items)<2:
			continue
		
		url = items[0]
		title = items[1]
		outputres = line_u.strip()
		terms=segmentor.simpleseg(title)
		segwords=" ".join(terms)
		outputres += "\t" + segwords.decode('gb18030').encode('utf-8')
		print outputres
	segmentor.close()




