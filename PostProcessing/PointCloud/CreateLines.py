
import numpy as np
import warnings
import matplotlib.pyplot as plt

class CreateLines():
    
    @staticmethod
    def point_clouds_to_lines(point_clouds: list, debug=False) -> list:
        """Converts list of point cloud points into separate lines. 

        Args:
            point_clouds (list): [[[x,y,z], ...], ...].
            debug (bool, optional): Debug visualization. Defaults to False.

        Returns:
            list: All lines as a series of [x, y].
        """
        warnings.simplefilter('ignore', np.RankWarning)
        lines = []
        for point_cloud in point_clouds:
            x, y = [], []
            x1 = np.inf
            x2 = -np.inf
            for i in range(len(point_cloud)):
                if point_cloud[i] == []:
                    continue
                val_x, val_y, _ = point_cloud[i]
                x.append(val_x)
                y.append(val_y)
                x1 = val_x if val_x < x1 else x1
                x2 = val_x if val_x > x2 else x2
                
            if (len(x) == 0 or len(y) == 0):
                continue
            x = np.array(x)
            y = np.array(y)
            a, b = np.polyfit(x,y,1)
            
            y1 = a*x1 + b
            y2 = a*x2 + b
            
            if debug:
                plt.plot(x, y, 'o')
                plt.plot(x, (a*x + b))
            lines.append([[x1, y1], [x2, y2]])
        if debug:
            plt.show()
        return lines