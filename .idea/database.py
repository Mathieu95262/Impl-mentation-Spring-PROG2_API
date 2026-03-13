from typing import List, Dict, Tuple
from datetime import date
from models import Booking

bookings_db: Dict[Tuple[int, date], Booking] = {}

def add_booking(booking: Booking) -> bool:
    key = (booking.number, booking.booking_date)
    if key in bookings_db:
        return False
    bookings_db[key] = booking
    return True

def get_all_bookings() -> List[Booking]:
    return list(bookings_db.values())