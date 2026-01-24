#!/bin/bash

# This program is free software: you can redistribute it under
# the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, 
# or any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
                                                                                
echo "++++++++++++++++++++++++++++++++++++++++"
echo "+                                      +"
echo "+        Service AUTO STARTER          +"
echo "+                                      +"
echo "+      Developed by: Letum Devil       +"
echo "+     Email: letumdevil@gmail.com      +"
echo "+                                      +"
echo "+  github.com/letumdevil/autostarter/  +" 
echo "+                                      +"
echo "++++++++++++++++++++++++++++++++++++++++"
echo
echo "      ----- Choose an option -----      "
echo
echo -n "   [1] Start programming services"
echo
echo -n "   [2] Start Postgresql & Metasploit Service"
echo
echo -n "   [3] Start Networking Service"
echo
echo -n "   [4] Start TOR Service"
echo
echo -n "   [5] Start BEEF Service"
echo
echo
echo -n "Press [Q] To exit"
echo
read -n 1 option
echo

if [ "$option" == "1" ]; then
 /etc/init.d/apache2 start
 /etc/init.d/mysql start
 echo "[*] Programming services started"
 exit 1
elif [ "$option" == "2" ]; then
 /etc/init.d/postgresql start
 /etc/init.d/metasploit start
 echo "[*] Postgresql & Metasploit services started"
 exit 1
elif [ "$option" == "3" ]; then
 /etc/init.d/networking start
 echo "[*] Networking service started"
 exit 1
elif [ "$option" == "4" ]; then
 /etc/init.d/tor start
 echo "[*] TOR service started"
 exit 1
elif [ "$option" == "5" ]; then
 /etc/init.d/beef-xss start
 echo "[*] BEEF service started"
 exit 1
elif [ "$option" == "Q" ]; then
 echo "++ Thank you for using AUTO Starter ++"
 exit 1
elif [ "$option" == "q" ]; then
 echo "++ Thank you for using AUTO Starter ++"
 exit 1
fi

