from eye_auth.tracker import EyeTracker
from eye_auth.gaze_position import GazePosition
from eye_auth.ui import UI
from eye_auth.crypt import Crypt

SURFACE_NAME = "Surface 1"

def main():


    ui = UI()
    ui.run()

    # tracker = EyeTracker('localhost', 50020)
    # tracker.connect()
    # tracker.subscribe('surfaces')

    # gaze_positions  = tracker.collectData(SURFACE_NAME)

    # if( gaze_positions ):
    #     print(f"Collected {len(gaze_positions)} gaze positions.")
    #     gaze = GazePosition(gaze_positions)
    #     gaze.preprocess()

if __name__ == "__main__":
    main()