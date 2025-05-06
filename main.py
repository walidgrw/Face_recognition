import cv2
import dlib
import face_recognition
import numpy as np
import pickle
import os
from scipy.spatial import distance as dist
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import pandas as pd

FACE_DATA_FILE = "faces.pkl"
LOG_FILE = "access_log.txt"
ADMIN_PASSWORD = "admin123"  # Change this in real deployment

# EAR calculation for blink detection
def calculate_EAR(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def log_access(name, status):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{timestamp} {status} - {name}\n")

def load_known_faces():
    if os.path.exists(FACE_DATA_FILE):
        with open(FACE_DATA_FILE, "rb") as f:
            return pickle.load(f)
    return [], []

def save_face(name, encoding):
    known_names, known_encodings = load_known_faces()
    known_names.append(name)
    known_encodings.append(encoding)
    with open(FACE_DATA_FILE, "wb") as f:
        pickle.dump((known_names, known_encodings), f)

def view_access_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as log:
            return log.readlines()[-10:]
    return ["No logs found."]

def delete_face():
    password = simpledialog.askstring("Admin", "Enter admin password:", show='*')
    if password != ADMIN_PASSWORD:
        messagebox.showerror("Access Denied", "Incorrect password")
        return

    known_names, known_encodings = load_known_faces()
    if not known_names:
        messagebox.showinfo("Delete", "No users found.")
        return

    name_to_delete = simpledialog.askstring("Delete Face", f"Registered users: {', '.join(known_names)}\nEnter name to delete:")
    if name_to_delete in known_names:
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name_to_delete}?")
        if confirm:
            index = known_names.index(name_to_delete)
            del known_names[index]
            del known_encodings[index]
            with open(FACE_DATA_FILE, "wb") as f:
                pickle.dump((known_names, known_encodings), f)
            messagebox.showinfo("Deleted", f"Deleted data for {name_to_delete}.")
    else:
        messagebox.showwarning("Not Found", "Name not found.")

def export_logs_to_excel():
    if not os.path.exists(LOG_FILE):
        messagebox.showerror("Error", "No logs to export.")
        return
    df = pd.read_csv(LOG_FILE, sep=" - ", header=None, engine='python')
    df.columns = ["Timestamp_Status", "Name"]
    export_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if export_path:
        df.to_excel(export_path, index=False)
        messagebox.showinfo("Success", f"Logs exported to {export_path}")

def register_face():
    name = simpledialog.askstring("Register", "Enter your name:")
    if not name:
        return

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Info", "Look at the camera and press 's' to save, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Register - Press 's' to Save, 'q' to Quit", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locations = face_recognition.face_locations(rgb)
            if not locations:
                messagebox.showwarning("No Face", "No face detected. Try again.")
                continue
            encoding = face_recognition.face_encodings(rgb, locations)[0]
            save_face(name, encoding)
            messagebox.showinfo("Saved", f"{name} registered.")
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_face_with_blink():
    known_names, known_encodings = load_known_faces()
    if not known_encodings:
        messagebox.showerror("Error", "No registered faces.")
        return

    cap = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    left_eye_idx = list(range(42, 48))
    right_eye_idx = list(range(36, 42))

    EAR_THRESHOLD = 0.21
    CONSEC_FRAMES = 2
    blink_counter = 0
    blink_detected = False

    messagebox.showinfo("Liveness Check", "Blink to confirm you're real. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector(gray)

        for face in faces:
            shape = predictor(gray, face)
            coords = np.array([[p.x, p.y] for p in shape.parts()])

            left_eye = coords[left_eye_idx]
            right_eye = coords[right_eye_idx]
            left_EAR = calculate_EAR(left_eye)
            right_EAR = calculate_EAR(right_eye)
            avg_EAR = (left_EAR + right_EAR) / 2.0

            if avg_EAR < EAR_THRESHOLD:
                blink_counter += 1
            else:
                if blink_counter >= CONSEC_FRAMES:
                    blink_detected = True
                blink_counter = 0

        if blink_detected:
            face_locations = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, face_locations)
            for encoding in encodings:
                matches = face_recognition.compare_faces(known_encodings, encoding)
                name = "Unknown"
                if True in matches:
                    match_idx = matches.index(True)
                    name = known_names[match_idx]
                    log_access(name, "✅ Access Granted")
                    messagebox.showinfo("Access", f"✅ Access Granted: {name}")
                else:
                    log_access(name, "⛔ Access Denied")
                    messagebox.showwarning("Access", "⛔ Access Denied")
            break

        cv2.imshow("Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def build_gui():
    root = tk.Tk()
    root.title("Face Recognition System")
    root.geometry("400x400")

    tk.Button(root, text="Register New Face", width=25, command=register_face).pack(pady=10)
    tk.Button(root, text="Recognize Face (with blink)", width=25, command=recognize_face_with_blink).pack(pady=10)
    tk.Button(root, text="View Access Log", width=25, command=lambda: messagebox.showinfo("Logs", "\n".join(view_access_log()))).pack(pady=10)
    tk.Button(root, text="Delete Registered Face", width=25, command=delete_face).pack(pady=10)
    tk.Button(root, text="Export Logs to Excel", width=25, command=export_logs_to_excel).pack(pady=10)
    tk.Button(root, text="Exit", width=25, command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    build_gui()
