# Flight Booking API

**Complete flight reservation system** for Nigerian domestic flights with search, booking, payment processing, and user management.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🚀 Features

### Core Functionality
- ✅ **Flight Search** - Search flights by origin, destination, date, class
- ✅ **Real-time Availability** - Live seat availability tracking
- ✅ **Booking Management** - Create, view, cancel bookings
- ✅ **Multi-passenger Support** - Book for up to 9 passengers
- ✅ **Payment Processing** - Integrated payment system
- ✅ **User Authentication** - JWT-based secure authentication
- ✅ **Booking History** - Complete user booking records
- ✅ **Statistics Dashboard** - Booking analytics and insights

### Technical Features
- ✅ **RESTful API Design** - Industry-standard architecture
- ✅ **PostgreSQL Database** - Production-grade data storage
- ✅ **Docker Deployment** - Containerized for easy setup
- ✅ **Auto Documentation** - Interactive Swagger UI
- ✅ **Type Safety** - Pydantic validation models
- ✅ **Nigerian Airlines** - Pre-loaded with 8 local carriers
- ✅ **Nigerian Airports** - 10 major airports included
- ✅ **30 Days of Flights** - 2000+ sample flights

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Usage Examples](#usage-examples)
- [Testing Guide](#testing-guide)
- [Project Structure](#project-structure)

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Terminal access

### Setup (3 Simple Steps)

**Step 1: Navigate to project**
```bash
cd flight-booking-api
```

**Step 2: Start Docker containers**
```bash
docker-compose up --build
```

**Step 3: Seed database (in new terminal)**
```bash
docker exec flight_api python seed_data.py
```

**Done!** Your API is running at:
- **API:** http://localhost:8001
- **Docs:** http://localhost:8001/api/docs

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/token` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user info |

### Flights
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/flights/search` | Search available flights |
| GET | `/api/flights/{id}` | Get flight details |
| GET | `/api/flights` | List all flights |
| GET | `/api/airports` | List all airports |

### Bookings
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/bookings` | Create new booking |
| GET | `/api/bookings` | Get user bookings |
| GET | `/api/bookings/{id}` | Get booking details |
| PUT | `/api/bookings/{id}/cancel` | Cancel booking |
| GET | `/api/bookings/stats/summary` | Get booking statistics |

### Payment
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/process` | Process payment |

## 💡 Usage Examples

### 1. Register User

```bash
curl -X POST "http://localhost:8001/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "gabriel",
    "email": "gabriel@example.com",
    "password": "securepass123",
    "full_name": "Gabriel Oyetunji",
    "phone_number": "+2348012345678"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8001/api/auth/token" \
  -d "username=gabriel&password=securepass123"
```

**Save the token you receive!**

### 3. Search Flights

```bash
curl -X GET "http://localhost:8001/api/flights/search?origin=LOS&destination=ABV&departure_date=2026-02-01&passengers=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Create Booking

```bash
curl -X POST "http://localhost:8001/api/bookings" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "flight_id": 1,
    "passengers": [
      {
        "first_name": "Gabriel",
        "last_name": "Oyetunji",
        "date_of_birth": "1995-05-15",
        "gender": "male",
        "nationality": "Nigerian",
        "passport_number": "A12345678"
      }
    ]
  }'
```

### 5. Process Payment

```bash
curl -X POST "http://localhost:8001/api/payments/process" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 1,
    "payment_method": "card"
  }'
```

## 🧪 Testing Guide

### Using Swagger UI (Easiest)

1. Go to http://localhost:8001/api/docs
2. Click green "Authorize" button
3. Login to get token
4. Paste token in format: `Bearer YOUR_TOKEN`
5. Click "Authorize"
6. Now test all endpoints!

### Sample Test Flow

1. **Register** → Create account
2. **Login** → Get auth token
3. **Get Airports** → See available airports
4. **Search Flights** → Find LOS → ABV flights
5. **Create Booking** → Book a flight
6. **View Bookings** → See your bookings
7. **Process Payment** → Complete payment
8. **Get Statistics** → View booking stats

## 📁 Project Structure

```
flight-booking-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & routes
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   └── database.py          # Database configuration
├── seed_data.py             # Database seeding script
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🗄️ Database Schema

### Users
- Authentication and profile information
- Links to bookings

### Airports
- 10 Nigerian airports with IATA codes
- LOS, ABV, KAN, PHC, CBQ, IBA, ENU, BNI, MIU, ILR

### Airlines
- 8 Nigerian airlines
- Arik Air, Air Peace, Dana Air, etc.

### Flights
- 2000+ flights for next 30 days
- Multiple flights per route daily
- Economy, Business, First class
- Real Nigerian pricing (₦35,000 - ₦340,000)

### Bookings
- Links users to flights
- Passenger information
- Payment status tracking

### Payments
- Payment records
- Transaction references
- Payment method tracking

## 🎯 Nigerian Aviation Data

### Airports Included
- **LOS** - Lagos (Murtala Muhammed International)
- **ABV** - Abuja (Nnamdi Azikiwe International)
- **KAN** - Kano (Mallam Aminu Kano International)
- **PHC** - Port Harcourt International
- **CBQ** - Calabar (Margaret Ekpo International)
- **IBA** - Ibadan Airport
- **ENU** - Enugu (Akanu Ibiam International)
- **BNI** - Benin Airport
- **MIU** - Maiduguri International
- **ILR** - Ilorin International

### Airlines Included
- Arik Air (W3)
- Air Peace (P4)
- Dana Air (DA, 9J)
- Overland Airways (OJ)
- Aero Contractors (AJ)
- United Nigeria Airlines (UJ)
- Max Air (QM)

### Popular Routes
- Lagos ↔ Abuja
- Lagos ↔ Port Harcourt
- Lagos ↔ Kano
- Abuja ↔ Kano
- Abuja ↔ Port Harcourt
- Plus 11 more routes

## 🐳 Docker Commands

```bash
# Start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs api

# Seed database
docker exec flight_api python seed_data.py

# Access database
docker exec -it flight_postgres psql -U flightuser -d flightdb

# Restart API only
docker-compose restart api
```

## 🔐 Security Features

- **JWT Authentication** - Industry standard tokens
- **Password Hashing** - Bcrypt encryption
- **CORS Protection** - Configurable origins
- **Input Validation** - Pydantic models
- **SQL Injection Prevention** - SQLAlchemy ORM

## 📊 Business Logic

### Seat Management
- Automatic seat deduction on booking
- Seat restoration on cancellation
- Real-time availability updates

### Payment Flow
1. Create booking (status: pending)
2. Process payment
3. Update booking (status: completed)
4. Generate transaction reference

### Price Calculation
- Automatic calculation based on passengers
- Class-based pricing (Economy, Business, First)
- Real Nigerian market rates

## 🚀 Production Ready Features

- ✅ Environment variables
- ✅ Error handling
- ✅ Database migrations
- ✅ Type safety
- ✅ API documentation
- ✅ Docker deployment
- ✅ Logging
- ✅ Input validation

## 📈 Use Cases

### For Airlines
- Manage flight inventory
- Track bookings
- Process payments
- Customer management

### For Travel Agencies
- Search and compare flights
- Book multiple passengers
- Manage client bookings
- Payment processing

### For Passengers
- Search flights
- Compare prices
- Book tickets
- View booking history
- Cancel bookings

## 🎓 Learning Outcomes

This project demonstrates:
- RESTful API design
- Database modeling
- Authentication systems
- Payment processing
- Docker deployment
- Nigerian aviation domain knowledge
- Production-ready code structure

## 📝 API Response Examples

### Flight Search Response
```json
[
  {
    "id": 1,
    "flight_number": "W3245",
    "origin": "LOS",
    "destination": "ABV",
    "departure_date": "2026-02-01",
    "departure_time": "08:30:00",
    "arrival_date": "2026-02-01",
    "arrival_time": "09:45:00",
    "duration_minutes": 75,
    "class_type": "economy",
    "price": "45000.00",
    "available_seats": 142,
    "aircraft_type": "Boeing 737-800"
  }
]
```

### Booking Response
```json
{
  "id": 1,
  "booking_reference": null,
  "user_id": 1,
  "flight_id": 1,
  "total_passengers": 1,
  "total_amount": "45000.00",
  "booking_status": "confirmed",
  "payment_status": "pending",
  "created_at": "2026-01-14T10:00:00"
}
```

## 🔧 Troubleshooting

### Port Already in Use
Ports 8001 (API) and 5433 (DB) are used. If conflicts occur:
```bash
# Edit docker-compose.yml ports section
# Change 8001:8000 to 8002:8000
# Change 5433:5432 to 5434:5432
```

### Database Not Seeding
```bash
# Reset and reseed
docker-compose down -v
docker-compose up --build
docker exec flight_api python seed_data.py
```

## 👤 Author

**Gabriel Oyetunji**
- Backend Python Developer
- Machine Learning Engineer
- Email: gabrieloyetunji25@gmail.com
- Portfolio: https://gabriel-portfolio-orpin.vercel.app
- GitHub: [@GabrielOyetunji](https://github.com/GabrielOyetunji)

## 📜 License

This project is available for portfolio use.

---

**Built with FastAPI + PostgreSQL + Docker 🚀**

*Designed for Flyme - Nigerian Flight Booking System*
