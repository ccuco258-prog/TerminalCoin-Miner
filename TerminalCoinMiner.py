import time
import os
import json
import random
import webbrowser
import requests
from colorama import init, Fore, Style
import keyboard
import re

# Inicializa colorama para que los colores funcionen en la consola.
init()

# --- Variables del Juego ---
SAVE_FILE = "terminalcoin_save.json"
wallet = 0.0
mining_speed = 0.1
last_update_time = time.time()
boost_active = False
boost_end_time = 0
boost_multiplier = 1
unlocked_codes = [] 
used_special_codes = []
tv_helper_purchased = False
mbc_purchased = False 
bitcoin_monitor_purchased = False
rickroll_sticker_purchased = False
idiot_sticker_purchased = False
freddy_sticker_purchased = False
current_language = 'es' # Idioma por defecto

# --- Diccionario de traducciones ---
translations = {
    'es': {
        'menu_title': "TerminalCoin Miner",
        'wallet': "Monedero: {:.2f} TC",
        'mining_speed': "Velocidad de minado: {:.2f} TC/s",
        'boost_active': "BOOST ACTIVO: {}x - Quedan {} segundos.",
        'options_menu': "Opciones:",
        'buy_upgrades': "1. Comprar mejoras (Upgrades)",
        'buy_boosts': "2. Comprar boosts",
        'view_programs': "3. Ver catálogo de programas",
        'view_codes': "4. Ver y usar códigos",
        'save_game': "5. Guardar partida",
        'play_music': "6. Reproducir música",
        'view_stickers': "7. Ver y usar stickers",
        'change_language': "8. Cambiar Idioma",
        'exit_game': "9. Salir",
        'choice_prompt': "Elige una opción: ",
        'invalid_option': "Opción no válida. Inténtalo de nuevo.",
        'game_saved': "✅ Partida guardada con éxito.",
        'game_loaded': "¡Partida cargada con éxito!",
        'code_unlocked': "\n¡🎉 CÓDIGO DESBLOQUEADO! 🎉\nHas alcanzado los {} TC. Tu nuevo código es: {}",
        'boost_ended': "El boost ha finalizado.",
        'upgrades_catalog': "Catálogo de Mejoras",
        'id_cost_speed': "ID: {} - Coste: {} TC - Aumenta la velocidad en: {} TC/s",
        'enter_upgrade_id': "Introduce el ID de la mejora a comprar (o 'salir'): ",
        'purchase_successful_speed': "¡Compra exitosa! Velocidad actual: {:.2f} TC/s",
        'not_enough_tc': "No tienes suficientes TerminalCoins.",
        'invalid_upgrade_id': "ID de mejora no válido.",
        'press_enter_to_continue': "\nPulsa Enter para continuar...",
        'boosts_catalog': "Catálogo de Boosts",
        'id_cost_multiplier_duration': "ID: {} - Coste: {} TC - Multiplicador: {}x - Duración: {}s",
        'enter_boost_id': "Introduce el ID del boost a comprar (o 'salir'): ",
        'boost_activated': "¡Boost activado! ¡A minar más rápido!",
        'boost_already_active': "Ya tienes un boost activo. Espera a que termine.",
        'invalid_boost_id': "ID de boost no válido.",
        'codes_available': "Códigos Disponibles",
        'milestone_codes': "Códigos por hitos:",
        'no_codes_unlocked': "Aún no has desbloqueado ningún código por hito. ¡Sigue minando!",
        'enter_code': "\n--- Introduce un Código ---\nIntroduce el código que quieres usar (o 'salir'): ",
        'code_already_used': "Este código ya ha sido usado.",
        'tc1_code_used': "¡Código TC1 usado! Se han añadido 1000 TC a tu monedero.",
        'code_used_speed_increase': "Código '{}' usado. ¡Tu velocidad de minado ha aumentado en {} TC/s!",
        'code_used_boost': "Código '{}' usado. ¡Has activado un boost de {}x!",
        'invalid_or_unlocked_code': "Código no válido o no desbloqueado.",
        'music_player': "Reproductor de Música",
        'songs_available': "Canciones disponibles:",
        'song_info': "[{}] - '{}' de {} - Coste: {} TC",
        'purchase_song_prompt': "\nIntroduce el número de la canción a comprar y reproducir (o 'salir'): ",
        'song_purchased_opening': "¡Has comprado la canción! Abriendo '{}' en tu navegador... 🎶",
        'not_enough_tc_song': "❌ No tienes suficientes TerminalCoins para comprar esta canción.",
        'invalid_option_song': "❌ Opción no válida.",
        'programs_store': "Tienda de Programas",
        'store_intro': "¡Utiliza tus TerminalCoins para comprar otros programas desarrollados con Python!",
        'programs_available': "Programas disponibles:",
        'tv_helper': "'TV Helper': Te ayuda a encontrar la mejor televisión para ti.",
        'cost': "Costo: {} TC",
        'purchased': "(Comprado)",
        'mbc_program': "'MonsterBattleCreator': Un juego de lucha donde creas y entrenas un monstruo.",
        'bitcoin_monitor': "'BitcoinMonitor': Muestra el valor en vivo de Bitcoin.",
        'buy_or_run_program': "\nIntroduce el número del programa que quieres comprar o ejecutar (o 'salir'): ",
        'purchase_successful_program': "¡Compra exitosa! Ahora puedes usar el programa '{}'.",
        'not_enough_tc_program': "No tienes suficientes TerminalCoins para comprar este programa.",
        'program_already_active': "El programa ya está activo y se muestra en la pantalla principal.",
        'stickers_store': "Tienda de Stickers",
        'stickers_intro': "¡Compra y colecciona stickers con arte ASCII!",
        'rickroll_sticker': "'Rickroll': ¡Una broma clásica! Te enviará a un video sorpresa.",
        'virus_sticker': "'Virus, eres un idiota': Un mensaje en pantalla... ¡tranquilo, no es un virus!",
        'freddy_sticker': "'Freddy Fazbear': ¡El famoso animatrónico en tu terminal!",
        'buy_or_use_sticker': "\nIntroduce el número del sticker que quieres comprar o usar (o 'salir'): ",
        'sticker_purchase_successful': "¡Compra exitosa! Ahora puedes usar el sticker '{}'.",
        'not_enough_tc_sticker': "No tienes suficientes TerminalCoins para comprar este sticker.",
        'rickrolled_message': "¡Has sido rickrolleado!",
        'virus_message_1': "¡HAS SIDO INFECTADO! VIRUS.EXE DETECTADO EN TU SISTEMA",
        'virus_message_2': "¡ERES UN IDIOTA!",
        'virus_message_3': "(Pero no un virus, eh.)",
        'press_enter_to_continue_virus': "\nPresiona Enter para continuar...",
        'freddy_message_1': "¡Cuidado con Freddy!",
        'freddy_message_2': "Freddy se ha ido! Por ahora...",
        'language_options': "--- Opciones de Idioma ---\nElige tu idioma (escribe el código):\n- es (Español)\n- en (Inglés)\n- de (Alemán)",
        'language_change_successful': "Idioma cambiado a {}.",
        'invalid_language': "Idioma no válido. Volviendo al menú principal."
    },
    'en': {
        'menu_title': "TerminalCoin Miner",
        'wallet': "Wallet: {:.2f} TC",
        'mining_speed': "Mining Speed: {:.2f} TC/s",
        'boost_active': "BOOST ACTIVE: {}x - {} seconds left.",
        'options_menu': "Options:",
        'buy_upgrades': "1. Buy Upgrades",
        'buy_boosts': "2. Buy Boosts",
        'view_programs': "3. View Program Catalog",
        'view_codes': "4. View and Use Codes",
        'save_game': "5. Save Game",
        'play_music': "6. Play Music",
        'view_stickers': "7. View and Use Stickers",
        'change_language': "8. Change Language",
        'exit_game': "9. Exit",
        'choice_prompt': "Choose an option: ",
        'invalid_option': "Invalid option. Please try again.",
        'game_saved': "✅ Game saved successfully.",
        'game_loaded': "Game loaded successfully!",
        'code_unlocked': "\n¡🎉 CODE UNLOCKED! 🎉\nYou have reached {} TC. Your new code is: {}",
        'boost_ended': "The boost has ended.",
        'upgrades_catalog': "Upgrades Catalog",
        'id_cost_speed': "ID: {} - Cost: {} TC - Increases speed by: {} TC/s",
        'enter_upgrade_id': "Enter the ID of the upgrade to buy (or 'exit'): ",
        'purchase_successful_speed': "Purchase successful! Current speed: {:.2f} TC/s",
        'not_enough_tc': "You do not have enough TerminalCoins.",
        'invalid_upgrade_id': "Invalid upgrade ID.",
        'press_enter_to_continue': "\nPress Enter to continue...",
        'boosts_catalog': "Boosts Catalog",
        'id_cost_multiplier_duration': "ID: {} - Cost: {} TC - Multiplier: {}x - Duration: {}s",
        'enter_boost_id': "Enter the ID of the boost to buy (or 'exit'): ",
        'boost_activated': "Boost activated! Mine faster!",
        'boost_already_active': "You already have an active boost. Wait for it to end.",
        'invalid_boost_id': "Invalid boost ID.",
        'codes_available': "Available Codes",
        'milestone_codes': "Milestone codes:",
        'no_codes_unlocked': "You haven't unlocked any milestone codes yet. Keep mining!",
        'enter_code': "\n--- Enter a Code ---\nEnter the code you want to use (or 'exit'): ",
        'code_already_used': "This code has already been used.",
        'tc1_code_used': "Code TC1 used! 1000 TC have been added to your wallet.",
        'code_used_speed_increase': "Code '{}' used. Your mining speed has increased by {} TC/s!",
        'code_used_boost': "Code '{}' used. You have activated a boost of {}x!",
        'invalid_or_unlocked_code': "Invalid or unlocked code.",
        'music_player': "Music Player",
        'songs_available': "Available songs:",
        'song_info': "[{}] - '{}' by {} - Cost: {} TC",
        'purchase_song_prompt': "\nEnter the number of the song to buy and play (or 'exit'): ",
        'song_purchased_opening': "You have purchased the song! Opening '{}' in your browser... 🎶",
        'not_enough_tc_song': "❌ You do not have enough TerminalCoins to buy this song.",
        'invalid_option_song': "❌ Invalid option.",
        'programs_store': "Program Store",
        'store_intro': "Use your TerminalCoins to buy other programs developed with Python!",
        'programs_available': "Available programs:",
        'tv_helper': "'TV Helper': Helps you find the best TV for you.",
        'cost': "Cost: {} TC",
        'purchased': "(Purchased)",
        'mbc_program': "'MonsterBattleCreator': A fighting game where you create and train a monster.",
        'bitcoin_monitor': "'BitcoinMonitor': Shows the live value of Bitcoin.",
        'buy_or_run_program': "\nEnter the number of the program you want to buy or run (or 'exit'): ",
        'purchase_successful_program': "Purchase successful! You can now use the '{}' program.",
        'not_enough_tc_program': "You do not have enough TerminalCoins to buy this program.",
        'program_already_active': "The program is already active and is displayed on the main screen.",
        'stickers_store': "Sticker Store",
        'stickers_intro': "Buy and collect stickers with ASCII art!",
        'rickroll_sticker': "'Rickroll': A classic prank! It will send you to a surprise video.",
        'virus_sticker': "'Virus, you're an idiot': A message on the screen... don't worry, it's not a virus!",
        'freddy_sticker': "'Freddy Fazbear': The famous animatronic on your terminal!",
        'buy_or_use_sticker': "\nEnter the number of the sticker you want to buy or use (or 'exit'): ",
        'sticker_purchase_successful': "Purchase successful! You can now use the '{}' sticker.",
        'not_enough_tc_sticker': "You do not have enough TerminalCoins to buy this sticker.",
        'rickrolled_message': "You've been rickrolled!",
        'virus_message_1': "YOU HAVE BEEN INFECTED! VIRUS.EXE DETECTED ON YOUR SYSTEM",
        'virus_message_2': "YOU ARE AN IDIOT!",
        'virus_message_3': "(But not a virus, huh.)",
        'press_enter_to_continue_virus': "\nPress Enter to continue...",
        'freddy_message_1': "Watch out for Freddy!",
        'freddy_message_2': "Freddy is gone! For now...",
        'language_options': "--- Language Options ---\nChoose your language (enter the code):\n- es (Spanish)\n- en (English)\n- de (German)",
        'language_change_successful': "Language changed to {}.",
        'invalid_language': "Invalid language. Returning to the main menu."
    },
    'de': {
        'menu_title': "TerminalCoin-Miner",
        'wallet': "Geldbörse: {:.2f} TC",
        'mining_speed': "Mining-Geschwindigkeit: {:.2f} TC/s",
        'boost_active': "BOOST AKTIV: {}x - Noch {} Sekunden.",
        'options_menu': "Optionen:",
        'buy_upgrades': "1. Upgrades kaufen",
        'buy_boosts': "2. Boosts kaufen",
        'view_programs': "3. Programm-Katalog ansehen",
        'view_codes': "4. Codes ansehen und benutzen",
        'save_game': "5. Spiel speichern",
        'play_music': "6. Musik abspielen",
        'view_stickers': "7. Sticker ansehen und benutzen",
        'change_language': "8. Sprache ändern",
        'exit_game': "9. Beenden",
        'choice_prompt': "Wähle eine Option: ",
        'invalid_option': "Ungültige Option. Bitte versuche es erneut.",
        'game_saved': "✅ Spiel erfolgreich gespeichert.",
        'game_loaded': "Spiel erfolgreich geladen!",
        'code_unlocked': "\n¡🎉 CODE FREIGESCHALTET! 🎉\nDu hast {} TC erreicht. Dein neuer Code ist: {}",
        'boost_ended': "Der Boost ist beendet.",
        'upgrades_catalog': "Upgrade-Katalog",
        'id_cost_speed': "ID: {} - Kosten: {} TC - Erhöht die Geschwindigkeit um: {} TC/s",
        'enter_upgrade_id': "Gib die ID des Upgrades ein, das du kaufen möchtest (oder 'exit'): ",
        'purchase_successful_speed': "Kauf erfolgreich! Aktuelle Geschwindigkeit: {:.2f} TC/s",
        'not_enough_tc': "Du hast nicht genügend TerminalCoins.",
        'invalid_upgrade_id': "Ungültige Upgrade-ID.",
        'press_enter_to_continue': "\nDrücke Enter, um fortzufahren...",
        'boosts_catalog': "Boost-Katalog",
        'id_cost_multiplier_duration': "ID: {} - Kosten: {} TC - Multiplikator: {}x - Dauer: {}s",
        'enter_boost_id': "Gib die ID des Boosts ein, den du kaufen möchtest (oder 'exit'): ",
        'boost_activated': "Boost aktiviert! Schneller minen!",
        'boost_already_active': "Du hast bereits einen aktiven Boost. Warte, bis er endet.",
        'invalid_boost_id': "Ungültige Boost-ID.",
        'codes_available': "Verfügbare Codes",
        'milestone_codes': "Meilenstein-Codes:",
        'no_codes_unlocked': "Du hast noch keine Meilenstein-Codes freigeschaltet. Weiterminen!",
        'enter_code': "\n--- Gib einen Code ein ---\nGib den Code ein, den du verwenden möchtest (oder 'exit'): ",
        'code_already_used': "Dieser Code wurde bereits verwendet.",
        'tc1_code_used': "Code TC1 verwendet! 1000 TC wurden zu deiner Geldbörse hinzugefügt.",
        'code_used_speed_increase': "Code '{}' verwendet. Deine Mining-Geschwindigkeit wurde um {} TC/s erhöht!",
        'code_used_boost': "Code '{}' verwendet. Du hast einen Boost von {}x aktiviert!",
        'invalid_or_unlocked_code': "Ungültiger oder nicht freigeschalteter Code.",
        'music_player': "Musik-Player",
        'songs_available': "Verfügbare Lieder:",
        'song_info': "[{}] - '{}' von {} - Kosten: {} TC",
        'purchase_song_prompt': "\nGib die Nummer des Liedes ein, das du kaufen und abspielen möchtest (oder 'exit'): ",
        'song_purchased_opening': "Du hast das Lied gekauft! Öffne '{}' in deinem Browser... 🎶",
        'not_enough_tc_song': "❌ Du hast nicht genügend TerminalCoins, um dieses Lied zu kaufen.",
        'invalid_option_song': "❌ Ungültige Option.",
        'programs_store': "Programm-Shop",
        'store_intro': "Verwende deine TerminalCoins, um andere mit Python entwickelte Programme zu kaufen!",
        'programs_available': "Verfügbare Programme:",
        'tv_helper': "'TV Helper': Hilft dir, den besten Fernseher für dich zu finden.",
        'cost': "Kosten: {} TC",
        'purchased': "(Gekauft)",
        'mbc_program': "'MonsterBattleCreator': Ein Kampfspiel, in dem du ein Monster erschaffst und trainierst.",
        'bitcoin_monitor': "'BitcoinMonitor': Zeigt den Live-Wert von Bitcoin an.",
        'buy_or_run_program': "\nGib die Nummer des Programms ein, das du kaufen oder ausführen möchtest (oder 'exit'): ",
        'purchase_successful_program': "Kauf erfolgreich! Du kannst jetzt das Programm '{}' verwenden.",
        'not_enough_tc_program': "Du hast nicht genügend TerminalCoins, um dieses Programm zu kaufen.",
        'program_already_active': "Das Programm ist bereits aktiv und wird auf dem Hauptbildschirm angezeigt.",
        'stickers_store': "Sticker-Shop",
        'stickers_intro': "Kaufe und sammle Sticker mit ASCII-Kunst!",
        'rickroll_sticker': "'Rickroll': Ein klassischer Streich! Es wird dich zu einem Überraschungsvideo weiterleiten.",
        'virus_sticker': "'Virus, du bist ein Idiot': Eine Nachricht auf dem Bildschirm... keine Sorge, es ist kein Virus!",
        'freddy_sticker': "'Freddy Fazbear': Der berühmte Animatronic in deinem Terminal!",
        'buy_or_use_sticker': "\nGib die Nummer des Stickers ein, den du kaufen oder verwenden möchtest (oder 'exit'): ",
        'sticker_purchase_successful': "Kauf erfolgreich! Du kannst jetzt den '{}'-Sticker verwenden.",
        'not_enough_tc_sticker': "Du hast nicht genügend TerminalCoins, um diesen Sticker zu kaufen.",
        'rickrolled_message': "Du wurdest gerickrollt!",
        'virus_message_1': "DU WURDEST INFIZIERT! VIRUS.EXE AUF DEINEM SYSTEM ERKANNT",
        'virus_message_2': "DU BIST EIN IDIOT!",
        'virus_message_3': "(Aber kein Virus, oder?)",
        'press_enter_to_continue_virus': "\nDrücke Enter, um fortzufahren...",
        'freddy_message_1': "Nimm dich vor Freddy in Acht!",
        'freddy_message_2': "Freddy ist weg! Vorerst...",
        'language_options': "--- Sprachoptionen ---\nWähle deine Sprache (gib den Code ein):\n- es (Spanisch)\n- en (Englisch)\n- de (Deutsch)",
        'language_change_successful': "Sprache zu {} geändert.",
        'invalid_language': "Ungültige Sprache. Kehre zum Hauptmenü zurück."
    }
}

# --- Códigos de recompensa por progreso ---
codes = {
    10: {"code": "FASTSTART", "reward_type": "speed_increase", "value": 0.5},
    50: {"code": "TCBOOST", "reward_type": "boost", "value": 2, "duration": 60},
    100: {"code": "MINERPRO", "reward_type": "speed_increase", "value": 1.0},
    250: {"code": "SUPERBOOST", "reward_type": "boost", "value": 5, "duration": 90},
    500: {"code": "GOLDENAGE", "reward_type": "speed_increase", "value": 5.0},
    800: {"code": "MASTERMIND", "reward_type": "boost", "value": 10, "duration": 120},
    1000: {"code": "ULTIMATE", "reward_type": "speed_increase", "value": 15.0},
}

# --- Catálogo de Mejoras y Boosts con precios y efectos ajustados ---
upgrades = {
    "mejora_hardware": {"cost": 100, "speed_increase": 0.5},
    "optimizacion_software": {"cost": 500, "speed_increase": 2.0},
    "ventilador_gpu": {"cost": 2500, "speed_increase": 10.0},
}

boosts = {
    "boost_x2": {"cost": 150, "multiplier": 2, "duration": 60},
    "boost_x10": {"cost": 1000, "multiplier": 10, "duration": 30},
}

# --- Catálogo de Canciones con enlaces ---
SONGS_CATALOG = {
    "1": {"title": "I Got No Time", "artist": "The Living Tombstone", "cost": 20, "url": "http://music.youtube.com/watch?v=PMF-V6NbzrY"}
}

def clear_screen():
    """Limpia la consola para una mejor visualización."""
    os.system('cls' if os.name == 'nt' else 'clear')

def save_game():
    """Guarda el estado actual del juego en un archivo JSON."""
    data = {
        "wallet": wallet,
        "mining_speed": mining_speed,
        "boost_active": boost_active,
        "boost_end_time": boost_end_time,
        "boost_multiplier": boost_multiplier,
        "unlocked_codes": unlocked_codes,
        "used_special_codes": used_special_codes,
        "tv_helper_purchased": tv_helper_purchased,
        "mbc_purchased": mbc_purchased,
        "bitcoin_monitor_purchased": bitcoin_monitor_purchased,
        "rickroll_sticker_purchased": rickroll_sticker_purchased,
        "idiot_sticker_purchased": idiot_sticker_purchased,
        "freddy_sticker_purchased": freddy_sticker_purchased,
        "current_language": current_language
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)
    print(translations[current_language]['game_saved'])
    time.sleep(1)

def load_game():
    """Carga el estado del juego desde un archivo JSON si existe."""
    global wallet, mining_speed, boost_active, boost_end_time, boost_multiplier, last_update_time, unlocked_codes, used_special_codes, tv_helper_purchased, mbc_purchased, bitcoin_monitor_purchased, rickroll_sticker_purchased, idiot_sticker_purchased, freddy_sticker_purchased, current_language
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            wallet = data.get("wallet", 0.0)
            mining_speed = data.get("mining_speed", 0.1)
            boost_active = data.get("boost_active", False)
            boost_end_time = data.get("boost_end_time", 0)
            boost_multiplier = data.get("boost_multiplier", 1)
            unlocked_codes = data.get("unlocked_codes", [])
            used_special_codes = data.get("used_special_codes", [])
            tv_helper_purchased = data.get("tv_helper_purchased", False)
            mbc_purchased = data.get("mbc_purchased", False)
            bitcoin_monitor_purchased = data.get("bitcoin_monitor_purchased", False)
            rickroll_sticker_purchased = data.get("rickroll_sticker_purchased", False)
            idiot_sticker_purchased = data.get("idiot_sticker_purchased", False)
            freddy_sticker_purchased = data.get("freddy_sticker_purchased", False)
            current_language = data.get("current_language", 'es')
            last_update_time = time.time()
        print(translations[current_language]['game_loaded'])

def check_for_new_codes():
    """Verifica si se han desbloqueado nuevos códigos al alcanzar una cantidad de TC."""
    for tc_amount, code_data in codes.items():
        if wallet >= tc_amount and code_data["code"] not in unlocked_codes:
            unlocked_codes.append(code_data["code"])
            print(translations[current_language]['code_unlocked'].format(tc_amount, code_data['code']))
            time.sleep(2)

def update_wallet():
    """Actualiza el monedero basándose en el tiempo transcurrido."""
    global wallet, last_update_time, mining_speed, boost_active, boost_end_time, boost_multiplier
    
    current_time = time.time()
    time_elapsed = current_time - last_update_time
    
    current_mining_speed = mining_speed * boost_multiplier
    
    wallet += time_elapsed * current_mining_speed
    last_update_time = current_time
    
    if boost_active and current_time >= boost_end_time:
        boost_active = False
        boost_multiplier = 1
        print(translations[current_language]['boost_ended'])
        time.sleep(1)

def get_crypto_price_display():
    """Obtiene y formatea el precio de Bitcoin para mostrarlo en pantalla."""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": "usd"}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        bitcoin_price = data.get("bitcoin", {}).get("usd", "Error")
        if isinstance(bitcoin_price, (int, float)):
            return f"💰 BTC: ${bitcoin_price:,.2f}"
        return f"💰 BTC: {bitcoin_price}"
    except requests.exceptions.RequestException:
        return "❌ BTC: API Error"

def display_terminalcoin_logo():
    """Muestra el logo de la TerminalCoin usando caracteres ASCII."""
    crypto_display = ""
    if bitcoin_monitor_purchased:
        crypto_display = get_crypto_price_display()
        
    print("---------------------------------------------")
    print("        .---------------------.            ")
    print("       /                       \           ")
    print("      |          .-.          |          ")
    print("      |          |T|          |          ")
    print("      |          '-'          |          ")
    print("       \                       /           ")
    print("        `---------------------'            ")
    print(f"            {translations[current_language]['menu_title'].upper()}        ")
    if bitcoin_monitor_purchased:
        print(f"        {crypto_display}")
    print("---------------------------------------------")

def show_status():
    """Muestra el estado actual del juego."""
    print(f"--- ⛏️ {translations[current_language]['menu_title']} ---")
    print(translations[current_language]['wallet'].format(wallet))
    print(translations[current_language]['mining_speed'].format(mining_speed * boost_multiplier))
    if boost_active:
        time_left = int(boost_end_time - time.time())
        print(translations[current_language]['boost_active'].format(boost_multiplier, time_left))
    print(f"\n{translations[current_language]['options_menu']}")
    print(translations[current_language]['buy_upgrades'])
    print(translations[current_language]['buy_boosts'])
    print(translations[current_language]['view_programs'])
    print(translations[current_language]['view_codes'])
    print(translations[current_language]['save_game'])
    print(translations[current_language]['play_music'])
    print(translations[current_language]['view_stickers'])
    print(translations[current_language]['change_language'])
    print(translations[current_language]['exit_game'])

def buy_upgrade():
    """Permite comprar mejoras."""
    global wallet, mining_speed
    print(f"\n--- {translations[current_language]['upgrades_catalog']} ---")
    for key, value in upgrades.items():
        print(translations[current_language]['id_cost_speed'].format(key, value['cost'], value['speed_increase']))
    
    choice = input(translations[current_language]['enter_upgrade_id'])
    if choice in upgrades:
        if wallet >= upgrades[choice]["cost"]:
            wallet -= upgrades[choice]["cost"]
            mining_speed += upgrades[choice]["speed_increase"]
            print(translations[current_language]['purchase_successful_speed'].format(mining_speed))
        else:
            print(translations[current_language]['not_enough_tc'])
    elif choice.lower() != 'salir' and choice.lower() != 'exit' and choice.lower() != 'beenden':
        print(translations[current_language]['invalid_upgrade_id'])
    input(translations[current_language]['press_enter_to_continue'])

def buy_boost():
    """Permite comprar boosts momentáneos."""
    global wallet, boost_active, boost_end_time, boost_multiplier
    print(f"\n--- {translations[current_language]['boosts_catalog']} ---")
    for key, value in boosts.items():
        print(translations[current_language]['id_cost_multiplier_duration'].format(key, value['cost'], value['multiplier'], value['duration']))
    
    choice = input(translations[current_language]['enter_boost_id'])
    if choice in boosts:
        if not boost_active:
            if wallet >= boosts[choice]["cost"]:
                wallet -= boosts[choice]["cost"]
                boost_multiplier = boosts[choice]["multiplier"]
                boost_end_time = time.time() + boosts[choice]["duration"]
                boost_active = True
                print(translations[current_language]['boost_activated'])
            else:
                print(translations[current_language]['not_enough_tc'])
        else:
            print(translations[current_language]['boost_already_active'])
    elif choice.lower() != 'salir' and choice.lower() != 'exit' and choice.lower() != 'beenden':
        print(translations[current_language]['invalid_boost_id'])
    input(translations[current_language]['press_enter_to_continue'])

def show_programs_store():
    """Simula una tienda de programas."""
    global wallet, tv_helper_purchased, mbc_purchased, bitcoin_monitor_purchased
    print(f"\n--- {translations[current_language]['programs_store']} ---")
    print(translations[current_language]['store_intro'])
    print(f"\n{translations[current_language]['programs_available']}")
    
    if not tv_helper_purchased:
        print(f"1. {translations[current_language]['tv_helper']}")
        print(f"   {translations[current_language]['cost'].format(500)}")
    else:
        print(f"1. {translations[current_language]['tv_helper']} {translations[current_language]['purchased']}")
        
    if not mbc_purchased:
        print(f"2. {translations[current_language]['mbc_program']}")
        print(f"   {translations[current_language]['cost'].format(3000)}")
    else:
        print(f"2. {translations[current_language]['mbc_program']} {translations[current_language]['purchased']}")
        
    if not bitcoin_monitor_purchased:
        print(f"3. {translations[current_language]['bitcoin_monitor']}")
        print(f"   {translations[current_language]['cost'].format(1000)}")
    else:
        print(f"3. {translations[current_language]['bitcoin_monitor']} {translations[current_language]['purchased']}")
        
    choice = input(translations[current_language]['buy_or_run_program'])
    
    if choice == '1':
        if not tv_helper_purchased:
            if wallet >= 500:
                wallet -= 500
                tv_helper_purchased = True
                print(translations[current_language]['purchase_successful_program'].format('TV Helper'))
            else:
                print(translations[current_language]['not_enough_tc_program'])
        else:
            run_tv_helper()
            
    elif choice == '2':
        if not mbc_purchased:
            if wallet >= 3000:
                wallet -= 3000
                mbc_purchased = True
                print(translations[current_language]['purchase_successful_program'].format('MonsterBattleCreator'))
            else:
                print(translations[current_language]['not_enough_tc_program'])
        else:
            run_monster_battle_creator()
            
    elif choice == '3':
        if not bitcoin_monitor_purchased:
            if wallet >= 1000:
                wallet -= 1000
                bitcoin_monitor_purchased = True
                print(translations[current_language]['purchase_successful_program'].format('BitcoinMonitor'))
            else:
                print(translations[current_language]['not_enough_tc_program'])
        else:
            print(translations[current_language]['program_already_active'])

    elif choice.lower() != 'salir' and choice.lower() != 'exit' and choice.lower() != 'beenden':
        print(translations[current_language]['invalid_option'])
    
    input(translations[current_language]['press_enter_to_continue'])

def manage_codes():
    """Permite al usuario ver y usar los códigos."""
    global mining_speed, boost_active, boost_end_time, boost_multiplier, wallet
    
    print(f"\n--- {translations[current_language]['codes_available']} ---")
    print(translations[current_language]['milestone_codes'])
    if not unlocked_codes:
        print(translations[current_language]['no_codes_unlocked'])
    else:
        for code in unlocked_codes:
            print(f"- {code}")
            
    choice = input(translations[current_language]['enter_code'])
    
    if choice.upper() == "TC1":
        if "TC1" in used_special_codes:
            print(translations[current_language]['code_already_used'])
        else:
            wallet += 1000
            used_special_codes.append("TC1")
            print(translations[current_language]['tc1_code_used'])
    
    else:
        found = False
        for tc_amount, code_data in codes.items():
            if code_data["code"] == choice and choice in unlocked_codes:
                found = True
                if code_data["reward_type"] == "speed_increase":
                    mining_speed += code_data["value"]
                    unlocked_codes.remove(choice)
                    print(translations[current_language]['code_used_speed_increase'].format(choice, code_data['value']))
                elif code_data["reward_type"] == "boost":
                    if not boost_active:
                        boost_multiplier = code_data["value"]
                        boost_end_time = time.time() + code_data["duration"]
                        boost_active = True
                        unlocked_codes.remove(choice)
                        print(translations[current_language]['code_used_boost'].format(choice, code_data['value']))
                    else:
                        print(translations[current_language]['boost_already_active'])
                break
        
        if not found and choice.lower() != 'salir' and choice.lower() != 'exit' and choice.lower() != 'beenden':
            print(translations[current_language]['invalid_or_unlocked_code'])
            
    input(translations[current_language]['press_enter_to_continue'])

def play_music():
    """Permite al usuario comprar y reproducir una canción."""
    global wallet
    print(f"\n--- {translations[current_language]['music_player']} ---")
    print(translations[current_language]['songs_available'])
    for key, song in SONGS_CATALOG.items():
        print(translations[current_language]['song_info'].format(key, song['title'], song['artist'], song['cost']))
        
    choice = input(translations[current_language]['purchase_song_prompt'])
    
    if choice in SONGS_CATALOG:
        song_to_play = SONGS_CATALOG[choice]
        if wallet >= song_to_play['cost']:
            wallet -= song_to_play['cost']
            print(translations[current_language]['song_purchased_opening'].format(song_to_play['title']))
            webbrowser.open_new_tab(song_to_play['url'])
            time.sleep(2)
        else:
            print(translations[current_language]['not_enough_tc_song'])
    elif choice.lower() != 'salir' and choice.lower() != 'exit' and choice.lower() != 'beenden':
        print(translations[current_language]['invalid_option_song'])
    
    input(translations[current_language]['press_enter_to_continue'])

def show_stickers_store():
    """Muestra y gestiona la compra y uso de stickers."""
    global wallet, rickroll_sticker_purchased, idiot_sticker_purchased, freddy_sticker_purchased
    
    print(f"\n--- {translations[current_language]['stickers_store']} ---")
    print(translations[current_language]['stickers_intro'])
    print(f"\n{translations[current_language]['stickers_available']}")
    
    if not rickroll_sticker_purchased:
        print(f"1. {translations[current_language]['rickroll_sticker']}")
        print(f"   {translations[current_language]['cost'].format(10000)}")
    else:
        print(f"1. '{translations[current_language]['rickroll_sticker'].split(':')[0]}' {translations[current_language]['purchased']}")
        
    if not idiot_sticker_purchased:
        print(f"2. {translations[current_language]['virus_sticker']}")
        print(f"   {translations[current_language]['cost'].format(20000)}")
    else:
        print(f"2. '{translations[current_language]['virus_sticker'].split(':')[0]}' {translations[current_language]['purchased']}")
        
    if not freddy_sticker_purchased:
        print(f"3. {translations[current_language]['freddy_sticker']}")
        print(f"   {translations[current_language]['cost'].format(30000)}")
    else:
        print(f"3. '{translations[current_language]['freddy_sticker'].split(':')[0]}' {translations[current_language]['purchased']}")
        
    choice = input(translations[current_language]['buy_or_use_sticker'])

    if choice == '1':
        if not rickroll_sticker_purchased:
            if wallet >= 10000:
                wallet -= 10000
                rickroll_sticker_purchased = True
                print(translations[current_language]['sticker_purchase_successful'].format('Rickroll'))
            else:
                print(translations[current_language]['not_enough_tc_sticker'])
        else:
            run_rickroll()

    elif choice == '2':
        if not idiot_sticker_purchased:
            if wallet >= 20000:
                wallet -= 20000
                idiot_sticker_purchased = True
                print(translations[current_language]['sticker_purchase_successful'].format('Virus, eres un idiota'))
            else:
                print(translations[current_language]['not_enough_tc_sticker'])
        else:
            run_idiot_sticker()

    elif choice == '3':
        if not freddy_sticker_purchased:
            if wallet >= 30000:
                wallet -= 30000
                freddy_sticker_purchased = True
                print(translations[current_language]['sticker_purchase_successful'].format('Freddy Fazbear'))
            else:
                print(translations[current_language]['not_enough_tc_sticker'])
        else:
            run_freddy_sticker()

    elif choice.lower() != 'salir' and choice.lower() != 'exit' and choice.lower() != 'beenden':
        print(translations[current_language]['invalid_option'])

    input(translations[current_language]['press_enter_to_continue'])

def change_language():
    """Permite al usuario cambiar el idioma del juego."""
    global current_language
    print(translations['es']['language_options'])
    new_lang = input(">>> ").lower()
    
    if new_lang in translations:
        current_language = new_lang
        print(translations[current_language]['language_change_successful'].format(new_lang.upper()))
    else:
        print(translations['es']['invalid_language'])
    
    input(translations[current_language]['press_enter_to_continue'])


def run_rickroll():
    """Abre un enlace de Rickroll en el navegador."""
    print(translations[current_language]['rickrolled_message'])
    webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    time.sleep(2)
    
def run_idiot_sticker():
    """Muestra un mensaje de 'virus' en ASCII."""
    clear_screen()
    print(Fore.RED + "==========================================================")
    print(f"  {translations[current_language]['virus_message_1'].upper().center(58)}")
    print("==========================================================")
    print("          .---.")
    print("         /     \\")
    print("        |   _   |")
    print("        |  (o)  |")
    print("        |   _   |")
    print("         \\     /")
    print("          `---'")
    print("==========================================================")
    print(Fore.RED + f"           {translations[current_language]['virus_message_2'].upper()}")
    print(Fore.YELLOW + f"            {translations[current_language]['virus_message_3']}")
    print(Fore.RED + "==========================================================")
    print(Style.RESET_ALL)
    input(translations[current_language]['press_enter_to_continue_virus'])
    
def run_freddy_sticker():
    """Simula una animación GIF de Freddy Fazbear con arte ASCII."""
    frames = [
        # Frame 1: Normal
        """
  .-.
 (o.o)
 | ^ |
 '--'
""",
        # Frame 2: Parpadeo
        """
  .-.
 (-.-)
 | ^ |
 '--'
""",
        # Frame 3: Con la mano arriba
        """
  .-.
 (o.o)
 | ^ |
 '--'
   _
 _/ |
|  |_
| / \\
""",
        # Frame 4: Mano en alto
        """
  .-.
 (o.o)
 | ^ |
 '--'
   _
 _/|
|  |
|  |
"""
    ]
    
    print(translations[current_language]['freddy_message_1'])
    time.sleep(1)
    
    for _ in range(3):
        for frame in frames:
            clear_screen()
            print(Fore.BLUE + Style.BRIGHT + "   F R E D D Y  F A Z B E A R" + Style.RESET_ALL)
            print(Fore.CYAN + frame + Style.RESET_ALL)
            time.sleep(0.3)
    
    clear_screen()
    print(translations[current_language]['freddy_message_2'])
    time.sleep(1)

# --- FUNCIONALIDAD DEL PROGRAMA TV HELPER ---
def run_tv_helper():
    clear_screen()
    print("--- Bienvenido a 'TV Helper' ---")
    print("Este programa te ayudará a encontrar la mejor televisión para ti.")
    time.sleep(2)
    
    class Televisor:
        """Clase que representa un televisor real con sus especificaciones."""
        def __init__(self, marca, modelo, tamano, resolucion, frecuencia, procesador, precio):
            self.marca = marca
            self.modelo = modelo
            self.tamano = tamano
            self.resolucion = resolucion
            self.frecuencia = frecuencia
            self.procesador = procesador
            self.precio = precio

    def obtener_datos_usuario():
        """Función para obtener las preferencias del usuario de forma interactiva."""
        print("--- ¡Bienvenido al Buscador de Televisores! ---")
        
        while True:
            respuesta_marca = input("¿Tienes una marca de televisor que te interese? (sí/no): ").lower()
            if respuesta_marca in ["si", "sí"]:
                marca_preferida = input("¿Cuál marca prefieres? ").capitalize()
                break
            elif respuesta_marca in ["no", "n"]:
                marca_preferida = None
                break
            else:
                print("❌ Respuesta no válida. Por favor, responde 'sí' o 'no'.")

        while True:
            try:
                tamano_deseado = int(input("¿Qué tamaño de televisor (en pulgadas) buscas? "))
                break
            except ValueError:
                print("❌ Por favor, ingresa un valor numérico válido.")

        resoluciones_disponibles = ["720p", "1080p", "4K", "8K"]
        while True:
            resolucion_deseada = input("¿Qué resolución quieres? (720p, 1080p, 4K, 8K): ").upper()
            if resolucion_deseada.lower() in [r.lower() for r in resoluciones_disponibles]:
                resolucion_deseada = resolucion_deseada.lower().replace("p", "P")
                break
            else:
                print("❌ Resolución no válida. Por favor, elige una de la lista.")

        while True:
            try:
                presupuesto_maximo = float(input("¿Cuál es tu presupuesto máximo en euros? (€): "))
                if presupuesto_maximo <= 0:
                    print("❌ Por favor, ingresa un valor positivo.")
                    continue
                break
            except ValueError:
                print("❌ Por favor, ingresa un valor numérico válido.")
        
        return marca_preferida, tamano_deseado, resolucion_deseada, presupuesto_maximo

    # --- Base de datos de televisores reales (Ampliada) ---
    DB_TELEVISORES_REALES = [
        # Gama alta (OLED/QLED)
        Televisor("LG", "OLED C3", 55, "4K", 120, "Alpha 9 Gen6", 1599.00),
        Televisor("LG", "OLED G3", 65, "4K", 120, "Alpha 9 Gen6", 2499.00),
        Televisor("Samsung", "S95C OLED", 65, "4K", 144, "Neural Quantum 4K", 2799.00),
        Televisor("Sony", "BRAVIA XR A95K", 65, "4K", 120, "Cognitive Processor XR", 2999.00),
        Televisor("LG", "OLED B3", 55, "4K", 120, "Alpha 7 Gen6", 1299.00),
        # Gama media (Mini-LED/QLED)
        Televisor("TCL", "C845", 65, "4K", 144, "AiPQ Processor 3.0", 1199.00),
        Televisor("Hisense", "U8K", 65, "4K", 144, "Hi-View Engine", 999.00),
        Televisor("Samsung", "QN90C Neo QLED", 55, "4K", 120, "Neural Quantum 4K", 1499.00),
        Televisor("LG", "Qned81", 65, "4K", 120, "Alpha 7 Gen6", 999.00),
        Televisor("Philips", "The One PUS8808", 55, "4K", 120, "P5 Perfect Picture", 799.00),
        # Gama baja (LED/LCD)
        Televisor("Hisense", "A6K", 50, "4K", 60, "Quad Core", 429.00),
        Televisor("TCL", "TCL 4K S4505B", 55, "4K", 60, "AiPQ", 399.00),
        Televisor("Samsung", "CU7105", 55, "4K", 50, "Crystal Processor 4K", 449.00),
        Televisor("Xiaomi", "TV A2", 43, "4K", 60, "Cortex-A55", 359.00),
        Televisor("LG", "UR7800", 50, "4K", 50, "Alpha 5 Gen6", 459.00),
        # Televisores Full HD y HD
        Televisor("Hisense", "A4K", 32, "1080p", 60, "Quad Core", 219.00),
        Televisor("Samsung", "T5305", 43, "1080p", 60, "Hyper Real", 299.00),
        Televisor("Xiaomi", "TV F2", 43, "1080p", 60, "A55 Quad-Core", 299.00),
        Televisor("TOSHIBA", "32CV510U", 32, "720p", 60, "no tiene", 180.00),
        Televisor("LG", "LQ5700", 32, "720p", 60, "Alpha 5 Gen5", 229.00),
        Televisor("Philips", "32PFS6906", 32, "1080p", 60, "P5", 249.00),
        # Televisores 8K
        Televisor("Samsung", "QN900C", 75, "8K", 144, "Neural Quantum 8K", 6999.00),
        Televisor("LG", "QNED99", 75, "8K", 120, "Alpha 9 Gen5", 3999.00),
    ]

    def encontrar_mejor_tv(db_televisores, marca_preferida, tamano_deseado, resolucion_deseada, presupuesto_maximo):
        """Encuentra y recomienda el mejor televisor según los criterios del usuario."""
        opciones_filtradas = []
        
        for tv in db_televisores:
            if marca_preferida and tv.marca.capitalize() != marca_preferida:
                continue
            if tv.precio > presupuesto_maximo:
                continue
            if tv.tamano != tamano_deseado:
                continue
            if tv.resolucion.upper() != resolucion_deseada.upper():
                continue
            opciones_filtradas.append(tv)
        
        if not opciones_filtradas:
            print("\n🤔 No se encontraron resultados con todos los criterios. Ampliando la búsqueda...")
            opciones_filtradas = []
            for tv in db_televisores:
                if tv.precio > presupuesto_maximo:
                    continue
                if tv.resolucion.upper() != resolucion_deseada.upper():
                    continue
                opciones_filtradas.append(tv)

        if not opciones_filtradas:
            print("\n🤔 No se encontraron resultados con los criterios de resolución y presupuesto. Mostrando las mejores opciones dentro de su presupuesto.")
            opciones_filtradas = []
            for tv in db_televisores:
                if tv.precio > presupuesto_maximo:
                    continue
                opciones_filtradas.append(tv)

        if not opciones_filtradas:
            return []

        opciones_con_score = []
        for tv in opciones_filtradas:
            score = 0
            
            resolucion_map = {"720p": 10, "1080p": 20, "4K": 50, "8K": 70}
            score += resolucion_map.get(tv.resolucion.lower(), 0)
            
            if tv.frecuencia >= 120:
                score += 40
            elif tv.frecuencia >= 60:
                score += 20
            
            if "Alpha" in tv.procesador or "Neural" in tv.procesador or "Cognitive" in tv.procesador:
                score += 30
            else:
                score += 10

            if tv.precio > 0:
                score = (score / tv.precio) * 1000

            opciones_con_score.append((score, tv))
            
        opciones_con_score.sort(key=lambda x: x[0], reverse=True)
        
        return opciones_con_score

    def mostrar_recomendacion(opciones_filtradas):
        """Muestra los 3 mejores televisores encontrados."""
        print("\n" + "="*50)
        print("          ✨ ¡Tu Televisor Ideal! ✨")
        print("="*50)
        
        if not opciones_filtradas:
            print("\nLo sentimos, no pudimos encontrar un televisor que se ajuste a tus criterios. \nTe recomendamos ajustar tu presupuesto o considerar otras opciones.")
        else:
            print("\nAquí tienes las 3 mejores opciones que se adaptan a tus necesidades:")
            for i, (score, tv) in enumerate(opciones_filtradas[:3]):
                print(f"\n{i+1}. {tv.marca} {tv.modelo}:")
                print(f"    - **Tamaño**: {tv.tamano} pulgadas")
                print(f"    - **Resolución**: {tv.resolucion}")
                print(f"    - **Frecuencia**: {tv.frecuencia} Hz")
                print(f"    - **Procesador de Imagen**: {tv.procesador}")
                print(f"    - **Precio**: {tv.precio:.2f}€")

    # --- Ejecución del programa ---
    marca_preferida, tamano_deseado, resolucion_deseada, presupuesto_maximo = obtener_datos_usuario()
    
    mejores_opciones = encontrar_mejor_tv(DB_TELEVISORES_REALES, marca_preferida, tamano_deseado, resolucion_deseada, presupuesto_maximo)
    mostrar_recomendacion(mejores_opciones)
    
    input("\nPulsa Enter para volver a TerminalCoin...")

# --- FUNCIONALIDAD DEL PROGRAMA MONSTER BATTLE CREATOR ---
def run_monster_battle_creator():
    """Ejecuta el juego Monster Battle Creator."""
    
    # Definición del archivo de guardado
    ARCHIVO_PROGRESO = 'progreso.json'

    # --- Definiciones de Partes del Monstruo ---
    opciones_cabeza = [
        ("Cabeza de Cíclope", "Un solo ojo y un cuerno en espiral.", "  _.-.\n  /  _ \\\n |  (o)  |\n  \\  _  /\n   `---'"),
        ("Cabeza de Dragón", "Dientes afilados y un aliento ardiente.", "  /vvvvv\\\n ( O   O )\n  \\  ^  /\n   \\___/"),
        ("Cabeza de Alien", "Grandes ojos negros y una forma alargada.", "  /\\_/\\\n | `~` |\n  \\___/"),
        ("Cabeza de Demonio", "Cuernos retorcidos y una mirada malvada.", " .-'--'-.\n/        \\\n|  O    O  |\n \\    --   /\n  `--__--'")
    ]

    opciones_cuerpo = [
        ("Cuerpo de Golem", "Fuerte y robusto, hecho de piedra.", "  [O.O]\n  /   \\\n /_____\\"),
        ("Cuerpo de Slime", "Viscoso y gelatinoso, capaz de cambiar de forma.", "  ~~~~~\n /     \\\n|_______|"),
        ("Cuerpo de Araña", "Ocho patas peludas y un cuerpo redondo.", "  /\\__/\\\n /      \\\n |______|"),
        ("Cuerpo de Momia", "Vendado y frágil, pero con gran resistencia.", " |---o---|\n |-------|\n  \\-----/")
    ]
        
    opciones_brazos = [
        ("Brazos de Robot", "Fuertes pero lentos, hechos de metal.", "  _|_|_\n (_____)"),
        ("Brazos de Mono", "Ágiles pero débiles, con pulgares oponibles.", "  /\\ /\\\n ( (o) )\n  \\   /"),
        ("Brazos de Dragón", "Lentos, pero fuertes, con garras afiladas.", "  || ||\n  \\ //\n   V V"),
        ("Brazos de Tentáculos", "Flexibles y largos, para agarrar objetos.", " ()()()()\n (      )\n  \\____/")
    ]

    opciones_piernas = [
        ("Piernas Humanoides", "Equilibradas y versátiles.", "  |_|  |_|\n  | |  | |"),
        ("Piernas de Centauro", "Fuertes y rápidas, con pezuñas.", "  | |  | |\n (  ) (  )"),
        ("Piernas de Lagarto", "Capaces de escalar superficies verticales.", "  /  \\  /  \\\n (____)(____)"),
        ("Piernas de Araña", "Múltiples patas para una movilidad superior.", "  / \\ / \\\n /   \   \\\n  -   -")
    ]

    # --- Arte ASCII de los trofeos ---
    TROFEO_CAMPEON = """
         _
        | |
        | |
        | |
        | |
       /---\
      |-----|
      `-----'
       || ||
       `-' `-'
    """

    TROFEO_VETERANO = """
           /`\\
          ( @ )
         /`\\ /`\\
        /   Y   \
       |  (.)  |
       `-------'
    """

    TROFEO_LEYENDA = """
         _ _
        | | |
       / / /
      | |_| |
      |_____|
      `-----'
       || ||
       `-' `-'
    """

    # Nuevas listas de nombres para enemigos y jefes
    nombres_rivales = [
        "Goro el Implacable", "Sombra de la Furia", "Gólem Dorado", "Lama Tóxica",
        "El Guerrero Oxidado", "Besta de las Profundidades", "El Acechador Sombrío",
        "El Vigilante de la Cripta"
    ]

    nombres_jefes = [
        "El Devorador de Mundos", "El Dragón Espectral", "El Titán Ancestral",
        "La Reina Silente", "El Amo de las Sombras"
    ]

    # --- Funciones de Juego ---
    def limpiar_pantalla():
        """Limpia la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_encabezado():
        """Muestra el título del programa."""
        limpiar_pantalla()
        print(Fore.CYAN + Style.BRIGHT + "=" * 60)
        print("== " + "C R E A D O R   Y   T O R N E O   D E   M O N S T R U O S".center(54) + " ==")
        print("=" * 60)
        print(Style.RESET_ALL)
        print(Fore.WHITE + "¡Crea a tu monstruo para el torneo! " + Style.RESET_ALL)
        time.sleep(1)

    def seleccionar_parte(titulo, opciones):
        """
        Función genérica para seleccionar una parte del monstruo.
        """
        while True:
            limpiar_pantalla()
            print(Fore.YELLOW + "--- " + titulo + " ---" + Style.RESET_ALL)
            for i, (nombre, descripcion, _) in enumerate(opciones, 1):
                print(f"{Fore.WHITE}{i}. {nombre}: {descripcion}{Style.RESET_ALL}")
            
            eleccion = input(f"\nElige tu opción (1, 2, 3 o 4): ")
            
            try:
                indice = int(eleccion) - 1
                if 0 <= indice < len(opciones):
                    return opciones[indice]
                else:
                    print(Fore.RED + "Opción inválida. Inténtalo de nuevo." + Style.RESET_ALL)
                    time.sleep(2)
            except ValueError:
                print(Fore.RED + "Entrada no válida. Por favor, ingresa un número." + Style.RESET_ALL)
                time.sleep(2)

    def generar_monstruo_aleatorio(nombre, es_boss=False):
        """Genera un monstruo con partes y colores aleatorios."""
        partes = {
            "cabeza": random.choice(opciones_cabeza),
            "cuerpo": random.choice(opciones_cuerpo),
            "brazos": random.choice(opciones_brazos),
            "piernas": random.choice(opciones_piernas)
        }
        colores_disponibles = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.YELLOW, Fore.CYAN]
        color1_elegido = random.choice(colores_disponibles)
        
        vida_base = 100
        if es_boss:
            vida_base = 200
        
        return {
            "nombre": nombre,
            "vida": float(vida_base),
            "energia": 100.0,
            "partes": partes,
            "color1": color1_elegido,
            "color2": random.choice([c for c in colores_disponibles if c != color1_elegido])
        }
        
    def mostrar_monstruo(monstruo):
        """Muestra un monstruo con sus partes y colores."""
        print(f"\n{Style.BRIGHT}{monstruo['nombre']}{Style.RESET_ALL}\n")
        print(monstruo['color1'] + "      " + monstruo['partes']['cabeza'][2])
        print(monstruo['color2'] + "    " + monstruo['partes']['cuerpo'][2])
        print(monstruo['color1'] + "  " + monstruo['partes']['brazos'][2])
        print(monstruo['color2'] + "  " + monstruo['partes']['piernas'][2])
        print(Style.RESET_ALL)

    def mostrar_monstruos_en_batalla(jugador, oponente):
        """Muestra a ambos monstruos uno al lado del otro, bien formados y con sus colores."""
        jugador_partes_split = [part[2].split('\n') for part in jugador['partes'].values()]
        oponente_partes_split = [part[2].split('\n') for part in oponente['partes'].values()]

        jugador_full_lines = []
        jugador_colors = [jugador['color1'], jugador['color2'], jugador['color1'], jugador['color2']]
        for i, part_lines in enumerate(jugador_partes_split):
            for line in part_lines:
                jugador_full_lines.append(jugador_colors[i] + line + Style.RESET_ALL)
                
        oponente_full_lines = []
        oponente_colors = [oponente['color1'], oponente['color2'], oponente['color1'], oponente['color2']]
        for i, part_lines in enumerate(oponente_partes_split):
            for line in part_lines:
                oponente_full_lines.append(oponente_colors[i] + line + Style.RESET_ALL)

        max_height = max(len(jugador_full_lines), len(oponente_full_lines))
        jugador_full_lines += [''] * (max_height - len(jugador_full_lines))
        oponente_full_lines += [''] * (max_height - len(oponente_full_lines))

        column_width = 30
        print(f"\n{Style.BRIGHT}{jugador['nombre']:<{column_width}}{oponente['nombre']:>{column_width}}{Style.RESET_ALL}")
        
        for i in range(max_height):
            def remove_ansi_escapes(s):
                return re.sub(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', '', s)
            
            clean_jugador_line = remove_ansi_escapes(jugador_full_lines[i])
            clean_oponente_line = remove_ansi_escapes(oponente_full_lines[i])
            
            jugador_padding = column_width - len(clean_jugador_line)
            oponente_padding = column_width - len(clean_oponente_line)
            
            print(f"{jugador_full_lines[i]}{' ' * jugador_padding}{' ' * oponente_padding}{oponente_full_lines[i]}")

    def mostrar_barras(vida_jugador, vida_oponente, energia_jugador):
        """Muestra las barras de vida y energía."""
        vida_jugador_clamped = max(0, vida_jugador)
        vida_oponente_clamped = max(0, vida_oponente)
        energia_jugador_clamped = max(0, energia_jugador)

        barra_vida_jugador = "█" * int(vida_jugador_clamped / 10)
        barra_vida_oponente = "█" * int(vida_oponente_clamped / 10)
        barra_energia = "█" * int(energia_jugador_clamped / 10)
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}VIDA:{Style.RESET_ALL} {Fore.GREEN}{barra_vida_jugador}{Fore.WHITE:<10}{Fore.RED}{Style.BRIGHT}VS{Style.RESET_ALL}{Fore.WHITE:>10}{Fore.RED}{barra_vida_oponente}{Fore.RED} VIDA:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}ENERGÍA:{Style.RESET_ALL} {Fore.BLUE}{barra_energia}{Style.RESET_ALL}")
        
    def pedir_combinacion(ronda, tipo_ataque="defensa"):
        """
        Pide una combinación de teclas al usuario y verifica si se presiona a tiempo.
        El tiempo de espera es más corto en rondas más altas.
        """
        
        keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
        
        combinacion = random.sample(keys, 2)
        key1, key2 = combinacion[0], combinacion[1]
        
        tiempo_espera = 2.0 - (ronda * 0.2)
        if tiempo_espera < 0.5:
            tiempo_espera = 0.5
            
        if tipo_ataque == "defensa":
            print(f"\n¡EL RIVAL ATACA! Rápido, presiona la combinación '{Fore.YELLOW}{key1} + {key2}{Style.RESET_ALL}' para defenderte.")
            print(f"Tienes {tiempo_espera:.2f} segundos para reaccionar...")
        else:
            print(f"\n¡ES TU TURNO! Presiona la combinación '{Fore.YELLOW}{key1} + {key2}{Style.RESET_ALL}' para atacar.")
            print(f"Tienes {tiempo_espera:.2f} segundos para reaccionar...")

        start_time = time.time()
        
        while time.time() - start_time < tiempo_espera:
            if keyboard.is_pressed(key1) and keyboard.is_pressed(key2):
                return True
                
        return False

    def simular_batalla_street_fighter(jugador, oponente, es_boss, ronda):
        """Simula una batalla interactiva al estilo de Street Fighter con combinaciones de teclas."""
        
        vida_jugador = float(jugador['vida'])
        energia_jugador = float(jugador['energia'])
        vida_oponente = float(oponente['vida'])

        print(Fore.CYAN + "\n=== ¡COMIENZA LA BATALLA! ===" + Style.RESET_ALL)
        input("Presiona Enter para continuar...")
        
        while vida_jugador > 0 and vida_oponente > 0:
            limpiar_pantalla()
            mostrar_barras(vida_jugador, vida_oponente, energia_jugador)
            mostrar_monstruos_en_batalla(jugador, oponente)
            
            # --- Fase de Defensa del Jugador ---
            print(Fore.RED + "\n--- FASE DE DEFENSA ---" + Style.RESET_ALL)
            if pedir_combinacion(ronda, tipo_ataque="defensa"):
                print(Fore.GREEN + "\n¡Combinación exitosa! Has creado una barrera y te has defendido del ataque del rival." + Style.RESET_ALL)
                time.sleep(2)
            else:
                daño_oponente = random.randint(15, 30)
                if es_boss and ronda == 4:
                    print(f"¡El ataque del jefe es devastador!")
                    daño_oponente = vida_jugador + 10
                vida_jugador -= daño_oponente
                print(Fore.RED + f"\n¡Combinación fallida! {oponente['nombre']} te golpea. Recibes {daño_oponente} de daño." + Style.RESET_ALL)
                time.sleep(2)
            
            if vida_jugador <= 0:
                break
                
            # --- Fase de Ataque del Jugador ---
            print(Fore.BLUE + "\n--- FASE DE ATAQUE ---" + Style.RESET_ALL)
            if pedir_combinacion(ronda, tipo_ataque="ofensiva"):
                daño_jugador = random.randint(20, 40)
                vida_oponente -= daño_jugador
                print(Fore.GREEN + f"\n¡Combinación exitosa! ¡Has atacado a {oponente['nombre']} y le has hecho {daño_jugador} de daño!" + Style.RESET_ALL)
                time.sleep(2)
            else:
                print(Fore.RED + "\n¡Combinación fallida! Pierdes tu turno de ataque." + Style.RESET_ALL)
                time.sleep(2)

        jugador['vida'] = vida_jugador
        jugador['energia'] = energia_jugador
        
        if vida_jugador <= 0:
            return oponente
        else:
            return jugador

    def cargar_progreso():
        """Carga el progreso del juego desde el archivo de guardado."""
        if os.path.exists(ARCHIVO_PROGRESO):
            try:
                with open(ARCHIVO_PROGRESO, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {'victorias': 0, 'trofeos': []}
        return {'victorias': 0, 'trofeos': []}

    def guardar_progreso(progreso):
        """Guarda el progreso del juego en el archivo de guardado."""
        with open(ARCHIVO_PROGRESO, 'w') as f:
            json.dump(progreso, f, indent=4)

    def mostrar_sala_trofeos(progreso):
        """Muestra la sala de trofeos del jugador."""
        limpiar_pantalla()
        print(Fore.YELLOW + Style.BRIGHT + "=== SALA DE TROFEOS ===" + Style.RESET_ALL)
        print(Fore.WHITE + f"Victorias en el Torneo: {progreso['victorias']}\n" + Style.RESET_ALL)
        
        if "leyenda" in progreso['trofeos']:
            print(Fore.CYAN + "--- Trofeo de Leyenda ---" + Style.RESET_ALL)
            print(Fore.CYAN + TROFEO_LEYENDA + Style.RESET_ALL)
            print(Fore.WHITE + "¡Has ganado 10 torneos! ¡Eres una leyenda del combate!\n" + Style.RESET_ALL)
        
        if "veterano" in progreso['trofeos']:
            print(Fore.GREEN + "--- Trofeo de Veterano ---" + Style.RESET_ALL)
            print(Fore.GREEN + TROFEO_VETERANO + Style.RESET_ALL)
            print(Fore.WHITE + "¡Has ganado 5 torneos! Un verdadero veterano.\n" + Style.RESET_ALL)

        if "campeon" in progreso['trofeos']:
            print(Fore.YELLOW + "--- Trofeo de Campeón ---" + Style.RESET_ALL)
            print(Fore.YELLOW + TROFEO_CAMPEON + Style.RESET_ALL)
            print(Fore.WHITE + "¡Has derrotado al Jefe Final y ganado un torneo!\n" + Style.RESET_ALL)
        
        if not progreso['trofeos']:
            print(Fore.WHITE + "Aún no tienes trofeos. ¡Gana el torneo para conseguir el primero!\n" + Style.RESET_ALL)
        
        input(Fore.BLUE + "Presiona Enter para volver al menú principal..." + Style.RESET_ALL)
    
    # Bucle principal del juego Monster Battle Creator
    while True:
        progreso = cargar_progreso()
        
        limpiar_pantalla()
        print(Fore.CYAN + Style.BRIGHT + "=" * 60)
        print("== " + "M E N Ú   P R I N C I P A L".center(54) + " ==")
        print("=" * 60)
        print(Style.RESET_ALL)
        print(Fore.WHITE + "1. ¡Comenzar un nuevo torneo!" + Style.RESET_ALL)
        print(Fore.YELLOW + "2. Ver mi Sala de Trofeos" + Style.RESET_ALL)
        print(Fore.RED + "3. Salir" + Style.RESET_ALL)
        
        opcion = input("\nElige una opción: ")
        
        if opcion == '1':
            mostrar_encabezado()
            time.sleep(1)
            
            print(Fore.GREEN + "\n--- CREA A TU MONSTRUO PARA EL TORNEO ---" + Style.RESET_ALL)
            _, descripcion_cabeza, arte_cabeza = seleccionar_parte("Selecciona una cabeza para tu monstruo", opciones_cabeza)
            _, descripcion_cuerpo, arte_cuerpo = seleccionar_parte("Ahora, selecciona un cuerpo", opciones_cuerpo)
            _, descripcion_brazos, arte_brazos = seleccionar_parte("Y por último, elige unos brazos", opciones_brazos)
            _, descripcion_piernas, arte_piernas = seleccionar_parte("Finalmente, elige unas piernas", opciones_piernas)
            
            nombre_jugador = input("\n¡Ponle un nombre a tu campeón!: ")

            monstruo_jugador = generar_monstruo_aleatorio(nombre_jugador)
            monstruo_jugador["partes"] = {
                "cabeza": ("Cabeza", descripcion_cabeza, arte_cabeza),
                "cuerpo": ("Cuerpo", descripcion_cuerpo, arte_cuerpo),
                "brazos": ("Brazos", descripcion_brazos, arte_brazos),
                "piernas": ("Piernas", descripcion_piernas, arte_piernas)
            }

            limpiar_pantalla()
            print(Fore.GREEN + Style.BRIGHT + "=" * 50)
            print("== " + "¡T U   M O N S T R U O   H A   S I D O   C R E A D O !".center(44) + " ==")
            print("=" * 50 + Style.RESET_ALL)
            mostrar_monstruo(monstruo_jugador)
            print(Fore.WHITE + "\n--- Características de tu campeón ---" + Style.RESET_ALL)
            print(f"{Fore.WHITE}CABEZA: {descripcion_cabeza}")
            print(f"{Fore.WHITE}CUERPO: {descripcion_cuerpo}")
            print(f"{Fore.WHITE}BRAZOS: {descripcion_brazos}")
            print(f"{Fore.WHITE}PIERNAS: {descripcion_piernas}{Style.RESET_ALL}")
            input(Fore.BLUE + "\nPresiona Enter para comenzar el torneo..." + Style.RESET_ALL)
            
            # --- TUTORIAL DE JUEGO ---
            limpiar_pantalla()
            print(Fore.CYAN + Style.BRIGHT + "=== TUTORIAL DE COMBATE ===" + Style.RESET_ALL)
            print(Fore.WHITE + "¡Bienvenido al Torneo de Monstruos! Para ganar, deberás dominar las combinaciones de teclas.")
            print("La batalla se divide en dos fases por turno:")
            print(f"\n{Fore.RED}{Style.BRIGHT}1. FASE DE DEFENSA:{Style.RESET_ALL} El rival te atacará.")
            print(f"   Debes presionar una combinación de 2 teclas (ej: 'a' + 's') para defenderte.")
            print(f"   Si lo logras, te defenderás. Si fallas, recibirás daño.")
            print(f"\n{Fore.BLUE}{Style.BRIGHT}2. FASE DE ATAQUE:{Style.RESET_ALL} Es tu turno.")
            print(f"   Debes presionar una nueva combinación de 2 teclas para atacar.")
            print(f"   Si lo consigues, dañarás al rival. Si no, perderás el turno.")
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}¡Importante!:{Style.RESET_ALL} El tiempo para reaccionar se reduce en cada ronda.")
            print("   En la batalla final, deberás ser extremadamente rápido para sobrevivir.")
            input(Fore.BLUE + "\nPresiona Enter para continuar y comenzar la primera batalla..." + Style.RESET_ALL)

            # --- FASE 2: EL TORNEO ---
            rivales_torneo = random.sample(nombres_rivales, 3)
            nombre_jefe_final = random.choice(nombres_jefes)
            rivales_torneo.append(nombre_jefe_final)
            
            torneo_ganado = False
            
            for i, nombre_rival in enumerate(rivales_torneo):
                es_boss = (nombre_rival == nombre_jefe_final)
                limpiar_pantalla()
                if es_boss:
                    print(Fore.RED + f"--- ¡EL JEFE FINAL! ---" + Style.RESET_ALL)
                    oponente = generar_monstruo_aleatorio(nombre_rival, es_boss=True)
                else:
                    print(Fore.YELLOW + f"--- BATALLA {i+1} DE {len(rivales_torneo)} ---" + Style.RESET_ALL)
                    oponente = generar_monstruo_aleatorio(nombre_rival)

                print(f"\n¡Tu monstruo {monstruo_jugador['nombre']} se enfrenta a {oponente['nombre']}!")
                input("Presiona Enter para luchar...")

                ganador = simular_batalla_street_fighter(monstruo_jugador, oponente, es_boss, i+1)

                if ganador['nombre'] == monstruo_jugador['nombre']:
                    print(Fore.GREEN + f"\n¡Has derrotado a {oponente['nombre']}! ¡Felicidades!" + Style.RESET_ALL)
                    if es_boss:
                        print(Fore.YELLOW + Style.BRIGHT + "\n¡¡¡HAS DERROTADO AL JEFE FINAL Y GANADO EL TORNEO!!!" + Style.RESET_ALL)
                        torneo_ganado = True
                        break
                    input("\nPresiona Enter para pasar a la siguiente batalla...")
                else:
                    print(Fore.RED + f"\n¡Has sido derrotado por {oponente['nombre']}! ¡El torneo ha terminado!" + Style.RESET_ALL)
                    break

            # Actualizar el progreso al final del torneo
            if torneo_ganado:
                progreso['victorias'] += 1
                if "campeon" not in progreso['trofeos']:
                    progreso['trofeos'].append('campeon')
                if progreso['victorias'] >= 5 and "veterano" not in progreso['trofeos']:
                    progreso['trofeos'].append('veterano')
                    print(Fore.GREEN + "\n¡Has desbloqueado el Trofeo de Veterano!" + Style.RESET_ALL)
                if progreso['victorias'] >= 10 and "leyenda" not in progreso['trofeos']:
                    progreso['trofeos'].append('leyenda')
                    print(Fore.CYAN + "\n¡Has desbloqueado el Trofeo de Leyenda! ¡Eres un maestro!" + Style.RESET_ALL)
            
            guardar_progreso(progreso)

            # Comprobar el resultado final del juego
            if monstruo_jugador['vida'] > 0:
                limpiar_pantalla()
                print(Fore.YELLOW + Style.BRIGHT + "=" * 50)
                print("== " + "¡VICTORIA! ¡ERES EL CAMPEÓN DEL TORNEO!".center(44) + " ==")
                print("=" * 50 + Style.RESET_ALL)
                mostrar_monstruo(monstruo_jugador)
                print(Fore.GREEN + "\n¡Tu monstruo ha vencido a todos los rivales y al JEFE FINAL!" + Style.RESET_ALL)
            
            print("\n¿Quieres jugar de nuevo? (Presiona Enter para reiniciar)")
            input()
            
        elif opcion == '2':
            mostrar_sala_trofeos(progreso)
            
        elif opcion == '3':
            print("Saliendo del juego...")
            break
            
        else:
            print(Fore.RED + "Opción no válida. Por favor, elige 1, 2 o 3." + Style.RESET_ALL)
            time.sleep(2)

# --- Bucle principal del juego ---
if __name__ == "__main__":
    load_game()
    while True:
        clear_screen()
        display_terminalcoin_logo()
        update_wallet()
        check_for_new_codes()
        show_status()
        
        user_input = input(translations[current_language]['choice_prompt'])
        
        if user_input == '1':
            buy_upgrade()
        elif user_input == '2':
            buy_boost()
        elif user_input == '3':
            show_programs_store()
        elif user_input == '4':
            manage_codes()
        elif user_input == '5':
            save_game()
        elif user_input == '6':
            play_music()
        elif user_input == '7':
            show_stickers_store()
        elif user_input == '8':
            change_language()
        elif user_input == '9':
            save_game()
            print(translations[current_language]['exit_game'])
            break
        else:
            print(translations[current_language]['invalid_option'])
            time.sleep(1)
