import cherrypy
from paste.translogger import TransLogger
from app import create_app


def run_server(app):
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 55555,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


@cherrypy.expose
def shutdown(self):
    cherrypy.engine.exit()


if __name__ == "__main__":
    # dataset_path = os.path.join('datasets', 'ml-latest')
    app = create_app()

    # start web server
    run_server(app)
