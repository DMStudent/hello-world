import urllib
import sys
protocol, s1 = urllib.splittype(sys.argv[1])
host, s2=  urllib.splithost(s1)
print host

