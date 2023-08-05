"""User class created from firestore website clickstream data."""

__author__ = 'Merijn van Es'

# TODO: add ppcVisitorAcco, which is a funnel event


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
import dataclasses
import json
import re
import operator

import google.auth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import vaknl_user.Event as EventDataclass


# ----------------------------------------------------------------------------------------------------------------------
# User defined functions
# ----------------------------------------------------------------------------------------------------------------------
def _create_firestore_client(project_id: str):
    """Sets up Firestore client."""
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {'projectId': project_id})
    return firestore.client()


def _try_dict_key_to_get_value(dct: dict, keys: list):
    """Safely tries to get value for combination of keys in nested dictionary."""
    result = dct
    for key in keys:
        try:
            result = result[key]
        except KeyError:
            return None
    return result


# ----------------------------------------------------------------------------------------------------------------------
# Default input variables
# ----------------------------------------------------------------------------------------------------------------------
_, _project_id = google.auth.default()
_firestore_collection_source = u'in_website_clickstream'
_firestore_collection_destination = u'dmp_users'
_firestore_client = _create_firestore_client(_project_id)


# ----------------------------------------------------------------------------------------------------------------------
# User class
# ----------------------------------------------------------------------------------------------------------------------
class User(object):
    """User class where user object is identified by dmp_user_id user."""

    def __init__(self, dmp_user_id):
        self.dmp_user_id = dmp_user_id
        self.events = []
        self.statistics = {
            'first_seen': 0,
            'last_seen': 0,
            'funnel_step': 'visitor',
            'last_viewed_acco': None,
            'last_booked_acco': None,
            'most_viewed_acco': None,
            'most_used_departure_airport': None,
            'n_events': 0,
            'n_pageviews': 0,
            'n_price_clicks': 0,
            'n_image_clicks': 0,
            'n_search_page_filter_selections': 0,
            'viewed_productpages_frequencies': dict(),
            'search_departure_airport_frequencies': dict(),
        }

    @staticmethod
    def create_event(clickstream_event_json):
        """Assigns event to a (event-)dataclass based on event clickstream json.

        Args:
            clickstream_event_json: str, clickstream event json string

        Return:
            dataclass, event dataclass.
        """
        event_value_type = _try_dict_key_to_get_value(clickstream_event_json, ['eventValueType'])
        event_trigger = _try_dict_key_to_get_value(clickstream_event_json, ['info', 'eventTrigger'])
        standard_event_arguments = {
            'event_id': _try_dict_key_to_get_value(clickstream_event_json, ['eventId']),
            'timestamp': _try_dict_key_to_get_value(clickstream_event_json, ['timestamp']),
            'dmp_session_id': _try_dict_key_to_get_value(clickstream_event_json, ['info', 'dmpSessionId'])
        }
        if event_value_type == 'undefined':
            pass
        else:
            event_value_json = json.loads(_try_dict_key_to_get_value(clickstream_event_json, ['eventValueJson']))
            if event_value_type == 'session':
                event = EventDataclass.Session(
                    ip=_try_dict_key_to_get_value(clickstream_event_json, ['remoteIp']),
                    time_zone=_try_dict_key_to_get_value(clickstream_event_json, ['timeZone']),
                    continent=_try_dict_key_to_get_value(clickstream_event_json, ['continent']),
                    country=_try_dict_key_to_get_value(clickstream_event_json, ['country']),
                    region=_try_dict_key_to_get_value(clickstream_event_json, ['mostSpecificSubdivision']),
                    device=_try_dict_key_to_get_value(
                        event_value_json,
                        [event_value_type, 'userAgent', 'uaDeviceType']
                    ),
                    **standard_event_arguments
                )
            elif event_value_type == 'pageview':
                page_type = _try_dict_key_to_get_value(event_value_json, [event_value_type, 'pageType'])
                if page_type == 'homePage':
                    event = EventDataclass.PageviewHomePage(
                        **standard_event_arguments
                    )
                elif page_type == 'productPage':
                    event = EventDataclass.PageviewProductPage(
                        giataid=re.findall(r"hotelId=(\d+)", event_value_json[event_value_type]['url'])[0],
                        **standard_event_arguments
                    )
                elif page_type in ('brandedSearchPage', 'Search', 'nonBrandedSearchPage', 'Branded Search'):
                    event = EventDataclass.PageviewSearch(
                        **standard_event_arguments
                    )
                elif page_type == 'bookingForm':
                    event = EventDataclass.PageviewBookingStep(
                        **standard_event_arguments
                    )
                elif page_type == 'dealPage':
                    event = EventDataclass.PageviewDealPage(
                        **standard_event_arguments
                    )
                elif page_type == 'searchAssistantPage':
                    event = EventDataclass.PageviewKeuzehulp(
                        **standard_event_arguments
                    )
                elif page_type == 'content':
                    event = EventDataclass.PageviewContent(
                        **standard_event_arguments
                    )
                elif page_type == 'newsPage':
                    event = EventDataclass.PageviewBlog(
                        **standard_event_arguments
                    )
                elif page_type in ('errorPage', '404Page'):
                    event = EventDataclass.PageviewError(
                        **standard_event_arguments
                    )
                else:
                    event = EventDataclass.PageviewOther(
                        **standard_event_arguments
                    )
            elif event_value_type == 'reservation':
                reservation_status = _try_dict_key_to_get_value(
                    event_value_json,
                    [event_value_type, 'reservationStatus']
                )
                giataid = event_value_json['reservation']['packages'][0]['productCode']
                if event_trigger == 'ibe-extras':
                    event = EventDataclass.ReservationExtras(
                        giataid=giataid,
                        **standard_event_arguments
                    )
                elif event_trigger == 'ibe-personaldata':
                    event = EventDataclass.ReservationPersonalData(
                        giataid=giataid,
                        **standard_event_arguments
                    )
                elif event_trigger == 'ibe-overview-payment':
                    event = EventDataclass.ReservationOverview(
                        giataid=giataid,
                        **standard_event_arguments
                    )
                elif event_trigger == 'ibe-confirmation' and reservation_status == 'Booked':
                    event = EventDataclass.ReservationBooked(
                        giataid=giataid,
                        reservation_id=_try_dict_key_to_get_value(event_value_json, [event_value_type, 'reservationId']),
                        **standard_event_arguments
                    )
                else:
                    event = EventDataclass.ReservationOther(
                        reservation_status=reservation_status,
                        giataid=giataid,
                        **standard_event_arguments
                    )
            elif event_value_type == 'priceClick':
                event = EventDataclass.PriceClick(
                    giataid=_try_dict_key_to_get_value(event_value_json, ['packagePrice', 'productCode']),
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'imgClick':
                event = EventDataclass.ImageClick(
                    giataid=_try_dict_key_to_get_value(event_value_json, ['value']),
                    **standard_event_arguments
                )
            elif event_value_type == 'search' and event_trigger == 'search':
                filters = _try_dict_key_to_get_value(event_value_json, [event_value_type, 'filters'])
                departure_date = \
                    next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == "departure"),
                         [None])[0]
                geo = next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == "geo"), None)
                theme = \
                    next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'theme'),
                         None)[0]
                departure_airports = next(
                    (list(item['filterValues'].keys()) for item in filters if item['filterName'] == "airports"), None)
                distance_to_beach = \
                    next((list(item['filterValues'].keys()) for item in filters if
                          item['filterName'] == 'distanceToBeach'),
                         [0])[0]
                if distance_to_beach == '0':
                    distance_to_beach = None
                elif distance_to_beach == 'on-beach':
                    distance_to_beach = 0
                else:
                    distance_to_beach = int(distance_to_beach)
                mealplans = next(
                    (list(item['filterValues'].keys()) for item in filters if item['filterName'] == "mealplans"), None)
                hotel_ratings = int(next(
                    (list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'hotelRatings'),
                    [-1])[0])
                star_rating = int(
                    next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'rating'),
                         [0])[0])
                budget = int(
                    next((list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'budget'),
                         [0])[0])
                party_composition = next(
                    (list(item['filterValues'].keys()) for item in filters if item['filterName'] == 'partyComposition'),
                    [None])[0]
                event = EventDataclass.SearchPageSearchQuery(
                    departure_date=departure_date,
                    geo=geo,
                    theme=theme if theme != '0' else None,
                    departure_airports=departure_airports,
                    distance_to_beach=distance_to_beach if distance_to_beach != 0 else None,
                    mealplans=mealplans,
                    hotel_ratings=hotel_ratings if hotel_ratings != -1 else None,
                    star_rating=star_rating if star_rating != 0 else None,
                    budget=budget if budget != 0 else None,
                    party_composition=party_composition,
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'selectFilter':
                event = EventDataclass.SearchPageFilter(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'filterDepartureDate':
                event = EventDataclass.ProductPageFilterDepDate(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'filterAirport':
                event = EventDataclass.ProductPageFilterAirport(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'filterMealplan':
                event = EventDataclass.ProductPageFilterMealPlan(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'selectFlightFilter':
                event = EventDataclass.ProductPageFilterFlight(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'filterDurationRange':
                event = EventDataclass.ProductPageFilterDurationRange(
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'partyCompositionFilter':
                event = EventDataclass.GlobalFilterPartyComposition(
                    **standard_event_arguments
                )
            elif event_value_type == 'packageAvailability':
                event = EventDataclass.ProductAvailability(
                    **standard_event_arguments
                )
            elif event_value_type == 'productService':
                event = EventDataclass.ProductService(
                    giataid=_try_dict_key_to_get_value(event_value_json, ['package', 'productCode']),
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger in \
                    ('changeTransfer', 'changeInsurance', 'changeLuggage'):
                event = EventDataclass.SelectExtrasBookingStep(
                    type=re.findall(r"change(.+)", event_trigger.lower())[0],
                    **standard_event_arguments
                )
            elif event_value_type == 'basic' and event_trigger == 'showTop10':
                event = EventDataclass.KeuzehulpShowTop10(
                    **standard_event_arguments
                )
            else:
                event = EventDataclass.EventOther(
                    event_value_type=event_value_type,
                    event_trigger=event_trigger,
                    **standard_event_arguments
                )

            return event

    @staticmethod
    def update_funnel_step(statistics, event):
        """Updates the funnel step the user is in.
        For speed: only trigger if event.funnel_event == True.

        Args:
            statistics: dict, user statistics dictionary.
            event: dataclass, clickstream event.

        Return:
            str, name of funnel step the user is in.
        """
        funnel_step = statistics['funnel_step']
        if isinstance(event, EventDataclass.ReservationBooked):
            funnel_step = 'booked'
        elif funnel_step != 'in_market':
            if isinstance(event, (EventDataclass.ReservationPersonalData, EventDataclass.ReservationOverview,
                                  EventDataclass.SelectExtrasBookingStep)):
                funnel_step = 'in_market'
            elif funnel_step != 'active_plus':
                if (
                        isinstance(event, (EventDataclass.ProductService, EventDataclass.ProductPageFilterFlight,
                                           EventDataclass.ProductPageFilterAirport,
                                           EventDataclass.ProductPageFilterMealPlan,
                                           EventDataclass.ProductAvailability, EventDataclass.ReservationExtras)) or
                        len(statistics['viewed_productpages_frequencies'].keys()) >= 5
                ):
                    funnel_step = 'active_plus'
                elif funnel_step != 'active':
                    if (
                            (isinstance(event, EventDataclass.SearchPageSearchQuery) and event.departure_date) or
                            isinstance(event, (
                                    EventDataclass.ProductPageFilterDepDate,
                                    EventDataclass.GlobalFilterPartyComposition,
                                    EventDataclass.KeuzehulpShowTop10, EventDataclass.PriceClick)) or
                            statistics['n_image_clicks'] >= 3 or
                            statistics['n_search_page_filter_selections'] >= 2
                            # OR landing from ppc campaign on product page
                    ):
                        funnel_step = 'active'
        return funnel_step

    def update_statistics(self, event):
        """Update user statistics with event.

        Args:
            event: dataclass, clickstream event.
        """
        if self.statistics['n_events'] == 0:
            self.statistics['first_seen'] = event.timestamp
        else:
            self.statistics['first_seen'] = min(self.statistics['first_seen'], event.timestamp)

        self.statistics['last_seen'] = max(self.statistics['last_seen'], event.timestamp)
        self.statistics['n_events'] += 1

        if isinstance(event, EventDataclass.Pageview):
            self.statistics['n_pageviews'] += 1
            if isinstance(event, EventDataclass.PageviewProductPage):
                giataid = event.giataid
                giataid_counter = self.statistics['viewed_productpages_frequencies']
                if giataid in giataid_counter:
                    giataid_counter[giataid] += 1
                else:
                    giataid_counter[giataid] = 1
                self.statistics['viewed_productpages_frequencies'] = giataid_counter
                self.statistics['last_viewed_acco'] = giataid
                self.statistics['most_viewed_acco'] = max(giataid_counter, key=giataid_counter.get)
        elif isinstance(event, EventDataclass.PriceClick):
            self.statistics['n_price_clicks'] += 1
        elif isinstance(event, EventDataclass.ImageClick):
            self.statistics['n_image_clicks'] += 1
        elif isinstance(event, EventDataclass.SearchPageFilter):
            self.statistics['n_search_page_filter_selections'] += 1
        elif isinstance(event, EventDataclass.ReservationBooked):
            self.statistics['last_booked_acco'] = event.giataid
        elif isinstance(event, EventDataclass.SearchPageSearchQuery):
            airports = event.departure_airports
            if airports:
                departure_airport_counter = self.statistics['search_departure_airport_frequencies']
                for airport in airports:
                    if airport in departure_airport_counter:
                        departure_airport_counter[airport] += 1
                    else:
                        departure_airport_counter[airport] = 1
                self.statistics['search_departure_airport_frequencies'] = departure_airport_counter
                self.statistics['most_used_departure_airport'] = max(departure_airport_counter,
                                                                     key=departure_airport_counter.get)
        if self.statistics['funnel_step'] != 'booked' and event.funnel_event:
            self.statistics['funnel_step'] = self.update_funnel_step(self.statistics, event)

    def add_event(self, clickstream_event_json):
        """Adds event to user based on clickstream json and updates statistics.

        Args:
            clickstream_event_json: str, clickstream event json string
        """
        event = self.create_event(clickstream_event_json)
        if event:
            self.events.append(event)
            self.update_statistics(event)

    def add_multiple_events(self, clickstream_event_json_list):
        """Adds multiple events to event_list at a time.

        Args:
            clickstream_event_json_list: [str], list of clickstream event json strings
        """
        for clickstream_event_json in clickstream_event_json_list:
            self.add_event(clickstream_event_json)

    def sort_events_by_timestamp(self):
        """Sort self.events (event list) ascending on timestamp."""
        self.events = sorted(self.events, key=operator.attrgetter('timestamp'))

    def events_to_dict(self):
        """Outputs list of event dicts (decoded from the list of event dataclasses).

        Return:
            [dict], list of events as dictionaries
        """
        return [{'event_name': event.__class__.__name__, 'values': dataclasses.asdict(event)} for event in self.events]

    def to_firestore(self):
        """Writes user to firestore."""
        global _firestore_client, _firestore_collection_source
        doc_ref = _firestore_client.collection(_firestore_collection_source).document(self.dmp_user_id)
        doc_ref.set({
            'statistics': self.statistics,
            'event_list': self.events_to_dict()
        })

    def create_user_from_clickstream(self):
        """Gets all available website clickstream data from Firestore for the given dmp_user_id and fills the User class
        with information."""
        global _firestore_client, _firestore_collection_source
        doc_ref = _firestore_client.collection(_firestore_collection_source).document(self.dmp_user_id) \
            .collection(u'sessions').stream()
        sessions = [doc.id for doc in doc_ref]

        event_list = []
        for session in sessions:
            event_list += _firestore_client.collection(_firestore_collection_source).document(self.dmp_user_id) \
                .collection(u'sessions').document(session) \
                .collection(u'events').document(u'event_list').get().to_dict()['event_list']

        self.add_multiple_events(event_list)
        self.sort_events_by_timestamp()
