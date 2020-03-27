
#!/usr/bin/env python
from core.colors import color
from cgi import escape
from time import sleep
import gzip
import os
import base64
import html
from database.database_module import save_data
import urllib
# try:
#     import StringIO # python2
# except ImportError:
#     from io import StringIO
#     # python3
#

def encodeall(target):
    from core.build_menu import buildmenu
    try:
        st = input(color.yellow(' [-] Enter a string to be encoded/decoded :> '))
        m64 = base64.b64encode(st.encode())
        data=m64.decode()
        print(color.green(' [+] Base64 Encoded String : ')+color.yellow(data))
        #save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
    except Exception as e:
        pass
    try:
        m32 = base64.b32encode(st.encode())
        data=m32.decode()
        print(color.green(' [+] Base32 Encoded String : ')+color.yellow(data))
        #save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
    except Exception as e:
        pass        
    try:
        m16 = base64.b16encode(st.encode())
        data=m16.decode()
        print(color.green(' [+] Base16/Hex Encoded String : ')+color.yellow(data))
        #save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
    except Exception as e:
        print(color.red(" [-] Caught Exception : "+str(e)))
    try:
        m64d = base64.b64decode(st.encode())    
        data=m64d.decode()
        print(color.green(' [+] Base64 Decoded String : ')+color.yellow(data))
        #save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
    except Exception as e:
        pass
    try:
        m32d = base64.b32decode(st.encode())
        data=m32d.decode()
        print(color.green(' [+] Base32 Decoded String : ')+color.yellow(data))
        #save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
    except Exception as e:
        pass
    try:
        m16d = base64.b16decode(st.encode())
        data=m16d.decode()
        print(color.green(' [+] Base16/Hex Decoded String : ')+color.yellow(data))
        #save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, str(data))
    except Exception as e:
        pass
    try:
        data=urllib.parse.quote(st, safe='')
        print(color.green(' [+] URL Encoded String : ')+color.yellow(data))
        data=urllib.parse.quote_plus(st,safe='')
        print(color.green(' [+] URL plus Encoded String : ')+color.yellow(data))
    except Exception as e:
        pass
    try:
        data=urllib.parse.unquote(st)
        print(color.green(' [+] URL Decoded String : ')+color.yellow(data))
        data=urllib.parse.unquote_plus(st)
        print(color.green(' [+] URL plus Decoded String : ')+color.yellow(data))
    except Exception as e:
        pass
    # more types of encoding still need added
        # encod = ''
        # stri = list(st)
        # for i in stri:
        #     encod = encod + escape(i)
        # print(color.green(' [+] Encoded String : ')+color.yellow(encod))
        # m = st.encode('base64', 'strict')
        # print(color.green(' [+] Encoded String : ')+color.yellow(m))
        # m = st.encode('hex', 'strict')
        # print(color.green(' [+] Encoded String : ')+color.yellow(m))
        # result = []
        # for char in st:
        #     result.append('\%o' % ord(char))
        # print(color.green(' [+] Octal Encoded String : ')+color.yellow(str(''.join(result))))
        # m = ''.join(format(ord(x),'b') for x in st)
        # print(color.green(' [+] Encoded String : ')+color.yellow(m))
        # m = st.encode('zlib','strict')
        # print(color.green(' [+] Encoded String : ')+color.yellow(m))
    st = input(color.blue(' [#] Press')+color.red(' Enter ')+color.blue('to continue... '))
    buildmenu(target,target[0].main_menu,'Main Menu','')
