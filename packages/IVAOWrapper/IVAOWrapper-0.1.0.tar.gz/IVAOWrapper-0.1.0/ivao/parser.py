import requests
from .atc import Controller
from .client import Client
from .pilot import Pilot


class Parser:

    def __init__(self):
        """
        Getting latest whazzup file, and selecting only clients
        """
        request = requests.get("http://api.ivao.aero/getdata/whazzup/whazzup.txt")
        self.content = str(request.text)
        self.clients = self.content.split('!CLIENTS\n')[1].split('!AIRPORTS')[0].split('\n')[:-1]

    def get_raw_data(self):
        """
        Return raw whazzup file
        :return: str
        """
        return self.content

    def get_clients_object(self):
        """
        Parsing all data
        :return: dict
        """
        folme = []
        atc = []
        pilot = []
        for client in self.clients:
            data = client.split(':')  # Splitting by ":" to get an array of params
            if len(data) == 49:  # Checking if correct length of data, to prevent errors
                if data[3] == "ATC":  # If client is connected as ATC
                    if data[18] == '0' and len(data) == 47:  # Observer without atis
                        user = Controller(callsign=data[0], vid=data[1], latitude=data[5], longitude=data[6],
                                          server=data[14],
                                          connection_time=data[35], soft_name=data[36], soft_version=data[37],
                                          admin_rating=data[38], client_rating=data[39], frequencies=data[4],
                                          facility=data[18],
                                          visual_range=data[19], atis="", atis_time="")
                    else:
                        user = Controller(callsign=data[0], vid=data[1], latitude=data[5], longitude=data[6],
                                          server=data[14],
                                          connection_time=data[37], soft_name=data[38], soft_version=data[39],
                                          admin_rating=data[40], client_rating=data[41], frequencies=data[4],
                                          facility=data[18],
                                          visual_range=data[19], atis=data[35], atis_time=data[36])
                    atc.append(user)
                elif data[3] == 'PILOT':  # If client is connected as Pilot
                    user = Pilot(callsign=data[0], vid=data[1], latitude=data[5], longitude=data[6], altitude=data[7],
                                 server=data[14], connection_time=data[37], soft_name=data[38], soft_version=data[39],
                                 admin_rating=data[40], client_rating=data[41], groundspeed=data[8], aircraft=data[9],
                                 cruise_speed=data[10], departure_airport=data[11], cruise_level=data[12],
                                 destination_airport=data[13], transponder=data[17], flight_rule=data[21],
                                 departure_time=data[22], actual_departure_time=data[23], alternate_airport=data[28],
                                 fpl_remark=data[29], route=data[30], flight_type=data[43], passengers=data[44],
                                 heading=data[45], ground=data[46], simulator=data[47])
                    pilot.append(user)
                else:  # If client is connected as Follow Me
                    user = Client(callsign=data[0], vid=data[1], latitude=data[5], longitude=data[6], altitude=data[7],
                                  server=data[14], connection_time=data[37], soft_name=data[38], soft_version=data[39],
                                  admin_rating=data[40], client_rating=data[41], client_type=data[3])
                    folme.append(user)

        return {'folme': folme, "atc": atc, "pilot": pilot}
