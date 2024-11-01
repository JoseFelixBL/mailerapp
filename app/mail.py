from flask import (
    Blueprint
)

bp = Blueprint('mail', __name__, url_prefix="/")


@bp.route('/', methods=['GET'])
def index():
    return 'chanchito super feliz'
