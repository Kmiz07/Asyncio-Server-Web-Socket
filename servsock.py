import uasyncio
import usocket
import uos
import ubinascii
import hashlib
import urandom

a=''
class Servsock:
    def __init__(self,si_recibe=None,puerto=80,tambuf=-1,encriptado=False):
        self.si_recibe=si_recibe#evento cuando recibe datos
        self.puerto=puerto
        self.tambuf=tambuf
        self.tarea_inicio= uasyncio.create_task(self.inicia_socket())
        self.tarea_recepcion=uasyncio.create_task(self.recibe_datos())
        self.escritura=b''#bufer datos de entrada
        self.terminar=False#puntero para determinar cuando terminar todo.
        self.clientes=[]
        self.enviobool=False
        self.encriptado=encriptado
        
    async def inicia_socket(self):
        self.servidor=usocket.socket()
        confserv=("",self.puerto)
        self.servidor.bind(confserv)
        self.servidor.setblocking(False)
        self.servidor.listen()
        while not self.terminar:
            conexion=None
            try:
                conexion,direccion=self.servidor.accept()
                conexion.setblocking(False)
            except Exception as err:
                if err.args[0]==11:
                    pass
            if conexion:
                self.clientes.append([conexion,direccion,False])
            await uasyncio.sleep(0)
        for cliente in clientes:
            cliente[0].close()
        clientes.clear()
        servidor.close()
           
            
    async def recibe_datos(self):
        while not self.terminar:
            mensaje_completo=b''
            for cliente in self.clientes:
                try:
                    mensaje=cliente[0].read(self.tambuf)
                except:
                    pass
                if mensaje:
                    mensaje_completo+=mensaje
                    while mensaje:
                        mensaje=cliente[0].read(self.tambuf)
                        if mensaje:
                            mensaje_completo+=mensaje
                            if len(mensaje)<self.tambuf or self.tambuf==-1:break
                    await self.procesa(cliente,mensaje_completo)
            await uasyncio.sleep(0)
        
    async def finaliza(self):
        await self.desconecta_global()
        self.terminar=True
        self.servidor.close()
        
    async def envia(self,cliente,mensaje):
        try:
            cliente[0].send(mensaje)
            await uasyncio.sleep(0)
        except:
            pass
        
    async def envio_global(self,mensaje):
        for cliente in self.clientes:
            await self.envia(cliente,mensaje)
                        
    async def desconecta(self,cliente):
        cliente[0].close()
        self.clientes.remove(cliente)
        
    async def desconecta_global(self):
        for cliente in self.clientes:
            await self.desconecta(cliente)
            
    async def procesaws(self,cliente,mensaje):
        magicstring='258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        keyws=None
        for linea in mensaje:
            if 'Sec-WebSocket-Key:' in linea:
                keyws=linea.split(' ')[1]
        if keyws:
            keyws+=magicstring
            keyhash=hashlib.sha1(keyws.encode('utf-8'))
            keystr=keyhash.digest()
            keyb64=ubinascii.b2a_base64(keystr)
            strb64=keyb64.decode('utf-8').replace('\n','')
            await self.envia(cliente,"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "+strb64+"\r\n\r\n")
            cliente[2]=True
            self.enviobool=True
        else:
            await self.envia("HTTP/1.1 404 OK\r\nContent-Type: \text/html\r\nConnection: keep-alive\r\n\r\nerror\r\n")
            await self.desconecta(cliente)
            
    async def envio_a_clientes(self,mensaje):
        if len(self.clientes)>0:
            mensajeenv= self.encoder(self.enviarws(mensaje,self.encriptado))
            await self.envio_global(self.encoder(self.enviarws(mensaje,self.encriptado)))
            
            
            
    async def procesa(self,cliente,mensaje):
        nombre=''
        socket=cliente[0]
        IP=cliente[1][0]
        puerto=cliente[1][1]
        esWS=cliente[2]
        if not esWS:
            data=mensaje.decode()
            lineas=data.split('\r\n')
            palabras=lineas[0].split(' ')
            host=lineas[1].split(' ')[1]
            if palabras[0]=='GET':
                if palabras[1]=='/':
                    if 'Upgrade: websocket' in mensaje:
                        await self.procesaws(cliente,lineas)
                        return
                    else:
                        nombre='index.html'
                else:#si hay nombre de pagina
                    nombre=palabras[1][1:len(palabras[1])]
                binario=False
                
                if nombre in uos.listdir('/HTML'):#si existe la pagina en el directorio HTML
                    extension= nombre.split('.')[-1]
                    if extension=='html':
                        variable='text/html'
                    elif extension=='css':
                        variable='text/css'
                    elif extension=='js':
                        variable='text/javascript'
                    elif extension=='ico':
                        variable='image/*'
                        binario=True
                    else:
                        variable='application/octet-stream'
                    nombre='/HTML/'+nombre
                    cabecera="HTTP/1.1 200 OK\r\nContent-Type: "+variable+"\r\nContent-Lenght: "+str(uos.stat(nombre)[6])+"\r\nConnection: keep-alive\r\n\r\n"
                    await self.envia(cliente,cabecera)
                    with open(nombre,'r')as f:
                        for xlin in f:
                            xline=xlin.replace('XXX.XXX.XXX.XXX',host)
                            await uasyncio.sleep(0)
                            await self.envia(cliente,xline)
                else:
                    xlin="HTTP/1.1 404 OK\r\nContent-Type: \text/html\r\nConnection: keep-alive\r\n\r\nerror\r\n"
                    await self.envia(cliente,xlin)
                await self.desconecta(cliente)
        else:#Si es ws.
            data=mensaje
            #El byte uno determina bit7=ultimo/unico parte de MENSAJE
            #los bits 6,5 y4 no se usan. Los bits 3,2,1y0 indican el modo
            #solo se utiliza normalmente 0001=texto;0010=binario;1000=cerrar conexiones
            #1001=PING, 1010=PONG
            #byte1='{0:08b}'.format(ord(data[0]))
            #El segundo byte , el bit 7 determina si el mensaje estara encriptado (debe ser que si y ser 1)
            #el resto de los bits indica el tamaño de los mensajes debera ser de menos de 125 para simplificar.
            #byte2='{0:08b}'.format(ord(data[1])
            #comprobar si bit 7 de byte0 es 1 (>=128)
            #byte0=int(ord(data[0]))
            byte0=data[0]
            byte1=data[1]
            byteop=byte0 & 15
            if byteop==1:#es texto
                pass
            elif byteop==2:#es binario
                pass
            elif byteop==8:#cerrar conexiones
                self.desconecta(cliente)
                self.enviobool=False
            elif byteop==9:#es PING
                print("recibido PING.")
            elif byteop==10:
                #es PONG
                print("Recibido PONG.")
            else:#respuesta no esperada
                pass
            if byte1>=128:#El mensaje viene encriptado
                pass
            else:#El mensaje no viene encriptado (Se debe rechazar.)
                pass
            byteop=byte1 & 127
            if byteop <= 125:#El mensaje consta de un maximo de 125 bytes
                strcrypto=data[2:6]
                msg=data[6:]
            elif byteop==126:#el tamaño lo determinan los bytes 2 y 3 (maximo 65536 bytes)
                peso=ord(data[2])*256+ord(data[3])
                strcrypto=data[4:8]
                msg=data[8:]
            elif byteop==127:#el tamaño lo determinan los siguientes 8 bytes
                msg=data[14:]
                strcrypto=data[10:14]
            result=self.encdecrypt(msg,strcrypto)
            self.si_recibe(self,cliente,result)
            if self.enviobool:
                await uasyncio.sleep(0)
                mensajeenv=self.enviarws("OK recibido correctamente.",self.encriptado)
                data=b''
                mensajeenv= self.encoder(mensajeenv)
                await self.envia(cliente,mensajeenv)
                self.enviobool=False
        
    def encdecrypt(self,cadcrypt,keycrypt):
        salida=[]
        for n in range(0,len(cadcrypt)):
            provisional=cadcrypt[n]^keycrypt[n%4]
            salida.append(chr(provisional))
        return "".join(salida)
              
    def enviarws(self,msgws=b"ok",encriptado=False):#Google crome no acepta enmascarar los envios desde servidor, pero Firefox si.
        salidaws=[]   
        salidaws.append(chr(129))#mensaje unico y de texto
        byte1 = 0
        if len(msgws)<=125:
            longitud=chr(len(msgws))
            byte1=byte1|len(msgws)
            salidaws.append(chr(byte1))
        elif len(msgws)>125:
            byte1=byte1|126
            salidaws.append(chr(byte1))
            salidaws.append(chr(len(msgws)//256))
            salidaws.append(chr(len(msgws)%256))
        if encriptado:
            byte1=byte1|128
            salidaws[1]=chr(byte1)
            clave=[0,0,0,0]
            for x in range(0,4):
                clave[x]= chr(int(urandom.getrandbits(8)))
                salidaws.append(clave[x])#key de encriptacion
            clave1=self.encoder(clave)
            salidaws.append(self.encdecrypt(self.encoder(msgws),clave1))
        else:
            salidaws.append(msgws)
        return ''.join(salidaws)
                    
    def encoder(self,cadena):
        global a
        salida=b''
        for l in cadena:
            x=ord(l)
            if x<128:
                a=(bytes(chr(x),'utf-8'))
            else:
                comando=f"global a ; a=b'\\x{hex(x)[2:]}'"
                exec(comando)
            salida += a
        return salida
            
                
            