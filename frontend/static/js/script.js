document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault();

    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let message = document.getElementById("message");

    // simple validation
    if (email === "" || password === "") {
        message.style.color = "red";
        message.textContent = "Please fill all fields";
        return;
    }

    // Temporary frontend check (replace with backend later)
    if (email === "admin@gmail.com" && password === "12345") {
        message.style.color = "green";
        message.textContent = "Login Successful!";
    } else {
        message.style.color = "red";
        message.textContent = "Invalid email or password";
    }
});
