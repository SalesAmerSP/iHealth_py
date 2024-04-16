#user creds obtained from iHealth Settings
import base64

#client ID
cID=''
#client Secret
cSec=''
basic = cID+':'+cSec
ascii_string = basic.encode('ascii')
byte_auth = base64.b64encode(ascii_string)
bauth = byte_auth.decode()
