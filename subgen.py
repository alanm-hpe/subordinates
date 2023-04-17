import ssl
import json
from ldap3 import Server, \
    Connection, \
    SUBTREE, \
    Tls

# ldapsearch -x -h example-ldap.com -b "dc=dcldap,dc=dit"
# alanm, people, dcldap.dit
# dn: uid=alanm,ou=people,dc=ldap,dc=dit
# uid: alanm
# objectClass: posixAccount
# objectClass: shadowAccount
# objectClass: inetOrgPerson
# objectClass: organizationalPerson
# mail: alan.mutschelknaus@hpe.com
# uidNumber: 
# gidNumber:
# homeDirectory: /home/users/alanm
# cn: Alan Mutschelknaus
# gecos: Alan Mutschelknaus
# sn: Alan Mutschelknaus
# loginShell: /bin/bash

LDAP_HOST = 'example-ldap.com'
LDAP_BASE_DN = 'dc=ldap,dc=dit'
ATTRIBUTES = ['cn', 'uid', 'uidNumber', 'gidNumber']
OPERATIONAL_ATTRIBUTES=False
tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1)

SUBUID_START = 200000000
SUBUID_STOP  = 400000000
SUBUID_CUR   = SUBUID_START
OFFSET       = 65536

def get_users():
    with ldap_connection() as c:
        c.search(search_base=LDAP_BASE_DN,
                 search_filter='(uid=*)',
                 search_scope=SUBTREE,
                 attributes=ATTRIBUTES,
                 get_operational_attributes=OPERATIONAL_ATTRIBUTES)

        json_object = json.loads(c.response_to_json())
        #json_formatted_str = json.dumps(json_object, indent=2)
        #print(json_formatted_str)

    return json_object


def ldap_connection():
    server = ldap_server()
    return Connection(server, user='',
                      password='',
                      auto_bind=True)

def ldap_server():
    return Server(LDAP_HOST, use_ssl=True, tls=tls_configuration)


users=get_users()
num_users=len(users['entries'])

if SUBUID_STOP != '' and SUBUID_START+num_users*OFFSET > SUBUID_STOP:
    print('SUBUID range will be exceeded!')
    exit(1)

for user in users['entries']:
    #print(user['attributes']['uid'][0]+':'+str(SUBUID_CUR)+':'+str(OFFSET))
    print(str(user['attributes']['uidNumber'])+':'+str(SUBUID_CUR)+':'+str(OFFSET))
    SUBUID_CUR=SUBUID_CUR+OFFSET

