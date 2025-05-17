let username = ""
let socket = null
let tg = initializeTelegram();
let tgUserName = tg.initDataUnsafe.user.username;

let initializeTelegram = () => {
    console.log("Luni Started");
    if (window.Telegram === undefined) {
        console.error("Telegram WebApp is not available");
        return null;
    }
    return window.Telegram.WebApp;
};

async function register() {
    username = document.getElementById("username").value
    const password = document.getElementById("password").value
    await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    alert("Registered!")
}

async function login() {
    username = document.getElementById("username").value
    const password = document.getElementById("password").value
    await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    alert("Logged in!")
    socket = new WebSocket(`ws://localhost:8000/ws/${username}`)
    socket.onmessage = (event) => {
        const chat = document.getElementById("chat")
        chat.innerHTML += `<div>${event.data}</div>`
    }
}

function sendMessage() {
    const msg = document.getElementById("message").value
    socket.send(msg)
}