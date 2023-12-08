import faker
from datetime import datetime, timedelta
import random
import psycopg2

fake = faker.Faker()

def generate_timestamp_utc7():
    now = datetime.utcnow()
    offset = timedelta(hours=7)

    # Add the offset to the datetime object
    datetime_object_utc_plus_7 = now + offset

    return datetime_object_utc_plus_7.timestamp()

def generate_transaction():
    user = fake.simple_profile()
    return {
        'transaction_id': fake.uuid4(),
        'user_id': user['username'],
        'timestamp': generate_timestamp_utc7(),
        'amount': round(random.uniform(10,1000),2),
        'currency': random.choice(['USD', 'GBP']),
        'city': fake.city(),
        'country': fake.country(),
        'merchant_name': fake.company(),
        'payment_method': random.choice(['credit_card', 'debit_card', 'online_transfer']),
        'ip_address': fake.ipv4(),
        "voucher_code": random.choice(['', 'DISCOUNT10', '']),
        'affiliate_id': fake.uuid4()
    }

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255),
        timestamp TIMESTAMP,
        amount DECIMAL,
        currency VARCHAR(255),
        city VARCHAR(255),
        country VARCHAR(255),
        merchant_name VARCHAR(255),
        payment_method VARCHAR(255),
        ip_address VARCHAR(255),
        voucher_code VARCHAR(255),
        affiliate_id VARCHAR(255)
    )
    """)

    cursor.close()
    conn.commit()

if __name__=="__main__":
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='financial_db',
        user='postgres',
        password='postgres'
    )

    create_table(conn)

    transaction = generate_transaction()
    print(transaction)
    
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO transactions(transaction_id, user_id, timestamp, amount, currency, city, country, merchant_name, payment_method, 
        ip_address, voucher_code, affiliate_id)
        VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (transaction["transaction_id"], transaction["user_id"], datetime.fromtimestamp(transaction["timestamp"]).strftime('%Y-%m-%d %H:%M:%S'),
              transaction["amount"], transaction["currency"], transaction["city"], transaction["country"],
              transaction["merchant_name"], transaction["payment_method"], transaction["ip_address"],
              transaction["voucher_code"], transaction["affiliate_id"])
    )

    cursor.close()
    conn.commit()

