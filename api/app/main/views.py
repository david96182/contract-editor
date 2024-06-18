from . import main

@main.route('/ping', methods=['GET'])
def index():
    return 'pong!'
