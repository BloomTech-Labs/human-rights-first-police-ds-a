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
