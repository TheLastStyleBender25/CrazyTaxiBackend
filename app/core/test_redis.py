from app.core.redis_client import redis_cl

redis_cl.flushall()
print("flushing completed")