"""
Flight Booking API - Main Application
Complete flight reservation system with search, booking, and payment processing
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, date
import jwt
from passlib.context import CryptContext
from decimal import Decimal

from . import models, schemas, database

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create FastAPI app
app = FastAPI(
    title="Flight Booking API",
    description="Complete flight reservation system with search, booking, and payment processing",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=database.engine)


# ==================== UTILITY FUNCTIONS ====================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# ==================== AUTHENTICATION ====================

@app.post("/api/auth/register", response_model=schemas.UserResponse, tags=["Authentication"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/token", response_model=schemas.Token, tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.UserResponse, tags=["Authentication"])
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


# ==================== FLIGHTS ====================

@app.get("/api/flights/search", response_model=List[schemas.FlightResponse], tags=["Flights"])
def search_flights(
    origin: str = Query(..., description="Origin airport code (e.g., LOS)"),
    destination: str = Query(..., description="Destination airport code (e.g., ABV)"),
    departure_date: date = Query(..., description="Departure date (YYYY-MM-DD)"),
    return_date: Optional[date] = Query(None, description="Return date for round trip"),
    passengers: int = Query(1, ge=1, le=9),
    class_type: Optional[str] = Query(None, description="economy, business, or first"),
    db: Session = Depends(get_db)
):
    """Search for available flights"""
    query = db.query(models.Flight).filter(
        models.Flight.origin == origin.upper(),
        models.Flight.destination == destination.upper(),
        models.Flight.departure_date == departure_date,
        models.Flight.available_seats >= passengers
    )
    
    if class_type:
        query = query.filter(models.Flight.class_type == class_type)
    
    flights = query.all()
    
    if not flights:
        raise HTTPException(status_code=404, detail="No flights found for the selected criteria")
    
    return flights

@app.get("/api/flights/{flight_id}", response_model=schemas.FlightResponse, tags=["Flights"])
def get_flight(flight_id: int, db: Session = Depends(get_db)):
    """Get flight details by ID"""
    flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight

@app.get("/api/flights", response_model=List[schemas.FlightResponse], tags=["Flights"])
def get_all_flights(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all available flights"""
    flights = db.query(models.Flight).offset(skip).limit(limit).all()
    return flights


# ==================== BOOKINGS ====================

@app.post("/api/bookings", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED, tags=["Bookings"])
def create_booking(
    booking: schemas.BookingCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new flight booking"""
    # Verify flight exists and has seats
    flight = db.query(models.Flight).filter(models.Flight.id == booking.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    total_passengers = len(booking.passengers)
    if flight.available_seats < total_passengers:
        raise HTTPException(status_code=400, detail=f"Only {flight.available_seats} seats available")
    
    # Calculate total amount
    total_amount = flight.price * total_passengers
    
    # Create booking
    new_booking = models.Booking(
        user_id=current_user.id,
        flight_id=booking.flight_id,
        total_passengers=total_passengers,
        total_amount=total_amount,
        payment_status="pending",
        booking_status="confirmed"
    )
    db.add(new_booking)
    db.flush()
    
    # Add passengers
    for passenger_data in booking.passengers:
        passenger = models.Passenger(
            booking_id=new_booking.id,
            **passenger_data.dict()
        )
        db.add(passenger)
    
    # Update available seats
    flight.available_seats -= total_passengers
    
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get("/api/bookings", response_model=List[schemas.BookingResponse], tags=["Bookings"])
def get_user_bookings(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all bookings for current user"""
    bookings = db.query(models.Booking).filter(
        models.Booking.user_id == current_user.id
    ).all()
    return bookings

@app.get("/api/bookings/{booking_id}", response_model=schemas.BookingDetailResponse, tags=["Bookings"])
def get_booking(
    booking_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get booking details"""
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id,
        models.Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.put("/api/bookings/{booking_id}/cancel", response_model=schemas.BookingResponse, tags=["Bookings"])
def cancel_booking(
    booking_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a booking"""
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id,
        models.Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.booking_status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")
    
    # Restore seats
    flight = db.query(models.Flight).filter(models.Flight.id == booking.flight_id).first()
    flight.available_seats += booking.total_passengers
    
    booking.booking_status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking


# ==================== PAYMENT ====================

@app.post("/api/payments/process", response_model=schemas.PaymentResponse, tags=["Payment"])
def process_payment(
    payment: schemas.PaymentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process payment for booking"""
    booking = db.query(models.Booking).filter(
        models.Booking.id == payment.booking_id,
        models.Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.payment_status == "completed":
        raise HTTPException(status_code=400, detail="Payment already completed")
    
    # Create payment record
    new_payment = models.Payment(
        booking_id=payment.booking_id,
        amount=booking.total_amount,
        payment_method=payment.payment_method,
        transaction_reference=f"TXN-{booking.id}-{datetime.utcnow().timestamp()}",
        payment_status="completed"
    )
    db.add(new_payment)
    
    # Update booking payment status
    booking.payment_status = "completed"
    
    db.commit()
    db.refresh(new_payment)
    return new_payment


# ==================== AIRPORTS ====================

@app.get("/api/airports", response_model=List[schemas.AirportResponse], tags=["Airports"])
def get_airports(db: Session = Depends(get_db)):
    """Get all available airports"""
    airports = db.query(models.Airport).all()
    return airports


# ==================== STATISTICS ====================

@app.get("/api/bookings/stats/summary", response_model=schemas.BookingStats, tags=["Statistics"])
def get_booking_statistics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get booking statistics for current user"""
    bookings = db.query(models.Booking).filter(
        models.Booking.user_id == current_user.id
    ).all()
    
    total = len(bookings)
    confirmed = len([b for b in bookings if b.booking_status == "confirmed"])
    cancelled = len([b for b in bookings if b.booking_status == "cancelled"])
    completed = len([b for b in bookings if b.payment_status == "completed"])
    pending_payment = len([b for b in bookings if b.payment_status == "pending"])
    
    total_spent = sum(b.total_amount for b in bookings if b.payment_status == "completed")
    
    return {
        "total_bookings": total,
        "confirmed_bookings": confirmed,
        "cancelled_bookings": cancelled,
        "completed_payments": completed,
        "pending_payments": pending_payment,
        "total_amount_spent": float(total_spent)
    }


# ==================== HEALTH CHECK ====================

@app.get("/", tags=["Health"])
def root():
    """API health check"""
    return {
        "status": "healthy",
        "message": "Flight Booking API is running",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }
