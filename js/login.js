const login_form = document.getElementById("logins")
const pre = document.getElementById("inf")

login_form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const form_data = new FormData(event.target);
    const data = new URLSearchParams(form_data)

    try {
        console.log("error")
        const response = await fetch("https://fictional-space-computing-machine-7g4r447j9jxcx9xv-8000.app.github.dev/login", {
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