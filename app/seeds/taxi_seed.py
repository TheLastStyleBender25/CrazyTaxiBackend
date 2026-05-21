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

    taxis = [

        AvailableTaxi(
            id=1,
            taxi_type="basic taxi",
            price=0,
            fuel=100,
            fuel_cost_per_km=10,
            health=100,
            health_cost_per_km=10,
            base_fare_price=0
        ),

        AvailableTaxi(
            id=2,
            taxi_type="basic taxi",
            price=1000,
            fuel=150,
            fuel_cost_per_km=12,
            health=150,
            health_cost_per_km=12,
            base_fare_price=10
        ),

        AvailableTaxi(
            id=3,
            taxi_type="basic taxi",
            price=2500,
            fuel=250,
            fuel_cost_per_km=15,
            health=250,
            health_cost_per_km=15,
            base_fare_price=25
        ),

        AvailableTaxi(
            id=4,
            taxi_type="sports taxi",
            price=6000,
            fuel=500,
            fuel_cost_per_km=25,
            health=500,
            health_cost_per_km=25,
            base_fare_price=200
        ),

        AvailableTaxi(
            id=5,
            taxi_type="sports taxi",
            price=8500,
            fuel=700,
            fuel_cost_per_km=30,
            health=700,
            health_cost_per_km=30,
            base_fare_price=320
        ),

        AvailableTaxi(
            id=6,
            taxi_type="sports taxi",
            price=12000,
            fuel=1000,
            fuel_cost_per_km=38,
            health=950,
            health_cost_per_km=35,
            base_fare_price=450
        ),

        AvailableTaxi(
            id=7,
            taxi_type="luxury taxi",
            price=18000,
            fuel=1400,
            fuel_cost_per_km=45,
            health=1300,
            health_cost_per_km=40,
            base_fare_price=700
        ),

        AvailableTaxi(
            id=8,
            taxi_type="luxury taxi",
            price=25000,
            fuel=1800,
            fuel_cost_per_km=55,
            health=1700,
            health_cost_per_km=50,
            base_fare_price=1000
        ),

        AvailableTaxi(
            id=9,
            taxi_type="luxury taxi",
            price=35000,
            fuel=2500,
            fuel_cost_per_km=65,
            health=2400,
            health_cost_per_km=60,
            base_fare_price=1500
        ),

        AvailableTaxi(
            id=10,
            taxi_type="luxury taxi",
            price=50000,
            fuel=3200,
            fuel_cost_per_km=80,
            health=3000,
            health_cost_per_km=75,
            base_fare_price=2200
        ),

        AvailableTaxi(
            id=11,
            taxi_type="electric taxi",
            price=70000,
            fuel=5000,
            fuel_cost_per_km=35,
            health=4500,
            health_cost_per_km=30,
            base_fare_price=3200
        ),

        AvailableTaxi(
            id=12,
            taxi_type="electric taxi",
            price=95000,
            fuel=7000,
            fuel_cost_per_km=40,
            health=6500,
            health_cost_per_km=35,
            base_fare_price=4500
        ),

        AvailableTaxi(
            id=13,
            taxi_type="electric taxi",
            price=130000,
            fuel=9000,
            fuel_cost_per_km=48,
            health=8500,
            health_cost_per_km=40,
            base_fare_price=6000
        ),

        AvailableTaxi(
            id=14,
            taxi_type="legendary taxi",
            price=180000,
            fuel=12000,
            fuel_cost_per_km=70,
            health=11000,
            health_cost_per_km=60,
            base_fare_price=9000
        ),

        AvailableTaxi(
            id=15,
            taxi_type="legendary taxi",
            price=250000,
            fuel=16000,
            fuel_cost_per_km=90,
            health=15000,
            health_cost_per_km=80,
            base_fare_price=13000
        )
    ]

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
        ),

        RideMilestone(
            id=5,
            required_rides=1000,
            gem_reward=500
        ),

        RideMilestone(
            id=6,
            required_rides=2500,
            gem_reward=1200
        ),

        RideMilestone(
            id=7,
            required_rides=5000,
            gem_reward=2500
        ),

        RideMilestone(
            id=8,
            required_rides=10000,
            gem_reward=6000
        ),

        RideMilestone(
            id=9,
            required_rides=25000,
            gem_reward=15000
        ),

        RideMilestone(
            id=10,
            required_rides=50000,
            gem_reward=40000
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
        ),

        CityLevel(
            id=6,
            level=6,
            gems_required=450
        ),

        CityLevel(
            id=7,
            level=7,
            gems_required=650
        ),

        CityLevel(
            id=8,
            level=8,
            gems_required=900
        ),

        CityLevel(
            id=9,
            level=9,
            gems_required=1200
        ),

        CityLevel(
            id=10,
            level=10,
            gems_required=1600
        ),

        CityLevel(
            id=11,
            level=11,
            gems_required=2100
        ),

        CityLevel(
            id=12,
            level=12,
            gems_required=2800
        )
    ]


    db.add_all(taxis)
    db.add_all(milestones)
    db.add_all(city_levels)
    db.commit()

    print("Taxi and ride milestone seed completed")
