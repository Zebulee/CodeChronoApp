import socketio

# Initialiser un client Socket.IO
sio = socketio.Client()

# Variables pour les données à envoyer
course_name = 'Physique Avancée'
course_id = 1
group_name = 'Groupe B'
group_id = 2
session_date = '2024-10-27'
session_id = 1
barcode = '9876543210987'

# Connexion au serveur WebSocket
sio.connect('http://localhost:3001')

# Gérer la connexion
@sio.event
def connect():
    print('Connecté au serveur WebSocket')

    # Exemple d'envoi de données en utilisant des variables
    # Envoyer un nouveau cours
    sio.emit('add_data', {
        'type': 'add_course',
        'course_name': course_name
    })

    # Envoyer un nouveau groupe
    sio.emit('add_data', {
        'type': 'add_group',
        'course_id': course_id,
        'group_name': group_name
    })

    # Envoyer une nouvelle session
    sio.emit('add_data', {
        'type': 'add_session',
        'course_id': course_id,
        'group_id': group_id,
        'session_date': session_date
    })

    # Envoyer un code scanné
    sio.emit('add_data', {
        'type': 'add_scanned_code',
        'session_id': session_id,
        'barcode': barcode
    })

# Gérer la déconnexion
@sio.event
def disconnect():
    print('Déconnecté du serveur WebSocket')

# Maintenir la connexion ouverte
sio.wait()
