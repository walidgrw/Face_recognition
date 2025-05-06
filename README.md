# Face Recognition with Blink Detection and GUI

A multi-user face recognition system built with Python, OpenCV, Dlib, and Tkinter. It features:

- 🧠 Blink-based liveness detection (to prevent spoofing with photos)
- ✅ Multi-user face registration and recognition
- 🔐 Admin-protected deletion of registered users
- 📜 Access logging (granted or denied)
- 📊 View last 10 access attempts
- 📥 Export logs to Excel
- 🖥️ GUI with Tkinter for easy interaction

---

## 🖥️ Technologies Used

- Python 3.8+
- OpenCV
- Dlib
- face_recognition
- Tkinter
- Pandas

---

## 📦 Features

### 🔐 Secure Recognition
- Users must blink to confirm they're a live person.
- Prevents photo-based attacks.

### 👤 Multi-User Support
- Register any number of users.
- Each face is encoded and saved securely.

### 🗂️ Log System
- All access attempts are saved to `access_log.txt`.
- Results are either ✅ Access Granted or ⛔ Access Denied.

### 🔧 Admin Features
- View log history
- Delete registered users (password-protected)
- Export logs to Excel

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/walidgrw/Face_recognition.git
cd Face_recognition
```

### 2. Install Required Packages
```bash
pip install opencv-python face_recognition dlib pandas openpyxl
```

### 3. Download the Landmark Model

This file is **required** for blink detection:

1. Download from: [http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
2. Extract it (you can use 7-Zip or WinRAR)
3. Place the file `shape_predictor_68_face_landmarks.dat` in the root project folder

### 4. Run the App
```bash
python main.py
```
This will launch the Tkinter-based GUI.

---

## 📁 Project Structure

```
face_project/
├── main.py                      # Main GUI application
├── faces.pkl                   # Serialized face encodings (auto-generated)
├── access_log.txt              # Log file (auto-generated)
├── shape_predictor_68_face_landmarks.dat  # Downloaded model
├── README.md
├── .gitignore
```

---

## 📤 Export Logs
Use the GUI button `Export Logs to Excel` to export access logs into `.xlsx` format.

---

## 🔒 Admin Password
To delete a user, you must enter the password:
```text
admin123
```
You can change this by editing the `ADMIN_PASSWORD` variable in `main.py`.

---

## 📌 Notes
- Make sure your webcam is working.
- The system is case-sensitive for names.
- Do not rename `faces.pkl` or `shape_predictor_68_face_landmarks.dat`.

---

## 📝 License
This project is for educational use. Dlib’s model is under the Boost Software License.

---

## 🤝 Contributions
Feel free to fork this repo and open pull requests with improvements!

---

## 👨‍💻 Author
**Walid Graw**  
[GitHub: walidgrw](https://github.com/walidgrw)
