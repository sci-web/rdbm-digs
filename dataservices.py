import time, sys


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        q = kw.get('query', method.__name__)
        action = "%s().%s" % (q.im_class.__name__, q.__name__)
        print action
        print '%s`s time of %s : %2.2f s' % (method.__name__, action, (te - ts))
        return result
    return timed


@timeit
def query_execution(**kwargs):
  if kwargs['sql'] != "":
    try:
      # print kwargs['query'], kwargs['sql'], kwargs['pattern']
      # print kwargs['query'](kwargs['sql'], kwargs['pattern'])
      method = kwargs['query'](kwargs['sql'], kwargs['pattern'])
    except Exception, e1:
      try:
        method = kwargs['query'](kwargs['sql'])
      except Exception, e2:
        print "1. Error in", e1, "\n2.", kwargs['sql'], e2, "(check config.py)"
        # sys.exit(1)
  else:
    kwargs['query']()
  return method
