class Store():
    def storeRoom(self, vertices, faces):
        name = input("Enter file name: ")
        f = open(name + ".obj", "w")
        for i in range(len(vertices)):
            f.write("v " + str(vertices[i][0]) + " " + str(vertices[i][1]) + " " + str(vertices[i][2]) + " 1.0" + "\n")
        for i in range(len(faces)):
            f.write("f ")
            for j in range(len(faces[i])):
                f.write(str(faces[i][j]) + " ")
            f.write("\n")
        f.close()