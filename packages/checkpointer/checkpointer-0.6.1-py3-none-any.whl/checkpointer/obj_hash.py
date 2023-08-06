import inspect
from pprint import pprint
import dis
from termcolor import colored
from relib import hashing
import builtins
from .simple_memoize import simple_memoize
from functools import reduce
from collections import namedtuple
from .utils import pickles, unwrap_func, abs_to_rel_path, is_local_file

CodeSummary = namedtuple('CodeSummary', ['file_name', 'instructions', 'children', 'hash'])

debug = False

def debug_print(*args):
  if debug:
    print(*args)

def get_attr_list(instructions):
  for i in range(1, len(instructions)):
    if instructions[i].opname != 'LOAD_ATTR':
      break
  return [inst.argval for inst in instructions[:i]]

def get_val(attr_list, code_globals):
  fst_attr, *rest_attrs = attr_list
  if fst_attr in code_globals:
    val = code_globals[fst_attr]
  elif hasattr(builtins, fst_attr):
    # builtins is even more global than code_globals
    val = getattr(builtins, fst_attr)
  else:
    # this shouldn't happen in a runnable function
    return None
  for attr in rest_attrs:
    val = getattr(val, attr)
  return val

def make_substitute_instruct(state, inst, values, indent_str=''):
  val = [inst.opcode, inst.arg, inst.offset, *values]
  debug_print(indent_str, colored(inst.opname, 'grey'), colored(val, 'grey'))
  return state._replace(instructions=state.instructions + [val])

@simple_memoize(lambda code, *args, **kwargs: code)
def inspect_instructions(code, file_name, code_globals, circular=[], indent=0):
  indent_str = '  ' * indent
  source, start_line = inspect.getsourcelines(code)
  debug_print(indent_str, colored(str(code), 'red'))
  instructions = list(dis.get_instructions(code))

  def reducer(state, i):
    inst = instructions[i]
    if inst.starts_line != None:
      code_line_index = inst.starts_line - start_line
      code_line = source[code_line_index].strip() if code_line_index < len(source) else 'code unknown'
      debug_print(indent_str, colored(code_line, 'yellow'))

    # Closure
    if inst.opname == 'LOAD_CONST' and inspect.iscode(inst.argval):
      child_state = inspect_instructions(inst.argval, file_name, code_globals, circular=circular, indent=indent + 1)
      state = make_substitute_instruct(state, inst, ['child_code', child_state.hash], indent_str=indent_str)
      return state._replace(children=state.children + child_state.children)

    elif inst.opname in ['LOAD_NAME', 'LOAD_GLOBAL']:
      attr_list = get_attr_list(instructions[i:])
      val = get_val(attr_list, code_globals)
      if id(val) in map(id, circular):
        return make_substitute_instruct(state, inst, ['circular', attr_list], indent_str=indent_str)
      elif inspect.isfunction(val):
        val = unwrap_func(val)
        func_file = inspect.getfile(val)
        if is_local_file(func_file):
          child_state = get_function_summary(val, circular=circular, indent=indent)
          state = make_substitute_instruct(state, inst, ['global_code', child_state.hash], indent_str=indent_str)
          return state._replace(children=state.children + [child_state])
      elif not inspect.isbuiltin(val) and pickles(val):
        return make_substitute_instruct(state, inst, ['evaluated_argval', val], indent_str=indent_str)

    # LOAD_DEREF is proceeded by some other instruction and thus handled in some cases already. It might be preferably handled like LOAD_GLOBAL.
    # LOAD_ATTR is proceeded by LOAD_GLOBAL or LOAD_DEREF and thus handled already.

    # Catch all instructions
    return make_substitute_instruct(state, inst, [inst.argval], indent_str=indent_str)

  state = reduce(reducer, range(len(instructions)), CodeSummary(
    file_name=file_name,
    instructions=[],
    children=[],
    hash=None,
  ))

  hash = hashing.hash(state.instructions)

  return state._replace(hash=hash)

def get_function_summary(func, circular=[], indent=-1):
  return inspect_instructions(
    func.__code__,
    abs_to_rel_path(inspect.getfile(func)),
    func.__globals__,
    circular=circular + [func],
    indent=indent + 1,
  )

def get_module_summary(module, circular=[], indent=-1):
  return inspect_instructions(
    module.__loader__.get_code(module.__loader__.name),
    abs_to_rel_path(inspect.getfile(module)),
    vars(module),
    circular=circular, # + [module],
    indent=indent + 1,
  )

def get_summary(val):
  if inspect.isfunction(val):
    return get_function_summary(val)
  else:
    return get_module_summary(val)

def get_obj_hash(val):
  return get_summary(val).hash

def get_dependency_map(code_summary, state={}):
  self = code_summary.file_name
  for child in code_summary.children:
    state[child.file_name] = state.get(child.file_name, [])
    if self != child.file_name and self not in state[child.file_name]:
      state[child.file_name].append(self)
    get_dependency_map(child, state)
  return state
