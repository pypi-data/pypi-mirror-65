from Variables.configs import *
from Variables.main_vars import *
from Resources.Passenger.Api import Api
from Resources.Driver.DriverApi import DriverApi
from Resources.Driver.DriverDatabase import DriverDatabase


class worker():
    passenger_api = Api()
    driver_api = DriverApi()
    driver_db = DriverDatabase()

    def __init__(self, passenger_cellphone=passenger_cellphone, driver_cellphone=eco_username):
        self.passenger_cellphone = passenger_cellphone
        self.driver_cellphone = driver_cellphone
        self.passenger_token = self.passenger_api.get_passenger_token_with_otp_from_api(passenger_cellphone)
        self.driver_token = self.driver_api.get_driver_token(cellphone=driver_cellphone)
        self.ride_id = None
        self.origin_lat = regular_lat
        self.origin_lng = regular_lng
        self.destination_lat = regular_lat_dest
        self.destination_lng = regular_lng_dest


    def create_ride(self, origin_lat=None, origin_lng=None,
                    destination_lat=None, service_type=1,
                    destination_lng=None,
                    extra_destination_lat=0, extra_destination_lng=0, waiting=0,
                    round_trip=False, voucher_code=0, state='Accepted'):
        origin_lat = origin_lat or self.origin_lat
        origin_lng = origin_lng or self.origin_lng
        destination_lat = destination_lat or self.destination_lat
        destination_lng = destination_lng or self.destination_lng
        self.driver_db.change_driver_ride_status(status='available', cellphone=self.driver_cellphone)
        if state == 'Waiting':
            res = self.passenger_api.get_price_and_request_ride_from_api(token=self.passenger_token, origin_lat=origin_lat,
                                                                   origin_lng=origin_lng,
                                                                   destination_lat=destination_lat,
                                                                   destination_lng=destination_lng,
                                                                   service_type=service_type,
                                                                   extra_destination_lat=extra_destination_lat,
                                                                   extra_destination_lng=extra_destination_lng,
                                                                   waiting=waiting, round_trip=round_trip,
                                                                   voucher_code=voucher_code)
            #res = self.driver_api.check_ride_receive_from_api(token=self.driver_token, lat=regular_lat, lng=regular_lng)
            self.ride_id = res['ride_id']
        if state == 'Accepted':
            self.passenger_api.get_price_and_request_ride_from_api(token=self.passenger_token, origin_lat=origin_lat,
                                                                   origin_lng=origin_lng,
                                                                   destination_lat=destination_lat,
                                                                   destination_lng=destination_lng,
                                                                   service_type=service_type,
                                                                   extra_destination_lat=extra_destination_lat,
                                                                   extra_destination_lng=extra_destination_lng,
                                                                   waiting=waiting, round_trip=round_trip,
                                                                   voucher_code=voucher_code)
            res = self.driver_api.check_ride_receive_from_api(token=self.driver_token, lat=regular_lat, lng=regular_lng)
            self.ride_id = res
            self.driver_api.driver_accept_ride_from_api(token=self.driver_token, ride_id=res)
        if state == 'Arrived':
            self.passenger_api.get_price_and_request_ride_from_api(token=self.passenger_token, origin_lat=origin_lat,
                                                                   origin_lng=origin_lng,
                                                                   destination_lat=destination_lat,
                                                                   destination_lng=destination_lng,
                                                                   service_type=service_type,
                                                                   extra_destination_lat=extra_destination_lat,
                                                                   extra_destination_lng=extra_destination_lng,
                                                                   waiting=waiting, round_trip=round_trip,
                                                                   voucher_code=voucher_code)
            res = self.driver_api.check_ride_receive_from_api(token=self.driver_token, lat=regular_lat, lng=regular_lng)
            self.ride_id = res
            self.driver_api.driver_accept_ride_from_api(token=self.driver_token, ride_id=res)
            self.driver_api.driver_arrived_to_passenger_ride_from_api(token=self.driver_token, ride_id=res)
        if state == 'Boarded':
            self.passenger_api.get_price_and_request_ride_from_api(token=self.passenger_token, origin_lat=origin_lat,
                                                                   origin_lng=origin_lng,
                                                                   destination_lat=destination_lat,
                                                                   destination_lng=destination_lng,
                                                                   service_type=service_type,
                                                                   extra_destination_lat=extra_destination_lat,
                                                                   extra_destination_lng=extra_destination_lng,
                                                                   waiting=waiting, round_trip=round_trip,
                                                                   voucher_code=voucher_code)
            res = self.driver_api.check_ride_receive_from_api(token=self.driver_token, lat=regular_lat, lng=regular_lng)
            self.ride_id = res
            self.driver_api.driver_accept_ride_from_api(token=self.driver_token, ride_id=res)
            self.driver_api.driver_arrived_to_passenger_ride_from_api(token=self.driver_token, ride_id=res)
            self.driver_api.passenger_boarded_in_driver_car_from_api(token=self.driver_token, ride_id=res)
        if state == 'Finished':
            self.passenger_api.get_price_and_request_ride_from_api(token=self.passenger_token, origin_lat=origin_lat,
                                                                   origin_lng=origin_lng,
                                                                   destination_lat=destination_lat,
                                                                   destination_lng=destination_lng,
                                                                   service_type=service_type,
                                                                   extra_destination_lat=extra_destination_lat,
                                                                   extra_destination_lng=extra_destination_lng,
                                                                   waiting=waiting, round_trip=round_trip,
                                                                   voucher_code=voucher_code)
            self.driver_api.driver_get_and_finish_ride_from_api(token=self.driver_token, lat=regular_lat,
                                                                lng=regular_lng,
                                                                round_trip=False,
                                                                sec_dest=0)

    def add_ride_option(self, extra_destination_lat=None, extra_destination_lng=None,
                        round_trip=False, waiting=0):
        self.passenger_api.add_ride_option_in_ride(token=self.passenger_token, ride_id=self.ride_id,
                                                   extra_destination_lat=extra_destination_lat,
                                                   extra_destination_lng=extra_destination_lng, round_trip=round_trip,
                                                   waiting=waiting)

    def add_voucher_in_ride(self, voucher='snapp'):
        self.passenger_api.add_voucher_from_api(token=self.passenger_token, ride_id=self.ride_id, voucher=voucher)

    def driver_finish_ride_from_boarded_state(self):
        self.driver_api.driver_finish_ride_from_api(token=self.driver_token, ride_id=self.ride_id)
