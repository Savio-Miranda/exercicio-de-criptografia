let namespace = '/';
let url = location.protocol + '//' + document.domain + ':' + location.port + namespace;
let socket = io.connect(url);

let username_input = document.getElementById("username");
let group_generator = document.getElementById("group-generator");
let private_key = document.getElementById("private-key");


socket.on("send_gg", data =>{
    let username = data["username"]
    let group = data["group"]
    let generator = data["generator"]
    let sk = data["Sk"]
    let pk = data["Pk"] // esperando
    username_input.innerHTML = "Username: " + username
    group_generator.innerHTML = `Group: ${group} - Generator: ${generator}`;
    private_key.innerHTML = "Private key: " + sk
});

window.onload = () => {
    data_to_send = {"group": parseInt(group), "generator": parseInt(generator)}
    socket.emit("get_creator_gg", data_to_send);
};