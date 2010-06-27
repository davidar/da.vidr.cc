import os

path = os.environ['PATH_INFO']
print 'Status: 301'
print 'Location: ', path[:path.rfind('index')]
print
