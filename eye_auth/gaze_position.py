import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.cm as cm

class GazePosition:
    def __init__(self, gaze_positions:list):
        self.gaze_positions = gaze_positions

    def deduplicate(self,threshold) -> list:
        deduped = []
        for pt in self.gaze_positions:
            if not deduped or np.linalg.norm(np.array(pt[:2]) - np.array(deduped[-1][:2])) > threshold:
                deduped.append(pt)
        return deduped
    
    def preprocess(self, threshold=0.002) -> list:
        """
        Preprocess the gaze positions.
        """

        self.gaze_positions.sort(key=lambda pt: pt[2])
        return self.deduplicate(threshold)
    
    def create_grid(n=3):
        coords = np.linspace(0, 1, n+1)
        centers = (coords[:-1] + coords[1:]) / 2
        return centers, coords
    
    def save_image(self, image_path:str):
        """
        Save the gaze positions to an image file.
        """

        x_raw = np.array([pt[0] for pt in self.gaze_positions])
        y_raw = np.array([pt[1] for pt in self.gaze_positions])
        t_raw = np.array([pt[2] for pt in self.gaze_positions])
        t_raw_norm = (t_raw - t_raw.min()) / (t_raw.max() - t_raw.min()) if len(t_raw) > 1 else np.zeros_like(t_raw)

        points_raw = np.array([x_raw, y_raw]).T.reshape(-1, 1, 2)
        segments_raw = np.concatenate([points_raw[:-1], points_raw[1:]], axis=1)

        grid_centers, grid_lines = self.create_grid(n=3)

        fig, ax = plt.subplots(figsize=(6, 6))

        for v in grid_lines:
            ax.plot([v, v], [0, 1], color='lightgray', linestyle='--', linewidth=1)
            ax.plot([0, 1], [v, v], color='lightgray', linestyle='--', linewidth=1)

        ax.plot([0, 1], [0, 1], color='lightgray', linestyle='--', linewidth=1)
        ax.plot([0, 1], [1, 0], color='lightgray', linestyle='--', linewidth=1)

        xx, yy = np.meshgrid(grid_centers, grid_centers)
        ax.scatter(xx.flatten(), yy.flatten(), color='green', s=100, marker='o', edgecolors='black', label='Centres cases')

        cmap = cm.get_cmap('coolwarm')  # palette de couleur
        colors = cmap(t_raw_norm)

        lc = LineCollection(segments_raw, colors=colors[:-1], linewidths=3, alpha=0.9)
        ax.add_collection(lc)

        scatter = ax.scatter(x_raw, y_raw, c=t_raw_norm, cmap=cmap, s=40, edgecolors='black', label='Points fixations')

        cbar = plt.colorbar(scatter, ax=ax, orientation='vertical')
        cbar.set_label('Progression temporelle')

       
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(False)
        ax.legend()

        filename = f"{image_path}/gaze_{int(time.time())}.png"
        plt.savefig(filename)
    