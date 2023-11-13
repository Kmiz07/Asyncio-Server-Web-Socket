var wsUri = "ws://XXX.XXX.XXX.XXX";//Nombre+Puerto del servidor
var output;

function init() {
output = document.getElementById("panel");
cliWebSocket();
boton = document.getElementById("flash");
led = document.getElementById("led");
}
function pulsado(){
    doSend("led");
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
    //writeToScreen("CONNECTED");
    output.innerHTML="Conectado";
    doSend("WS Conectado");
}

function onClose(evt) {
    //writeToScreen("DISCONNECTED");
    output.innerHTML="Desconectado";
}

function onMessage(evt) {
    
   if(evt.data == "Flash=1"){flash.innerHTML="Flash liberado";}
   if(evt.data == "Flash=0"){flash.innerHTML="Flash pulsado";}
   if(evt.data == "led=0"){led.innerHTML="led encendido";}
   if(evt.data == "led=1"){led.innerHTML="led apagado";}
    doSend("MSG_OK");
}

function onError(evt) {
    writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data);
}

function doSend(message) {
    //writeToScreen("SENT: " + message);
    websocket.send(message);
}

function writeToScreen(message) {
    var pre = document.createElement("p");
    pre.style.wordWrap = "break-word";
    pre.innerHTML = message;
    output.appendChild(pre);
}


window.addEventListener("load", init, false);
