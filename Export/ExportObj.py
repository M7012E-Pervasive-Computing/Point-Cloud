
class ExportObj():
    
    @staticmethod
    def faces(filename: str, vertices: list, faces: list) -> None:
        """Export obj file with vertices and faces.

        Args:
            filename (str): Filename of obj file.
            vertices (list): All vertices as [x, y, z].
            faces (list): Faces as indexes of vertices; [index1, ... indexN].
        """
        file = open(f'Models/{filename}.obj', 'w')
        for v in vertices:
            file.write(f'v {v[0]} {v[1]} {v[2]} 1.0\n')
        for f in faces:
            file.write(f'f {f[0]} {f[1]} {f[2]} {f[3]}\n')
        file.close()
        
    @staticmethod
    def faces_vertices(filename: str, vertices: list, faces: list) -> None:
        """Export obj file of faces, vertices but also export 
        vertices as a separate obj file. 

        Args:
            filename (str): Filename of obj file.
            vertices (list): All vertices as [x, y, z].
            faces (list): Faces as indexes of vertices; [index1, ... indexN].
        """
        ExportObj.faces(filename=filename, vertices=vertices, faces=faces)
        file = open(f'Models/{filename}_v.obj', 'w')
        for v in vertices:
            file.write(f'v {v[0]} {v[1]} {v[2]} 1.0\n')
        file.close() 