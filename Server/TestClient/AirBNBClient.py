import math
import time

from PROJECT.Client.Core.Client import Client
from PROJECT.Client.GUI.Map import Map
import pickle
from socket import *
import threading
from PROJECT.Client.GUI.Interface import App, Window


def from_pickle(p):
    """
    Safely tries to turn bytes into objects via pickle
    :param p: bytes to load
    :return: loaded objects or None
    """
    try:
        return pickle.loads(p)
    except (pickle.UnpicklingError, EOFError):
        return False


def to_pickle(p):
    """
    Safely tries to turn objects into bytes via pickle
    :param p: object to pickle
    :return: pickled bytes
    """
    try:
        return pickle.dumps(p)
    except pickle.UnpicklingError:
        return False


class AirBNBClient(Client):
    def __init__(self, server_ip: str = gethostbyname_ex(gethostname())[-1][-1], server_port: int = 56545,
                 encrypted: bool = False, sum_length: int = 8, server_name: str = None,
                 *args, **kwargs):
        print(gethostbyname_ex(gethostname())[-1][-1])
        self.selected_marker_pos = None
        self.purchase_window = None
        self.offers = None

        self.start_location = (31.8928, 34.8113)

        self.app_thread = threading.Thread(target=self.__setup_app)
        try: self.app_thread.start()
        except KeyboardInterrupt:
            pass

        self.client_thread = threading.Thread(target=self.__setup_client,
                                              kwargs={'server_addr': (server_ip, server_port), 'encrypted': encrypted,
                                                      'sum_length': sum_length, 'server_name': server_name})
        try: self.client_thread.start()
        except KeyboardInterrupt:
            pass

    def __create_map(self, root, preval='', *args, **kwargs):
        """
        Creates the map and adds it into the app
        updates the offers in the map
        """
        self.__map = Map(root, self.start_location, *args, **kwargs)
        self.__map.marker_click_event += self.__marker_click
        self.__map.add_right_click_menu_command(label="Add Offer", command=self.app.create_offer_frame,
                                                pass_coords=True)

        self.app.map = self.__map

        self.update_offers_in_map()

        self.to_focus = True

    def __setup_client(self, *args, **kwargs):
        """
        Creates the client object and tries to connect it to the server
        """
        super(AirBNBClient, self).__init__(*args, **kwargs)

        self.connection_interrupted_event += lambda termination_state: \
            self.app.disconnected() if self.app.active else None
        self.add_listen_event(self.__listen_for_update)

        self.connect()

        time.sleep(1)

        def check_server_connectivity(data):
            if from_pickle(data):
                self.app.start()
                return True
            return False

        self.add_listen_once_event(check_server_connectivity)

        self.send('ping')

    def __setup_app(self):
        """
        Creates the app and inserts all of the events into it
        """
        # Creates app
        self.app = App()
        self.app.on_login += self.login
        self.app.on_logout += self.logout
        self.app.on_signup += self.sign_up
        self.app.on_map_create += self.__create_map
        self.app.on_close += self.terminate_connection
        self.app.on_get_own_offers += self.get_my_offers
        self.app.on_get_own_purchases += self.get_my_purchases
        self.app.on_update_search += self.__update_search
        self.app.on_dispute_purchase += self.dispute_purchase
        self.app.on_get_admin += self.admin
        self.app.on_create_offer += self.create_offer
        self.app.on_review_purchase += self.review_purchase
        self.app.on_change_date += self.change_date
        # Starts app
        self.app.connecting()

    def __listen_for_update(self, data: bytes):
        """
        Listens continuously to data from the server and checks it
        :param data: data from the server
        """
        # Checks if data is OFFER UPDATE
        if data[:len(b'Offer Update ')] == b'Offer Update ' and self.app.current_frame_name == 'MAP':
            offers = from_pickle(data[len(b'Offer Update '):])
            if offers:
                self.offers = offers
                if self.selected_marker_pos and self.purchase_window:
                    offer = self.__get_offer_by_pos(self.selected_marker_pos)
                    if offer and not offer['Taken']: self.__unselect_marker()
                self.__map.update_markers(self.__get_updated_offers(self.offers))
                if self.to_focus:
                    self.__update_search()
                    self.app.update_selected()
                    self.to_focus = False
                return
        # Checks if data is ATTRACTIONS
        if data[:len(b'Attractions ')] == b'Attractions ' and self.app.current_frame_name == 'MAP':
            attractions = from_pickle(data[len(b'Attractions '):])
            if attractions:
                self.attractions = attractions
                self.__map.update_attractions(attractions)
                return
        # Checks if data is a message from the server to the user
        pdata = from_pickle(data)
        if type(pdata) is str and str(pdata).startswith('Update: '):
            self.app.display_message(pdata[len('Update: '):])

    # region App Events

    def admin(self):
        """
        Sends a message to the server regarding admin info and adds response handling
        """
        def listen_for_admin_data(data):
            if data[:len(b'All Data ')] == b'All Data ':
                self.admin_data = from_pickle(data[len(b'All Data '):])
                self.app.update_admin(self.admin_data)
            else:
                return False
            return True

        self.add_listen_once_event(listen_for_admin_data)

        self.send(b'admin')

    def login(self, email, password):
        """
        Sends a message to the server regarding login and adds response handling
        """
        def listen_for_login(data):
            pdata = from_pickle(data)
            if pdata == 'login worked':
                self.app.home_frame()
                self.app.set_logged_in(True)
            elif pdata == 'login worked: Admin':
                self.app.home_frame()
                self.app.set_logged_in(True, True)
            elif pdata == 'login failed':
                self.app.display_login_error('Incorrect login credentials!', 'red')
            elif pdata == 'login failed: User already logged in':
                self.app.display_login_error('User already logged in!', 'red')
            else:
                return False
            return True

        self.add_listen_once_event(listen_for_login)

        self.send(b'login ' + to_pickle({'email': email, 'password': password}))

    def logout(self):
        """
        Sends a message to the server regarding logout and adds response handling
        """
        # Destroys purchase windows in case of logout
        if self.purchase_window: self.purchase_window.destroy()

        def listen_for_logout(data):
            pdata = from_pickle(data)
            if pdata == 'logout worked':
                self.app.home_frame()
                self.app.set_logged_in(False)
                return True
            return False

        self.add_listen_once_event(listen_for_logout)

        self.send(b'logout')

    def sign_up(self, username, email, password):
        """
        Sends a message to the server regarding sign up and adds response handling
        """
        def listen_for_sign_up(data):
            pdata = from_pickle(data)
            if pdata == 'signup worked':
                self.app.home_frame()
                self.app.set_logged_in(True)
                return True
            if type(pdata) is str and pdata.split(': ')[0] == 'signup failed':
                self.app.display_signup_error(pdata.split(': ')[1], 'red')
                return True
            return False

        self.add_listen_once_event(listen_for_sign_up)

        self.send(b'user create ' + to_pickle({'username': username, 'email': email, 'password': password}))

    def get_my_offers(self):
        """
        Sends a message to the server regarding own offers and adds response handling
        """
        def listen_for_own_offers(data):
            if data[:len(b'Own Offers ')] == b'Own Offers ':
                self.own_offers = from_pickle(data[len(b'Own Offers '):])
                if self.own_offers is not False:
                    self.app.update_own_offers(self.own_offers)
                    return True
            return False

        self.add_listen_once_event(listen_for_own_offers)

        self.send(b'offer myoffers')

    def create_offer(self, room_name, location, price_per_day, start_date, end_date, conditions, images):
        """
        Sends a message to the server regarding offer creation and adds response handling
        """
        def listen_for_offer_creation(data):
            pdata = from_pickle(data)
            if pdata == 'offer created':
                self.app.home_frame()
                return True
            return False

        self.add_listen_once_event(listen_for_offer_creation)

        self.send(b'offer create ' + to_pickle((room_name, location, price_per_day, start_date, end_date, conditions,
                                                images)))

    def get_my_purchases(self):
        """
        Sends a message to the server regarding own purchases and adds response handling
        """
        def listen_for_own_purchases(data):
            if data[:len(b'Own Purchases ')] == b'Own Purchases ':
                self.own_purchases = from_pickle(data[len(b'Own Purchases '):])
                if self.own_purchases is not False:
                    self.app.update_own_purchases(self.own_purchases)
                    return True
            return False

        self.add_listen_once_event(listen_for_own_purchases)

        self.send(b'purchase mypurchases')

    def purchase(self, offer_id, start_date, end_date, conditions):
        """
        Sends a message to the server regarding making a purchase and adds response handling
        """
        def listen_for_purchase(data):
            pdata = from_pickle(data)
            if pdata == 'purchase worked':
                self.__unselect_marker()
                self.send(b'offer get ' + to_pickle(offer_id))
            elif pdata == 'purchase failed':
                # self.purchase_window.display_purchase_error('Incorrect login credentials!', 'red')
                print(pdata)
            elif pdata == 'purchase failed: Invalid Start Date':
                # self.purchase_window.display_purchase_error('Incorrect login credentials!', 'red')
                print(pdata)
            elif pdata == 'purchase failed: Invalid End Date':
                # self.purchase_window.display_purchase_error('User already logged in!', 'red')
                print(pdata)
            else:
                return False
            return True

        self.add_listen_once_event(listen_for_purchase)

        self.send(b'purchase create ' + to_pickle((offer_id, start_date, end_date, conditions)))

    def dispute_purchase(self, purchase_id):
        """
        Sends a message to the server regarding disputing a purchase and adds response handling
        """
        def listen_for_dispute(data):
            pdata = from_pickle(data)
            if pdata == 'purchase dispute worked':
                self.app.own_purchases_frame()
            elif pdata == 'purchase dispute failed':
                pass
            elif pdata == 'purchase dispute failed: Purchase Ongoing':
                pass
            else:
                return False
            return True

        self.add_listen_once_event(listen_for_dispute)

        self.send(b'purchase dispute ' + to_pickle(purchase_id))

    def review_purchase(self, purchase_id, review, text):
        """
        Sends a message to the server regarding reviewing a purchase
        """
        self.send(b'purchase review ' + to_pickle((purchase_id, review, text)))

    def change_date(self, date):
        """
        Sends a message to the server to change the server's current date
        """
        self.send(b'time ' + to_pickle(date))

    # endregion

    # region Map Events

    def __marker_click(self, marker):
        """
        Client handling when clicking a marker
        """
        if not self.offers: return
        offer = self.__get_offer_by_pos(marker.position)
        if marker.position == self.selected_marker_pos:
            # Unselecting marker and notifying server
            self.__unselect_marker()
            self.send(b'offer get ' + to_pickle(offer["offer_id"]))
        elif not offer['Taken']:
            # Selecting marker and notifying server
            self.__select_marker(offer["offer_id"], marker)

    def __select_marker(self, id, marker):
        """
        Selects a marker and opens its information window after listening to its response
        """
        if self.purchase_window: self.purchase_window.destroy()
        self.selected_marker_pos = marker.position
        self.purchase_window = Window(self.app)
        # In case of closing the window, acts as if the marker has been clicked again to disable it
        self.purchase_window.protocol("WM_DELETE_WINDOW", lambda: self.__marker_click(marker))

        def listen_for_offer(data):
            if data[:len(b'Offer ')] == b'Offer ' and self.app.current_frame_name == 'MAP':
                try:
                    self.current_offer = pickle.loads(data[len(b'Offer '):])
                    self.purchase_window.start(self.current_offer, self.purchase)
                    return True
                except (pickle.UnpicklingError, UnicodeDecodeError):
                    pass
            return False

        self.add_listen_once_event(listen_for_offer)

        self.send(b'offer get ' + to_pickle(id))

    def __unselect_marker(self):
        """
        Unselects marker and destroys its information window
        """
        if self.purchase_window: self.purchase_window.destroy()
        self.selected_marker_pos = None
        self.purchase_window = None

    def update_offers_in_map(self):
        """
        Sends a message to the server to get all offers
        """
        self.send('offer all')

    def __update_search(self):
        """
        Updates the markers by filtering the offers through the search requirements
        and updates the listbox in the map page
        """
        offers = self.__get_updated_offers(self.offers)
        self.__map.update_markers(offers)
        self.app.update_search_listbox(offers)

    def __get_updated_offers(self, offers):
        """
        Filters and sorts offers through search requirements and returns the filtered result
        :param offers: offers to filter
        :return: filtered offers
        """
        if not offers: return {}
        sort_by = (lambda offer: float(offer['price_per_day'])) if self.app.sort_mode == 1 else \
            (lambda offer: math.dist((float(offer['x']), float(offer['y'])), self.start_location))
        return list(
            sorted(
                map(lambda offer: {**offer, **{
                    'Triggered': True if str(self.app.search_var.get()).lower() in str(
                        offer['name']).lower() else False,
                    'Selected': True if self.__get_offer_by_pos(self.selected_marker_pos) == offer else False}},
                    offers),
                key=sort_by
            )
        )

    def __get_offer_by_pos(self, pos):
        """
        Returns the offer in the specified position
        :param pos: tuple of floats (x, y)
        :return: offer in pos
        """
        for offer in self.offers:
            if (float(offer['x']), float(offer['y'])) == pos: return offer
        return None

    # endregion


if __name__ == '__main__':
    AirBNBClient(width=500, height=700)
