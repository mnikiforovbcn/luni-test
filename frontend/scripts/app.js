let username = ""
let socket = null
let tg = initializeTelegram();

async function initializeApp() {
    setDefaults(tg);
    const tgUserId = document.getElementById("tgUserId").value;
    
    try {
        const response = await fetch(`https://luni-backend-mkhailluni.amvera.io/check_user?tg_user_id=${tgUserId}`, {
            method: "POST"
        });
        const data = await response.json();
        
        if (data.exists) {
            // User exists - show contact list
            username = data.username;
            document.getElementById("register_container").style.display = "none";
            document.getElementById("contact_list").style.display = "block";
            document.getElementById("chat_container").style.display = "block";
            initializeWebSocket();
        } else {
            // User doesn't exist - show registration
            document.getElementById("register_container").style.display = "block";
            document.getElementById("contact_list").style.display = "none";
            document.getElementById("chat_container").style.display = "none";
        }
    } catch (error) {
        console.error("Error checking user:", error);
        alert("Error checking user status");
    }
}

function initializeTelegram () {
    console.log("Luni Started");
    if (window.Telegram === undefined) {
        alert("Telegram WebApp is not available");
        console.error("Telegram WebApp is not available");
        return null;
    }
    let telegtam = window.Telegram.WebApp;
    return telegtam;
};

function initializeWebSocket() {
    socket = new WebSocket(`ws://luni-backend-mkhailluni.amvera.io/ws/${username}`);
    socket.onmessage = (event) => {
        const chat = document.getElementById("chat");
        chat.innerHTML += `<div>${event.data}</div>`;
    };
    socket.onclose = () => {
        console.log("WebSocket connection closed");
    };
    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };
}

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
            document.getElementById("contact_list").style.display = "block";
            document.getElementById("chat_container").style.display = "block";
            initializeWebSocket();
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
        tgUserId: document.getElementById("tgUserId").value,
        username: document.getElementById("username").value,
        age: document.getElementById("age").value,
        gender: document.getElementById("gender").value,
        tgUserName: document.getElementById("tgUserName").value
    };
    try {
        const response = await fetch("https://luni-backend-mkhailluni.amvera.io/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const data = await response.json();
            username = data.username;
            document.getElementById("register_container").style.display = "none";
            document.getElementById("contact_list").style.display = "block";
            document.getElementById("chat_container").style.display = "block";
            initializeWebSocket();
        } else {
            alert("Login failed");
        }
    } catch (error) {
        console.error("Error during login:", error);
        alert("An error occurred during login");
    }
}

function sendMessage() {
    const msg = document.getElementById("message").value;
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(msg);
        document.getElementById("message").value = "";
    } else {
        alert("WebSocket connection is not open");
    }
}
