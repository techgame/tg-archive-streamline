#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variiables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def findHGALLSite(path='.', configFile='.hgall'):
    join = os.path.join
    exists = os.path.exists
    abspath = os.path.abspath

    pathRoot = abspath(path)
    parent = pathRoot
    while True:
        path = parent
        cf = join(path, configFile)
        if exists(cf):
            return path

        parent = abspath(join(path, '..'))
        if path == parent:
            break

    raise RuntimeError("No %s file found anywhere in %r" % (configFile, pathRoot))

if sys.platform == 'win32':
    ansiNormal = ''
    ansiRed = ''
    ansiGreen = ''
    ansiBlue = ''
    ansiLtRed = ''
    ansiLtGreen = ''
    ansiLtBlue = ''
else:
    ansiNormal = '\033[0m'
    ansiRed = '\033[0;31m'
    ansiGreen = '\033[0;32m'
    ansiBlue = '\033[0;34m'
    ansiLtRed = '\033[1;31m'
    ansiLtGreen = '\033[1;32m'
    ansiLtBlue = '\033[1;34m'

def hgcmd(argv):
    if argv[:1] == ['--refresh']:
        argv = argv[1:]
        os.system('find . -name ".hg" > .hgall')
    else:
        site = findHGALLSite()
        os.chdir(site)

    hgRepos = [os.path.split(s.strip())[0] for s in file('.hgall', 'rb').readlines()]

    if not argv:
        argv = ['status']

    print ansiLtBlue, '>>> hg -R {REPO}', ' '.join(argv), ansiNormal
    for repo in hgRepos:
        repo = os.path.normpath(repo)
        print ansiLtGreen, "REPO:", repo, ansiNormal
        r = os.system('hg -R "%s" %s' % (repo, ' '.join(argv))) 
        if r != 0:
            print ansiLtRed, "ERROR:", r


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    hgcmd(sys.argv[1:])

