import os
import asyncio
import random
import sys
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# Chargement du .env
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TARGET_BOT = os.getenv("TARGET_BOT")

# Récupération et conversion des IDs de groupes
GROUP_I = int(os.getenv("GROUPI")) if os.getenv("GROUPI") else None
GROUP_II = int(os.getenv("GROUPII")) if os.getenv("GROUPII") else None

if not all([API_ID, API_HASH, TARGET_BOT, GROUP_I, GROUP_II]):
    raise ValueError("❌ Erreur : Variables manquantes dans le fichier .env")

# Liste des cibles : Privé + Groupe I + Groupe II
TARGET_CHATS = [TARGET_BOT, GROUP_I, GROUP_II]

# Tes commandes
COMMANDS_LIST = ["/acc", "/roue 1000", "/mescontratsbc"]

# Ton délai de 0.6s (qui passe bien grâce à l'alternance des 3 salons)
BASE_DELAY = 0.6

async def main():
    client = TelegramClient('session_userbot', int(API_ID), API_HASH)
    await client.start()
    print("🟩 Userbot de REFORME lancé avec protection maximale !")
    print(f"📢 Rotation sur 3 salons : Privé, Groupe I, Groupe II")
    print("⚠️ Sécurité : Au moindre FloodWait, le script s'arrêtera immédiatement.\n")

    try:
        while True:
            for chat_id in TARGET_CHATS:
                print(f"💬 Cible actuelle : {chat_id}")
                
                for commande in COMMANDS_LIST:
                    try:
                        print(f"  ✈️ Envoi : {commande}")
                        await client.send_message(chat_id, commande)
                        
                        # Délai de 0.6s avec une micro-variation humaine pour le camouflage
                        actual_delay = BASE_DELAY + random.uniform(0.0, 0.15)
                        await asyncio.sleep(actual_delay)
                        
                    except FloodWaitError as e:
                        # 🚨 BLINDAGE ANTI-BAN : Arrêt immédiat au premier signal de Telegram
                        security_time = e.seconds + 10
                        print("\n" + "!" * 50)
                        print("🚨 DANGER : TELEGRAM A ÉMIS UN SIGNAL DE FLOOD !")
                        print(f"Le serveur demandait : {e.seconds} secondes d'attente.")
                        print(f"Marge de sécurité appliquée : REPOS TOTAL DE {security_time} SECONDES.")
                        print("Arrêt immédiat du script pour protéger ton compte.")
                        print("!" * 50 + "\n")
                        
                        # Déconnexion propre de la session pour ne pas corrompre la clé d'authentification
                        await client.disconnect()
                        
                        # Simulation du repos de sécurité avant fermeture définitive du terminal
                        print(f"⏳ Extinction dans {security_time} secondes...")
                        await asyncio.sleep(security_time)
                        sys.exit(1) # Fermeture forcée du programme Python
                        
                    except Exception as e:
                        print(f"❌ Erreur mineure (Bot ou réseau) : {e}")
                        await asyncio.sleep(1.5)
                        
            # Pause de 1.5 seconde avant de relancer la boucle complète (Privé -> G1 -> G2)
            await asyncio.sleep(1.5)

    except KeyboardInterrupt:
        print("\n🟥 Arrêt manuel demandé (CTRL+C).")
    finally:
        if client.is_connected():
            await client.disconnect()
        print("🏁 Userbot déconnecté en toute sécurité.")

if __name__ == '__main__':
    asyncio.run(main())