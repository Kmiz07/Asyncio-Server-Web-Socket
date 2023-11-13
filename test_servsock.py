import uasyncio
import network
import servsock
red = 'xxxxxxxx'
clave = 'xxxxxxxx'

mensaje_completo = b''

def conecta_wifi():
            wifi = network.WLAN(network.STA_IF)
            wifi.active(True)
            wifi.connect(red, clave)
        
            while wifi.isconnected() == False:
                pass
        
            print('Conectada a Wifi')
            print('************************')
            print('RED:     %s' % red)
            print('IP:      %s\nSUBNET:  %s\nGATEWAY: %s\nDNS:     %s' % wifi.ifconfig()[0:4])
            a = wifi.config('mac')
            print('MAC:     {:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(a[0],a[1],a[2],a[3],a[4]))
            print('************************+')
conecta_wifi()

def si_conecta(conexion,direccion):
    print(f'id socket= {id(conexion)}\nDireccion={direccion}')
    
def si_desconecta(conexion):
    print(f'\nsocket id={id(conexion[0])} DESCONECTADO')
        
def si_recibe(objeto,cliente,mensaje,tambuf):
    global mensaje_completo
    print(f'Mensaje recibido en socket id= {id(cliente[0])}\ncon direccion={cliente[1][0]}; Puerto={cliente[1][1]}\n\nMensaje:\n{mensaje}')
    mensaje_completo = mensaje_completo + mensaje
    if len(mensaje)<tambuf or tambuf==-1:#mensaje completado
        lineas_de_mensaje = mensaje_completo.decode().split('\r\n')
        print(lineas_de_mensaje[0])
        
        objeto.envia(cliente[0],mensaje_completo)
        objeto.desconecta(cliente[0])
        mensaje_completo=b''
def si_error(conexion,error):
    print(f'error {error} en socket id {id(conexion[0])}.')
async def inicio():
    global tamaño_bufer
    servidor=servsock.Servsock(si_conecta,si_desconecta,si_recibe,si_error,80,-1)
    while True:
        await uasyncio.sleep(10)
#         print('.',end='')
uasyncio.run(inicio())
