
class CreateFaces():
    
    @staticmethod
    def lines_to_faces(heights: list, height_lines: list) -> tuple:
        """Creates faces from lines using the heights.

        Args:
            heights (list): All heights in series of [min, max].
            height_lines (list): All lines per height.

        Returns:
            tuple: all vertices as [x, y, z] and faces as list of vertex indices.
        """
        vertices = []
        faces = []
        for height_idx, lines in enumerate(height_lines, start=0):
            for line in lines:
                for line_idx in range(1, len(line)):
                    x1, y1 = line[line_idx-1]
                    x2, y2 = line[line_idx]
                    face = []
                    face_vertices = [
                        [x1, y1, heights[height_idx][1]], 
                        [x2, y2, heights[height_idx][1]], 
                        [x2, y2, heights[height_idx][0]], 
                        [x1, y1, heights[height_idx][0]]]
                    for v in face_vertices:
                        if v in vertices:
                            face.append(vertices.index(v)+1)
                        else:
                            face.append(len(vertices)+1)
                            vertices.append(v)
                    faces.append(face)
        return vertices, faces