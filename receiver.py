import redis
import strands

s0 = strands.Strand(160) # 5*32 = 160
s1 = strands.Strand(160)
s2 = strands.Strand(160)
s3 = strands.Strand(160)
s4 = strands.Strand(160)
sm = strands.StrandManager(screen, height, width)

def main():

    r = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe("beats")
    for msg in p.listen():
        data = msg["data"]

        # three options -
        # 1. "Beat"
        # 2. "noteoctave:{A-F},{1-7}"
        # 3. "{0-20}" (A number 0-20)
        print(data)

main()
