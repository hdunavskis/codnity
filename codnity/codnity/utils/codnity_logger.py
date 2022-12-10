from functools import wraps


class Logger:

    def __init__(self, logger):
        self.logger = logger

    def __call__(self, fn):
        @wraps(fn)
        def log(*args, **kwargs):
            self.logger.info('Starting %s with params = %s, %s',
            fn.__name__, str(args), str(kwargs))
            try:
                results = fn(*args, **kwargs)
                self.logger.info('Finished %s with params = %s, %s',
                fn.__name__, str(args), str(kwargs))
                return results
            except Exception as ex:
                self.logger.error('Error in function %s, %s', fn.__name__, ex)
                raise Exception from ex
        return log
