import os
import aescpp
import csv



class Crypt:
    """
    A class to handle encryption and decryption of data.
    """
    @staticmethod
    def load_gaze_csv(file_path):
        """
        Charge un fichier CSV contenant x, y, timestamp
        """
        
        points = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row['x'])
                y = float(row['y'])
                t = float(row['timestamp'])
                points.append((x, y, t))
        return points

    @staticmethod
    def encrypt(user: str):
        """
        Encrypts the user pattern file.
        """

        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "..", "userData", f"{user}.csv") 

        file = aescpp.File(file_path,file_path)
        key = aescpp.Key("9f3c7e1a54b82d6e0c1f4a9b3d6e7c1f")
        iv = aescpp.IV(aescpp.Utils.generateRandomIV())
        padding = aescpp.Padding(aescpp.Padding.PKcs7)
        file.encode(key, aescpp.ChainingMethod.GCM, iv, padding)


    @staticmethod
    def decrypt(user: str) -> str:
        """
        Decrypts the user pattern file.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "..", "userData", f"{user}.csv") 

        file = aescpp.File(file_path,file_path)
        key = aescpp.Key("9f3c7e1a54b82d6e0c1f4a9b3d6e7c1f")
        file.decode(key)

        return Crypt.load_gaze_csv(file_path)