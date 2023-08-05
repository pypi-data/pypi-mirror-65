"""Event dataclasses from website clickstream events."""

__author__ = 'Merijn van Es'


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass


# ----------------------------------------------------------------------------------------------------------------------
# Event
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(order=True)
class Event:
    """Super dataclass for all."""
    event_id: str
    timestamp: int
    dmp_session_id: str
    # pageview_id: str


# ----------------------------------------------------------------------------------------------------------------------
# Other subclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Session(Event):
    """event_value_type == 'session'"""
    ip: str
    time_zone: str
    continent: str
    country: str
    region: str
    device: str
    funnel_event: bool = False


@dataclass
class SearchPageSearchQuery(Event):
    """All filters applied in search on search page.
    event_value_type == 'search' and event_trigger == 'search'"""
    departure_date: str
    geo: list
    theme: str
    departure_airports: list
    # duration: list
    distance_to_beach: int
    mealplans: str
    hotel_ratings: int
    star_rating: int
    budget: int
    party_composition: str
    funnel_event: bool = True


@dataclass
class KeuzehulpShowTop10(Event):
    """event_value_type == 'basic' and event_trigger == 'showTop10'"""
    funnel_event: bool = True


@dataclass
class PriceClick(Event):
    """event_value_type == 'priceClick'"""
    giataid: str
    funnel_event: bool = True


@dataclass
class ImageClick(Event):
    """event_value_type == 'basic' and event_trigger == 'imgClick'"""
    giataid: str
    funnel_event: bool = True


@dataclass
class ProductService(Event):
    """event_type == 'productService'
    Is always: event_trigger in ('roomTypeSelection', 'mealPlanSelection', 'flightSelection')"""
    giataid: str
    funnel_event: bool = True


@dataclass
class ProductAvailability(Event):
    """event_type == 'productAvailability'
    Is always: event_trigger == 'packageAvailability'"""
    # No giataid available
    funnel_event: bool = True


@dataclass
class SelectExtrasBookingStep(Event):
    """event_type == 'basic' and event_trigger in ('changeTransfer', 'changeInsurance', 'changeLuggage')"""
    # No giataid available
    type: str
    funnel_event: bool = True


@dataclass
class EventOther(Event):
    """All other events that are not defined by the stated."""
    event_value_type: str
    event_trigger: str
    funnel_event: bool = False


# ----------------------------------------------------------------------------------------------------------------------
# Filter dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Filter(Event):
    """Filter super class"""
    pass


@dataclass
class SearchPageFilter(Filter):
    """Any filter adjustment on search page, except for party composition and departure date
    event_value_type == 'basic' and event_trigger == 'selectFilter'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterDepDate(Filter):
    """event_value_type == 'basic' and event_trigger == 'filterDepartureDate'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterAirport(Filter):
    """event_value_type == 'basic' and event_trigger == 'filterAirport'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterMealPlan(Filter):
    """event_value_type == 'basic' and event_trigger == 'filterMealplan'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterFlight(Filter):
    """Any of the flight filters.
    event_value_type == 'basic' and event_trigger == 'selectFlightFilter'"""
    funnel_event: bool = True


@dataclass
class ProductPageFilterDurationRange(Filter):
    """event_value_type == 'basic' and event_trigger == 'filterDurationRange'"""
    funnel_event: bool = False


@dataclass
class GlobalFilterPartyComposition(Filter):
    """Event for party composition everywhere on the site.
    event_value_type == 'basic' and event_trigger == 'partyCompositionFilter'"""
    funnel_event: bool = True


# ----------------------------------------------------------------------------------------------------------------------
# Pageview dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Pageview(Event):
    """Pageview superclass.
    event_value_type == 'pageview'"""
    # url: str
    # page_type: str
    pass


@dataclass
class PageviewHomePage(Pageview):
    """pageview_page_type == 'homePage'"""
    funnel_event: bool = False


@dataclass
class PageviewSearch(Pageview):
    """pageview_page_type in ('brandedSearchPage', 'Search', 'nonBrandedSearchPage', 'Branded Search')
    Last 2 are old ones from before 2019."""
    funnel_event: bool = False


@dataclass
class PageviewProductPage(Pageview):
    """pageview_page_type == 'productPage'"""
    giataid: str = ''
    funnel_event: bool = True


@dataclass
class PageviewBookingStep(Pageview):
    """pageview_page_type == 'bookingForm'"""
    funnel_event: bool = False


@dataclass
class PageviewDealPage(Pageview):
    """pageview_page_type == 'dealPage'"""
    funnel_event: bool = False


@dataclass
class PageviewKeuzehulp(Pageview):
    """pageview_page_type == 'searchAssistantPage'"""
    # page_type2: str
    funnel_event: bool = False


@dataclass
class PageviewContent(Pageview):
    """pageview_page_type == 'content'"""
    funnel_event: bool = False


@dataclass
class PageviewBlog(Pageview):
    """pageview_page_type == 'newsPage'"""
    funnel_event: bool = False


@dataclass
class PageviewError(Pageview):
    """pageview_page_type in ('errorPage', '404Page')"""
    funnel_event: bool = False


@dataclass
class PageviewOther(Pageview):
    """All other pageview events that are not defined as separate dataclass."""
    funnel_event: bool = False


# ----------------------------------------------------------------------------------------------------------------------
# Reservation dataclasses
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Reservation(Event):
    """Reservation superclass"""
    giataid: str


@dataclass
class ReservationExtras(Reservation):
    """event_trigger == 'ibe-extras'"""
    funnel_event: bool = False


@dataclass
class ReservationPersonalData(Reservation):
    """event_trigger == 'ibe-personaldata'"""
    funnel_event: bool = True


@dataclass
class ReservationOverview(Reservation):
    """event_trigger == 'ibe-overview-payment'"""
    funnel_event: bool = True


@dataclass
class ReservationBooked(Reservation):
    """event_trigger == 'ibe-confirmation' and reservation_status == 'Booked'"""
    reservation_id: str
    funnel_event: bool = True


@dataclass
class ReservationOther(Reservation):
    """All other reservation events that are not defined as separate dataclass."""
    reservation_status: str
    funnel_event: bool = False
