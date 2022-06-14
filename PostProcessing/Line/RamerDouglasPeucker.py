import numpy as np
from numpy import linalg as npl
from math import atan2, degrees, pi
from rdp import rdp

class RamerDouglasPeucker():
    
    @staticmethod
    def rdp(line, epsilon=0.5):
        return rdp(line, epsilon)
    
    @staticmethod
    def rdp_angle(line, dist_threshold, angle_multiplier):
        length = len(line)
        while length >= 3:
            largestDiff = -np.inf
            idx = None
            for i in range(1, length):
                A = np.array(line[(i-1) % length])
                B = np.array(line[i])
                C = np.array(line[(i+1) % length])
                
                angle = RamerDouglasPeucker._points_angle(A, B, C)
                dist = RamerDouglasPeucker._point_line_distance(A, B, C)      
                dist = (dist * angle_multiplier) if angle >= 60 else dist
    
            
                if dist < dist_threshold: 
                    diff = dist_threshold - dist
                    if diff > largestDiff:
                        largestDiff = diff
                        idx = i
                        
            if idx is None: 
                return line
            else:
                line.pop(idx)
                length -= 1
        return line 
    
    @staticmethod
    def _points_angle(A, B, C):
        Ax, Ay = A[0]-B[0], A[1]-B[1]
        Cx, Cy = C[0]-B[0], C[1]-B[1]
        a = atan2(Ay, Ax)
        c = atan2(Cy, Cx)
        a += pi*2 if a < 0 else 0 
        c += pi*2 if c < 0 else 0
        angle = (pi*2 + c - a) if a > c else (c - a)
        return degrees(angle)
      
    @staticmethod  
    def _point_line_distance(A, B, C):
        return npl.norm(np.cross(C-A, A-B))/npl.norm(C-A)