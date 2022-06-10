from ldap3 import Server, Connection, ALL, NTLM
#Server
#server = Server('ldap://EMEA.ZURICH.CORP:389',  get_info=ALL)
##conn = Connection(server, 'CN=GBNQIK,OU=Std,OU=zUsers,DC=emea,DC=zurich,DC=corp', 'Project@4321', auto_bind=True)
##conn = Connection('ldap://EMEA.ZURICH.CORP', auto_bind=True)

#print(server)
##print(server.schema)

server = Server('ipa.demo1.freeipa.org', use_ssl=True, get_info=ALL)
conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
print(conn)
