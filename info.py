import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

SESSION = environ.get('SESSION', 'Filee')
API_ID = int(19106809)
API_HASH = "1f47808d3d6bae5292a78665bf42fc5b"
PORT = environ.get("PORT", "8080")
STRING = "AQEji_kAIwiyCaixbmc3wpqY8DU3udVlJ8e-fYyeiwRLzDh5s5J4TZRzk9H1R84FvWtHZjCQGI3SnLhLQUUA1GAmD7hOjmIn7GPBNvIFywM163IazUHusKX9dSxM4G34nY5hvdvdOkEvSPWerlyL0I0_Bmb0zsBBEiEI_mrty5Dj_iFoibGdQBBuHR3Wa-8zERL4TM1BxMRCMmmNSDipT6Wuy-buLxyCKByCZxZrRBN5TVmJ1MJAvyS5b17J7lnIjLcUBxODWsrrdNZ2veQFRMqmBJD5RviVKT1nQKrQ8srQ4BVldKSrL6LGDcd5DtLP-JN7NAh6ra-22NBeTrTe3UJcziAv_wAAAAExZgYZAA"
CHANNEL = int(-1001806747214)

ADMINS = [
    int(admin) if id_pattern.search(admin) else admin
    for admin in environ.get('ADMINS', '6123610560, 6452804256, 5274370570').split(',')
]
