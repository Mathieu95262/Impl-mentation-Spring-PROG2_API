from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import date
from pydantic import BaseModel, Field, EmailStr

# Modèles de données
class Customer(BaseModel):
    name: str = Field(..., description="Nom du client")
    phone: str = Field(..., description="Numéro de téléphone")
    email: EmailStr = Field(..., description="Adresse email")

class Room(BaseModel):
    number: int = Field(..., ge=1, le=9, description="Numéro de chambre (1-9)")
    description: str = Field(..., description="Description de la chambre")

class Booking(Customer, Room):
    booking_date: date = Field(..., description="Date de la réservation")

# Base de données en mémoire
bookings_db = {}

# Initialisation de l'application FastAPI
app = FastAPI(
    title="STD24001",  # À remplacer par votre référence étudiant
    description="Hotel Booking API",
    version="1.0.0"
)

# Route GET /booking
@app.get("/booking", response_model=List[Booking])
async def get_bookings():
    return list(bookings_db.values())

# Route POST /booking
@app.post("/booking", response_model=List[Booking])
async def create_booking(booking: Booking):
    # Vérification numéro de chambre (1-9)
    if booking.number < 1 or booking.number > 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le numéro de chambre doit être compris entre 1 et 9"
        )
    
    # Vérification disponibilité
    key = (booking.number, booking.booking_date.isoformat())
    if key in bookings_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La chambre {booking.number} est déjà réservée pour le {booking.booking_date}"
        )
    
    # Ajout de la réservation
    bookings_db[key] = booking
    return list(bookings_db.values())

# Route bonus
@app.get("/rooms/{room_number}/bookings", response_model=List[Booking])
async def get_room_bookings(room_number: int):
    if room_number < 1 or room_number > 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le numéro de chambre doit être compris entre 1 et 9"
        )
    
    return [b for b in bookings_db.values() if b.number == room_number]

@app.get("/")
async def root():
    return {"message": "Hotel Booking API", "docs": "/docs"}

