//Displaying speak message
eel.expose(DisplayMessage);

function DisplayMessage(message) {
    const msg = document.querySelector(".siri-message");
    if (msg) {
        msg.textContent = message;
        msg.classList.remove("animate");
        void msg.offsetWidth; 
        msg.classList.add("animate");
    }
}




//Showing the main frame after delivering the message
eel.expose(Showhood);

function Showhood() {
    const oval = document.getElementById("oval");
    const SiriWave = document.getElementById("SiriWave");

    if (oval) oval.style.display = "block";
    if (SiriWave) SiriWave.hidden = true;
}



// the text sent by us
eel.expose(senderText)
function senderText(message){
    var chatBox = document.getElementById("chat-canvas-body");
    if(message.trim() !== ""){
        chatBox.innerHTML+=`<div class="row justify-content-end mb-4">
        <div class="width-size>
        <div class="sender_message">${message}</div>
        </div>`;

        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// The text sent by the virtual assistant
eel.expose(receiverText)
function receiverText(message){ 
    var chatBox = document.getElementById("chat-canvas-body");
    if(message.trim()!==""){
        chatBox.innerHTML+=`<div class="row justify-content-end mb-4">
        <div class="width-size>
        <div class="receiver_message">${message}</div>
        </div></div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}










// // Hide Loader and display Face Auth animation
// // Hide Loader and display Face Auth animation
// eel.expose(hideLoader);
// function hideLoader(){
//     document.querySelector("#Loader").classList.add("hidden");
//     document.querySelector("#FaceAuth").classList.remove("hidden");
// };



// // Hide Face Auth and display Face Auth success animation
// eel.expose(hideFaceAuth);
// function hideFaceAuth(){
//     document.querySelector("#FaceAuth").classList.add("hidden");
//     document.querySelector("#FaceAuthSuccess").classList.remove("hidden");
// };



// // Hide success and display greeting
// eel.expose(hideFaceAuthSuccess);
// function hideFaceAuthSuccess(){
//     document.querySelector("#FaceAuthSuccess").classList.add("hidden");
//     document.querySelector("#HelloGreet").classList.remove("hidden");
// };



// // Hide Start Page and display blob animation
// eel.expose(hideStart);
// function hideStart(){
//     document.querySelector("#Start").classList.add("hidden");

//     setTimeout(() => {
//         document.querySelector("#oval").classList.add("animate__animated", "animate__zoomIn");
//     }, 1000);

//     setTimeout(() => {
//         document.querySelector("#oval").classList.remove("hidden");
//     }, 1000);
// };
