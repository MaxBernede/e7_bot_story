import os
import cv2

template_cache = {}

def preload_images(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            file_lower = file.lower()
            if file_lower.endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(root, file)
                img = cv2.imread(path)
                if img is not None:
                    template_cache[path.lower()] = img 
                else:
                    print(f"❌ Erreur lors du chargement : {path}")