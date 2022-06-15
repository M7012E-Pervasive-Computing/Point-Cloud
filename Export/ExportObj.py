
class ExportObj():
    
    @staticmethod
    def faces(filename, vertices, faces) -> None:
        file = open(f'Models/{filename}.obj', 'w')
        for v in vertices:
            file.write(f'v {v[0]} {v[1]} {v[2]} 1.0\n')
        for f in faces:
            file.write(f'f {f[0]} {f[1]} {f[2]} {f[3]}\n')
        file.close()
        
    @staticmethod
    def faces_vertices(filename, vertices, faces) -> None:
        ExportObj.faces(filename=filename, vertices=vertices, faces=faces)
        file = open(f'Models/{filename}_v.obj', 'w')
        for v in vertices:
            file.write(f'v {v[0]} {v[1]} {v[2]} 1.0\n')
        file.close() 