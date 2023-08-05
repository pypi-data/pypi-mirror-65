from .client import Client


class Pilot(Client):

    def __init__(self, callsign, vid, latitude, longitude, altitude, server, connection_time, soft_name, soft_version,
                 admin_rating, client_rating, groundspeed, aircraft, cruise_speed, departure_airport, cruise_level,
                 destination_airport, transponder, flight_rule, departure_time, actual_departure_time,
                 alternate_airport, fpl_remark, route, flight_type, passengers, heading, ground, simulator):
        """
        Create a Pilot Object from string parsed in the Whazzup file, so all data is considered as a string
        :param callsign: Callsign of the controller (LFBD_TWR)
        :param vid: Client's VID (485573)
        :param latitude: Latitude of the center of the control zone
        :param longitude: Longitude of the center of the control zone
        :param altitude: Altitude of ther center of the control zone
        :param server: Server to which the client is connected (EU7)
        :param connection_time: Date and time, the client connected to the server
        :param soft_name: Name of the software used by the client
        :param soft_version: Version of the software used by the client
        :param admin_rating: Administrative rating
        :param client_rating: Pilot rank
        :param groundspeed: The groundspeed of the pilot.
        :param aircraft: 	According to ICAO flightplan specifications. (1/C172/L-CS/C)
        :param cruise_speed: According to ICAO flightplan specifications.
        :param departure_airport: According to ICAO flightplan specifications.
        :param cruise_level: According to ICAO flightplan specifications.
        :param destination_airport: According to ICAO flightplan specifications.
        :param transponder: The transponder code set by the pilot.
        :param flight_rule: According to ICAO flightplan specifications.
        :param departure_time: According to ICAO flightplan specifications.
        :param actual_departure_time: The actual departure time.
        :param alternate_airport: According to ICAO flightplan specifications.
        :param fpl_remark: According to ICAO flightplan specifications.
        :param route: According to ICAO flightplan specifications.
        :param flight_type: According to ICAO flightplan specifications.
        :param passengers: According to ICAO flightplan specifications.
        :param heading: The heading of the plane.
        :param ground: A flag indicating if the plane is on ground or not.
        :param simulator: The simulator used by the pilot.
        """
        super().__init__(callsign=callsign, vid=vid, client_type="PILOT", latitude=latitude, longitude=longitude,
                         altitude=altitude, server=server, connection_time=connection_time,
                         soft_name=soft_name, soft_version=soft_version, admin_rating=admin_rating,
                         client_rating=client_rating)
        self.destination_airport = destination_airport
        self.simulator = int(simulator)
        if ground == "1":
            self.ground = True
        else:
            self.ground = False
        self.heading = int(heading)
        if passengers != '':
            self.passengers = int(passengers)
        else:
            self.passengers = 0
        self.flight_type = flight_type
        if groundspeed != '':
            self.groundspeed = int(groundspeed)
        else:
            self.groundspeed = 0
        self.aircraft = aircraft
        self.cruise_speed = cruise_speed
        self.atis = departure_airport
        self.atis_time = cruise_level
        self.transponder = int(transponder)
        self.flight_rule = flight_rule
        self.departure_time = departure_time
        self.actual_departure_time = actual_departure_time
        self.alternate_airport = alternate_airport
        self.fpl_remark = fpl_remark
        self.route = route

    def get_simulator_name(self):
        """
        Get the name of the simulator used by the pilot
        :return: str
        """
        return {
            0: "Unknown",
            1: "Microsoft Flight Simulator 95",
            2: "Microsoft Flight Simulator 98",
            3: "Microsoft Combat Flight Simulator",
            4: "Microsoft Flight Simulator 2000",
            5: "Microsoft Combat Flight Simulator 2",
            6: "Microsoft Flight Simulator 2002",
            7: "Microsoft Combat Flight Simulator 3",
            8: "Microsoft Flight Simulator 2004",
            9: "Microsoft Flight Simulator X",
            11: "X-Plane",
            12: "X-Plane 8",
            13: "X-Plane 9",
            14: "X-Plane 10",
            15: "PS1",
            16: "X-Plane 11",
            17: "X-Plane 12",  # Really???
            20: "Fly!",
            21: "Fly! 2",
            25: "Prepar3D",
            30: "Prepar3D 1.x"
        }.get(self.simulator, 'Unknown')

    def get_client_rating_name(self):
        """
        Get the name of the pilot rank on the network
        :return: str
        """
        return {
            1: "Observer",
            2: "Basic Flight Student (FS1)",
            3: "Flight Student (FS2)",
            4: "Advanced Flight Student (FS3)",
            5: "Private Pilot (PP)",
            6: "Senior Private Pilot (SPP)",
            7: "Commercial Pilot (CP)",
            8: "Airline Transport Pilot (ATP)",
            9: "Senior Flight Instructor (SFI)",
            10: "Chief Flight Instructor (CFI)"
        }.get(self.client_rating, None)
