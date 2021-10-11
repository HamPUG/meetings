import redis
r = redis.Redis(host="localhost", port=6379, db=0)
r.delete("l1") # make sure it doesn't exist
r.rpush("l1", "c", "b", "a")
print(r.llen("l1"))
print([x.decode() for x in r.lrange("l1", 0, -1)])
r.lpush("l1", 1, 2, 3)
print(r.llen("l1"))
print([x.decode() for x in r.lrange("l1", 0, -1)])
r.ltrim("l1", 2, 4)
print(r.llen("l1"))
print([x.decode() for x in r.lrange("l1", 0, -1)])
r.lset("l1", 0, 11)
print([x.decode() for x in r.lrange("l1", 0, -1)])
