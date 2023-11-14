var wsUri = "ws://XXX.XXX.XXX.XXX";//Nombre+Puerto del servidor
var output;

function init() {
output = document.getElementById("panel");
boton = document.getElementById("flash");
led = document.getElementById("led");
cliWebSocket();
}
function pulsado(){
    doSend("led");
}

function apaga(){
    doSend("apaga")
}
function cliWebSocket() {
    websocket = new WebSocket(wsUri);
    websocket.onopen = function (evt) {
        onOpen(evt)
    };
    websocket.onclose = function (evt) {
        onClose(evt)
    };
    websocket.onmessage = function (evt) {
        onMessage(evt)
    };
    websocket.onerror = function (evt) {
        onError(evt)
    };
}

function onOpen(evt) {
    output.innerHTML="Conectado";
    doSend("WS Conectado");
}

function onClose(evt) {
    output.innerHTML="Desconectado";
}

function onMessage(evt) {
   if(evt.data == "Flash=1"){flash.innerHTML="Flash liberado";}
   if(evt.data == "Flash=0"){flash.innerHTML="Flash pulsado";}
   if(evt.data == "led=0"){led.innerHTML="led encendido";}
   if(evt.data == "led=1"){led.innerHTML="led apagado";}
}

function onError(evt) {
output.innerHTML=evt.data;
}

function doSend(message) {
    websocket.send(message);
}




window.addEventListener("load", init, false);
