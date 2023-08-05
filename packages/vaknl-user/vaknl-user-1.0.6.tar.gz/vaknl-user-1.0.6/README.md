# vaknl-user

Defines the vaknl User class. A user (here identified by a `dmp_user_id`) is a object that is defined by website 
clickstream data as a basis. The User class contains functions that can transform raw Firestore website clickstream data
to well defined Event dataclasses. These Event dataclasses are read and translated into user information. The User class
also includes functions to write the user to Firestore.


## Prerequisites

Firestore read and write permissions within the Google Cloud Platform (GCP), if one wants to make use of the Firestore 
functionality.


## User

### class User
User class where user object is identified by dmp_user_id user.

#### create_event(clickstream_event_json) @staticmethod
Assigns event to a (event-)dataclass based on event clickstream json.

#### update_funnel_step(statistics, event) @staticmethod
Updates the funnel step the user is in.

#### update_statistics(event)
Update user statistics with event.

#### add_event(clickstream_event_json)
Adds event to user based on clickstream json and updates statistics.

#### add_multiple_events(clickstream_event_json_list)
Adds multiple events to event_list at a time.

#### sort_events_by_timestamp()
Sort self.events (event list) ascending on timestamp.

#### events_to_dict()
Outputs list of event dicts (decoded from the list of event dataclasses).

#### to_firestore()
Writes user to firestore.

#### create_user_from_clickstream()
Gets all available website clickstream data from Firestore for the given dmp_user_id and fills the User class
with information.

### General script functions

Mostly functions that allow the user of this package to manually set private variables in this module.

#### set_project_id(name: str)
Set global variable `_project_id`, which represents the GCP project id. When function is called, it also 
automatically updates the firestore client.

#### set_firestore_collection_source(name: str)
Set global variable `_firestore_collection_source`, which should be the name of the Firestore source collection, 
from which the website clickstream data is gathered.

#### set_firestore_collection_destination(name: str)
Set global variable `_firestore_collection_destination`, which should be the name of the Firestore destination
collection to which the user is written.

#### create_firestore_client(project_id: str)
Sets up Firestore client. 


## Event

Contains Event dataclass and all sub-dataclasses that can go multiple layers deep.



