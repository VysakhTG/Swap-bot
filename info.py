import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

SESSION = environ.get('SESSION', 'Feewoss')
API_ID = int(20980764)
API_HASH = "e7ee72bff6d00b1e00987f968136b7e8"
PORT = environ.get("PORT", "8080")
STRING = "AQG2XXUAA0qVwJIIrUUgJ_9x9GQhGWecm6FOU7JumqqoNW77DaUuCC3DqBdvRjrjFvAOhIVkVtW8ikw0IU5bE08yQo7HOj8u-EdnYaPwxhlZNse0WZTg_4BTuzKe585QF2o3q0f-wwQOy54dC4Bw8pIK5EHFvk6JpmkrVeRSi5GEbzfb4MXLsW986TyqNYYl2jL0WwZyukQfu0M5zZDpLNs48VlqIZ374mXRZnqNuF9lykqiltqURAIKWQxaU4KNZvrEpyFqic1Tl5NGM_V09Bf_8Ti0Q6NrBeVkDBHWrSQT8j50ZFZfeUDwbhM0w5sVvbkVDygQhbJMuXbMcd1LYcw0_ym02AAAAAFzL2EnAA"
CHANNEL = int(-1001806747214)

ADMINS = [
    int(admin) if id_pattern.search(admin) else admin
    for admin in environ.get('ADMINS', '6123610560, 6452804256, 5274370570').split(',')
]
