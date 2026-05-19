import uuid
import random, json
from rsa import key
from app.models import Player
from app.core.config import RIDE_REWARD_MULTIPLIER, POINTS_PER_CITY_LEVEL, MAX_RIDE_POOL_SIZE, RIDE_REFRESH_INTERVAL, RIDE_EXPIRATION_SECONDS
from app.core.redis_client import redis_cl
from app.core.logger import logger

def generate_ride(db, current_user):
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    max_point = player.current_city_unlocked * POINTS_PER_CITY_LEVEL
    max_point -= 1
    pickup_point = random.randint(0, max_point)
    drop_point = random.randint(0, max_point)
    while pickup_point == drop_point:
        drop_point = random.randint(0, max_point)

    distance = abs(drop_point - pickup_point)
    reward = distance * RIDE_REWARD_MULTIPLIER
    ride = {"ride_id": str(uuid.uuid4()), "pickup_point": pickup_point, "drop_point": drop_point, "reward": reward}

    return ride

def generate_ride_pool(dn, current_user, pool_size = MAX_RIDE_POOL_SIZE):
    rides = []
    for i in range(pool_size):
        ride = generate_ride(dn, current_user)
        rides.append(ride)

    redis_key = (f"ride_pool:{current_user.id}")
    ##redis store strings not python lis/dictionary so we convert python object to string using dump
    try:
        redis_cl.setex(redis_key, 600, json.dumps(rides))
    except Exception as e:
        logger.error(f"redis failed {str(e)}")

    return rides

def get_ride_pool(current_user):
    redis_key = (f"ride_pool:{current_user.id}")
    rides = None
    try:
        rides = redis_cl.get(redis_key)
    except Exception as e:
        logger.error(f"redis failed {str(e)}")
    if not rides:
        logger.info(f"ride pool not found")
        return []
    return json.loads(rides) ##back to pyton object

def refresh_ride_pool(db, current_user):
    rides = get_ride_pool(current_user)
    remove_count = (MAX_RIDE_POOL_SIZE // 2)
    remove_rides = rides[:remove_count]
    remaining_rides = rides[remove_count:]

    new_rides = []
    for i in range(remove_count):
        ride = generate_ride(db, current_user)
        new_rides.append(ride)

    updated_pool = remaining_rides + new_rides
    redis_key = (f"ride_pool:{current_user.id}")
    try:
        redis_cl.setex(redis_key, 600, json.dumps(updated_pool))
    except Exception as e:
        logger.error(f"redis failed {str(e)}")

    return updated_pool

def get_active_rides(current_user):
    redis_key = (f"active_rides:{current_user.id}")
    rides = None
    try:
        rides = redis_cl.get(redis_key)
    except Exception as e:
        logger.error(f"redis failed {str(e)}")
    if not rides:
        logger.info(f"no active rides")
        return []
    return json.loads(rides)

def accept_ride(db, current_user, taxi_id, ride_id):
    ride_pool = get_ride_pool(current_user)
    selected_ride = None
    for ride in ride_pool:
        if ride["ride_id"] == ride_id:
            selected_ride = ride
            break
    if not selected_ride:
        logger.error(f"Ride not found: {ride_id}")
        raise ValueError("ride not found")
    active_rides = get_active_rides(current_user)
    for active_ride in active_rides:
        if active_ride.get("taxi_id") == taxi_id:
            logger.error(f"taxi is busy: {active_ride}")
            raise ValueError("taxi is busy")

    updated_pool = []
    for ride in ride_pool:
        if ride["ride_id"] != ride_id:
            updated_pool.append(ride)

    selected_ride["taxi_id"] = taxi_id

    active_rides.append(selected_ride)

    try:
        redis_cl.setex(f"ride_pool:{current_user.id}", 600, json.dumps(updated_pool))
        redis_cl.setex(f"active_rides:{current_user.id}", 1800, json.dumps(active_rides))
    except Exception as e:
        logger.error(f"redis failed {str(e)}")

    return {"updated_pool": updated_pool, "active_rides": active_rides, "accepted_ride": selected_ride}

def complete_rides(db, current_user, completed_rides):
    active_rides = get_active_rides(current_user)
    player = db.query(Player).filter(Player.user_id == current_user.id).first()
    completed = []
    remaining_active_rides = []
    total_reward = 0
    for active in active_rides:
        ride_completed = False
        for completed_ride in completed_rides:
            if (completed_ride.get("ride_id") == active.get("ride_id") and completed_ride.get("taxi_id") == active.get("taxi_id")):
                reward = completed_ride.get("reward", 0)
                total_reward += reward
                ride_completed = True
                active["reward"] = reward
                completed.append({
                    "ride_id": active.get("ride_id"),
                    "pickup_point": active.get("pickup_point"),
                    "drop_point": active.get("drop_point"),
                    "reward": reward,
                    "taxi_id": active.get("taxi_id")
                })
                break
        if not ride_completed:
            remaining_active_rides.append(active)

    player.coins += total_reward
    player.total_rides_completed += len(completed)
    db.commit()
    try:
        redis_cl.setex(f"active_rides:{current_user.id}", 1800, json.dumps(remaining_active_rides))
    except Exception as e:
        logger.error(f"redis failed {str(e)}")

    return { "completed_rides": completed, "coins": player.coins, "reward_earned": total_reward }
