let namespace = '/';
let url = location.protocol + '//' + document.domain + ':' + location.port + namespace;
let room_url = "";
let socket = io.connect(url);

let group_generators_p = document.getElementById("group-generators");

function NewValue(){
    let group = document.getElementById("group").value;
    socket.emit("handle_group", parseInt(group));
};

function GroupButton()
{
    let username = document.getElementById("username").value;
    let group = document.getElementById("group").value;
    let generator = document.getElementById("generator").value;
    let data_to_send = {"username": username, "group": parseInt(group), "generator": parseInt(generator)};
    socket.emit("handle_gg", data_to_send);
    window.location.href = url + group + "/" + generator;
};

socket.on("return_group", generators =>
{
    group_generators_p.innerHTML = "Group generators: " + generators
});