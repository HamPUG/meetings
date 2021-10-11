import redis
r = redis.Redis(host="localhost", port=6379, db=0)

def msg_handler(message):
    print(message)

p = r.pubsub()
p.psubscribe(**{"my_*": msg_handler})
p.run_in_thread(sleep_time=0.001)

