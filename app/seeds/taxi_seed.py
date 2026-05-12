from app.db.session import SessionLocal
from app.models import AvailableTaxi, RideMilestone, CityLevel

def seed_taxis():
    db = SessionLocal()
    existing = db.query(AvailableTaxi).first()
    exist = db.query(RideMilestone).first()
    ex = db.query(CityLevel).first()
    if existing and exist:
        print("seeds already available")
        return

    taxis = [AvailableTaxi( id = 1, taxi_type = "basic taxi", price = 0, fuel = 100, fuel_cost_per_km = 10,health = 100, health_cost_per_km = 10, base_fare_price = 0),
             AvailableTaxi(id = 2, taxi_type = "basic taxi", price = 1000, fuel = 100, fuel_cost_per_km = 10,health = 100, health_cost_per_km = 10, base_fare_price = 0),
             AvailableTaxi(id = 3, taxi_type = "basic taxi", price = 2500, fuel = 100, fuel_cost_per_km = 10,health = 100, health_cost_per_km = 10, base_fare_price = 20),
             AvailableTaxi(id = 4, taxi_type = "sports taxi", price = 6000, fuel = 500, fuel_cost_per_km = 25,health = 500, health_cost_per_km = 25, base_fare_price = 200),
             AvailableTaxi(id = 5, taxi_type = "luxury taxi", price = 9000, fuel = 800, fuel_cost_per_km = 40,health = 800, health_cost_per_km = 40, base_fare_price = 350)]

    milestones = [

        RideMilestone(
            id=1,
            required_rides=10,
            gem_reward=5
        ),

        RideMilestone(
            id=2,
            required_rides=50,
            gem_reward=20
        ),

        RideMilestone(
            id=3,
            required_rides=100,
            gem_reward=50
        ),

        RideMilestone(
            id=4,
            required_rides=500,
            gem_reward=200
        )
    ]

    city_levels = [

        CityLevel(
            id=1,
            level=1,
            gems_required=0
        ),

        CityLevel(
            id=2,
            level=2,
            gems_required=60
        ),

        CityLevel(
            id=3,
            level=3,
            gems_required=100
        ),

        CityLevel(
            id=4,
            level=4,
            gems_required=200
        ),

        CityLevel(
            id=5,
            level=5,
            gems_required=300
        )
    ]

    db.add_all(taxis)
    db.add_all(milestones)
    db.add_all(city_levels)
    db.commit()

    print("Taxi and ride milestone seed completed")