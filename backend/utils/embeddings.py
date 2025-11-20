# backend/utils/embeddings.py

import os
import numpy as np
import face_recognition
from typing import Tuple, Dict

# Correct absolute path to embeddings folder
EMBEDDINGS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "models", "embeddings")
)

# -----------------------------------------------------------
# Read SINGLE face image → return encoding (128D vector)
# -----------------------------------------------------------
def get_face_encoding(face_path: str):
    if not os.path.exists(face_path):
        raise ValueError(f"File not found: {face_path}")

    try:
        img = face_recognition.load_image_file(face_path)
    except Exception as e:
        raise ValueError(f"Failed to load image {face_path}: {e}")

    encs = face_recognition.face_encodings(img)

    if len(encs) == 0:
        raise ValueError(f"No encoding found in: {face_path}")

    return encs[0]


# -----------------------------------------------------------
# Load all embeddings (.npy files)
# -----------------------------------------------------------
def load_known_embeddings() -> Dict[str, np.ndarray]:
    known = {}

    if not os.path.isdir(EMBEDDINGS_DIR):
        print(f"[WARN] Embeddings folder not found: {EMBEDDINGS_DIR}")
        return known

    for fname in os.listdir(EMBEDDINGS_DIR):
        if not fname.lower().endswith(".npy"):
            continue

        full_path = os.path.join(EMBEDDINGS_DIR, fname)

        try:
            arr = np.load(full_path, allow_pickle=False)
            name = os.path.splitext(fname)[0]  # PersonA_embed → PersonA_embed
            known[name] = arr
            print(f"[INFO] Loaded embeddings for {name}: shape={arr.shape}")
        except Exception as e:
            print(f"[WARN] Could not load {full_path}: {e}")

    return known


# -----------------------------------------------------------
# Compare unknown embedding with known embeddings
# Returns best match + distance
# -----------------------------------------------------------
def compare_embeddings(
        unknown_embedding,
        known_dict,
        threshold: float = 0.62  # Relaxed for group videos
) -> Tuple[str, float]:

    if unknown_embedding is None or len(known_dict) == 0:
        return "Unknown", float("inf")

    best_name = "Unknown"
    best_dist = float("inf")

    for name, vectors in known_dict.items():

        try:
            distances = face_recognition.face_distance(vectors, unknown_embedding)
        except Exception:
            continue

        if len(distances) == 0:
            continue

        person_min = float(np.min(distances))

        if person_min < best_dist:
            best_dist = person_min
            best_name = name

    if best_dist > threshold:
        return "Unknown", best_dist

    return best_name, best_dist
