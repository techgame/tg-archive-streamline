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
    configFile = 'appsite.cfg'
    platformName = platform.system().lower()

    _basePath = None
    def getBasePath(self):
        if self._basePath is None:
            self._basePath = self.findPathSite()
            os.environ['APPSITE'] = self._basePath
        return self._basePath
    basePath = property(getBasePath)

    def cfgEntryPath(self, section, value):
        pathEntry = self.cfg.get(section, value, vars=self.locations)
        return self.joinPath(pathEntry)
    def joinPath(self, *args):
        return os.path.join(self.basePath, *args)
    def locationPath(self, location, *args):
        loc = self.cfg.get('locations', location)
        loc = loc.strip()
        if loc[:1] in ['"', "'"]:
            if loc[-1:] != loc[:1]:
                raise ValueError('Unmatched quotes in location: '+location)
            loc = loc[1:-1]

        return self.joinPath(loc, *args)

    def findPathSite(self, path='.', configFile=None):
        if configFile is None:
            configFile = self.configFile
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

        raise RuntimeError("No %s file found anywhere in %r" % (self.configFile, pathRoot))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getLocations(self):
        return self.cfg.get('locations')
    locations = property(getLocations, setLocations)

    _cfg = None
    def getCfg(self):
        if self._cfg is None:
            appsite = self.joinPath(self.configFile)
            self._cfg = SafeConfigParser()
            self._cfg.read(appsite)
        return self._cfg
    cfg = property(getCfg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def runApplet(self, appletName, argv=None):
        if argv is None:
            argv = sys.argv[1:]

        try:
            applet = self.cfg.get(
                            'appsite-' + self.platformName,
                            'applet', 
                            vars=dict(
                                base=self.basePath,
                                applet_name=appletName))
        except RuntimeError, e:
            print e
            raise SystemExit(-1)

        return os.system('"%s" %s' % (applet, ' '.join(argv)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

appsite = AppSite()

