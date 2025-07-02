from frechetdist import frdist
import numpy as np

class Comparator:
    """
    A class to compare two gaze trajectory.
    """

    def __init__(self, gaze1, gaze2):
        self.gaze1 = gaze1
        self.gaze2 = gaze2

    def resample_path(self, path, n_points=100):
        """
        Ré-échantillonne un chemin en n_points équidistants
        """

        if len(path) < 2:
            return path

        path = np.array(path)
        distances = np.sqrt(np.sum(np.diff(path, axis=0) ** 2, axis=1))
        cumulative = np.insert(np.cumsum(distances), 0, 0)
        total_length = cumulative[-1]
        new_distances = np.linspace(0, total_length, n_points)
        new_path = []

        for d in new_distances:
            idx = np.searchsorted(cumulative, d)
            if idx >= len(path):
                idx = len(path) - 1
            new_path.append(path[idx])
        return new_path

    def to_similarity_percent(self, distance, max_threshold):
        """
        Transforme une distance en % de ressemblance (entre 0% et 100%)
        """
        return max(0.0, 1.0 - distance / max_threshold) * 100
    
    def compare(self):
        """
        Compare the two gaze trajectories.
        """
        path1 = [(x, y) for x, y, t in self.gaze1]
        path2 = [(x, y) for x, y, t in self.gaze2]

        path1_rs = self.resample_path(path1, n_points=100)
        path2_rs = self.resample_path(path2, n_points=100)

        # Frechet
        frechet_distance = frdist(path1_rs, path2_rs)
        frechet_similarity = self.to_similarity_percent(frechet_distance, max_threshold=0.5)
        return frechet_similarity

