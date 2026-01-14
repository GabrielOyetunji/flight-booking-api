# 🚀 QUICK SETUP GUIDE

## Setup in 4 Steps

### 1. Extract Project
```bash
# Navigate to the extracted folder
cd flight-booking-api
```

### 2. Start Docker Services
```bash
docker-compose up --build
```

**Wait for:** `INFO: Application startup complete`

### 3. Seed Database (New Terminal)
```bash
docker exec -it flight_api python seed_data.py
```

### 4. Test API
Open browser: **http://localhost:8001/api/docs**

---

## First Test

1. **Register User**
   - Click POST `/api/auth/register`
   - Try it out
   - Use: `gabriel` / `gabriel@test.com` / `testpass123`

2. **Login**
   - Click POST `/api/auth/token`
   - Username: `gabriel`, Password: `testpass123`
   - **COPY THE TOKEN**

3. **Authorize**
   - Click green "Authorize" button (top right)
   - Enter: `Bearer YOUR_TOKEN_HERE`
   - Click "Authorize"

4. **Search Flights**
   - Click POST `/api/flights/search`
   - Try: `origin=Lagos&destination=London`
   - See available flights!

5. **Create Booking**
   - Click POST `/api/bookings`
   - Use a flight_id from search results
   - Add passenger details
   - Create booking!

---

## Ports

- **API:** http://localhost:8001
- **Database:** localhost:5433

**Note:** Different from Task Management API (port 8000) to avoid conflicts!

---

## Admin Access

- **Username:** admin
- **Password:** admin123
- Can create flights, airports, airlines

---

## Troubleshooting

**Database not seeded?**
```bash
docker exec -it flight_api python seed_data.py
```

**Port conflict?**
Edit `docker-compose.yml`:
- Change `8001:8000` to `8002:8000`
- Change `5433:5432` to `5434:5432`

**Start fresh?**
```bash
docker-compose down -v
docker-compose up --build
docker exec -it flight_api python seed_data.py
```

---

## What You Built

✅ Complete flight booking system  
✅ 300+ flights across 10 airports  
✅ Real-time seat availability  
✅ Multi-passenger bookings  
✅ Payment processing (mock)  
✅ JWT authentication  
✅ Admin features  

**This is YOUR Flyme proof-of-concept!** 🎯
