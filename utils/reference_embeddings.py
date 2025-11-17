# backend/utils/reference_embeddings.py

import os
import numpy as np
import face_recognition
from typing import Dict

# Correct absolute path to persons folder
PERSONS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "persons")
)

# -----------------------------------------------------------
# Load reference embeddings for each person
# -----------------------------------------------------------
def load_reference_embeddings(min_images_per_person: int = 1) -> Dict[str, np.ndarray]:
    """
    Returns: dict → person_name → (N x 128) ndarray of face embeddings
    """
    known = {}

    if not os.path.isdir(PERSONS_DIR):
        print(f"[WARN] persons dir not found: {PERSONS_DIR}")
        return known

    for person in os.listdir(PERSONS_DIR):
        person_dir = os.path.join(PERSONS_DIR, person)
        if not os.path.isdir(person_dir):
            continue

        encs = []

        for fname in os.listdir(person_dir):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            img_path = os.path.join(person_dir, fname)

            try:
                img = face_recognition.load_image_file(img_path)
                embedding_list = face_recognition.face_encodings(img)

                if embedding_list:
                    encs.append(embedding_list[0])

            except Exception as e:
                print(f"[WARN] failed load {img_path}: {e}")
                continue

        if len(encs) >= min_images_per_person:
            known[person] = np.vstack(encs)
            print(f"[INFO] Loaded embeddings for {person}: {len(encs)} images")
        else:
            print(f"[WARN] Not enough images for {person} (got {len(encs)}), skipping")

    return known


# -----------------------------------------------------------
# Compare an unknown encoding to dictionary of person embeddings
# -----------------------------------------------------------
def best_match_for_encoding(encoding, known_dict, threshold=0.55):
    """
    Returns: (best_person_name, best_distance)
    """
    if encoding is None or known_dict is None or len(known_dict) == 0:
        return "Unknown", float("inf")

    best_name = "Unknown"
    best_dist = float("inf")

    for name, encodings in known_dict.items():

        try:
            distances = face_recognition.face_distance(encodings, encoding)
            min_dist = float(np.min(distances))
        except Exception:
            continue

        if min_dist < best_dist:
            best_dist = min_dist
            best_name = name

    if best_dist > threshold:
        return "Unknown", best_dist

    return best_name, best_dist
