#Low level controllers first
from controllers.indexController import * #/
#from controllers.errorController import * #/error
#from controllers.searchController import * #/search

#Next, /admin/ controllers
from controllers.admin.adminController import * #/admin
# -> /admin/flags/
from controllers.admin.flags.adminDelFlagController  import * #/admin/flags/(.*)/delete
from controllers.admin.flags.adminEditFlagController  import * #/admin/flags/(.*)/edit
from controllers.admin.flags.adminViewFlagsController  import * #/admin/flags/(.*)
# -> /admin/users/
from controllers.admin.users.adminDelUserController  import * #/admin/users/(.*)/delete
from controllers.admin.users.adminEditUserController  import * #/admin/users/(.*)/edit
from controllers.admin.users.adminNewUserController  import * #/admin/users/new
from controllers.admin.users.adminViewUsersController  import * #/admin/users

#Next, /auth/ controllers
from controllers.auth.authLoginController import * #/auth/login
from controllers.auth.authLogoutController import * #/auth/logout
from controllers.auth.authRegisterController import * #/auth/register

#Next, /flags/ controllers
from controllers.flags.flagDelController  import * #/flag/(.*)/delete
from controllers.flags.flagEditController  import * #/flag/(.*)/edit
from controllers.flags.flagNewController  import * #/flag/new
from controllers.flags.flagViewController  import * #/flag/(.*)

#Next, /labels/ controllers
#from controllers.labels.labelsViewController import * #/labels/(.*)

#Next, /public/ controllers
#from controllers.public.publicLabelsController  import * #/public/labels
from controllers.public.publicFlagsController  import * #/public/flags

#Next, /user/ controllers
from controllers.user.userFlagsController  import * #/user/(.*)/flags
#from controllers.user.userLabelsController  import * #/user/(.*)/labels
from controllers.user.userProfileController  import * #/user/(.*)/profile

#Finally, /you/ controllers
from controllers.you.youDashboardController  import * #/your/dashboard
from controllers.you.youFlagsController  import * #/your/flags
#from controllers.you.youLabelsController  import * #/your/labels
from controllers.you.youProfileController  import * #/your/profile
from controllers.you.youSettingsController  import * #/your/settings
