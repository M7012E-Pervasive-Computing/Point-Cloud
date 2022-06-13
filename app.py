
from Import.ImportSession import ImportSession as Import

class App():
    
    def __init__(self) -> None:
        session_names = Import.session_names()
        session_name = self._select_session(session_names=session_names)
        points = Import.session_points(session_name=session_name)
        
    def _select_session(self, session_names: list) -> str:
            sessions_str = 'Pick a session:\n'
            for i, session in enumerate(session_names):
                sessions_str += f"[{i}] {session}\n"
            session_idx = self._get_int_input(len(session_names)-1, sessions_str)
            return session_names[session_idx]        

    @staticmethod
    def _get_int_input(max: int, print_str: str = '') -> int: 
        result = 0
        while True:
            try:
                result = int(input(print_str))
                if result > max or result < 0: 
                    print('Not a valid index')
                    continue
                break
            except ValueError:
                print('Not a valid input')
        return result

App()