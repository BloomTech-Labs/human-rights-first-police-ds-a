from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import redis, os, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def ping():
    try:
        conn = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            #password=os.getenv('REDIS_TOKEN'), 
            socket_connect_timeout=1
            )

        print(conn)
        conn.ping()
        logging.info('Connected!')
    except Exception as ex:
        logging.error('Failed to connect, terminating.')


class DistributedLock(object):

    def __init__(self, host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT')):
        self.conn = redis.Redis(host=host, port=port, db=0)

    def lock(self, key, exp):
        res = self.conn.set(key, 1, exp, nx=True)
        if res == True:
            return True

    def unlock(self, key):
        res = self.conn.delete(key)
        if res > 0:
            return True

        return False

lock = DistributedLock()
# print("unlocking", lock.unlock("rowentest"))
# print("locking", lock.lock("rowentest", 5))
# print("locking", lock.lock("rowentest", 5))
# print("unlocking", lock.unlock("rowentest"))
# print("locking", lock.lock("rowentest", 5))
# print("locking", lock.lock("rowentest", 5))
