val_by_id = {}

def simple_memoize(get_key):
  def wrapper(func):
    def inner_wrapper(*args, **kwargs):
      arg_id = get_key(*args, **kwargs)
      if arg_id in val_by_id:
        return val_by_id[arg_id]
      else:
        val_by_id[arg_id] = func(*args, **kwargs)
        return inner_wrapper(*args, **kwargs)
    return inner_wrapper
  return wrapper
