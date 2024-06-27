from datetime import datetime, timedelta
from typing import List

# Define Event class
class Event:
    def __init__(self, event_id: int, name: str, date: datetime, venue: str, category: str, available_seats: int):
        self.event_id = event_id
        self.name = name
        self.date = date
        self.venue = venue
        self.category = category
        self.available_seats = available_seats

    def book_seat(self) -> bool:
        if self.available_seats > 0:
            self.available_seats -= 1
            return True
        return False

# Define Subscription class
class Subscription:
    def __init__(self, subscription_id: int, name: str, price: float, event_limit: int, priority_booking: bool):
        self.subscription_id = subscription_id
        self.name = name
        self.price = price
        self.event_limit = event_limit
        self.priority_booking = priority_booking

# Define User class
class User:
    def __init__(self, user_id: int, name: str, email: str, subscription: Subscription):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.subscription = subscription
        self.booked_events: List[Event] = []

    def book_event(self, event: Event) -> bool:
        if len(self.booked_events) < self.subscription.event_limit:
            if event.book_seat():
                self.booked_events.append(event)
                return True
        return False

    def swap_event(self, old_event: Event, new_event: Event) -> bool:
        if new_event.book_seat():
            self.booked_events.remove(old_event)
            old_event.available_seats += 1
            self.booked_events.append(new_event)
            return True
        return False

# Define Booking class
class Booking:
    def __init__(self, user: User, event: Event):
        self.user = user
        self.event = event
        self.booking_date = datetime.now()

# Define EventSubscriptionService class
class EventSubscriptionService:
    def __init__(self):
        self.users: List[User] = []
        self.events: List[Event] = []
        self.subscriptions: List[Subscription] = []

    def add_user(self, user: User):
        self.users.append(user)

    def add_event(self, event: Event):
        self.events.append(event)

    def add_subscription(self, subscription: Subscription):
        self.subscriptions.append(subscription)

    def find_events_by_category(self, category: str) -> List[Event]:
        return [event for event in self.events if event.category == category and event.date > datetime.now()]

    def find_events_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Event]:
        return [event for event in self.events if start_date <= event.date <= end_date]

    def book_event_for_user(self, user_id: int, event_id: int) -> bool:
        user = next((u for u in self.users if u.user_id == user_id), None)
        event = next((e for e in self.events if e.event_id == event_id), None)
        if user and event:
            return user.book_event(event)
        return False

    def swap_event_for_user(self, user_id: int, old_event_id: int, new_event_id: int) -> bool:
        user = next((u for u in self.users if u.user_id == user_id), None)
        old_event = next((e for e in self.events if e.event_id == old_event_id), None)
        new_event = next((e for e in self.events if e.event_id == new_event_id), None)
        if user and old_event and new_event:
            return user.swap_event(old_event, new_event)
        return False

# Create some subscriptions
basic_subscription = Subscription(subscription_id=1, name="LivePass Basic", price=20.0, event_limit=3, priority_booking=False)
plus_subscription = Subscription(subscription_id=2, name="LivePass Plus", price=40.0, event_limit=6, priority_booking=True)
vip_subscription = Subscription(subscription_id=3, name="LivePass VIP", price=80.0, event_limit=10, priority_booking=True)

# Create some events
event1 = Event(event_id=101, name="Rock Concert", date=datetime(2024, 7, 20), venue="Stadium A", category="Music", available_seats=100)
event2 = Event(event_id=102, name="Broadway Show", date=datetime(2024, 8, 15), venue="Theatre B", category="Theatre", available_seats=50)
event3 = Event(event_id=103, name="Football Match", date=datetime(2024, 6, 10), venue="Arena C", category="Sports", available_seats=200)

# Initialize the EventSubscriptionService
service = EventSubscriptionService()

# Add subscriptions to the service
service.add_subscription(basic_subscription)
service.add_subscription(plus_subscription)
service.add_subscription(vip_subscription)

# Add events to the service
service.add_event(event1)
service.add_event(event2)
service.add_event(event3)

# Create a user and add to the service
user = User(user_id=1, name="Alice", email="alice@example.com", subscription=basic_subscription)
service.add_user(user)

# User books an event
if service.book_event_for_user(user_id=1, event_id=101):
    print(f"User {user.name} successfully booked {event1.name}")
else:
    print(f"User {user.name} failed to book {event1.name}")

# Find available music events
music_events = service.find_events_by_category("Music")
print(f"Available music events: {[event.name for event in music_events]}")

# User swaps an event
if service.swap_event_for_user(user_id=1, old_event_id=101, new_event_id=102):
    print(f"User {user.name} successfully swapped to {event2.name}")
else:
    print(f"User {user.name} failed to swap to {event2.name}")
