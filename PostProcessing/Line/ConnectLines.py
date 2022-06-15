
import numpy as np

class ConnectLines():
    
    @staticmethod
    def connect(lines: list, distance_threshold: float) -> list: 
        """Connects lines within distance_threshold.

        Args:
            lines (list): All lines where a line is a series of [x, y].
            distance_threshold (float): The maximum distance can have to another.

        Returns:
            list: List of lines where the lines have connected if possible. 
        """
        lines = ConnectLines.__sort_longest(lines)  
        connected_lines = [lines.pop(0)]
        has_reversed = False
        while len(lines) > 0: 
            point = connected_lines[-1][-1]
            best_distance = np.inf
            best = None
            idx = None 
            for i, line in enumerate(lines): 
                distance = [ConnectLines.__distance_points(point, x) for x in line]
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
    def __distance_points(p1: list, p2: list) -> float:
        """Distance between two points.

        Args:
            p1 (list): Point in form [x, y].
            p2 (list): Point in form [x, y].

        Returns:
            float: Distance between p1 and p2.
        """
        x1, y1 = p1
        x2, y2 = p2
        return np.sqrt((y2-y1)**2 + (x2-x1)**2) 
       
    @staticmethod         
    def __sort_longest(lines: list) -> list:
        """Sort list of lines for line distance.

        Args:
            lines (list): All lines as series of [x, y].

        Returns:
            list: lines sorted from longest to shortest.
        """
        sorted_lines = []
        while len(lines) > 0:
            longest = -np.inf
            best = None
            for idx, line in enumerate(lines):
                p1, p2 = line
                dist = ConnectLines.__distance_points(p1, p2)
                if dist > longest:
                    longest = dist
                    best = idx
            sorted_lines.append(lines.pop(best))
        return sorted_lines