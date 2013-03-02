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

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.4.4'
__CHEETAH_versionTuple__ = (2, 4, 4, 'development', 0)
__CHEETAH_genTime__ = 1362260463.520029
__CHEETAH_genTimestamp__ = 'Sat Mar  2 14:41:03 2013'
__CHEETAH_src__ = 'interface/templates/partials/alertsTmpl.tmpl'
__CHEETAH_srcLastModified__ = 'Sat Mar  2 12:42:20 2013'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class alertsTmpl(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(alertsTmpl, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def infoAlert(self, quip, message, **KWS):



        ## CHEETAH: generated from #def infoAlert($quip, $message) at line 1, col 1.
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
        
        write(u'''    <div class="alert alert-info ''')
        if len(VFFSL(SL,"message",True)) > 160: # generated from line 2, col 34
            write(u'''alert-block''')
        write(u'''">
        <button type="button" class="close" data-dismiss="alert"><i class="icon-remove-sign"></i></button>
''')
        if len(VFFSL(SL,"message",True)) > 160: # generated from line 4, col 9
            write(u'''            <h4><i class="icon-info-sign"></i> ''')
            _v = VFFSL(SL,"quip",True) # u'$quip' on line 5, col 48
            if _v is not None: write(_filter(_v, rawExpr=u'$quip')) # from line 5, col 48.
            write(u'''</h4>
            ''')
            _v = VFFSL(SL,"message",True) # u'$message' on line 6, col 13
            if _v is not None: write(_filter(_v, rawExpr=u'$message')) # from line 6, col 13.
            write(u'''
''')
        else: # generated from line 7, col 9
            write(u'''            <i class="icon-info-sign"></i> <strong>''')
            _v = VFFSL(SL,"quip",True) # u'$quip' on line 8, col 52
            if _v is not None: write(_filter(_v, rawExpr=u'$quip')) # from line 8, col 52.
            write(u'''</strong> ''')
            _v = VFFSL(SL,"message",True) # u'$message' on line 8, col 67
            if _v is not None: write(_filter(_v, rawExpr=u'$message')) # from line 8, col 67.
            write(u'''
''')
        write(u'''    </div>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def successAlert(self, quip, message, **KWS):



        ## CHEETAH: generated from #def successAlert($quip, $message) at line 13, col 1.
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
        
        write(u'''    <div class="alert alert-success ''')
        if len(VFFSL(SL,"message",True)) > 160: # generated from line 14, col 37
            write(u'''alert-block''')
        write(u'''">
        <button type="button" class="close" data-dismiss="alert"><i class="icon-remove-sign"></i></button>
''')
        if len(VFFSL(SL,"message",True)) > 160: # generated from line 16, col 9
            write(u'''            <h4><i class="icon-thumbs-up"></i> ''')
            _v = VFFSL(SL,"quip",True) # u'$quip' on line 17, col 48
            if _v is not None: write(_filter(_v, rawExpr=u'$quip')) # from line 17, col 48.
            write(u'''</h4>
            ''')
            _v = VFFSL(SL,"message",True) # u'$message' on line 18, col 13
            if _v is not None: write(_filter(_v, rawExpr=u'$message')) # from line 18, col 13.
            write(u'''
''')
        else: # generated from line 19, col 9
            write(u'''            <i class="icon-thumbs-up"></i> <strong>''')
            _v = VFFSL(SL,"quip",True) # u'$quip' on line 20, col 52
            if _v is not None: write(_filter(_v, rawExpr=u'$quip')) # from line 20, col 52.
            write(u'''</strong> ''')
            _v = VFFSL(SL,"message",True) # u'$message' on line 20, col 67
            if _v is not None: write(_filter(_v, rawExpr=u'$message')) # from line 20, col 67.
            write(u'''
''')
        write(u'''    </div>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def warningAlert(self, quip, message, **KWS):



        ## CHEETAH: generated from #def warningAlert($quip, $message) at line 25, col 1.
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
        
        write(u'''    <div class="alert ''')
        if len(VFFSL(SL,"message",True)) > 160: # generated from line 26, col 23
            write(u'''alert-block''')
        write(u'''">
        <button type="button" class="close" data-dismiss="alert"><i class="icon-remove-sign"></i></button>
''')
        if len(VFFSL(SL,"message",True)) > 160: # generated from line 28, col 9
            write(u'''            <h4><i class="icon-exclamation-sign"></i> ''')
            _v = VFFSL(SL,"quip",True) # u'$quip' on line 29, col 55
            if _v is not None: write(_filter(_v, rawExpr=u'$quip')) # from line 29, col 55.
            write(u'''</h4>
            ''')
            _v = VFFSL(SL,"message",True) # u'$message' on line 30, col 13
            if _v is not None: write(_filter(_v, rawExpr=u'$message')) # from line 30, col 13.
            write(u'''
''')
        else: # generated from line 31, col 9
            write(u'''            <i class="icon-exclamation-sign"></i> <strong>''')
            _v = VFFSL(SL,"quip",True) # u'$quip' on line 32, col 59
            if _v is not None: write(_filter(_v, rawExpr=u'$quip')) # from line 32, col 59.
            write(u'''</strong> ''')
            _v = VFFSL(SL,"message",True) # u'$message' on line 32, col 74
            if _v is not None: write(_filter(_v, rawExpr=u'$message')) # from line 32, col 74.
            write(u'''
''')
        write(u'''    </div>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def dangerAlert(self, quip, message, **KWS):



        ## CHEETAH: generated from #def dangerAlert($quip, $message) at line 37, col 1.
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
        
        write(u'''    <div class="alert alert-error ''')
        if len(VFFSL(SL,"message",True)) > 160: # generated from line 38, col 35
            write(u'''alert-block''')
        write(u'''">
        <button type="button" class="close" data-dismiss="alert"><i class="icon-remove-sign"></i></button>
''')
        if len(VFFSL(SL,"message",True)) > 160: # generated from line 40, col 9
            write(u'''            <h4><i class="icon-warning-sign"></i> ''')
            _v = VFFSL(SL,"quip",True) # u'$quip' on line 41, col 51
            if _v is not None: write(_filter(_v, rawExpr=u'$quip')) # from line 41, col 51.
            write(u'''</h4>
            ''')
            _v = VFFSL(SL,"message",True) # u'$message' on line 42, col 13
            if _v is not None: write(_filter(_v, rawExpr=u'$message')) # from line 42, col 13.
            write(u'''
''')
        else: # generated from line 43, col 9
            write(u'''            <i class="icon-warning-sign"></i> <strong>''')
            _v = VFFSL(SL,"quip",True) # u'$quip' on line 44, col 55
            if _v is not None: write(_filter(_v, rawExpr=u'$quip')) # from line 44, col 55.
            write(u'''</strong> ''')
            _v = VFFSL(SL,"message",True) # u'$message' on line 44, col 70
            if _v is not None: write(_filter(_v, rawExpr=u'$message')) # from line 44, col 70.
            write(u'''
''')
        write(u'''    </div>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
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

    _mainCheetahMethod_for_alertsTmpl= 'respond'

## END CLASS DEFINITION

if not hasattr(alertsTmpl, '_initCheetahAttributes'):
    templateAPIClass = getattr(alertsTmpl, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(alertsTmpl)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=alertsTmpl()).run()


