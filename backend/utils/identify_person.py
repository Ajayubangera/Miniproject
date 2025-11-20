# backend/utils/identify_person.py

import os
import cv2
import face_recognition
import numpy as np


KNOWN_BASE = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "known_faces"
))

print("[identify] Known faces folder:", KNOWN_BASE)


# ------------------------------------------------------------------------
# Load encodings from each person's folder
# ------------------------------------------------------------------------
def load_known_encodings():
    database = {}

    for person in os.listdir(KNOWN_BASE):
        folder = os.path.join(KNOWN_BASE, person)
        if not os.path.isdir(folder):
            continue

        encs = []
        for f in os.listdir(folder):
            if not f.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            img_path = os.path.join(folder, f)
            img = cv2.imread(img_path)

            if img is None:
                continue

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_locs = face_recognition.face_locations(rgb, model="hog")

            if not face_locs:
                continue

            enc = face_recognition.face_encodings(rgb, known_face_locations=face_locs)
            if len(enc):
                encs.append(enc[0])

        if encs:
            database[person] = encs

    print(f"[identify] Loaded encodings for {len(database)} people.")
    return database


KNOWN_DB = load_known_encodings()


# ------------------------------------------------------------------------
# Try encoding with rotations
# ------------------------------------------------------------------------
def try_all_rotations(image):
    """Try four rotations to fix sideways faces."""
    rotations = {
        "0°": image,
        "90°": cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE),
        "180°": cv2.rotate(image, cv2.ROTATE_180),
        "270°": cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE),
    }

    for angle, img in rotations.items():
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb, model="hog")

        if locs:
            enc = face_recognition.face_encodings(rgb, known_face_locations=locs)
            if len(enc):
                print(f"[identify] Face encoded successfully at rotation {angle}")
                return enc[0]

    print("[identify] No face detected at any rotation.")
    return None


# ------------------------------------------------------------------------
# Main identification
# ------------------------------------------------------------------------
def find_best_person(face_path):
    print("[identify] Processing:", face_path)

    img = cv2.imread(face_path)
    if img is None:
        print("[identify] ERROR: Could not load image.")
        return "Unknown", None, []

    # Step 1 — try encoding
    enc = try_all_rotations(img)

    if enc is None:
        print("[encoding error] No face enc found:", face_path)
        return "Unknown", None, []

    # Step 2 — compare with known encodings
    best_name = "Unknown"
    best_score = 999

    for person, enc_list in KNOWN_DB.items():
        for known_enc in enc_list:
            dist = np.linalg.norm(known_enc - enc)
            if dist < best_score:
                best_score = dist
                best_name = person

    # Threshold (tweakable)
    if best_score > 0.55:
        best_name = "Unknown"

    # Step 3 — return frontal.jpg list
    frontal_path = os.path.join(KNOWN_BASE, best_name, "frontal.jpg")
    if os.path.exists(frontal_path):
        return best_name, float(best_score), [frontal_path]

    return best_name, float(best_score), []
