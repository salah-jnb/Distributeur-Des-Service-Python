import os
from dotenv import load_dotenv

# Force le chargement du fichier .env
load_dotenv()


class Settings:
    # Vérifie bien que les noms à gauche correspondent à ton code
    # et les noms à droite (os.getenv) correspondent à ton fichier .env
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # Debug rapide : affiche si les variables sont chargées (à retirer après)
    if not SUPABASE_URL:
        print("❌ Erreur : SUPABASE_URL est introuvable dans les variables d'environnement")


settings = Settings()