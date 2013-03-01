#!/usr/bin/env python




##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from bootstrapSkeleton import bootstrapSkeleton

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.4.4'
__CHEETAH_versionTuple__ = (2, 4, 4, 'development', 0)
__CHEETAH_genTime__ = 1362168240.326714
__CHEETAH_genTimestamp__ = 'Fri Mar  1 13:04:00 2013'
__CHEETAH_src__ = 'interface/templates/user/userSettingsTmpl.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Feb 27 08:37:50 2013'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class userSettingsTmpl(bootstrapSkeleton):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(userSettingsTmpl, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def body(self, **KWS):



        ## CHEETAH: generated from #def body at line 3, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''<!-- Start settings template -->
<form class="horizontal-form" action="#settingsFormAddress" method="POST">
    <div class="control-group">
        <h3 class="control-label">Email <small>Just so it\'s easy for us to contact you...</small></h3>
        <div class="control">
            <input type="text" class="span10" id="email" placeholder="''')
        if VFFSL(SL,"user.email",True): # generated from line 9, col 71
            _v = VFFSL(SL,"user.email",True) # u'$user.email' on line 9, col 87
            if _v is not None: write(_filter(_v, rawExpr=u'$user.email')) # from line 9, col 87.
        else: # generated from line 9, col 98
            write(u'''example@example.com''')
        write(u'''">
        </div>
        <span class="help-block"><small class="muted">You don\'t have to register an email, and can remove it at anytime. We do not give away your email, and request it simply to make notifying you about updates or changes easier.</small></span>
    </div>
    <div class="control-group">
        <h3 class="control-label">Password <small>You don\'t have to update it, but we leave this here in case you do...</small></h3>
        <div class="control">
            <input type="password" class="span10" id="oldPassword" placeholder="************">
            <input type="password" class="span10" id="newPasswordOne" placeholder="************">
            <input type="password" class="span10" id="newPasswordTwo" placeholder="************">
        </div>
        <span class="help-block"><small class="muted">If you don\'t want to update your password, just leave this blank.</small></span>
    </div>
    <div class="form-actions">
        <button type="submit" class="btn btn-primary">Save changes</button>
    </div>
</form>
<!-- End settings template -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def writeBody(self, **KWS):



        ## CHEETAH: main method generated for this template
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_userSettingsTmpl= 'writeBody'

## END CLASS DEFINITION

if not hasattr(userSettingsTmpl, '_initCheetahAttributes'):
    templateAPIClass = getattr(userSettingsTmpl, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(userSettingsTmpl)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=userSettingsTmpl()).run()


