const messages = document.getElementById("messages");
const chatbox = document.getElementById("chatbox");

function create_message_element(message)
{
    const id = message[0];
    const time = message[1];
    const username = message[2];
    const content = message[3];

    const element = document.createElement("p");
    const msg = document.createTextNode(username + " - " + time + ": " + content);
    msg.id = "msg_" + id;
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