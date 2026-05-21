from app.models import Player, CityLevel
from app.core.logger import logger

def unlock_next_city(db, player):
    next_level = player.current_city_unlocked + 1
    city = db.query(CityLevel).filter(CityLevel.level == next_level).first()
    if not city:
        logger.error(f"no city to unlocked: {player.current_city_unlocked}")
        raise ValueError("No more cities available")
    if player.gems < city.gems_required:
        logger.error(f"gems required: {player.gems}")
        raise ValueError("Not enough gems")
    player.gems -= city.gems_required
    player.current_city_unlocked = next_level
    db.commit()

    return {
        "message": "City unlocked",
        "current_city_unlocked": player.current_city_unlocked,
        "remaining_gems": player.gems
    }



def get_city_level_all(db):
    cities = db.query(CityLevel).filter(CityLevel.level > 0).all()
    if not cities:
        logger.error(f"no cities found")
        raise ValueError("No cities found")

    return cities
