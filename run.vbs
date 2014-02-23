set ws=wscript.createobject("wscript.shell")
ws.run "manage.py runfcgi method=threaded host=127.0.0.1 port=9001",0