import logging

class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' in logrecord.__dict__
class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' not in logrecord.__dict__

logcfg = { 'version': 1,
           'formatters': {
               'normal': {'format': '%(levelname)-8s %(message)s'},
               'actor': {'format': '%(levelname)-8s %(actorAddress)s => %(message)s'}},
           'filters': { 'isActorLog': { '()': actorLogFilter},
                        'notActorLog': { '()': notActorLogFilter}},
           'handlers': { 'h1': {'class': 'logging.StreamHandler',
                                'stream': 'ext://sys.stdout',
                                'formatter': 'normal',
                                'filters': ['notActorLog'],
                                'level': logging.DEBUG},
                         'h2': {'class': 'logging.StreamHandler',
                                'stream': 'ext://sys.stdout',
                                'formatter': 'actor',
                                'filters': ['isActorLog'],
                                'level': logging.DEBUG},},
           'loggers' : { '': {'handlers': ['h1', 'h2'], 'level': logging.DEBUG}}
         }