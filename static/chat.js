const messages = document.getElementById("messages");
const chatbox = document.getElementById("chatbox");

let remaining = false;
let oldest_message_id = -1;

function create_message_element(message)
{
    const id = message[0];
    const time = message[1];
    const username = message[2];
    const content = message[3];

    let div = document.createElement("div");
    div.setAttribute("id", "msg_" + id);
    div.setAttribute("class", "chatmessage");

    let meta = document.createElement("span");
    meta.textContent = username + " - " + time + ": ";
    meta.setAttribute("class", "message_meta");
    let main = document.createElement("span");
    main.textContent = content;
    main.setAttribute("class", "content");

    div.appendChild(meta);
    div.appendChild(main);
    return div;
}

function append_data(data)
{
    const frag = document.createDocumentFragment();
    for(const message of data.messages)
    {
        let elem = create_message_element(message);
        frag.appendChild(elem);
    }
    if(data.old)
    {
        messages.append(frag);
        remaining = data.remaining;
        if(data.messages.length > 0)
        {
            oldest_message_id = data.messages[data.messages.length - 1][0]
        }
    } else
    {
        messages.prepend(frag);
    }
}

const socket = io();

socket.on("messages", (data) => {
    append_data(data);
});

socket.on("status", (users) => {
    for(const user of users)
    {
        let elem = document.getElementById("u_" + user.id);
        elem.style.color = user.online ? "green" : "gray";
    }
});

socket.on("error", (message) => {
    alert(message);
});

chatbox.onkeydown = (e) =>
{
    if(e.key === "Enter")
    {
        if(chatbox.value)
        {
            socket.emit("msg", chatbox.value);
            chatbox.value = "";
        }
    }
};

window.onbeforeunload = () =>
{
    socket.disconnect(true);
};

window.onscroll = (e) =>
{
    if((window.innerHeight + Math.round(window.scrollY)) >= document.body.scrollHeight)
    {
        if(remaining)
        {
            socket.emit("load_messages", oldest_message_id);
        }
    }
};