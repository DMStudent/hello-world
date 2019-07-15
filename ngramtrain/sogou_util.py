#!encoding:gbk
import os
import re
from datetime import datetime
import subprocess
import shlex
import time
import math

def chomp(line):
    return line.rstrip(os.linesep)

def splitbytab(line):
    return chomp(line).split('\t')

class PathConfParser:
    #shell variable pattern
    __shv_pattern = re.compile(r'\${(.+)}')

    def __init__(self, filename='/search/muyixiang/conf/PATH.CONF'):
        #shell variabel tempates
        self.__templates = {}
        self.parse_res = {}
        for line in file(filename):
            k, v = self.__process_conf_item(line)
            self.parse_res[k] = v
    
    #shell variable replace function
    def __shv_replace(self, match_obj):
        k = match_obj.group(1)
        if k in self.__templates:
            return self.__templates[k]
        else:
            return ''

    def __process_conf_item(self, line):
        line = chomp(line)
        k, v = line.split('=')
        v = v[1:-1]
        v = PathConfParser.__shv_pattern.sub(self.__shv_replace, v)
        self.__templates[k] = v
        return k, v

    def __getitem__(self, key):
        if key in self.parse_res:
            return self.parse_res[key]
        else:
            return ''

    def __setitem__(self, key, value):
        self.parse_res[key] = value

def report_progress(i):
    if i % 10000 == 0:
        print i

def hit_rate(hit_base, target):
    base = set()
    i = 0
    for line in file(hit_base):
        key = chomp(line).split('\t')[0]
        base.add(key)
        i += 1
        report_progress(i)

    k = 0
    n = 0
    for line in file(target):
        key = chomp(line).split('\t')[0]
        if key in base:
            k += 1
        n += 1

    print k, n, float(k) / n

def get_freq(infile):
    '''统计infile中第一列key的频率，返回频率字典'''
    d = {}
    for line in file(infile):
        key = chomp(line).split('\t')[0]
        d.setdefault(key, 0)
        d[key] += 1
    return d

def parse_frontweblog(line):
    '''解析suggestion点击日志'''
    res = {}
    line = chomp(line)
    toks = line.split('\t')
    res['item'] = toks[0]
    res['pos'] = int(toks[1])
    res['query'] = toks[2]
    res['ip'] = toks[3]
    res['timestamp'] = datetime(*time.strptime(toks[4], '[%d/%b/%Y:%H:%M:%S]')[:6])
    return res

def get_sugg_weighted_pos(infile):
    '''获得平均点击量加权位置'''
    tmp = {}
    for line in file(infile):
        res = parse_frontweblog(line)
        tmp.setdefault(res['item'], [0,0])
        tmp[res['item']][0] += res['pos']
        tmp[res['item']][1] += 1
    d = {}
    for k, v in tmp.items():
        d[k] = v[0] * 1.0 / v[1]
        del tmp[k]
    return d

def get_sugg_uv(infile):
    '''获取suggestion的UV统计'''
    tmp = {}
    for line in file(infile):
        res = parse_frontweblog(line)
        tmp.setdefault(res['item'], set())
        tmp[res['item']].add(res['ip'])
    d = {}
    for k, v in tmp.items():
        d[k] = len(v)
        del tmp[k]
    return d

def normalize(filename, inpath, outpath, logpath):
    binpath = '/search/muyixiang/opt/sogou/bin'
    norm_command = '%s/normalize %s %s %s -key WebSuggestion/PreProcess/NormalizeQueryLog'
    conffname = '/search/muyixiang/Suggestion/conf/normalizeQueryLog.conf'
    print filename
    ifilename = os.path.join(inpath, filename)
    ofilename = os.path.join(outpath, filename)
    ferr = open(os.path.join(logpath, filename), 'w')
    cmd = norm_command % (binpath, conffname, ifilename, ofilename)
    args = shlex.split(cmd)
    subprocess.call(args, stderr=ferr)
    ferr.close()

if __name__ == '__main__':
    #for k, v in parse_conf('./PATH.CONF').items():
    #    print k, v
    conf = PathConfParser()
    print conf['USER_EVAL_PATH']
