"""
Global utilities and functionality.
Contains core functionality used across the application.
"""

import cv2
import numpy as np
import os
import subprocess
from .image_cache import template_cache
from .screenshot import *
from .actions import *
from .config import GAME_WINDOW_NAME

class ImageNotFoundError(Exception):
    """Exception raised when the image template cannot be found or loaded."""
    pass

def get_image_to_search_and_screenshot(image_path, screenshot): #pas sur de la logique
    image_template = template_cache.get(image_path)
    if image_template is None:
        raise Exception(f"❌ Erreur : image modèle non chargée depuis {image_path}")

    if screenshot is None:
        try:
            screenshot = screenshot_window(GAME_WINDOW_NAME)
        except:
            raise Exception(f"❌ Erreur : screenshot error ")
    return image_template, screenshot

# ------------ Détection d'images ------------ 
def detect_image(image_path, screenshot=None, en_gris=False, seuil=0.90):
    """Cherche une image modèle dans une fenêtre (ou image passée) et retourne les coordonnées si trouvée."""

    image_template, screenshot = get_image_to_search_and_screenshot(image_path, screenshot)

    # Vérification du type de image
    if isinstance(screenshot, str):  # Si image est un chemin de fichier
        screenshot = cv2.imread(screenshot)
        if screenshot is None:
            raise Exception(f"❌ Impossible de charger l'image depuis le fichier {screenshot}")

    if en_gris:
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        image_template = cv2.cvtColor(image_template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot, image_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= seuil:
        h, w = image_template.shape[:2]
        center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
        if os.path.basename(image_path).lower().startswith("arrow"):
            center = (center[0], center[1] + 25)
        # debug_img = screenshot.copy()
        # cv2.circle(debug_img, center, 10, (0, 0, 255), -1)
        # cv2.imwrite("debug_match.png", debug_img) #debug avec rond rouge
        return center

    raise ImageNotFoundError(f"Image modèle non trouvée: {image_path}")


# ------------ Interaction avec l'interface ------------
def verify_images_folder(folder, en_gris=True, click=True):
    try :
        screenshot = screenshot_window(GAME_WINDOW_NAME)

        for filename in os.listdir(folder):
            if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            try:
                # print(f"🔎 Vérification de {filename}...")
                image_path = get_img_path(folder, filename)
                coord = detect_image(image_path, screenshot, en_gris=en_gris)
                if coord and click:
                    click_in_window(GAME_WINDOW_NAME, coord[0], coord[1])
                    
                    print(f"✅ Image '{filename}' trouvée.")
                    return True
            except ImageNotFoundError as e:
                continue
            except Exception as e:
                print(f"⚠️ Erreur dans verify folder : {e}")
                return False
    except:
        print("❌ Error while verifying images in folder")
        return False
        
    print("❌ Aucune image trouvée dans le dossier.")
    return False

def get_img_path(folder, image_name):
    # Convertir image_name et folder en minuscules pour éviter les problèmes de casse
    folder = folder.lower()
    image_name = image_name.lower()
    
    image_path = os.path.join(folder, image_name)

    image_path = os.path.normpath(image_path)

    if not os.path.isfile(image_path):
        print(f"❌ Image {image_name} non trouvée dans {folder}.")
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    return image_path

if __name__ == "__main__":
    print("here")