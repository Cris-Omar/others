On the Apache Server the reqtimeout should be disable for it to work:
https://www.kali.org/tools/apache2/#a2dismod
https://httpd.apache.org/docs/trunk/mod/mod_reqtimeout.html

sudo a2dismod reqtimeout

to re-enable it:
sudo a2enmod reqtimeout
______________________

Das Programm wird folgendermassen ausgeführt:

python3 slowloris.py <ip_vm>

Wenn das Programm ohne weitere Argumente aufgerufen wird, werden 150 Sockets erstellt und dann alle 15 Sekunden Daten gesendet.

Ein aktueller Apache Server auf Ubuntu 20.04.3 LTS kann ist aber auf 250 Verbindungen konfiguriert. Damit dieser Server angegriffen werden kann kann der folgende Befehl ausgeführt werden:

python3 slowloris.py <ip_vm> -s 500