const messages = document.getElementById("messages");

function create_message_element(message)
{
    const element = document.createElement("p");
    const msg = document.createTextNode(message.user + " - " + message.time + ": " + message.content);
    element.appendChild(msg);
    return element;
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