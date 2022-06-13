
from anyio import get_running_tasks
from Log.Logging import Log
from Import.ImportSession import ImportSession as Import

class App():
    
    def __init__(self) -> None:
        session_names = Import.session_names()
        session_name = _select_session(session_names=session_names)
        points = Import.session_points(session_name=session_name)
        
@staticmethod
def _select_session(session_names: list) -> str:
        sessions_str = 'Pick a session:\n'
        for i, session in enumerate(session_names):
            sessions_str += f"[{i}] {session}\n"
        session_idx = _get_int_input(len(session_names), sessions_str)
        return session_names[session_idx]        

@staticmethod
def _get_int_input(max: int, print_str: str = '') -> int: 
    result = 0
    while True:
        try:
            result = int(input(print_str))
            if result > max or result < 1: 
                Log.warn('Not a valid index')
                continue
            break
        except ValueError:
            Log.warn('Not a valid input')
    return result

App()