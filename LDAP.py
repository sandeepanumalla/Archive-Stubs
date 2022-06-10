from flask_ldap3_login import LDAP3LoginManager
from flask_ldap3_login import AuthenticationResponseStatus
from ldap3 import Server, Connection, ALL
config = dict()

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.

# Hostname of your LDAP Server
config['LDAP_HOST'] = 'ldap://localhost'
config['LDAP_PORT'] = 10389
# Base DN of your directory
config['LDAP_BASE_DN'] = 'ou=user,ou=system'

# Users DN to be prepended to the Base DN
config['LDAP_USER_DN'] = 'cn=mike'

# Groups DN to be prepended to the Base DN
config['LDAP_GROUP_DN'] = 'ou=user'

# The RDN attribute for your user schema on LDAP
config['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
config['LDAP_USER_LOGIN_ATTR'] = 'userPassword'

# The Username to bind to LDAP with
config['LDAP_BIND_USER_DN'] = 'cn=mike,ou=user,ou=system'

# The Password to bind to LDAP with
config['LDAP_BIND_USER_PASSWORD'] = '123456'
config['LDAP_USER_SEARCH_SCOPE'] = 'SUBTREE'
# config['LDAP_BIND_AUTHENTICATION_TYPE'] = None

# Setup a LDAP3 Login Manager.
ldap_manager = LDAP3LoginManager()

# Init the mamager with the config since we aren't using an app
ldap_manager.init_config(config)

# Check if the credentials are correct
response = ldap_manager.authenticate(config['LDAP_BIND_USER_DN'],config['LDAP_BIND_USER_PASSWORD'])
print(response.status)

