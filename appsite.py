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

import os, sys
import platform
from ConfigParser import SafeConfigParser

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AppSite(object):
    configFile = '.appsite'
    basePath = '.'
    platformName = platform.system().lower()

    def __init__(self):
        self.basePath = self.findPathSite()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def findPathSite(self, path='.', configFile=None):
        if configFile is None:
            configFile = self.configFile
        join = os.path.join
        exists = os.path.exists
        abspath = os.path.abspath

        parent = abspath(path)
        while True:
            path = parent
            cf = join(path, configFile)
            if exists(cf):
                return path

            parent = abspath(join(path, '..'))
            if path == parent:
                return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _cfg = None
    def getCfg(self):
        if self._cfg is None:
            appsite = os.path.join(self.basePath, self.configFile)
            self._cfg = SafeConfigParser()
            self._cfg.read(appsite)
        return self._cfg
    cfg = property(getCfg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def runApplet(self, appletName, argv=None):
        if argv is None:
            argv = sys.argv[1:]

        applet = self.cfg.get(
                        'appsite-' + self.platformName,
                        'applet', 
                        vars=dict(
                            base=self.basePath,
                            applet_name=appletName))

        os.system('"%s" %s' % (applet, ' '.join(argv)))

appsite = AppSite()

