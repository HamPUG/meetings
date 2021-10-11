import redis

r = redis.Redis(host="localhost", port=6379, db=0)

# listen for predictions
def msg_handler(message):
    print(message["data"].decode())

p = r.pubsub()
p.psubscribe(**{"predictions": msg_handler})
p.run_in_thread(sleep_time=0.001)


# push through 3 images
images = [
    "./data/alpine_sea_holly/image_06969.jpg",
    "./data/anthurium/image_01964.jpg",
    "./data/artichoke/image_04081.jpg",
]
for image in images:
    print("--> %s" % image)
    with open(image, "rb") as f:
        data = f.read()
        r.publish("images", data)

