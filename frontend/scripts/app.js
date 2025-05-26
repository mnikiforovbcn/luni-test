let username = ""
let socket = null
let tg = initializeTelegram();
setDefaults(tg);

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

function setDefaults(tg) {
    console.log("Setup values");
    let tgUserName = tg?.initDataUnsafe?.user?.username ?? "";
    let tgUserId = tg?.initDataUnsafe?.user?.id ?? "";
    console.log("Username: " + tgUserName);
    console.log("UserId: " + tgUserId);
    document.getElementById("tgUserId").value = tgUserId;
    document.getElementById("tgUserName").value = tgUserName;
    // let sCloseBtn1 = document.getElementsByClassName("exit-btn")[0];
    // sCloseBtn1.addEventListener("click", () => {
    //     tg.close();
    // });
}

async function register() {
    const formData = {
        username: document.getElementById("username").value,
        age: document.getElementById("age").value,
        gender: document.getElementById("gender").value,
        tgUserId: document.getElementById("tgUserId").value,
        tgUserName: document.getElementById("tgUserName").value
    };
    try {
        const response = await fetch("https://luni-backend-mkhailluni.amvera.io/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const data = await response.json();
            username = formData.username;
            document.getElementById("register_container").style.display = "none";
            document.getElementById("chat_container").style.display = "block";
            socket = new WebSocket(`ws://luni-backend-mkhailluni.amvera.io/ws/${username}`);
            socket.onmessage = (event) => {
                const chat = document.getElementById("chat");
                chat.innerHTML += `<div>${event.data}</div>`;
            };
        } else {
            alert("Registration failed");
        }
    } catch (error) {
        console.error("Error during registration:", error);
        alert("An error occurred during registration");
    }
}

async function login() {
    const formData = {
        username: document.getElementById("username").value,
        age: document.getElementById("age").value,
        gender: document.getElementById("gender").value,
        tgUserId: document.getElementById("tgUserId").value,
        tgUserName: document.getElementById("tgUserName").value
    };
    await fetch("https://luni-backend-mkhailluni.amvera.io/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData)
    })
    alert("Logged in!")
    socket = new WebSocket(`ws://luni-backend-mkhailluni.amvera.io/ws/${username}`)
    socket.onmessage = (event) => {
        const chat = document.getElementById("chat")
        chat.innerHTML += `<div>${event.data}</div>`
    }
}

function sendMessage() {
    const msg = document.getElementById("message").value
    socket.send(msg)
}