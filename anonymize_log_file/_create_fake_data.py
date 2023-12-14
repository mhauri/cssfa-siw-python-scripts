import csv
import faker
fake = faker.Faker()

data = []

for _ in range(50):
    date = fake.date_time()
    name = fake.name()
    postcode = fake.postcode()
    city = fake.city()
    email = fake.email()
    phone = fake.phone_number()
    ip_address = fake.ipv4()
    data.append([date, name, postcode, city, phone, email, ip_address])

# Schreiben der Daten in eine CSV-Datei
with open('log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
