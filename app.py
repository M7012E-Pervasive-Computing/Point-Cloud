
from Import.ImportSession import ImportSession as Import
from Export.ExportObj import ExportObj as Export

from PostProcessing.ProcessByInput import ProcessByInput

from Helper.Input import Input

class App():
    
    
    def __init__(self) -> None:
        """App main functionality."""
        session_names = Import.names()
        session_name = App._select_session(session_names=session_names)
        points = Import.points(session_name=session_name)
        vertices, faces = ProcessByInput.apply_post_input_processing(points=points)
        Export.faces(filename=input("filename?\n> "), vertices=vertices, faces=faces)
        
    @staticmethod
    def _select_session(session_names: list) -> str:
        """Generate a string for all session names and let user pick a session.

        Args:
            session_names (list): str of all session names.

        Returns:
            str: str of picked session.
        """
        sessions_str = 'Pick a session:\n> '
        for i, session in enumerate(session_names):
            sessions_str += f"[{i}] {session}\n"
        session_idx = Input.get_int_input(len(session_names)-1, sessions_str)
        return session_names[session_idx]  
        
App()