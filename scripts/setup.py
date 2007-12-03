##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys, os
from distutils.core import setup

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

scripts=['ipysl.py', 'pysl.py', 'appsl.py', 'hgall.py']

if os.name == 'posix':
    scripts = [os.path.splitext(e)[0] for e in scripts]
    print scripts

if os.name.startswith('win'):
    print
    print "NOTE:"
    print "For these scripts to run correctly, you need to make sure a few environment variables are set."
    print
    print "  PATH needs to include: \"%s\\Scripts\"" % (sys.exec_prefix,)
    print "  PATHEXT needs to include: \".PY\""
    print
        
setup(name='TG.streamline scripts', version='0.1', scripts=scripts)

