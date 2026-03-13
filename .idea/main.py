from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Booking, BookingResponse
from database import add_booking, get_all_bookings

app = FastAPI(
    title="STD24056",
    description="Hotel Booking API",
    version="1.0.0"
)

# Route GET /booking
@app.get("/booking",
         response_model=List[BookingResponse],
         status_code=status.HTTP_200_OK,
         summary="Récupère toutes les réservations",
         description="Retourne la liste de toutes les réservations en mémoire")
async def get_bookings():
    return get_all_bookings()

# Route POST /booking
@app.post("/booking",
          response_model=List[BookingResponse],
          status_code=status.HTTP_200_OK,
          summary="Crée une nouvelle réservation",
          description="Crée une réservation si la chambre est disponible à la date donnée")
async def create_booking(booking: Booking):

    if booking.number < 1 or booking.number > 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le numéro de chambre doit être compris entre 1 et 9"
        )

    # Tentative d'ajout de la réservation
    if add_booking(booking):
        return get_all_bookings()
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La chambre {booking.number} est déjà réservée pour le {booking.booking_date}"
        )

# Route pour le bonus avec sous-ressources
@app.get("/rooms/{room_number}/bookings",
         response_model=List[BookingResponse],
         summary="Récupère les réservations d'une chambre spécifique")
async def get_room_bookings(room_number: int):
    if room_number < 1 or room_number > 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le numéro de chambre doit être compris entre 1 et 9"
        )

    all_bookings = get_all_bookings()
    room_bookings = [b for b in all_bookings if b.number == room_number]
    return room_bookings