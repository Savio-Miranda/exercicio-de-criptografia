from criptosystems import Group
from flask import current_app
from flask_socketio import emit



def _handle_group(group_order):
    current_app.group = Group(group_order, "*")
    generators = current_app.group.generators
    emit("return_group", generators)


def _handle_gg(data):
    username = data["username"]
    group = data["group"]
    generator = data["generator"]
    gg = f"{group}_{generator}"
    if gg in current_app.gg:
        current_app.gg[gg][username] = current_app.group._random_exponent()
        return
    current_app.gg = {gg: {username: current_app.group._random_exponent()}}


def get_creator_gg(data):
    group = data["group"]
    generator = data["generator"]
    gg = f"{group}_{generator}"
    username = list(current_app.gg[gg].keys())[0]
    sk = current_app.gg[gg][username] # secret key
    pk = (generator ** sk) % group # public key
    data_to_send = {"username": username, "group": group, "generator": generator, "Sk": sk, "Pk": pk}
    print(data_to_send)
    emit("send_gg", data_to_send)


events_to_register = [
            ("handle_group", _handle_group),
            ("handle_gg", _handle_gg),
            ("get_creator_gg", get_creator_gg)
            ]