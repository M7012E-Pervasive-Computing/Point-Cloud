
import numpy as np

class ConnectLines():
    
    @staticmethod
    def connect(lines, distance_threshold): 
        lines = ConnectLines._sortLongest(lines)  
        connected_lines = [lines.pop(0)]
        has_reversed = False
        while len(lines) > 0: 
            point = connected_lines[-1][-1]
            best_distance = np.inf
            best = None
            idx = None 
            for i, line in enumerate(lines): 
                distance = [ConnectLines._distPoints(point, x) for x in line]
                distance = [np.inf if x > distance_threshold else x for x in distance]
                if distance[0] < distance[1] and distance[0] < best_distance:
                    best_distance = distance[0]
                    best = line
                    idx = i
                elif distance[1] < best_distance:
                    best_distance = distance[1]
                    line.reverse()
                    best = line
                    idx = i
            if best is None: 
                if has_reversed:
                    connected_lines.append(lines.pop(0))
                    has_reversed = False
                else:
                    connected_lines[-1].reverse()
                    has_reversed = True
            else: 
                connected_lines[-1].extend(best)
                lines.pop(idx)
                has_reversed = False
        return connected_lines
    
    @staticmethod
    def _distPoints(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return np.sqrt((y2-y1)**2 + (x2-x1)**2) 
       
    @staticmethod         
    def _sortLongest(lines):
        sorted_lines = []
        while len(lines) > 0:
            longest = -np.inf
            best = None
            for idx, line in enumerate(lines):
                p1, p2 = line
                dist = ConnectLines._distPoints(p1, p2)
                if dist > longest:
                    longest = dist
                    best = idx
            sorted_lines.append(lines.pop(best))
        return sorted_lines