import numpy as np
from numpy import linalg as npl
from math import atan2, degrees, pi
from rdp import rdp

class RamerDouglasPeucker():
    
    @staticmethod
    def rdp(line: list, epsilon=0.5) -> list:
        """Builtin Ramer-Douglas-Peucker.

        Args:
            line (list): Series of vertices as [x, y].
            epsilon (float, optional): Epsilon for algorithm. Defaults to 0.5.

        Returns:
            list: Reduced line.
        """
        return rdp(line, epsilon)
    
    @staticmethod
    def rdp_angle(line: list, distance_threshold: float, angle_multiplier: float) -> list:
        """Alteration of Ramer-Douglas-Peucker which takes angle into account.
        

        Args:
            line (list): Series of vertices as [x, y].
            distance_threshold (float): Distance between the line formed by adjacent vertices. 
            angle_multiplier (float): Multiplier to strengthen desired angles.

        Returns:
            list: Reduced line.
        """
        length = len(line)
        while length >= 3:
            largestDiff = -np.inf
            idx = None
            for i in range(1, length):
                A = np.array(line[(i-1) % length])
                B = np.array(line[i])
                C = np.array(line[(i+1) % length])
                
                angle = RamerDouglasPeucker.__points_angle(A, B, C)
                dist = RamerDouglasPeucker.__point_line_distance(A, B, C)      
                dist = (dist * angle_multiplier) if angle >= 60 else dist
    
            
                if dist < distance_threshold: 
                    diff = distance_threshold - dist
                    if diff > largestDiff:
                        largestDiff = diff
                        idx = i
                        
            if idx is None: 
                return line
            else:
                if not(idx == length-1 and line[0] == line[-1]):
                    line.pop(idx)
                length -= 1
        return line 
    
    @staticmethod
    def __points_angle(A: np.ndarray, B: np.ndarray, C: np.ndarray) -> float:
        """Get angle at point B.

        Args:
            A (np.ndarray): Point [x, y].
            B (np.ndarray): Point [x, y].
            C (np.ndarray): Point [x, y].

        Returns:
            float: angle at B.
        """
        Ax, Ay = A[0]-B[0], A[1]-B[1]
        Cx, Cy = C[0]-B[0], C[1]-B[1]
        a = atan2(Ay, Ax)
        c = atan2(Cy, Cx)
        a += pi*2 if a < 0 else 0 
        c += pi*2 if c < 0 else 0
        angle = (pi*2 + c - a) if a > c else (c - a)
        return degrees(angle)
      
    @staticmethod  
    def __point_line_distance(A: np.ndarray, B: np.ndarray, C: np.ndarray) -> float:
        """Get distance from point B to line formed between A and C.

        Args:
            A (np.ndarray): Point [x, y].
            B (np.ndarray): Point [x, y].
            C (np.ndarray): Point [x, y].

        Returns:
            float: Distance from B to line.
        """
        return npl.norm(np.cross(C-A, A-B))/npl.norm(C-A)