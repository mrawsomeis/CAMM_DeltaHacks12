import cv2 
import numpy as np
import pickle
import os
import keyboard

testing = True

script_dir = os.path.dirname(os.path.abspath(__file__))

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
id_to_name = {}

def getFace():
    global id_to_name
    
    model_path = os.path.join(script_dir, 'trained_model.yml')
    pkl_path = os.path.join(script_dir, 'id_to_name.pkl')
    
    if not os.path.exists(model_path):
        return None
    
    recognizer.read(model_path)
    
    if os.path.exists(pkl_path):
        with open(pkl_path, 'rb') as f:
            id_to_name = pickle.load(f)
    
    cap = cv2.VideoCapture(0)
    
    detected_id = None
    start_time = cv2.getTickCount()
    timeout = 0.5
    
    while detected_id is None:
        ret, img = cap.read()
        
        if not ret:
            break
        
        elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
        if elapsed > timeout:
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))
            
            predicted_id, confidence = recognizer.predict(face_roi)
            
            if confidence < 50:
                detected_id = id_to_name.get(predicted_id)
                break
    
    cap.release()
    cv2.destroyAllWindows()
    
    return detected_id
    
def generate_unique_id():
    import random
    import string
    
    training_dir = os.path.join(script_dir, 'training_data')
    
    existing_ids = set()
    if os.path.exists(training_dir):
        existing_ids = set(os.listdir(training_dir))
    
    while True:
        unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if unique_id not in existing_ids:
            return unique_id

def save_registry(person_id, note=""):
    registry_file = os.path.join(script_dir, 'registry.txt')
    
    with open(registry_file, 'a') as f:
        timestamp = cv2.getTickCount()
        f.write(f"{person_id}|{note}|{timestamp}\n")
    
    print(f"ID saved to {registry_file}")

def view_registry():
    registry_file = os.path.join(script_dir, 'registry.txt')
    
    if not os.path.exists(registry_file):
        print("No registry file found. No people registered yet.")
        return
    
    print("\n" + "="*60)
    print("REGISTERED PEOPLE")
    print("="*60)
    
    with open(registry_file, 'r') as f:
        lines = f.readlines()
        
    if not lines:
        print("No people registered yet.")
        return
    
    for i, line in enumerate(lines, 1):
        parts = line.strip().split('|')
        person_id = parts[0]
        note = parts[1] if len(parts) > 1 else ""
        
        print(f"{i}. ID: {person_id}")
        if note:
            print(f"   Note: {note}")
        print()

def capture_training_data():
    unique_id = generate_unique_id()
    
    training_dir = os.path.join(script_dir, 'training_data')
    person_dir = os.path.join(training_dir, unique_id)
    
    if not os.path.exists(training_dir):
        os.makedirs(training_dir)
    
    os.makedirs(person_dir)
    
    cap = cv2.VideoCapture(0)
    
    print(f"\n{'='*50}")
    print(f"Assigned ID: {unique_id}")
    print(f"{'='*50}")
    print("Look at the camera and move your head slightly between captures")
    print("Press SPACE to capture a photo, or 'q' to finish early")
    
    count = 0
    max_photos = 30
    
    while count < max_photos:
        ret, img = cap.read()
        
        if not ret:
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        display_img = img.copy()
        
        for (x, y, w, h) in faces:
            cv2.rectangle(display_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.putText(display_img, f"Photos: {count}/{max_photos}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(display_img, "Press SPACE to capture", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Capture Training Data', display_img)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            if len(faces) > 0:
                photo_path = os.path.join(person_dir, f'photo_{count}.jpg')
                cv2.imwrite(photo_path, img)
                count += 1
                print(f"Captured photo {count}/{max_photos}")
            else:
                print("No face detected! Try again.")
        
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if count == 0:
        print(f"\nNo photos captured. Deleting folder and not saving to registry.")
        os.rmdir(person_dir)
        return None
    
    print(f"\n{'='*50}")
    print(f"Successfully captured {count} photos!")
    print(f"Person ID: {unique_id}")
    print(f"{'='*50}")
    
    save_registry(unique_id)
    
    return unique_id

def train_recognizer():
    faces = []
    labels = []
    current_id = 0
    
    training_dir = os.path.join(script_dir, 'training_data')
    
    if not os.path.exists(training_dir):
        print(f"No training data found! Run capture_training_data() first.")
        return False
    
    for person_name in os.listdir(training_dir):
        person_path = os.path.join(training_dir, person_name)
        
        if not os.path.isdir(person_path):
            continue
            
        id_to_name[current_id] = person_name
        print(f"Training on {person_name} (ID: {current_id})...")
        
        for image_name in os.listdir(person_path):
            if not image_name.endswith('.jpg'):
                continue
                
            image_path = os.path.join(person_path, image_name)
            
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            if img is None:
                continue
            
            detected_faces = face_cascade.detectMultiScale(img, 1.3, 5)
            
            for (x, y, w, h) in detected_faces:
                face_roi = img[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (200, 200))
                faces.append(face_roi)
                labels.append(current_id)
        
        current_id += 1
    
    if len(faces) == 0:
        print("No faces found in training data!")
        return False
    
    print(f"Training with {len(faces)} face samples...")
    recognizer.train(faces, np.array(labels))
    
    model_path = os.path.join(script_dir, 'trained_model.yml')
    recognizer.save(model_path)
    
    pkl_path = os.path.join(script_dir, 'id_to_name.pkl')
    with open(pkl_path, 'wb') as f:
        pickle.dump(id_to_name, f)
    
    print("Training complete!")
    print("You can now run recognize_faces()")
    return True

def recognize_faces():
    global id_to_name
    
    model_path = os.path.join(script_dir, 'trained_model.yml')
    pkl_path = os.path.join(script_dir, 'id_to_name.pkl')
    
    if not os.path.exists(model_path):
        print("No trained model found!")
        print("\nPlease run these steps first:")
        print("1. capture_training_data() - to capture photos")
        print("2. train_recognizer() - to train the model")
        return
    
    recognizer.read(model_path)
    
    if os.path.exists(pkl_path):
        with open(pkl_path, 'rb') as f:
            id_to_name = pickle.load(f)
    
    cap = cv2.VideoCapture(0)
    
    print("Press 'q' to quit")
    
    while True: 
        ret, img = cap.read() 
        
        if not ret:
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            cv2.putText(img, "No face detected", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (200, 200))
                
                predicted_id, confidence = recognizer.predict(face_roi)
                
                if confidence < 50:
                    name = id_to_name.get(predicted_id, "Unknown")
                    color = (0, 255, 0)
                    label = f"{name} ({int(confidence)})"
                else:
                    name = "Unknown"
                    color = (0, 0, 255)
                    label = f"Unknown ({int(confidence)})"
                
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                
                cv2.rectangle(img, (x, y-35), (x+w, y), color, cv2.FILLED)
                cv2.putText(img, label, (x+6, y-6), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Face Recognition', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

while __name__ == "__main__" and testing:
    print("=" * 50)
    print("Face Recognition Component")
    print("=" * 50)
    print("\nAvailable functions:")
    print("1. capture_training_data() - Capture photos from webcam")
    print("2. train_recognizer() - Train the model with captured photos")
    print("3. recognize_faces() - Run face recognition")
    print("4. getFace() - Return the userID")
    print("q. Quit")
    pressed = False
    while(not pressed):
        if keyboard.is_pressed('1'):
            pressed = True
            capture_training_data()

        elif keyboard.is_pressed('2'):
            pressed = True
            train_recognizer()

        elif keyboard.is_pressed('3'):
            pressed = True
            recognize_faces()

        elif keyboard.is_pressed('4'):
            print(getFace())

        elif keyboard.is_pressed('q'):
            print("Exiting...")
            pressed = True
            testing = False
            break