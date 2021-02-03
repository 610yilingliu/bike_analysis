import datetime

class single_bike:
    """
    Contains single bike data
    :type bike_id: string
    :type ordered_time: List[string], time ordered by calendar and clock
    :type time_pos: Dict{String: Tuple}, key is the time, tuple is (latitude, longitude)
    """
    def __init__(self, bike_id):
        self.bike_id = bike_id
        self.ordered_times = []
        self.time_pos = dict()
    
    def order_time(self):
        """
        order self.ordered_time by calendar and clock
        """
        def get_list(date):
            return datetime.datetime.strptime(date,"%Y/%m/%d %H:%M:%S").timestamp()
        self.ordered_times = sorted(self.order_times, key = lambda t: get_list(t))

    def insert_data(self, data):
        """
        type data: Tuple or List, format: (time, latitude, longitude)
        """
        t, la, lo = data
        self.ordered_times.append(t)
        self.time_pos[t] = (la, lo)