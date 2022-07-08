

class DeviceBase:
    mqtt_client = None

    home_id: str
    room_id: str
    device_id: str

    #@property
    state: dict # general object for storing state

    def __init__(self):
        self.home_id = "0"
        self.room_id = "test"
        self.device_id = "deviceBase"

    def __del__(self):
        pass # destructor

    def get_base_path(self):
        return f"/{self.home_id}/{self.room_id}/{self.device_id}/"
