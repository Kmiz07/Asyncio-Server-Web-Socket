import uasyncio
import network
import servsock
from machine import Pin
red = 'xxxxxxxxxx'
clave = 'xxxxxxxxx'
mensaje_completo = b''
estado_led=1
flash=Pin(0,Pin.IN)
led=Pin(2,Pin.OUT)
led.value(1)
final=False
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
        
async def si_recibe(objeto,cliente,mensaje):
    global estado_led, final
    #objeto= para acceder a todas las funciones del objeto ejemplo: objeto.finaliza()
    #cliente= lista con datos del cliente[socket,IP,puerto,¿es winsocket?(normalmente sera True)]
    #mensaje=mensaje recibido
#     print(f"recibido: '{mensaje}' de IP: [{cliente[1][0]}]")
    if mensaje == 'led':
        if estado_led==0:
            estado_led=1
        else:
            estado_led=0
    if mensaje== 'WS Conectado':
        uasyncio.create_task(objeto.envio_a_cliente(cliente,f'Flash={flash.value()}'))
        uasyncio.create_task(objeto.envio_a_cliente(cliente,f'led={led.value()}'))
    if mensaje == 'apaga':
        await objeto.finaliza()
    if mensaje== 'FIN':
        final=True
        
async def inicio():
    global tamaño_bufer,final
    global estado_led
    estado_flash=1
    flash=Pin(0,Pin.IN)
    estado_flash=1
    led=Pin(2,Pin.OUT)
    led.value(1)
    servidor=servsock.Servsock(si_recibe,80,-1,False)#funcion de retorno,puerto,tamaño bufer(-1, todo el mensaje),mensajes encriptados(si se encriptan los mensajes chrome no funcionara correctamente)
    while not final:
        if flash.value() != estado_flash:
            uasyncio.create_task(servidor.envio_a_clientes(f'Flash={flash.value()}'))
            estado_flash=flash.value()
            await uasyncio.sleep(0)
        if led.value() != estado_led:
            led.value(estado_led)
            uasyncio.create_task(servidor.envio_a_clientes(f'led={led.value()}'))
        await uasyncio.sleep(0)
uasyncio.run(inicio())