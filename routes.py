from flask import Blueprint, render_template


bp = Blueprint("routes", __name__)


def init_app(app):
    app.register_blueprint(bp)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/<group>/<generator>")
def group_room(group, generator):
  return render_template("room.html", group=group, generator=generator)
