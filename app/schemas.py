"""
Pydantic Schemas
Request and response models for API validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date, time
from decimal import Decimal


# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1)
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== AUTHENTICATION SCHEMAS ====================

class Token(BaseModel):
    access_token: str
    token_type: str


# ==================== AIRPORT SCHEMAS ====================

class AirportResponse(BaseModel):
    id: int
    code: str
    name: str
    city: str
    country: str
    
    class Config:
        from_attributes = True


# ==================== AIRLINE SCHEMAS ====================

class AirlineResponse(BaseModel):
    id: int
    code: str
    name: str
    country: str
    
    class Config:
        from_attributes = True


# ==================== FLIGHT SCHEMAS ====================

class FlightBase(BaseModel):
    flight_number: str
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_date: date
    departure_time: time
    arrival_date: date
    arrival_time: time
    duration_minutes: int
    class_type: str = Field(..., pattern="^(economy|business|first)$")
    price: Decimal
    available_seats: int


class FlightResponse(FlightBase):
    id: int
    airline_id: int
    total_seats: int
    aircraft_type: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== PASSENGER SCHEMAS ====================

class PassengerBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    date_of_birth: date
    gender: str = Field(..., pattern="^(male|female|other)$")
    passport_number: Optional[str] = None
    nationality: str = Field(..., min_length=2)
    seat_number: Optional[str] = None


class PassengerCreate(PassengerBase):
    pass


class PassengerResponse(PassengerBase):
    id: int
    booking_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== BOOKING SCHEMAS ====================

class BookingBase(BaseModel):
    flight_id: int
    passengers: List[PassengerCreate] = Field(..., min_items=1, max_items=9)


class BookingCreate(BookingBase):
    pass


class BookingResponse(BaseModel):
    id: int
    booking_reference: Optional[str]
    user_id: int
    flight_id: int
    total_passengers: int
    total_amount: Decimal
    booking_status: str
    payment_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class BookingDetailResponse(BookingResponse):
    flight: FlightResponse
    passengers: List[PassengerResponse]
    
    class Config:
        from_attributes = True


# ==================== PAYMENT SCHEMAS ====================

class PaymentCreate(BaseModel):
    booking_id: int
    payment_method: str = Field(..., pattern="^(card|bank_transfer|paystack|stripe)$")


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: Decimal
    payment_method: str
    transaction_reference: str
    payment_status: str
    payment_date: datetime
    
    class Config:
        from_attributes = True


# ==================== STATISTICS SCHEMAS ====================

class BookingStats(BaseModel):
    total_bookings: int
    confirmed_bookings: int
    cancelled_bookings: int
    completed_payments: int
    pending_payments: int
    total_amount_spent: float
