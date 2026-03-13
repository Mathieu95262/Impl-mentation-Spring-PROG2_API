from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date
from typing import Optional, List

# Modèle pour le client
class Customer(BaseModel):
    name: str = Field(..., description="Nom du client")
    phone: str = Field(..., description="Numéro de téléphone")
    email: EmailStr = Field(..., description="Adresse email")

# Modèle pour la chambre
class Room(BaseModel):
    number: int = Field(..., ge=1, le=9, description="Numéro de chambre (1-9)")
    description: str = Field(..., description="Description de la chambre")

# Modèle pour la réservation
class Booking(Customer, Room):
    booking_date: date = Field(..., description="Date de la réservation")

    @field_validator('booking_date')
    def validate_booking_date(cls, v):
        return v

# Modèle pour la réponse
class BookingResponse(Booking):
    pass