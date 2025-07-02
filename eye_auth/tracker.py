import zmq
import msgpack

class EyeTracker:
    def __init__(self, ip:str, port:int):
        
        self.ip = ip
        self.port = port
        self.connected = False
        self.ctx = zmq.Context()
        self.pupil_remote = self.ctx.socket(zmq.REQ)




    def connect(self):
        """
        Connect to the eye tracker.
        """

        print(f"Connecting to eye tracker at {self.ip}:{self.port}...")

        try:
            self.pupil_remote.connect(f"tcp://{self.ip}:{self.port}")
            self.pupil_remote.send_string('SUB_PORT')
            self.sub_port = self.pupil_remote.recv_string()
            self.subscriber = self.ctx.socket(zmq.SUB)
            self.subscriber.connect(f'tcp://{self.ip}:{self.sub_port}')
            self.connected = True
            print("Connected successfully.")
        except zmq.ZMQError as e:
            print(f"Failed to connect to eye tracker: {e}")
            self.connected = False
            return
        
    def disconnect(self):
        """
        Disconnect from the eye tracker.
        """
        
        if self.connected:
            print("Disconnecting from eye tracker...")
            self.pupil_remote.close()
            self.ctx.term()
            self.connected = False
            print("Disconnected successfully.")
        else:
            print("Not connected to any eye tracker.")

    def subscribe(self, topic:str):
        """
        Subscribe to a specific topic from the eye tracker.
        """

        if not self.connected:
            print("Not connected to the eye tracker.")
            return
        
        try:
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, f'{topic}')
            print(f"Subscribed to {topic}")
        except zmq.ZMQError as e:
            print(f"Failed to subscribe to {topic}: {e}")



    def collectData(self, surface_name:str, confidence_threshold:float=0.9):
        """
        Collect data from the subscribed topic.
        """

        if not self.connected:
            print("Not connected to the eye tracker.")
            return
        
        if not hasattr(self, 'subscriber'):
            print("No subscription found. Please subscribe first.")
            return
        
        recording = False
        self.blink_start = None
        
        try:
            gaze_positions = []
            print("Collecting in progress... Press Ctrl+C to stop")
            while True:
                topic, payload = self.subscriber.recv_multipart()
                message = msgpack.loads(payload, raw=False)
                print(topic)

                if topic == b'surfaces.Surface 1' and recording:
                    print("ok")
                    if message.get('name') != surface_name:
                        continue

                    for gaze in message.get('gaze_on_surfaces', []):
                        if gaze['on_surf'] and gaze['confidence'] >= confidence_threshold:
                            x, y = gaze['norm_pos']
                            timestamp = gaze['timestamp']
                            gaze_positions.append((x, y, timestamp))

                

                # Dans la callback :
                if topic == b'blinks':
                    blink_type = message.get('type')
                    timestamp = message.get('timestamp')
                    

                    if blink_type == 'onset':
                        self.blink_start = timestamp
                    elif blink_type == 'offset' and self.blink_start is not None:
                        blink_duration = timestamp - self.blink_start
                        self.blink_start = None
                        if blink_duration > 0.4:
                            recording = not recording
                            if(not recording):
                                raise BlinkException()

        except BlinkException:
            return gaze_positions
        except zmq.ZMQError as e:
            print(f"Error while collecting data: {e}")
            return None
  
class BlinkException(Exception):
    """Exception levée quand un clignement est trop court pour être valide."""
    def __init__(self):
        message = f"Blink detected."
        super().__init__(message)