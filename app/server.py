from app.wsgi import application
import os

import cherrypy

server_config = {
    'global': {
        'server.socket_host': '0.0.0.0', 
        'server.socket_port': 8000, 
        'server.thread_pool': 30, 
        'server.max_request_body_size': 10485760, # Limit body size to 10M in bytes
        'server.max_request_header_size': 512000, # Limit header size to 512K in bytes
        'server.socket_timeout': 300, 
        'log.screen': True,
        'log.error_file': '/tmp/myapp.error.log',
        'log.access_file': '/tmp/myapp.access.log',
    }
}

if __name__ == '__main__':
    cherrypy.server.unsubscribe()
    development = os.environ.get("development", 0)
    if development == 0: 
        server_config["global"]["environment"] = 'production'
    cherrypy.config.update(server_config)
    cherrypy.tree.graft(application, '/')
    cherrypy.server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()