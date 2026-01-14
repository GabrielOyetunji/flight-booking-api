"""
Seed Database with Sample Data
Populates database with Nigerian airports, airlines, and flights
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time
from decimal import Decimal
import random

from app import models, database


def seed_airports(db: Session):
    """Seed Nigerian airports"""
    airports = [
        {"code": "LOS", "name": "Murtala Muhammed International Airport", "city": "Lagos", "country": "Nigeria"},
        {"code": "ABV", "name": "Nnamdi Azikiwe International Airport", "city": "Abuja", "country": "Nigeria"},
        {"code": "KAN", "name": "Mallam Aminu Kano International Airport", "city": "Kano", "country": "Nigeria"},
        {"code": "PHC", "name": "Port Harcourt International Airport", "city": "Port Harcourt", "country": "Nigeria"},
        {"code": "CBQ", "name": "Margaret Ekpo International Airport", "city": "Calabar", "country": "Nigeria"},
        {"code": "IBA", "name": "Ibadan Airport", "city": "Ibadan", "country": "Nigeria"},
        {"code": "ENU", "name": "Akanu Ibiam International Airport", "city": "Enugu", "country": "Nigeria"},
        {"code": "BNI", "name": "Benin Airport", "city": "Benin City", "country": "Nigeria"},
        {"code": "MIU", "name": "Maiduguri International Airport", "city": "Maiduguri", "country": "Nigeria"},
        {"code": "ILR", "name": "Ilorin International Airport", "city": "Ilorin", "country": "Nigeria"},
    ]
    
    for airport_data in airports:
        airport = models.Airport(**airport_data)
        db.add(airport)
    
    db.commit()
    print("✅ Seeded 10 Nigerian airports")


def seed_airlines(db: Session):
    """Seed Nigerian airlines"""
    airlines = [
        {"code": "W3", "name": "Arik Air", "country": "Nigeria"},
        {"code": "P4", "name": "Air Peace", "country": "Nigeria"},
        {"code": "DA", "name": "Dana Air", "country": "Nigeria"},
        {"code": "OJ", "name": "Overland Airways", "country": "Nigeria"},
        {"code": "AJ", "name": "Aero Contractors", "country": "Nigeria"},
        {"code": "9J", "name": "Dana Air", "country": "Nigeria"},
        {"code": "UJ", "name": "United Nigeria Airlines", "country": "Nigeria"},
        {"code": "QM", "name": "Max Air", "country": "Nigeria"},
    ]
    
    for airline_data in airlines:
        airline = models.Airline(**airline_data)
        db.add(airline)
    
    db.commit()
    print("✅ Seeded 8 Nigerian airlines")


def seed_flights(db: Session):
    """Seed flights for next 30 days"""
    airlines = db.query(models.Airline).all()
    airports = db.query(models.Airport).all()
    
    airport_codes = [a.code for a in airports]
    
    # Popular routes in Nigeria
    routes = [
        ("LOS", "ABV"),  # Lagos to Abuja
        ("ABV", "LOS"),  # Abuja to Lagos
        ("LOS", "PHC"),  # Lagos to Port Harcourt
        ("PHC", "LOS"),  # Port Harcourt to Lagos
        ("ABV", "KAN"),  # Abuja to Kano
        ("KAN", "ABV"),  # Kano to Abuja
        ("LOS", "KAN"),  # Lagos to Kano
        ("KAN", "LOS"),  # Kano to Lagos
        ("ABV", "PHC"),  # Abuja to Port Harcourt
        ("PHC", "ABV"),  # Port Harcourt to Abuja
        ("LOS", "ENU"),  # Lagos to Enugu
        ("ENU", "LOS"),  # Enugu to Lagos
        ("LOS", "CBQ"),  # Lagos to Calabar
        ("CBQ", "LOS"),  # Calabar to Lagos
        ("ABV", "ENU"),  # Abuja to Enugu
        ("ENU", "ABV"),  # Enugu to Abuja
    ]
    
    flight_count = 0
    
    # Generate flights for next 30 days
    for day_offset in range(30):
        flight_date = date.today() + timedelta(days=day_offset)
        
        for origin, destination in routes:
            # 3-5 flights per route per day
            num_flights = random.randint(3, 5)
            
            for _ in range(num_flights):
                airline = random.choice(airlines)
                
                # Random departure time (6 AM to 10 PM)
                dep_hour = random.randint(6, 22)
                dep_minute = random.choice([0, 15, 30, 45])
                departure_time_obj = time(dep_hour, dep_minute)
                
                # Flight duration (45 min to 2 hours for Nigerian domestic)
                duration = random.randint(45, 120)
                
                # Calculate arrival
                dep_datetime = datetime.combine(flight_date, departure_time_obj)
                arr_datetime = dep_datetime + timedelta(minutes=duration)
                arrival_date = arr_datetime.date()
                arrival_time_obj = arr_datetime.time()
                
                # Random class types
                class_types = ["economy", "economy", "economy", "business"]  # More economy flights
                class_type = random.choice(class_types)
                
                # Pricing based on class
                base_price = random.randint(35000, 85000)  # Nigerian Naira
                if class_type == "business":
                    price = base_price * 2.5
                elif class_type == "first":
                    price = base_price * 4
                else:
                    price = base_price
                
                # Seat capacity
                if class_type == "economy":
                    total_seats = random.randint(120, 180)
                elif class_type == "business":
                    total_seats = random.randint(20, 40)
                else:
                    total_seats = random.randint(8, 16)
                
                available_seats = random.randint(int(total_seats * 0.3), total_seats)
                
                # Aircraft types
                aircraft_types = ["Boeing 737-800", "Airbus A320", "Boeing 737-500", "Embraer E195"]
                aircraft = random.choice(aircraft_types)
                
                # Flight number
                flight_number = f"{airline.code}{random.randint(100, 999)}"
                
                flight = models.Flight(
                    flight_number=flight_number,
                    airline_id=airline.id,
                    origin=origin,
                    destination=destination,
                    departure_date=flight_date,
                    departure_time=departure_time_obj,
                    arrival_date=arrival_date,
                    arrival_time=arrival_time_obj,
                    duration_minutes=duration,
                    class_type=class_type,
                    price=Decimal(str(price)),
                    total_seats=total_seats,
                    available_seats=available_seats,
                    aircraft_type=aircraft,
                    status="scheduled"
                )
                db.add(flight)
                flight_count += 1
    
    db.commit()
    print(f"✅ Seeded {flight_count} flights for next 30 days")


def main():
    """Run all seed functions"""
    print("🌱 Starting database seeding...")
    
    # Create tables
    models.Base.metadata.create_all(bind=database.engine)
    
    db = database.SessionLocal()
    
    try:
        # Check if already seeded
        existing_airports = db.query(models.Airport).count()
        if existing_airports > 0:
            print("⚠️  Database already seeded. Skipping...")
            return
        
        seed_airports(db)
        seed_airlines(db)
        seed_flights(db)
        
        print("✅ Database seeding completed successfully!")
        print(f"   - Airports: {db.query(models.Airport).count()}")
        print(f"   - Airlines: {db.query(models.Airline).count()}")
        print(f"   - Flights: {db.query(models.Flight).count()}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
