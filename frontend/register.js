let registerButton = document.querySelector(".registerButton");
let usernameInput = document.querySelector(".username");
let passwordInput = document.querySelector(".password");
let emailInput = document.querySelector(".email");

registerButton.addEventListener("click", async (e) => {
    e.preventDefault();

    const username = usernameInput.value.trim();
    const password = passwordInput.value;
    const email = emailInput.value.trim();

    if (!username || !password || !email) {
        alert("Please fill out all fields.");
        return;
    }

    const url = "https://todoapi-3kjr.onrender.com/register/"; // Replace with your actual endpoint
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password, email })
    };

    try {
        const res = await fetch(url, options);

        if (!res.ok) {
            const errorData = await res.json();
            alert("Registration failed: " + (errorData.detail || res.status));
            return;
        }

        const data = await res.json();
        const token = data.token;
        

        // Save token and username in local storage
        localStorage.setItem("authToken", token);
        localStorage.setItem("username", data.username);

        alert("Registration successful!");
        window.location.href = "/Todo-API-django-rest-/frontend/index.html";
    } catch (error) {
        console.error("Registration error:", error);
        alert("Something went wrong. Check console.");
    }
});

