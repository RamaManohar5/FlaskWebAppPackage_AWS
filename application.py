from webAPI import application
import os

if __name__ == "__main__" :
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    application.run(HOST, PORT, debug=True)
