import json
from faker import Faker

fake = Faker()
fixtures = []

for _ in range(100):
    valor = fake.random_int(min=0, max=100)
    fecha_hora = fake.date_time_this_year()

    fixture = {
        "model": "SIL.IntensidadDeLuz",
        "pk": None,
        "fields": {
            "valor": valor,
            "planta_id": 1,
            "fecha_hora": fecha_hora.isoformat()
        }
    }

    fixtures.append(fixture)

with open('apps/SIL/fixtures/sil_intensidad.json', 'w') as file:
    json.dump(fixtures, file)
