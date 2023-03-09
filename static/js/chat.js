function sendMessage() {
    // get message text
    let message = document.getElementsByClassName('message-input')[0].value;
    if (message != ''){
        var messageTemplate = document.getElementsByClassName('card')[0];
        var newChat = messageTemplate.cloneNode(true);
        
        newChat.classList.remove("visually-hidden")

        var chatWindow = document.getElementsByClassName('container')[0];
        
        // set message content
        newChat.querySelector('div.card-body > blockquote > p').innerText = message
        // append new message to list
        chatWindow.append(newChat);
    }
  }