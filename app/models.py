"""
Database Models
SQLAlchemy ORM models for Flight Booking System
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Date, Time, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")


class Airport(Base):
    """Airport model"""
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, index=True, nullable=False)  # IATA code
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    timezone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Airline(Base):
    """Airline model"""
    __tablename__ = "airlines"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(2), unique=True, index=True, nullable=False)  # IATA code
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    flights = relationship("Flight", back_populates="airline")


class Flight(Base):
    """Flight model"""
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, nullable=False, index=True)
    airline_id = Column(Integer, ForeignKey("airlines.id"), nullable=False)
    origin = Column(String(3), nullable=False, index=True)  # Airport code
    destination = Column(String(3), nullable=False, index=True)  # Airport code
    departure_date = Column(Date, nullable=False, index=True)
    departure_time = Column(Time, nullable=False)
    arrival_date = Column(Date, nullable=False)
    arrival_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)  # Flight duration in minutes
    class_type = Column(String, nullable=False)  # economy, business, first
    price = Column(Numeric(10, 2), nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    aircraft_type = Column(String, nullable=True)
    status = Column(String, default="scheduled")  # scheduled, boarding, departed, arrived, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    airline = relationship("Airline", back_populates="flights")
    bookings = relationship("Booking", back_populates="flight")


class Booking(Base):
    """Booking model"""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    total_passengers = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    booking_status = Column(String, default="confirmed")  # confirmed, cancelled, completed
    payment_status = Column(String, default="pending")  # pending, completed, failed, refunded
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")
    passengers = relationship("Passenger", back_populates="booking", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")


class Passenger(Base):
    """Passenger model"""
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)  # male, female, other
    passport_number = Column(String, nullable=True)
    nationality = Column(String, nullable=False)
    seat_number = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    booking = relationship("Booking", back_populates="passengers")


class Payment(Base):
    """Payment model"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String, nullable=False)  # card, bank_transfer, paystack, stripe
    transaction_reference = Column(String, unique=True, index=True, nullable=False)
    payment_status = Column(String, default="pending")  # pending, completed, failed
    payment_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    booking = relationship("Booking", back_populates="payments")
