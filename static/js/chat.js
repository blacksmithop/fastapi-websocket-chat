let username = sessionStorage.getItem('username');

function sendMessage() {
  // get message text
  let message = document.getElementsByClassName("message-input")[0].value;
  if (message != "") {
    var messageTemplate = document.getElementsByClassName("card")[0];
    var newChat = messageTemplate.cloneNode(true);

    newChat.classList.remove("visually-hidden");

    var chatWindow = document.getElementsByClassName("container")[0];

    // set username
    newChat.querySelector("div.card-header > span").innerText = `    ${username}`;
    // set message content
    newChat.querySelector("div.card-body > blockquote > p").innerText = message;
    // set timestamp
    newChat.querySelector("div.card-body > blockquote > footer").innerText = getTimestamp();
    // append new message to list
    chatWindow.append(newChat);
  }
}



getTimestamp = () => {
    var now = new moment();
    return now.format("HH:mm:ss");  
}