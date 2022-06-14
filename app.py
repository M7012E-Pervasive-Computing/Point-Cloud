
from Import.ImportSession import ImportSession as Import
from Export.ExportObj import ExportObj as Export

from PostProcessing.ProcessByInput import ProcessByInput

from Helper.Input import Input

class App():
    
    
    def __init__(self) -> None:
        session_names = Import.names()
        session_name = App._select_session(session_names=session_names)
        points = Import.points(session_name=session_name)
        pcd = ProcessByInput._createPointCloud(points)
        pcd = ProcessByInput._denoise(pcd)
        pcd = ProcessByInput._cluster(pcd)
        
        
    @staticmethod
    def _select_session(session_names: list) -> str:
            sessions_str = 'Pick a session:\n'
            for i, session in enumerate(session_names):
                sessions_str += f"[{i}] {session}\n"
            session_idx = Input.get_int_input(len(session_names)-1, sessions_str)
            return session_names[session_idx]  

App()