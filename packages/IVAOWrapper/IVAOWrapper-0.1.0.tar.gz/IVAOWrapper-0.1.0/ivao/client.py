import datetime


class Client:

    def __init__(self, callsign, vid, client_type, latitude, longitude, altitude, server, connection_time, soft_name,
                 soft_version, admin_rating, client_rating):
        """
        Create a client connection object
        :param callsign: User's Callsign
        :param vid: User's VID
        :param client_type: PILOT, ATC or FOLLOW ME
        :param latitude: User's Latitude coordinates
        :param longitude: User's Longitude coordinates
        :param altitude: User's Altitude
        :param server: Server where the client is connected
        :param connection_time: Time when Client connected
        :param soft_name:  User's software name
        :param soft_version:  User's software version
        :param admin_rating:  User's Staff Rank
        :param client_rating:  User's Type Rank
        """
        self.callsign = callsign
        self.vid = int(vid)
        self.client_type = client_type
        self.latitude = latitude
        self.longitude = longitude
        if altitude != '':
            self.altitude = int(altitude)
        else:
            self.altitude = 0
        self.server = server
        self.connection_time = datetime.datetime(year=int(connection_time[:4]), month=int(connection_time[4:6]),
                                                 day=int(connection_time[6:8]), hour=int(connection_time[8:10]),
                                                 minute=int(connection_time[10:12]), second=int(connection_time[12:14]))
        self.soft_name = soft_name
        self.soft_version = soft_version
        self.admin_rating = int(admin_rating)
        self.client_rating = int(client_rating)

    def __str__(self):
        return "{} : {}({}) as {} on {} since {}.".format( self.get_admin_rating_name(), self.callsign, self.vid, self.client_type, self.server,
                                                             self.connection_time)

    def get_admin_rating_name(self):
        """
        Get the name of the rank of the client on the network
        :return: str
        """
        return {
            0: "Suspended",
            1: "Observer",
            2: "User",
            11: "Supervisor",
            12: "Administrator",
        }.get(self.admin_rating, None)
