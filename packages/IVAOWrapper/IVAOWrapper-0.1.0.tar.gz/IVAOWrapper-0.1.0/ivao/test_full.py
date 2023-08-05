import time
import unittest

from ivao import Server, Pilot, Controller


class AllTest(unittest.TestCase):

    def setUp(self):
        self.server = Server()

    def test_parser(self):
        @self.server.event("update")  # Not working
        def update(clients):
            self.assertTrue(clients)

        self.server.update_data()

    def test_create_pilot(self):
        now = time.gmtime()
        pilot = Pilot(callsign="AFL17DT", vid="485573", latitude="00.0000", longitude="00.0000", altitude="000",
                      server="EU7", connection_time=time.strftime("%Y%m%d%H%M%S", now), soft_name="Python Test",
                      soft_version="0.1", admin_rating="2",
                      client_rating="4", groundspeed="000", aircraft="1/A321/M-SDE3FGHIRWY/LB1", cruise_speed="N240",
                      departure_airport="LFPG", cruise_level="F330", destination_airport="LFBD", transponder="1000",
                      flight_rule="I", departure_time="1500", actual_departure_time="1501", alternate_airport="LFBO",
                      fpl_remark="PBN/A1B1C1D1O1S1 DOF/190320 REG/N321SB EET/LFFF0002 LFRR0004 OPR/AFL PER/C RMK/TCAS",
                      route="AGOPA UL167 ARKIP UQ237 LMG", flight_type="S", passengers="200", heading="240", ground="1",
                      simulator="9")
        self.assertEqual(pilot.__str__(), "User : AFL17DT(485573) as PILOT on EU7 since {}.".format(
            time.strftime("%Y-%m-%d %H:%M:%S", now)))

    def test_create_controller(self):
        now = time.gmtime()
        controller = Controller(callsign="LFBB_CTR", vid="485573", latitude="00.0000", longitude="00.0000",
                                server="EU4", connection_time=time.strftime("%Y%m%d%H%M%S", now),
                                soft_name="Python Test",
                                soft_version="0.1", admin_rating="12", client_rating="5", frequencies="122.800",
                                visual_range="200", facility="6", atis="IVAO Observer  -  No Active ATC Position",
                                atis_time=time.strftime("%Y%m%d%H%M%S", now))
        self.assertEqual(controller.__str__(), "Administrator : LFBB_CTR(485573) as ATC on EU4 since {}.".format(
            time.strftime("%Y-%m-%d %H:%M:%S", now)))

    def test_handlers(self):
        @self.server.event("land")  # Not working
        def update(client):
            self.assertIsNotNone(client)

        pilot = Pilot(callsign="AFL17DT", vid="485573", latitude="00.0000", longitude="00.0000", altitude="000",
                      server="EU7", connection_time=time.strftime("%Y%m%d%H%M%S", time.gmtime()),
                      soft_name="Python Test",
                      soft_version="0.1", admin_rating="2",
                      client_rating="4", groundspeed="000", aircraft="1/A321/M-SDE3FGHIRWY/LB1", cruise_speed="N240",
                      departure_airport="LFPG", cruise_level="F330", destination_airport="LFBD", transponder="1000",
                      flight_rule="I", departure_time="1500", actual_departure_time="1501", alternate_airport="LFBO",
                      fpl_remark="PBN/A1B1C1D1O1S1 DOF/190320 REG/N321SB EET/LFFF0002 LFRR0004 OPR/AFL PER/C RMK/TCAS",
                      route="AGOPA UL167 ARKIP UQ237 LMG", flight_type="S", passengers="200", heading="240", ground="1",
                      simulator="9")
        data = {'pilot': [pilot], 'atc': [], 'folme': []}
        self.server.update_data(data)
        data['pilot'][0].ground = False
        self.server.update_data(data)
