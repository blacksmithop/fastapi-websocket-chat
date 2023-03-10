let username = sessionStorage.getItem("username");

// Websocket logic
var ws = new WebSocket("ws://192.168.100.190/ws");

// ws event logic
ws.onmessage = function (event) {
  data = JSON.parse(event.data);

  console.log(data);

  if (data.hasOwnProperty('message')) {
    addNewMessage(data);
  }
};

addNewMessage = (data) => {
  message = data.message;
  username = data.username;

  var messageTemplate = document.getElementsByClassName("card")[0];
  var newChat = messageTemplate.cloneNode(true);

  newChat.classList.remove("visually-hidden");

  var chatWindow = document.getElementsByClassName("container")[0];

  // set username
  newChat.querySelector("div.card-header > span").innerText = `    ${username}`;
  // set message content
  newChat.querySelector("div.card-body > blockquote > p").innerText = message;
  // set timestamp
  newChat.querySelector("div.card-body > blockquote > footer").innerText =
    getTimestamp();
  // append new message to list
  chatWindow.append(newChat);
};

// timestamp generator
getTimestamp = () => {
  var now = new moment();
  return now.format("HH:mm:ss");
};

function sendMessage() {
  // get message text
  let message = document.getElementsByClassName("message-input")[0].value;
  if (message != "") {
    // send to websocket
    ws.send(JSON.stringify({ message: message, username: username }));
  }
}


// toasts
// let toastElList = document.querySelectorAll('.toast');
// let toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl, option));

// function welcomeToast() {
//   toastList.forEach(toast => toast.show());
// }
