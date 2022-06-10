from flask_ldap3_login import LDAP3LoginManager
from ldap3 import Server, Connection, ALL
config = dict()

# Setup LDAP Configuration Variables. Change these to your own settings.
# All configuration directives can be found in the documentation.

# Hostname of your LDAP Server
config['LDAP_HOST'] = 'ldap.forumsys.com  '
config['LDAP_PORT'] = 389
# Base DN of your directory
config['LDAP_BASE_DN'] = 'dc=example,dc=com'

# Users DN to be prepended to the Base DN
config['LDAP_USER_DN'] = 'cn=euler'

# Groups DN to be prepended to the Base DN
config['LDAP_GROUP_DN'] = 'ou=mathematicians'

# The RDN attribute for your user schema on LDAP
config['LDAP_USER_RDN_ATTR'] = 'cn'

# The Attribute you want users to authenticate to LDAP with.
config['LDAP_USER_LOGIN_ATTR'] = 'userPassword'

# The Username to bind to LDAP with
config['LDAP_BIND_USER_DN'] = 'ou=mathematicians,dc=example,dc=com'

# The Password to bind to LDAP with
config['LDAP_BIND_USER_PASSWORD'] = 'password'
config['LDAP_USER_SEARCH_SCOPE'] = 'SUBTREE'
# config['LDAP_BIND_AUTHENTICATION_TYPE'] = None

# Setup a LDAP3 Login Manager.
ldap_manager = LDAP3LoginManager()

# Init the mamager with the config since we aren't using an app
ldap_manager.init_config(config)

# Check if the credentials are correct
response = ldap_manager.authenticate(config['LDAP_BIND_USER_DN'],config['LDAP_BIND_USER_PASSWORD'])
print(response.status)


