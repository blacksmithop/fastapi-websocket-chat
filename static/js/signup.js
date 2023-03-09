saveUsername = () => {
    username = document.getElementsByClassName('form-control')[0].value;
    if (username == ''){
        username = `user${makeUser(5)};`
    }
    sessionStorage.setItem('username', username);
}


function makeUser(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}