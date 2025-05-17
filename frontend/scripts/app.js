let username = ""
let socket = null
let tg = initializeTelegram();
setButtons();
let tgUserName = tg.initDataUnsafe.user.username;

function initializeTelegram () {
    console.log("Luni Started");
    if (window.Telegram === undefined) {
        alert("Telegram WebApp is not available");
        console.error("Telegram WebApp is not available");
        return null;
    }
    let telegtam = window.Telegram.WebApp;
    return telegtam
};

function setButtons() {
    console.log("Setup Buttons");
    let sCloseBtn1 = document.getElementsByClassName("exit-btn")[0];
    sCloseBtn1.addEventListener("click", () => {
        tg.close();
    });
}

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