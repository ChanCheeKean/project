from app import server
import os, flask

##################
# Server route
##################

@server.route('/static/<path:path>')
def embed_video(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'static'),path)
