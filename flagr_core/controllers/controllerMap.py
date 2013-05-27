##Low level controllers first
#from controllers.indexController import * #/
#from controllers.errorController import * #/error
#from controllers.searchController import * #/search

##Next, /admin/ controllers
#from controllers.admin.adminController import * #/admin
## -> /admin/flags/
#from controllers.admin.flags.adminDelFlagController  import * #/admin/flags/(.*)/delete
#from controllers.admin.flags.adminEditFlagController  import * #/admin/flags/(.*)/edit
#from controllers.admin.flags.adminViewFlagsController  import * #/admin/flags/(.*)
## -> /admin/users/
#from controllers.admin.users.adminDelUserController  import * #/admin/users/(.*)/delete
#from controllers.admin.users.adminEditUserController  import * #/admin/users/(.*)/edit
#from controllers.admin.users.adminNewUserController  import * #/admin/users/new
#from controllers.admin.users.adminViewUsersController  import * #/admin/users
## -> /admin/dev/
#from controllers.admin.dev.buckets.adminDevBucketsViewController import * #/admin/dev/buckets
## -> /admin/templates/
#from controllers.admin.templates.adminViewTemplatesController import * #/admin/templates
#from controllers.admin.templates.adminEditTemplatesController import * #/admin/templates/(.*)/edit
#from controllers.admin.templates.adminDelTemplatesController import * #/admin/templates/(.*)/delete
#from controllers.admin.templates.adminBulkDelTemplatesController import * #/admin/templates/delete
#from controllers.admin.templates.adminTemplatesSettingsController import * #/admin/templates/settings
#from controllers.admin.templates.adminNewTemplatesController import * #/admin/templates/new
#from controllers.admin.templates.adminInfoTemplatesController import * #/admin/templates/(.*)
## -> /admin/requests/
#from controllers.admin.requests.adminViewRequestsController import * #/admin/requests
#from controllers.admin.requests.adminRequestsSettingsController import * #/admin/requests/settings
#from controllers.admin.requests.adminGrantRequestsController import * #/admin/requests/(.*)edit
#from controllers.admin.requests.adminDelRequestsController import * #/admin/requests/(.*)/delete

##Next, /auth/ controllers
#from controllers.auth.authLoginController import * #/auth/login
#from controllers.auth.authLogoutController import * #/auth/logout
#from controllers.auth.authRegisterController import * #/auth/register

##Next, /request/ controllers
#from controllers.request.requestsRegisterController import *
#from controllers.request.requestsRequestController import *
#from controllers.request.requestsThanksController import *

##Next, /flags/ controllers
#from controllers.flags.flagDelController  import * #/flag/(.*)/delete
#from controllers.flags.flagEditController  import * #/flag/(.*)/edit
#from controllers.flags.flagNewController  import * #/flag/new
#from controllers.flags.flagViewController  import * #/flag/(.*)

##Next, /labels/ controllers
#from controllers.labels.labelsViewController import * #/labels/(.*)

##Next, /public/ controllers
#from controllers.public.publicLabelsController  import * #/labels
#from controllers.public.publicFlagsController  import * #/flags

##Next, /user/ controllers
#from controllers.user.userFlagsController  import * #/user/(.*)/flags
#from controllers.user.userLabelsController  import * #/user/(.*)/labels
#from controllers.user.userProfileController  import * #/user/(.*)/profile

##Finally, /you/ controllers
#from controllers.you.youDashboardController  import * #/your/dashboard
#from controllers.you.youSearchController import * #/your/search
#from controllers.you.youFlagsController  import * #/your/flags
#from controllers.you.youLabelsController  import * #/your/labels
#from controllers.you.youProfileController  import * #/your/profile
#from controllers.you.youSettingsController  import * #/your/settings

import os
which = ""
path = os.path.dirname(__file__)
for folder in os.walk(path):
    base = folder[0][len(path):].replace("/", ".").strip(".")
    if len(base) > 0:
        which = "controllers." + base + "."
    else:
        which = "controllers."
    for module in folder[2]:
        if module == '__init__.py' \
                or module[-3:] != '.py' \
                or module == 'maintenanceController.py' \
                or module == 'controllerMap.py':
                    continue
        module = module[:-3]
        fullname = which + module
        __import__(fullname, locals(), globals(), ['*'])
        for k in dir(fullname):
            locals()[k] = getattr(fullname, k)
del module
