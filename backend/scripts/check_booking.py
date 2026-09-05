import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv('backend/.env')
p = urlparse(os.getenv('DATABASE_URL'))
conn = psycopg2.connect(dbname=p.path.lstrip('/'), user=p.username, password=p.password, host=p.hostname, port=p.port)
cur = conn.cursor()

cur.execute("SELECT id, booking_reference, customer_id, service_name, status, cancellation_reason FROM bookings WHERE id = 'dc3aaad7-9eda-4c10-b5ba-061413c690b3';")
row = cur.fetchone()
print("Booking row:", row)

cur.close()
conn.close()
