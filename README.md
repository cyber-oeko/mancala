Mancala
=======

Installation (Client)
---------------------
Recommended: via .deb-Package
https://github.com/cyber-oeko/mancala/releases/download/v1.0.0/python3-mancala_1.0.0-1_all.deb

Alternatively:
```
pip3 install -r requirements.txt
python3 setup.py install
```

Installation (Server)
---------------------
* Requirements: sql-compatible database, php running webserver
* Execute sql script `server/schema.sql`
* Set credentials in `server/db_connect.php`
* Move `server/db_connect.php` and `server/server.php` to php-webserver (e. g. via ftp)

Login
-----
1st player: just set url and name and click OK, then the game number appears
2nd player: set url and name, check "Join game" and insert the Game ID, that the 1st player told you

Gameplay
--------
* Click a hole to start your move and a neighboring hole to set the direction.
* Click on enemy hole to capture, click on own hole to not capture.


Color-Palette: https://coolors.co/8e9b90-93c0a4-b6c4a2-d4cdab-cdadb4
