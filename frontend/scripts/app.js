const API_BASE_URL = "https://luni-backend-mkhailluni.amvera.io/";
let username = ""
let socket = null
let tg = initializeTelegram();

async function initializeApp() {
    setDefaults(tg);
    const tgUserId = document.getElementById("tgUserId").value;
    
    initializeFormValidation();
    
    const userExists = await checkUserExists(tgUserId);
    
    updateUI(userExists, data?.username);
}

function initializeFormValidation() {
    const createAccountBtn = document.getElementById("create_account");
    createAccountBtn.disabled = true;
    createAccountBtn.style.opacity = 0.5;
    
    const formFields = [
        document.getElementById("username"),
        document.getElementById("age"),
        document.getElementById("gender")
    ];
    
    formFields.forEach(field => {
        field.addEventListener('input', checkFormValidity);
    });
    
    // Initial check
    checkFormValidity();
}

async function checkUserExists(tgUserId) {
    try {
        const response = await fetch(`${API_BASE_URL}check_user?tg_user_id=${tgUserId}`, {
            method: "POST"
        });
        const data = await response.json();
        return data.exists;
    } catch (error) {
        console.error("Error checking user:", error);
        alert("Error checking user status");
        return false;
    }
}

function updateUI(userExists, username = null) {
    if (userExists) {
        // User exists - show contact list
        username = username;
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
    socket = new WebSocket(`ws://${API_BASE_URL.replace("https://", "")}ws/${username}`);
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
    let tgUserName = tg?.initDataUnsafe?.user?.username ?? "Test";
    let tgUserId = tg?.initDataUnsafe?.user?.id ?? "0";
    let tgUserFirstName = tg?.initDataUnsafe?.user?.first_name ?? "Test";
    let tgUserLastName = tg?.initDataUnsafe?.user?.last_name ?? "";

    console.log("Username: " + tgUserName);
    console.log("UserId: " + tgUserId);
    console.log("UserFirstName: " + tgUserFirstName);
    
    // Set username as first name + last name
    const fullName = (tgUserFirstName + " " + tgUserLastName).trim();
    if (fullName) {
        document.getElementById("username").value = fullName;
    }
    
    document.getElementById("tgUserId").value = tgUserId;
    document.getElementById("tgUserName").value = tgUserName;
}

function checkFormValidity() {
    const username = document.getElementById("username").value.trim();
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const createAccountBtn = document.getElementById("create_account");
    
    const isValid = username && age && gender;
    createAccountBtn.disabled = !isValid;
    createAccountBtn.style.opacity = isValid ? 1 : 0.5;
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
        const response = await fetch(`${API_BASE_URL}register`, {
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
        const response = await fetch(`${API_BASE_URL}login`, {
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

async function sendMessage() {
    const msg = document.getElementById("message").value.trim();
    if (!msg) return; // Don't send empty messages

    if (socket && socket.readyState === WebSocket.OPEN) {
        try {
            // Send to WebSocket
            socket.send(msg);
            
            // Save to backend
            await fetch(`${API_BASE_URL}save_message`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    username: username,
                    message: msg,
                    tgUserId: document.getElementById("tgUserId").value
                })
            });
            
            // Clear input
            document.getElementById("message").value = "";
        } catch (error) {
            console.error("Error saving message:", error);
            alert("Failed to save message");
        }
    } else {
        alert("WebSocket connection is not open");
    }
}
