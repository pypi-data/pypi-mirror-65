let endpoint = window.location.protocol + "//" + window.location.hostname;
window.socket = io(endpoint);
window.socketConnected = true;
window.overlayDisconnectionDisable = false; 

window.socket.on("disconnect", () => {
  window.socketConnected = false;
  console.log("disconnected at: ", new Date().toString());
  window.timeoutSocketConnectionLost = setTimeout(function() {
    if(!window.overlayDisconnectionDisable){
    document.getElementsByClassName("global-overlay")[0].style.display =
      "initial";
    }
  }, 1500);
});

window.socket.on("reconnect", attemptNumber => {
  window.socketConnected = true;
  clearTimeout(window.timeoutSocketConnectionLost);
  document.getElementsByClassName("global-overlay")[0].style.display = "none";
});

window.socket.on("hello", (text) => {
console.log(text);
str = text.replace(/\r\n|\n|\r/gm, '<br />');
document.getElementById("output_text_area").innerHTML = str;
});


window.onload= function(){
document.getElementById("run").addEventListener('click', async () => {
    var textToSave = myCodeMirror.getValue();
    var encodedString = window.btoa(unescape(encodeURIComponent(textToSave)));
    window.socket.emit('zumi_run', encodedString);
    if(window.outputLoop){
      return;
    }
    window.outputLoop = true;
    window.socket.emit('check_output');    
    setInterval(
        function() {
        window.socket.emit('check_output');
        }.bind(this),
    3000
    );
    //window.socket.emit("send_file", textToSave);
}); 

document.getElementById("stop").addEventListener('click', async () => {
    console.log("sending stop");
    window.socket.emit("stop");
}); 



}

