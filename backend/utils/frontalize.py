import os
import cv2
import torch
import numpy as np
from torchvision import transforms
from PIL import Image


def load_gan_model(model_path):
    if not os.path.exists(model_path):
        print(f"[WARN] GAN NOT FOUND: {model_path}")
        return None

    try:
        model = torch.load(model_path, map_location="cpu")
        model.eval()
        return model
    except Exception as e:
        print("[ERROR] Failed loading GAN:", e)
        return None


def frontalize_with_gan_or_fallback(face_image_path, model_path, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    image = Image.open(face_image_path).convert("RGB")
    tensor = transforms.ToTensor()(image).unsqueeze(0)

    model = load_gan_model(model_path)
    output = None

    if model:
        try:
            with torch.no_grad():
                out = model(tensor)
            output = (out.squeeze(0).permute(1, 2, 0).numpy() * 255).astype(np.uint8)
            print("[INFO] GAN frontalization success")
        except Exception as e:
            print("[WARN] GAN failed:", e)

    if output is None:
        img = cv2.imread(face_image_path)
        h, w, _ = img.shape
        left = img[:, :w//2]
        right = cv2.flip(left, 1)
        output = np.concatenate([left, right], axis=1)
        print("[INFO] Used fallback frontalization")

    filename = f"frontalized_{os.path.basename(face_image_path)}"
    out_path = os.path.join(output_dir, filename)

    cv2.imwrite(out_path, output)
    return out_path
