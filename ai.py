import face_recognition
import os
import numpy

# yeah so basically all of this code is a modified version of code taken from Sentdex so credit to him
# (https://pythonprogramming.net/facial-recognition-python/)
# also check out his youtube at https://www.youtube.com/c/sentdex

KNOWN_FACES_DIR = 'Kenobi_pics'
TOLERANCE = 0.52
MODEL = "hog" 


def get_kenobi_encodings():
    
    known_faces = []
    
 
    for filename in os.listdir(f'{KNOWN_FACES_DIR}'):
        print(filename)
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{filename}')
        print(image)
        encoding = face_recognition.face_encodings(image)[0]

        known_faces.append(encoding)
    
    known_faces = numpy.array(known_faces)
    numpy.save("kenobi_face_encodings.npy", known_faces)


def scan_image(image):

    try:
        known_faces = list(numpy.load("kenobi_face_encodings.npy"))

        locations = face_recognition.face_locations(image, model=MODEL)

        encodings = face_recognition.face_encodings(image, locations)


        print(f'-> Found {len(encodings)} face(s)')
        for face_encoding, face_location in zip(encodings, locations):

            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

            match = None
            if True in results:
                print("-> KenobIdentified")
                return True
            else:
                print("-> No Kenobi detected")
                return False
    except:
        print("-> No faces found")
        return False
