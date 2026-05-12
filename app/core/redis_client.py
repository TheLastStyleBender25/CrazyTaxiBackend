import redis

redis_cl = redis.Redis(host='localhost', port=6379, decode_responses=True)