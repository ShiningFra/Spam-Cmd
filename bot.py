import os
import asyncio
import random
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# Chargement du .env
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TARGET_BOT = os.getenv("TARGET_BOT")

GROUP_I = int(os.getenv("GROUPI")) if os.getenv("GROUPI") else None
GROUP_II = int(os.getenv("GROUPII")) if os.getenv("GROUPII") else None

if not all([API_ID, API_HASH, TARGET_BOT, GROUP_I, GROUP_II]):
    raise ValueError("❌ Erreur : Variables manquantes dans le fichier .env")

# Liste des cibles : Privé, Groupe I, Groupe II
TARGET_CHATS = [TARGET_BOT, GROUP_I, GROUP_II]

# Liste des commandes
COMMANDS_LIST = ["/acc", "/roue 1000", "/mescontratsbc"]

# Délai de base entre CHAQUE message envoyé (très rapide car on change de chat à chaque fois)
BASE_DELAY = 2.5

async def main():
    client = TelegramClient('session_userbot', int(API_ID), API_HASH)
    await client.start()
    print("🟩 Userbot lancé en mode DISPERSION TOTALE !")
    print("🔄 Ordre d'envoi croisé pour tromper l'anti-spam.")
    print("👉 CTRL + C pour couper.\n")

    try:
        while True:
            # On prend une commande après l'autre
            for commande in COMMANDS_LIST:
                
                # Et on l'envoie dans chaque chat un par un avant de passer à la commande suivante
                for chat_id in TARGET_CHATS:
                    try:
                        print(f"✈️ Chat: {chat_id} ➔ Commande: {commande}")
                        await client.send_message(chat_id, commande)
                        
                        # Petite variation humaine de sécurité
                        actual_delay = BASE_DELAY + random.uniform(0.0, 0.15)
                        await asyncio.sleep(actual_delay)
                        
                    except FloodWaitError as e:
                        security_time = e.seconds + 10
                        print("\n" + "!" * 50)
                        print(f"⚠️ FLOODWAIT DETECTÉ : Repos de {security_time}s...")
                        print("!" * 50 + "\n")
                        await asyncio.sleep(security_time)
                        print("▶️ Reprise du cycle...\n")
                        
                    except Exception as e:
                        print(f"❌ Erreur mineure : {e}")
                        await asyncio.sleep(1.5)
                        
            # Pause de fin de cycle avant de recommencer toute la matrice
            print("💤 Cycle complet terminé. Pause de 2 secondes...")
            await asyncio.sleep(2.5)

    except KeyboardInterrupt:
        print("\n🟥 Arrêt manuel.")
    finally:
        if client.is_connected():
            await client.disconnect()
        print("🏁 Déconnecté.")

if __name__ == '__main__':
    asyncio.run(main())