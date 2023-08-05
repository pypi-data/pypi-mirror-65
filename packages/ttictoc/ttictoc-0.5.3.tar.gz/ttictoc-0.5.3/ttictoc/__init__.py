from .tictoc import Timer,tic,toc,tic2,toc2

def __get_version():
  import json
  with open('ttictoc/version.json') as f:
    version = json.load(f)['version']
  return version

__version__ = __get_version()
