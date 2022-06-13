class Store():
    def storeRoom(self, vertices, faces):
        name = input('Enter file name: ')
        file = open(f'{name}.obj', 'w')
        for v in vertices:
            file.write(f'v {v[0]} {v[1]} {v[2]} 1.0\n')
        for f in faces:
            file.write(f'f {f[0]} {f[1]} {f[2]} {f[3]}\n')
        file.close()