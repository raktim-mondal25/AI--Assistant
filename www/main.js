$(document).ready(function () {
    

    $('.text').textillate({
        loop: true,
        sync: true,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        },
    })
});



//siri-implementation from git-hub
var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
    amplitude: 1,
    speed: 0.30,
    autostart: true,
});

//siri animation
document.addEventListener("DOMContentLoaded", () => {
  const message = document.querySelector(".siri-message");

  function animateLoop() {
    // Fade In
    message.classList.remove("animate-out");
    message.style.animation = "fadeInUp 1s ease forwards";

    // Fade Out after delay
    setTimeout(() => {
      message.classList.add("animate-out");
      message.style.animation = "fadeOutUp 1s ease forwards";

      // Repeat the loop
      setTimeout(animateLoop, 1000);
    }, 2000);
  }

  animateLoop();
});



const oval = document.querySelector("#oval");
const wave = document.querySelector("#SiriWave");
document.querySelector("#mic-button").addEventListener("click", ()=>{
    oval.classList.add("hidden");
    eel.playAssistantSound();
    wave.classList.remove("hidden");
    eel.allCommands()();
});


function doc_keyUp(e){
  if(e.key ==='j' && e.metaKey){
    eel.playAssistantSound();
    oval.classList.add("hidden");
    wave.classList.remove("hidden");
    eel.allCommands()();
  }
}
document.addEventListener('keyup',doc_keyUp,false);


function PlayAssistant(message){
  if(message.trim()!==""){
    oval.classList.add("hidden");
    wave.classList.remove("hidden");
    eel.allCommands(message);
    document.querySelector("#chatbox").value = "";
    document.querySelector("#mic-button").classList.remove("hidden");
    document.querySelector("#SendBtn").classList.add("hidden");
  }
}

function ShowHideButton(message){
  if(message.length==0){
    document.querySelector("#mic-button").classList.remove("hidden");
    document.querySelector("#SendBtn").classList.add("hidden");
  }
  else{
    document.querySelector("#mic-button").classList.add("hidden");
    document.querySelector("#SendBtn").classList.remove("hidden");
  }
}

document.querySelector("#chatbox").addEventListener("keyup", ()=>{
  const message = document.querySelector("#chatbox").value;
  ShowHideButton(message);
});
document.querySelector("#SendBtn").addEventListener("click",()=>{
  const message = document.querySelector("#chatbox").value;
  PlayAssistant(message);
});


document.querySelector("#chatbox").addEventListener("keypress", (e)=>{
  if(e.key==="Enter"){
    const message = document.querySelector("#chatbox").value;
    PlayAssistant(message);
  }
});