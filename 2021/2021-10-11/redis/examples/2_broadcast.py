import redis
r = redis.Redis(host="localhost", port=6379, db=0)
r.publish("my_channel1", "1st message")
r.publish("my_channel2", "2nd message")
