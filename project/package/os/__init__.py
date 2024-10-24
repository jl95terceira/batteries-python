import abc
import os
import signal
import sys
import threading
import typing
import uuid

def is_this_windows():

    return sys.platform == 'win32'

TEMP_DIR = 'C:\\Temp' if is_this_windows() else '/tmp'

def get_user_env(name  :str,
                 expand:bool=False):
    
    return (os.popen(f'powershell -NoProfile -Command "(Get-Item -Path HKCU:\\Environment).GetValue(\'{name}\')"') if expand else \
            os.popen(f'powershell -NoProfile -Command "(Get-Item -Path HKCU:\\Environment).GetValue(\'{name}\', $null, \'DoNotExpandEnvironmentNames\')"')).read()

_SIGINT_HOOKS:dict[str, typing.Callable[[],None]] = dict()
def _SIGINT_MASTER_HANDLER(*aa, **kaa):

    with _SIGINT_HOOKS_LOCK:
        
        for hook in _SIGINT_HOOKS.values(): 
            
            hook()

_SIGINT_HOOKS_LOCK = threading.Lock()
signal.signal(signal.SIGINT, _SIGINT_MASTER_HANDLER)

class HookHandler(abc.ABC):

    @abc.abstractmethod
    def remove(self): pass

class _SIGINT_HOOK_HANDLER(HookHandler):

    def __init__(self, key:str): self._key = key

    @typing.override
    def remove(self):
        
        with _SIGINT_HOOKS_LOCK:

            del _SIGINT_HOOKS[self._key]

def add_sigint_hook(hook:typing.Callable[[],None]) -> HookHandler:

    with _SIGINT_HOOKS_LOCK:

        key                = uuid.uuid4()
        _SIGINT_HOOKS[key] = hook
        return _SIGINT_HOOK_HANDLER(key)

add_sigint_hook(lambda: print('--------SIGINT--------'))
