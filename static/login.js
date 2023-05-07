const login_form = document.getElementById("login");
const register_form = document.getElementById("register");

const login_password = document.getElementById("login_password");
const register_password = document.getElementById("register_password");

const login_error = document.getElementById("login_error");
const register_error = document.getElementById("register_error");

function submit(form, url, error_status, error_text)
{
    error_text.textContent = "";

    const form_data = new FormData(form);
    fetch(url, {
        method: "POST",
        redirect: "follow",
        body: form_data
    }).then(response =>
    {
        if(response.status == error_status)
        {
            return response.json();
        } else if (response.redirected)
        {
            window.location.href = "/";
        }
    }).then(data =>
    {
        error_text.textContent = data.message;
    });
}

login_password.onkeydown = (e) =>
{
    if(e.key == "Enter")
    {
        submit(login_form, "login", 401, login_error);
        login_form.reset();
    }
};

register_password.onkeydown = (e) =>
{
    if(e.key == "Enter")
    {
        submit(register_form, "register", 409, register_error);
        register_form.reset();
    }
};