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

    applet_darwin='"%(app_base)s/Contents/MacOS/%(app_name)s"'
    applet_winows='"%(app_base)s/Contents/Windows/%(app_name)s.exe"'

    _basePath = None
    def getBasePath(self):
        if self._basePath is None:
            self._basePath = self.findPathSite()
            os.environ['APPSITE'] = self._basePath
        return self._basePath
    basePath = property(getBasePath)

    def cfgEntry(self, section, value, vars={}):
        entry = self.cfg.get(section, value, vars=vars)
        entry = self._dequote(entry)
        return entry
    def cfgEntryPath(self, section, value):
        loc = self.cfg.get(section, value, vars=self.locations)
        loc = self._dequote(loc)
        return self.joinPath(loc)
    def joinPath(self, *args):
        return os.path.join(self.basePath, *args)
    def locationPath(self, location, *args):
        loc = self.cfg.get('locations', location)
        loc = self._dequote(loc)
        return self.joinPath(loc, *args)

    def _dequote(self, loc):
        loc = loc.strip()
        if loc[:1] in ['"', "'"]:
            if loc[-1:] == loc[:1]:
                loc = loc[1:-1]
        return loc

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
        return dict(self.cfg.items('locations'))
    locations = property(getLocations)

    _cfg = None
    def getCfg(self):
        if self._cfg is None:
            appsite = self.joinPath(self.configFile)
            self._cfg = SafeConfigParser()
            self._cfg.read(appsite)
        return self._cfg
    cfg = property(getCfg)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def runApplet(self, appletName=None, argv=None):
        if argv is None:
            argv = sys.argv[1:]

        applet = self.getApplet(appletName)
        cmd = '%s %s' % (applet, ' '.join(argv))
        print cmd
        return os.system(cmd)

    def getApplet(self, appletName=None):
        proj = self.cfg.get('appsite', 'current')

        if self.cfg.has_option(proj, 'app_host'):
            app_host = self.cfg.get(proj, 'app_host')
        else: app_host = None
        if not app_host:
            app_host = self.getBasePath()

        if appletName is None:
            appletName = self.cfg.get(proj, 'app_name')

        if not self.cfg.has_option('appsite', 'applet_'+self.platformName):
            self.cfg.set('appsite', 'applet_'+self.platformName, getattr(self, 'applet_'+self.platformName))

        try:
            applet = self.cfg.get(
                            'appsite',
                            'applet_'+self.platformName, 
                            vars=dict(
                                base=self.basePath,
                                app_host=app_host,
                                app_base=os.path.join(self.basePath, app_host),
                                app_name=appletName))
        except RuntimeError, e:
            print e
            raise SystemExit(-1)
        
        return applet

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

appsite = AppSite()

