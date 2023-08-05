from .client import Client


class Controller(Client):

    def __init__(self, callsign, vid, latitude, longitude, server, connection_time, soft_name, soft_version,
                 admin_rating, client_rating, frequencies, facility, visual_range, atis, atis_time):
        """
        Create a Controller Object from string parsed in the Whazzup file, so all data is considered as a string
        :param callsign: Callsign of the controller (LFBD_TWR)
        :param vid: Client's VID (485573)
        :param latitude: Latitude of the center of the control zone
        :param longitude: Longitude of the center of the control zone
        :param server: Server to which the client is connected (EU7)
        :param connection_time: Date and time, the client connected to the server
        :param soft_name: Name of the software used by the client
        :param soft_version: Version of the software used by the client
        :param admin_rating: Administrative rating
        :param client_rating: ATC rank
        :param frequencies: The frequencies the client is currently using
        :param facility: The facility provided by the ATC.
        :param visual_range: The range of the ATC radar.
        :param atis: The ATIS set by the controller.
        :param atis_time: The time the ATIS was defined.

        """
        super().__init__(callsign=callsign, vid=vid, client_type="ATC", latitude=latitude, longitude=longitude,
                         altitude=0, server=server, connection_time=connection_time,
                         soft_name=soft_name, soft_version=soft_version, admin_rating=admin_rating,
                         client_rating=client_rating)
        self.frequencies = frequencies.split("&")
        self.facility = int(facility)
        self.visual_range = float(visual_range)
        self.atis = atis
        self.atis_time = atis_time

    def get_facility_name(self):
        """
        Get the name of the position opnened by the client on the network
        :return: str
        """
        return {
            0: "Observer",
            1: "Flight Information",
            2: "Delivery",
            3: "Ground",
            4: "Tower",
            5: "Approach",
            6: "Area Control Centre",
            7: "Departure"
        }.get(self.facility, None)

    def get_client_rating_name(self):
        """
        Get the name of the ATC rank of the client on the network
        :return: str
        """
        return {
            1: "Observer",
            2: "ATC Applicant (AS1)",
            3: "ATC Trainee (AS2)",
            4: "Advanced ATC Trainee (AS3)",
            5: "Aerodrome Controller (ADC)",
            6: "Approach Controller (APC)",
            7: "Center Controller (ACC)",
            8: "Senior Controller (SEC)",
            9: "Senior ATC Instructor (SAI)",
            10: "Chief ATC Instructor (CAI)"
        }.get(self.client_rating, None)
