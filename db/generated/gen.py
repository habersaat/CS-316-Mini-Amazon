from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 200
num_products = 4000
num_purchases = 5000
num_reviews = 100
num_inventory = 200

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = []
    with open('ProductsGen2.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=3)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            description_short = fake.sentence(nb_words=10)
            description_long = fake.sentence(nb_words=200)
            rating = f'{str(fake.random_int(min=1,max=4))}.{str(fake.random_int(max=9))}'
            img_url = fake.image_url()
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, description_short, description_long, rating, img_url, price, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_carts(num_cart_items, available_pids):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for id in range(num_cart_items):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            writer.writerow([id, uid, pid])
        print(f'{num_cart_items} generated')

def gen_reviews(num_reviews, available_pids):
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for id in range(num_reviews):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            rating = fake.random_int(min=1, max=5)
            comment = fake.sentence(nb_words=10)
            timestamp = fake.date_time()
            upvotes = fake.random_int(min=0, max=100)
            writer.writerow([id, pid, uid, rating, comment, timestamp, upvotes])
        print(f'{num_reviews} generated')

def gen_inventory(num_inventory, available_pids, num_users):
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for inventory_id in range(num_inventory):
            if inventory_id % 100 == 0:
                print(f'{inventory_id}', end=' ', flush=True)
            sid = fake.random_int(min=0, max=num_users-1)  
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=0, max=100) 
            available = fake.boolean() 
            writer.writerow([inventory_id, sid, pid, quantity, available])
        print(f'{num_inventory} generated')


def main():
    num_inventory = 10000  # Or however many inventory items you want to generate
    num_users = 200  # This should match the number you used in gen_users
    available_pids = gen_products(num_products)  # This should be the list of available product IDs

    gen_users(num_users)
    gen_purchases(num_purchases, available_pids)
    gen_carts(num_purchases, available_pids)
    gen_reviews(num_reviews, available_pids)
    gen_inventory(num_inventory, available_pids, num_users)  # Pass the required arguments here

if __name__ == "__main__":
    main()
