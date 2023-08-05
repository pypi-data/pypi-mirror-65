from dane_server.server import app, cfg
import gunicorn.app.base
from gunicorn.six import iteritems

class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def main():
    options = {
        'bind': '%s:%s' % (cfg.DANE.HOST, cfg.DANE.PORT),
        'workers': 4, # TODO should make this configable probably
    }
    print('Launching DANE-server on {}:{}'.format(cfg.DANE.HOST, cfg.DANE.PORT))
    StandaloneApplication(app, options).run()

if __name__ == '__main__':
    main()
