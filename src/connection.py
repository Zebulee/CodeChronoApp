import requests

# URL de base du serveur
BASE_URL = 'http://localhost:3001'

# Créer un nouveau cours si n'existe pas
def create_course(course_code):
    response = requests.post(f'{BASE_URL}/courses', json={'course_name': course_code})
    print('Réponse pour le cours :', response.json())

# Créer un nouveau groupe si n'existe pas
def create_group(course_code, group_name):
    response = requests.post(f'{BASE_URL}/groups', json={'course_id': course_code, 'group_name': group_name})
    print('Réponse pour le groupe :', response.json())

# Envoyer une nouvelle scéance
def create_session(course_code, group_name, session_date):
    response = requests.post(f'{BASE_URL}/sessions', json={'course_id': course_code, 'group_id': group_name, 'session_date': session_date})
    print('Réponse pour la session :', response.json())

# Envoyer un code scanné
def send_scanned_code(session_date, barcode):
    response = requests.post(f'{BASE_URL}/scanned_codes', json={'session_date': session_date, 'barcode': barcode})
    print('Réponse pour le code scanné :', response.json())
