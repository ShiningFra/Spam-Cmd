import os
import asyncio
import random
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# Chargement du fichier .env
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TARGET_BOT = os.getenv("TARGET_BOT")
GROUP_I = int(os.getenv("GROUPI")) if os.getenv("GROUPI") else None
GROUP_II = int(os.getenv("GROUPII")) if os.getenv("GROUPII") else None

if not all([API_ID, API_HASH, TARGET_BOT, GROUP_I, GROUP_II]):
    raise ValueError("❌ Erreur : Variables manquantes dans le fichier .env")

# Liste de tes chats et de tes commandes
TARGET_CHATS = [TARGET_BOT, GROUP_I, GROUP_II]
COMMANDS_LIST = [
    "/acc",
    "/daily",
    "/work",
    "/pay @AsunaYuukiFra 1",
    "/richlist",
    "/blackjack 1000",
    "/roulette 1000 impair",
    "/slots 1000",
    "/roue 1000"
]

async def main():
    client = TelegramClient('session_userbot', int(API_ID), API_HASH)
    await client.start()
    print("🟩 Userbot lancé en mode FANTÔME INTÉGRAL !")
    print("🎭 Simulation 'Typing' + Dispersion de l'ordre + Délais dynamiques actifs.\n")

    try:
        while True:
            # Mélange l'ordre des groupes à chaque nouveau cycle pour détruire tout pattern linéaire
            chats_aleatoires = TARGET_CHATS.copy()
            random.shuffle(chats_aleatoires)
            
            for commande in COMMANDS_LIST:
                for chat_id in chats_aleatoires:
                    try:
                        # -----------------------------------------------------------------
                        # 1. SIMULATION DE L'ÉCRITURE (Le fameux 'typing...')
                        # -----------------------------------------------------------------
                        # On définit un temps d'écriture réaliste (ex: entre 1.5 et 3.5 secondes)
                        temps_ecriture = random.uniform(1.0, 2.0)
                        
                        async with client.action(chat_id, 'typing'):
                            # Pendant que Telegram affiche "En train d'écrire...", le script patiente
                            await asyncio.sleep(temps_ecriture)
                        
                        # Envoi de la commande après la simulation de frappe
                        print(f"✈️ Chat: {chat_id} ➔ Commande: {commande} (Écrit pendant {round(temps_ecriture, 1)}s)")
                        await client.send_message(chat_id, commande)
                        
                        # -----------------------------------------------------------------
                        # 2. PAUSE ALÉATOIRE ENTRE CHAQUE MESSAGE
                        # -----------------------------------------------------------------
                        # Fini les 3s fixes. On simule le temps qu'un humain met à changer de chat (3 à 7 secondes)
                        pause_inter_message = random.uniform(2.5, 4.0)
                        await asyncio.sleep(pause_inter_message)
                        
                    except FloodWaitError as e:
                        # Si Telegram te met une sécurité, on l'esquive intelligemment
                        temps_securite = e.seconds + 15
                        print(f"\n⚠️ FLOODWAIT DETECTÉ : Repos forcé de {temps_securite}s...\n")
                        await asyncio.sleep(temps_securite)
                    except Exception as e:
                        print(f"❌ Erreur avec le chat {chat_id} : {e}")
                        await asyncio.sleep(4.0)
            
            # -----------------------------------------------------------------
            # 3. GRANDE PAUSE DE FIN DE CYCLE
            # -----------------------------------------------------------------
            # Très important pour réinitialiser les compteurs de requêtes de Telegram.
            # Le script s'endort entre 45 secondes et 1 minute 30 avant de recommencer.
            pause_cycle = random.uniform(6.0, 10.0)
            print(f"\n💤 Cycle terminé. L'humain lâche son téléphone pendant {round(pause_cycle, 1)}s...\n")
            await asyncio.sleep(pause_cycle)

    except KeyboardInterrupt:
        print("\n🟥 Arrêt manuel demandé par l'utilisateur.")
    finally:
        if client.is_connected():
            await client.disconnect()
        print("🏁 Userbot correctement déconnecté.")

if __name__ == '__main__':
    asyncio.run(main())