const login_form = document.getElementById("logins")
const pre = document.getElementById("inf")

login_form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const form_data = new FormData(event.target);
    const data = new URLSearchParams(form_data)

    try {
        console.log("error")
        const response = await fetch("https://crispy-chainsaw-vx7g77p7x4q34vg-8000.app.github.dev/token", {
            "method": "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: data.toString()
        });

        if (response.ok) {
            const result = await response.json();
            pre.textContent = `Logged in. Token: ${result.access_token}`;
        } else {
           pre.textContent = 'Login failed';
        }
        
    } catch (error) {
        console.error("Error ", error);
        pre.textContent = `Error ${error}`;
    }
});