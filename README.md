# Asyncio-Server-Web-Socket
Libreria micropython asyncrona para comunicacion por websocket
Servsock.py es una clase para simplificar la comunicacion con el cliente web.
en HTTP debemos crear nuestro proyecto web. 
En el archivo que crea la conexion websocket, en el lugar donde se asigna la direccion web del servidor, hay que poner 'ws:XXX.XXX.XXX.XXX'. ejemplo: [var wsUri = "ws://XXX.XXX.XXX.XXX";].
La clase substituira las X por la direccion del servidor.
en el ejemplo, editando test_servsock.py con los datos del wifi podremos probar la eficacia sin añadir ningun hardware al nodemcu.
detectara las pulsaciones en el pulsador flash y podremos encender y apagar el led del chip.Simultaneamente en varios equipos actualizando todos ellos simultaneramente.
Esta clase esta en su primera version y aun en su periodo de depuracion.
