# backend/utils/frontalize_local.py

import os
import shutil


def frontalize_local(frontal_img_path, results_dir, track_id):
    """
    Copies the frontal.jpg of the matched person to results folder.

    frontal_img_path → existing static image
    returns → full output image path
    """

    if not frontal_img_path or not os.path.exists(frontal_img_path):
        return None

    os.makedirs(results_dir, exist_ok=True)

    out_name = f"{track_id}_frontal.jpg"
    out_path = os.path.join(results_dir, out_name)

    try:
        shutil.copy(frontal_img_path, out_path)
    except Exception as e:
        print("[frontalize_local ERROR]", e)
        return None

    return out_path
