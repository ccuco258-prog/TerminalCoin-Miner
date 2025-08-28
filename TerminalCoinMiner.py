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
current_language = 'en' # Idioma por defecto

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
        'invalid_language': "Idioma no válido. Volviendo al menú principal.",
        
        # Traducciones de TV Helper
        'tvh_welcome': "--- Bienvenido a 'TV Helper' ---",
        'tvh_intro': "Este programa te ayudará a encontrar la mejor televisión para ti.",
        'tvh_prompt_brand_interest': "¿Tienes una marca de televisor que te interese? (sí/no): ",
        'tvh_prompt_preferred_brand': "¿Cuál marca prefieres? ",
        'tvh_prompt_size': "¿Qué tamaño de televisor (en pulgadas) buscas? ",
        'tvh_prompt_resolution': "¿Qué resolución quieres? (720p, 1080p, 4K, 8K): ",
        'tvh_prompt_budget': "¿Cuál es tu presupuesto máximo en euros? (€): ",
        'tvh_invalid_response': "❌ Respuesta no válida. Por favor, responde 'sí' o 'no'.",
        'tvh_invalid_number': "❌ Por favor, ingresa un valor numérico válido.",
        'tvh_invalid_resolution': "❌ Resolución no válida. Por favor, elige una de la lista.",
        'tvh_positive_value_required': "❌ Por favor, ingresa un valor positivo.",
        'tvh_no_results_all_criteria': "\n🤔 No se encontraron resultados con todos los criterios. Ampliando la búsqueda...",
        'tvh_no_results_res_budget': "\n🤔 No se encontraron resultados con los criterios de resolución y presupuesto. Mostrando las mejores opciones dentro de su presupuesto.",
        'tvh_recommendation_title': "✨ ¡Tu Televisor Ideal! ✨",
        'tvh_recommendation_intro': "\nAquí tienes las 3 mejores opciones que se adaptan a tus necesidades:",
        'tvh_no_results_found': "\nLo sentimos, no pudimos encontrar un televisor que se ajuste a tus criterios. \nTe recomendamos ajustar tu presupuesto o considerar otras opciones.",
        'tvh_size': "    - **Tamaño**: {} pulgadas",
        'tvh_resolution': "    - **Resolución**: {}",
        'tvh_refresh_rate': "    - **Frecuencia**: {} Hz",
        'tvh_processor': "    - **Procesador de Imagen**: {}",
        'tvh_price': "    - **Precio**: {:.2f}€",
        'tvh_return_to_main': "\nPulsa Enter para volver a TerminalCoin...",
        
        # Traducciones de Monster Battle Creator
        'mbc_title_1': "C R E A D O R   Y   T O R N E O   D E   M O N S T R U O S",
        'mbc_intro_1': "¡Crea a tu monstruo para el torneo! ",
        'mbc_menu_title': "M E N Ú   P R I N C I P A L",
        'mbc_option_1': "1. ¡Comenzar un nuevo torneo!",
        'mbc_option_2': "2. Ver mi Sala de Trofeos",
        'mbc_option_3': "3. Salir",
        'mbc_choice_prompt': "\nElige una opción: ",
        'mbc_invalid_menu_option': "Opción no válida. Por favor, elige 1, 2 o 3.",
        'mbc_intro_2': "--- CREA A TU MONSTRUO PARA EL TORNEO ---",
        'mbc_select_head': "Selecciona una cabeza para tu monstruo",
        'mbc_select_body': "Ahora, selecciona un cuerpo",
        'mbc_select_arms': "Y por último, elige unos brazos",
        'mbc_select_legs': "Finalmente, elige unas piernas",
        'mbc_prompt_name': "\n¡Ponle un nombre a tu campeón!: ",
        'mbc_created_title': "¡T U   M O N S T R U O   H A   S I D O   C R E A D O !",
        'mbc_char_title': "--- Características de tu campeón ---",
        'mbc_head_char': "CABEZA: {}",
        'mbc_body_char': "CUERPO: {}",
        'mbc_arms_char': "BRAZOS: {}",
        'mbc_legs_char': "PIERNAS: {}",
        'mbc_press_to_start': "\nPresiona Enter para comenzar el torneo...",
        'mbc_tutorial_title': "=== TUTORIAL DE COMBATE ===",
        'mbc_tutorial_intro': "¡Bienvenido al Torneo de Monstruos! Para ganar, deberás dominar las combinaciones de teclas.",
        'mbc_tutorial_phases': "La batalla se divide en dos fases por turno:",
        'mbc_tutorial_defense': "1. FASE DE DEFENSA:",
        'mbc_tutorial_defense_desc': "El rival te atacará. Debes presionar una combinación de 2 teclas (ej: 'a' + 's') para defenderte. Si lo logras, te defenderás. Si fallas, recibirás daño.",
        'mbc_tutorial_attack': "2. FASE DE ATAQUE:",
        'mbc_tutorial_attack_desc': "Es tu turno. Debes presionar una nueva combinación de 2 teclas para atacar. Si lo consigues, dañarás al rival. Si no, perderás el turno.",
        'mbc_tutorial_important': "¡Importante!:",
        'mbc_tutorial_important_desc': "El tiempo para reaccionar se reduce en cada ronda. En la batalla final, deberás ser extremadamente rápido para sobrevivir.",
        'mbc_tutorial_continue': "\nPresiona Enter para continuar y comenzar la primera batalla...",
        'mbc_battle_start': "=== ¡COMIENZA LA BATALLA! ===",
        'mbc_press_to_continue': "Presiona Enter para continuar...",
        'mbc_phase_defense': "--- FASE DE DEFENSA ---",
        'mbc_prompt_defense': "¡EL RIVAL ATACA! Rápido, presiona la combinación '{} + {}' para defenderte. Tienes {:.2f} segundos para reaccionar...",
        'mbc_defense_success': "\n¡Combinación exitosa! Has creado una barrera y te has defendido del ataque del rival.",
        'mbc_defense_fail': "\n¡Combinación fallida! {} te golpea. Recibes {} de daño.",
        'mbc_boss_attack_strong': "¡El ataque del jefe es devastador!",
        'mbc_phase_attack': "--- FASE DE ATAQUE ---",
        'mbc_prompt_attack': "¡ES TU TURNO! Presiona la combinación '{} + {}' para atacar. Tienes {:.2f} segundos para reaccionar...",
        'mbc_attack_success': "\n¡Combinación exitosa! ¡Has atacado a {} y le has hecho {} de daño!",
        'mbc_attack_fail': "\n¡Combinación fallida! Pierdes tu turno de ataque.",
        'mbc_win_battle': "\n¡Has derrotado a {}! ¡Felicidades!",
        'mbc_win_final_boss': "\n¡¡¡HAS DERROTADO AL JEFE FINAL Y GANADO EL TORNEO!!!",
        'mbc_lose_battle': "\n¡Has sido derrotado por {}! ¡El torneo ha terminado!",
        'mbc_win_trophy_veteran': "\n¡Has desbloqueado el Trofeo de Veterano!",
        'mbc_win_trophy_legend': "\n¡Has desbloqueado el Trofeo de Leyenda! ¡Eres un maestro!",
        'mbc_final_victory': "¡VICTORIA! ¡ERES EL CAMPEÓN DEL TORNEO!",
        'mbc_final_victory_desc': "\n¡Tu monstruo ha vencido a todos los rivales y al JEFE FINAL!",
        'mbc_play_again': "\n¿Quieres jugar de nuevo? (Presiona Enter para reiniciar)",
        'mbc_trophy_room_title': "=== SALA DE TROFEOS ===",
        'mbc_trophies_won_count': "Victorias en el Torneo: {}",
        'mbc_trophy_legend_title': "--- Trofeo de Leyenda ---",
        'mbc_trophy_legend_desc': "¡Has ganado 10 torneos! ¡Eres una leyenda del combate!",
        'mbc_trophy_veteran_title': "--- Trofeo de Veterano ---",
        'mbc_trophy_veteran_desc': "¡Has ganado 5 torneos! Un verdadero veterano.",
        'mbc_trophy_champion_title': "--- Trofeo de Campeón ---",
        'mbc_trophy_champion_desc': "¡Has derrotado al Jefe Final y ganado un torneo!",
        'mbc_no_trophies': "Aún no tienes trofeos. ¡Gana el torneo para conseguir el primero!",
        'mbc_return_to_menu': "Presiona Enter para volver al menú principal...",
        'mbc_exit_game': "Saliendo del juego...",
        'mbc_health': "VIDA:",
        'mbc_energy': "ENERGÍA:",
        'mbc_vs': "VS",
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
        'invalid_language': "Invalid language. Returning to the main menu.",
        
        # TV Helper translations
        'tvh_welcome': "--- Welcome to 'TV Helper' ---",
        'tvh_intro': "This program will help you find the best TV for you.",
        'tvh_prompt_brand_interest': "Do you have a TV brand you're interested in? (yes/no): ",
        'tvh_prompt_preferred_brand': "Which brand do you prefer? ",
        'tvh_prompt_size': "What size TV (in inches) are you looking for? ",
        'tvh_prompt_resolution': "What resolution do you want? (720p, 1080p, 4K, 8K): ",
        'tvh_prompt_budget': "What is your maximum budget in Euros? (€): ",
        'tvh_invalid_response': "❌ Invalid response. Please answer 'yes' or 'no'.",
        'tvh_invalid_number': "❌ Please enter a valid number.",
        'tvh_invalid_resolution': "❌ Invalid resolution. Please choose from the list.",
        'tvh_positive_value_required': "❌ Please enter a positive value.",
        'tvh_no_results_all_criteria': "\n🤔 No results found with all criteria. Broadening the search...",
        'tvh_no_results_res_budget': "\n🤔 No results found with resolution and budget criteria. Displaying the best options within your budget.",
        'tvh_recommendation_title': "✨ Your Ideal TV! ✨",
        'tvh_recommendation_intro': "\nHere are the top 3 options that fit your needs:",
        'tvh_no_results_found': "\nSorry, we couldn't find a TV that fits your criteria. \nWe recommend adjusting your budget or considering other options.",
        'tvh_size': "    - **Size**: {} inches",
        'tvh_resolution': "    - **Resolution**: {}",
        'tvh_refresh_rate': "    - **Refresh Rate**: {} Hz",
        'tvh_processor': "    - **Image Processor**: {}",
        'tvh_price': "    - **Price**: {:.2f}€",
        'tvh_return_to_main': "\nPress Enter to return to TerminalCoin...",

        # Monster Battle Creator translations
        'mbc_title_1': "M O N S T E R   C R E A T O R   A N D   T O U R N A M E N T",
        'mbc_intro_1': "Create your monster for the tournament! ",
        'mbc_menu_title': "M A I N   M E N U",
        'mbc_option_1': "1. Start a new tournament!",
        'mbc_option_2': "2. View my Trophy Room",
        'mbc_option_3': "3. Exit",
        'mbc_choice_prompt': "\nChoose an option: ",
        'mbc_invalid_menu_option': "Invalid option. Please choose 1, 2, or 3.",
        'mbc_intro_2': "--- CREATE YOUR MONSTER FOR THE TOURNAMENT ---",
        'mbc_select_head': "Select a head for your monster",
        'mbc_select_body': "Now, select a body",
        'mbc_select_arms': "And finally, choose a pair of arms",
        'mbc_select_legs': "Lastly, choose a pair of legs",
        'mbc_prompt_name': "\nGive your champion a name!: ",
        'mbc_created_title': "Y O U R   M O N S T E R   H A S   B E E N   C R E A T E D !",
        'mbc_char_title': "--- Characteristics of your champion ---",
        'mbc_head_char': "HEAD: {}",
        'mbc_body_char': "BODY: {}",
        'mbc_arms_char': "ARMS: {}",
        'mbc_legs_char': "LEGS: {}",
        'mbc_press_to_start': "\nPress Enter to start the tournament...",
        'mbc_tutorial_title': "=== BATTLE TUTORIAL ===",
        'mbc_tutorial_intro': "Welcome to the Monster Tournament! To win, you must master the key combinations.",
        'mbc_tutorial_phases': "The battle is divided into two phases per turn:",
        'mbc_tutorial_defense': "1. DEFENSE PHASE:",
        'mbc_tutorial_defense_desc': "The opponent will attack you. You must press a 2-key combination (e.g., 'a' + 's') to defend yourself. If you succeed, you will defend. If you fail, you will take damage.",
        'mbc_tutorial_attack': "2. ATTACK PHASE:",
        'mbc_tutorial_attack_desc': "It's your turn. You must press a new 2-key combination to attack. If you succeed, you will damage the opponent. If not, you will lose your turn.",
        'mbc_tutorial_important': "Important!:",
        'mbc_tutorial_important_desc': "The reaction time decreases with each round. In the final battle, you must be extremely fast to survive.",
        'mbc_tutorial_continue': "\nPress Enter to continue and start the first battle...",
        'mbc_battle_start': "=== BATTLE BEGINS! ===",
        'mbc_press_to_continue': "Press Enter to continue...",
        'mbc_phase_defense': "--- DEFENSE PHASE ---",
        'mbc_prompt_defense': "THE OPPONENT ATTACKS! Quick, press the combination '{} + {}' to defend yourself. You have {:.2f} seconds to react...",
        'mbc_defense_success': "\nCombination successful! You have created a barrier and defended yourself from the opponent's attack.",
        'mbc_defense_fail': "\nCombination failed! {} hits you. You take {} damage.",
        'mbc_boss_attack_strong': "The boss's attack is devastating!",
        'mbc_phase_attack': "--- ATTACK PHASE ---",
        'mbc_prompt_attack': "IT'S YOUR TURN! Press the combination '{} + {}' to attack. You have {:.2f} seconds to react...",
        'mbc_attack_success': "\nCombination successful! You have attacked {} and dealt {} damage!",
        'mbc_attack_fail': "\nCombination failed! You lose your attack turn.",
        'mbc_win_battle': "\nYou have defeated {}! Congratulations!",
        'mbc_win_final_boss': "\nYOU HAVE DEFEATED THE FINAL BOSS AND WON THE TOURNAMENT!!!",
        'mbc_lose_battle': "\nYou have been defeated by {}! The tournament is over!",
        'mbc_win_trophy_veteran': "\nYou have unlocked the Veteran Trophy!",
        'mbc_win_trophy_legend': "\nYou have unlocked the Legend Trophy! You are a master!",
        'mbc_final_victory': "VICTORY! YOU ARE THE TOURNAMENT CHAMPION!",
        'mbc_final_victory_desc': "\nYour monster has defeated all rivals and the FINAL BOSS!",
        'mbc_play_again': "\nDo you want to play again? (Press Enter to restart)",
        'mbc_trophy_room_title': "=== TROPHY ROOM ===",
        'mbc_trophies_won_count': "Tournament Victories: {}",
        'mbc_trophy_legend_title': "--- Legend Trophy ---",
        'mbc_trophy_legend_desc': "You have won 10 tournaments! You are a combat legend!",
        'mbc_trophy_veteran_title': "--- Veteran Trophy ---",
        'mbc_trophy_veteran_desc': "You have won 5 tournaments! A true veteran.",
        'mbc_trophy_champion_title': "--- Champion Trophy ---",
        'mbc_trophy_champion_desc': "You have defeated the Final Boss and won a tournament!",
        'mbc_no_trophies': "You don't have any trophies yet. Win the tournament to get your first one!",
        'mbc_return_to_menu': "Press Enter to return to the main menu...",
        'mbc_exit_game': "Exiting the game...",
        'mbc_health': "HEALTH:",
        'mbc_energy': "ENERGY:",
        'mbc_vs': "VS",
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
        'invalid_language': "Ungültige Sprache. Kehre zum Hauptmenü zurück.",

        # TV Helper translations
        'tvh_welcome': "--- Willkommen bei 'TV Helper' ---",
        'tvh_intro': "Dieses Programm hilft dir, den besten Fernseher für dich zu finden.",
        'tvh_prompt_brand_interest': "Bist du an einer bestimmten TV-Marke interessiert? (ja/nein): ",
        'tvh_prompt_preferred_brand': "Welche Marke bevorzugst du? ",
        'tvh_prompt_size': "Welche TV-Größe (in Zoll) suchst du? ",
        'tvh_prompt_resolution': "Welche Auflösung möchtest du? (720p, 1080p, 4K, 8K): ",
        'tvh_prompt_budget': "Was ist dein maximales Budget in Euro? (€): ",
        'tvh_invalid_response': "❌ Ungültige Antwort. Bitte antworte 'ja' oder 'nein'.",
        'tvh_invalid_number': "❌ Bitte gib eine gültige Zahl ein.",
        'tvh_invalid_resolution': "❌ Ungültige Auflösung. Bitte wähle aus der Liste.",
        'tvh_positive_value_required': "❌ Bitte gib einen positiven Wert ein.",
        'tvh_no_results_all_criteria': "\n🤔 Keine Ergebnisse mit allen Kriterien gefunden. Suche wird erweitert...",
        'tvh_no_results_res_budget': "\n🤔 Keine Ergebnisse mit den Kriterien Auflösung und Budget gefunden. Es werden die besten Optionen innerhalb deines Budgets angezeigt.",
        'tvh_recommendation_title': "✨ Dein Idealer Fernseher! ✨",
        'tvh_recommendation_intro': "\nHier sind die 3 besten Optionen, die zu deinen Bedürfnissen passen:",
        'tvh_no_results_found': "\nLeider konnten wir keinen Fernseher finden, der deinen Kriterien entspricht. \nWir empfehlen, dein Budget anzupassen oder andere Optionen in Betracht zu ziehen.",
        'tvh_size': "    - **Größe**: {} Zoll",
        'tvh_resolution': "    - **Auflösung**: {}",
        'tvh_refresh_rate': "    - **Bildwiederholfrequenz**: {} Hz",
        'tvh_processor': "    - **Bildprozessor**: {}",
        'tvh_price': "    - **Preis**: {:.2f}€",
        'tvh_return_to_main': "\nDrücke Enter, um zu TerminalCoin zurückzukehren...",

        # Monster Battle Creator translations
        'mbc_title_1': "M O N S T E R - E R S T E L L E R   U N D   T U R N I E R",
        'mbc_intro_1': "Erstelle dein Monster für das Turnier! ",
        'mbc_menu_title': "H A U P T M E N Ü",
        'mbc_option_1': "1. Ein neues Turnier starten!",
        'mbc_option_2': "2. Meine Trophäenkammer ansehen",
        'mbc_option_3': "3. Beenden",
        'mbc_choice_prompt': "\nWähle eine Option: ",
        'mbc_invalid_menu_option': "Ungültige Option. Bitte wähle 1, 2 oder 3.",
        'mbc_intro_2': "--- ERSTELLE DEIN MONSTER FÜR DAS TURNIER ---",
        'mbc_select_head': "Wähle einen Kopf für dein Monster",
        'mbc_select_body': "Jetzt, wähle einen Körper",
        'mbc_select_arms': "Und zum Schluss, wähle ein Paar Arme",
        'mbc_select_legs': "Zuletzt, wähle ein Paar Beine",
        'mbc_prompt_name': "\nGib deinem Champion einen Namen!: ",
        'mbc_created_title': "D E I N   M O N S T E R   W U R D E   E R S T E L L T !",
        'mbc_char_title': "--- Eigenschaften deines Champions ---",
        'mbc_head_char': "KOPF: {}",
        'mbc_body_char': "KÖRPER: {}",
        'mbc_arms_char': "ARME: {}",
        'mbc_legs_char': "BEINE: {}",
        'mbc_press_to_start': "\nDrücke Enter, um das Turnier zu starten...",
        'mbc_tutorial_title': "=== KAMPF-TUTORIAL ===",
        'mbc_tutorial_intro': "Willkommen beim Monster-Turnier! Um zu gewinnen, musst du die Tastenkombinationen meistern.",
        'mbc_tutorial_phases': "Der Kampf ist pro Zug in zwei Phasen unterteilt:",
        'mbc_tutorial_defense': "1. VERTEIDIGUNGSPHASE:",
        'mbc_tutorial_defense_desc': "Der Gegner wird dich angreifen. Du musst eine 2-Tasten-Kombination (z.B. 'a' + 's') drücken, um dich zu verteidigen. Wenn du Erfolg hast, verteidigst du dich. Wenn du scheiterst, nimmst du Schaden.",
        'mbc_tutorial_attack': "2. ANGRIFFSPHASE:",
        'mbc_tutorial_attack_desc': "Du bist am Zug. Du musst eine neue 2-Tasten-Kombination drücken, um anzugreifen. Wenn du Erfolg hast, fügst du dem Gegner Schaden zu. Wenn nicht, verlierst du deinen Zug.",
        'mbc_tutorial_important': "Wichtig!:",
        'mbc_tutorial_important_desc': "Die Reaktionszeit wird mit jeder Runde kürzer. Im Endkampf musst du extrem schnell sein, um zu überleben.",
        'mbc_tutorial_continue': "\nDrücke Enter, um fortzufahren und den ersten Kampf zu beginnen...",
        'mbc_battle_start': "=== KAMPF BEGINNT! ===",
        'mbc_press_to_continue': "Drücke Enter, um fortzufahren...",
        'mbc_phase_defense': "--- VERTEIDIGUNGSPHASE ---",
        'mbc_prompt_defense': "DER GEGNER GREIFT AN! Schnell, drücke die Kombination '{} + {}', um dich zu verteidigen. Du hast {:.2f} Sekunden zum Reagieren...",
        'mbc_defense_success': "\nKombination erfolgreich! Du hast eine Barriere erschaffen und dich vor dem Angriff des Gegners verteidigt.",
        'mbc_defense_fail': "\nKombination fehlgeschlagen! {} trifft dich. Du erleidest {} Schaden.",
        'mbc_boss_attack_strong': "Der Angriff des Bosses ist verheerend!",
        'mbc_phase_attack': "--- ANGRIFFSPHASE ---",
        'mbc_prompt_attack': "DU BIST AM ZUG! Drücke die Kombination '{} + {}', um anzugreifen. Du hast {:.2f} Sekunden zum Reagieren...",
        'mbc_attack_success': "\nKombination erfolgreich! Du hast {} angegriffen und {} Schaden verursacht!",
        'mbc_attack_fail': "\nKombination fehlgeschlagen! Du verlierst deinen Angriffs-Zug.",
        'mbc_win_battle': "\nDu hast {} besiegt! Herzlichen Glückwunsch!",
        'mbc_win_final_boss': "\nDU HAST DEN ENDBOSS BESIEGT UND DAS TURNIER GEWONNEN!!!",
        'mbc_lose_battle': "\nDu wurdest von {} besiegt! Das Turnier ist vorbei!",
        'mbc_win_trophy_veteran': "\nDu hast die Veteranen-Trophäe freigeschaltet!",
        'mbc_win_trophy_legend': "\nDu hast die Legenden-Trophäe freigeschaltet! Du bist ein Meister!",
        'mbc_final_victory': "SIEG! DU BIST DER TURNIER-CHAMPION!",
        'mbc_final_victory_desc': "\nDein Monster hat alle Rivalen und den ENDBOSS besiegt!",
        'mbc_play_again': "\nMöchtest du noch einmal spielen? (Drücke Enter, um neu zu starten)",
        'mbc_trophy_room_title': "=== TROPHÄENKAMMER ===",
        'mbc_trophies_won_count': "Turniersiege: {}",
        'mbc_trophy_legend_title': "--- Legenden-Trophäe ---",
        'mbc_trophy_legend_desc': "Du hast 10 Turniere gewonnen! Du bist eine Kampflegende!",
        'mbc_trophy_veteran_title': "--- Veteranen-Trophäe ---",
        'mbc_trophy_veteran_desc': "Du hast 5 Turniere gewonnen! Ein wahrer Veteran.",
        'mbc_trophy_champion_title': "--- Champion-Trophäe ---",
        'mbc_trophy_champion_desc': "Du hast den Endboss besiegt und ein Turnier gewonnen!",
        'mbc_no_trophies': "Du hast noch keine Trophäen. Gewinne das Turnier, um deine erste zu bekommen!",
        'mbc_return_to_menu': "Drücke Enter, um zum Hauptmenü zurückzukehren...",
        'mbc_exit_game': "Spiel wird beendet...",
        'mbc_health': "LEBEN:",
        'mbc_energy': "ENERGIE:",
        'mbc_vs': "GEGEN",
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
            current_language = data.get("current_language", 'en')
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
    print(translations[current_language]['tvh_welcome'])
    print(translations[current_language]['tvh_intro'])
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
        print(f"--- {translations[current_language]['tvh_welcome'].replace('---', '')} ---")
        
        while True:
            respuesta_marca = input(translations[current_language]['tvh_prompt_brand_interest']).lower()
            if respuesta_marca in [translations['es']['tvh_prompt_brand_interest'].split('(')[1].strip().split('/')[0], translations['es']['tvh_prompt_brand_interest'].split('(')[1].strip().split('/')[0].replace('í','i')]:
                marca_preferida = input(translations[current_language]['tvh_prompt_preferred_brand']).capitalize()
                break
            elif respuesta_marca in [translations['es']['tvh_prompt_brand_interest'].split('(')[1].strip().split('/')[1].replace(')','')]:
                marca_preferida = None
                break
            else:
                print(translations[current_language]['tvh_invalid_response'])

        while True:
            try:
                tamano_deseado = int(input(translations[current_language]['tvh_prompt_size']))
                break
            except ValueError:
                print(translations[current_language]['tvh_invalid_number'])

        resoluciones_disponibles = ["720p", "1080p", "4K", "8K"]
        while True:
            resolucion_deseada = input(translations[current_language]['tvh_prompt_resolution']).upper()
            if resolucion_deseada.lower() in [r.lower() for r in resoluciones_disponibles]:
                resolucion_deseada = resolucion_deseada.lower().replace("p", "P")
                break
            else:
                print(translations[current_language]['tvh_invalid_resolution'])

        while True:
            try:
                presupuesto_maximo = float(input(translations[current_language]['tvh_prompt_budget']))
                if presupuesto_maximo <= 0:
                    print(translations[current_language]['tvh_positive_value_required'])
                    continue
                break
            except ValueError:
                print(translations[current_language]['tvh_invalid_number'])
        
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
            print(translations[current_language]['tvh_no_results_all_criteria'])
            opciones_filtradas = []
            for tv in db_televisores:
                if tv.precio > presupuesto_maximo:
                    continue
                if tv.resolucion.upper() != resolucion_deseada.upper():
                    continue
                opciones_filtradas.append(tv)

        if not opciones_filtradas:
            print(translations[current_language]['tvh_no_results_res_budget'])
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
        print(f"          {translations[current_language]['tvh_recommendation_title']}")
        print("="*50)
        
        if not opciones_filtradas:
            print(translations[current_language]['tvh_no_results_found'])
        else:
            print(translations[current_language]['tvh_recommendation_intro'])
            for i, (score, tv) in enumerate(opciones_filtradas[:3]):
                print(f"\n{i+1}. {tv.marca} {tv.modelo}:")
                print(translations[current_language]['tvh_size'].format(tv.tamano))
                print(translations[current_language]['tvh_resolution'].format(tv.resolucion))
                print(translations[current_language]['tvh_refresh_rate'].format(tv.frecuencia))
                print(translations[current_language]['tvh_processor'].format(tv.procesador))
                print(translations[current_language]['tvh_price'].format(tv.precio))

    # --- Ejecución del programa ---
    marca_preferida, tamano_deseado, resolucion_deseada, presupuesto_maximo = obtener_datos_usuario()
    
    mejores_opciones = encontrar_mejor_tv(DB_TELEVISORES_REALES, marca_preferida, tamano_deseado, resolucion_deseada, presupuesto_maximo)
    mostrar_recomendacion(mejores_opciones)
    
    input(translations[current_language]['tvh_return_to_main'])

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
    
    # Mapeo de traducciones para las partes del monstruo
    part_translations = {
        'es': {
            'head_cyclops_name': "Cabeza de Cíclope", 'head_cyclops_desc': "Un solo ojo y un cuerno en espiral.",
            'head_dragon_name': "Cabeza de Dragón", 'head_dragon_desc': "Dientes afilados y un aliento ardiente.",
            'head_alien_name': "Cabeza de Alien", 'head_alien_desc': "Grandes ojos negros y una forma alargada.",
            'head_demon_name': "Cabeza de Demonio", 'head_demon_desc': "Cuernos retorcidos y una mirada malvada.",
            'body_golem_name': "Cuerpo de Golem", 'body_golem_desc': "Fuerte y robusto, hecho de piedra.",
            'body_slime_name': "Cuerpo de Slime", 'body_slime_desc': "Viscoso y gelatinoso, capaz de cambiar de forma.",
            'body_spider_name': "Cuerpo de Araña", 'body_spider_desc': "Ocho patas peludas y un cuerpo redondo.",
            'body_mummy_name': "Cuerpo de Momia", 'body_mummy_desc': "Vendado y frágil, pero con gran resistencia.",
            'arms_robot_name': "Brazos de Robot", 'arms_robot_desc': "Fuertes pero lentos, hechos de metal.",
            'arms_monkey_name': "Brazos de Mono", 'arms_monkey_desc': "Ágiles pero débiles, con pulgares oponibles.",
            'arms_dragon_name': "Brazos de Dragón", 'arms_dragon_desc': "Lentos, pero fuertes, con garras afiladas.",
            'arms_tentacle_name': "Brazos de Tentáculos", 'arms_tentacle_desc': "Flexibles y largos, para agarrar objetos.",
            'legs_human_name': "Piernas Humanoides", 'legs_human_desc': "Equilibradas y versátiles.",
            'legs_centaur_name': "Piernas de Centauro", 'legs_centaur_desc': "Fuertes y rápidas, con pezuñas.",
            'legs_lizard_name': "Piernas de Lagarto", 'legs_lizard_desc': "Capaces de escalar superficies verticales.",
            'legs_spider_name': "Piernas de Araña", 'legs_spider_desc': "Múltiples patas para una movilidad superior.",
        },
        'en': {
            'head_cyclops_name': "Cyclops Head", 'head_cyclops_desc': "A single eye and a spiral horn.",
            'head_dragon_name': "Dragon Head", 'head_dragon_desc': "Sharp teeth and fiery breath.",
            'head_alien_name': "Alien Head", 'head_alien_desc': "Large black eyes and an elongated shape.",
            'head_demon_name': "Demon Head", 'head_demon_desc': "Twisted horns and an evil glare.",
            'body_golem_name': "Golem Body", 'body_golem_desc': "Strong and sturdy, made of stone.",
            'body_slime_name': "Slime Body", 'body_slime_desc': "Viscous and gelatinous, able to change shape.",
            'body_spider_name': "Spider Body", 'body_spider_desc': "Eight furry legs and a round body.",
            'body_mummy_name': "Mummy Body", 'body_mummy_desc': "Bandaged and frail, but with great resistance.",
            'arms_robot_name': "Robot Arms", 'arms_robot_desc': "Strong but slow, made of metal.",
            'arms_monkey_name': "Monkey Arms", 'arms_monkey_desc': "Agile but weak, with opposable thumbs.",
            'arms_dragon_name': "Dragon Arms", 'arms_dragon_desc': "Slow but strong, with sharp claws.",
            'arms_tentacle_name': "Tentacle Arms", 'arms_tentacle_desc': "Flexible and long, for grabbing objects.",
            'legs_human_name': "Humanoid Legs", 'legs_human_desc': "Balanced and versatile.",
            'legs_centaur_name': "Centaur Legs", 'legs_centaur_desc': "Strong and fast, with hooves.",
            'legs_lizard_name': "Lizard Legs", 'legs_lizard_desc': "Able to climb vertical surfaces.",
            'legs_spider_name': "Spider Legs", 'legs_spider_desc': "Multiple legs for superior mobility.",
        },
        'de': {
            'head_cyclops_name': "Zyklopenkopf", 'head_cyclops_desc': "Ein einziges Auge und ein spiralförmiges Horn.",
            'head_dragon_name': "Drachenkopf", 'head_dragon_desc': "Scharfe Zähne und feuriger Atem.",
            'head_alien_name': "Alien-Kopf", 'head_alien_desc': "Große schwarze Augen und eine längliche Form.",
            'head_demon_name': "Dämonenkopf", 'head_demon_desc': "Gedrehte Hörner und ein böser Blick.",
            'body_golem_name': "Golem-Körper", 'body_golem_desc': "Stark und robust, aus Stein gemacht.",
            'body_slime_name': "Schleim-Körper", 'body_slime_desc': "Schleimig und gallertartig, kann die Form ändern.",
            'body_spider_name': "Spinnen-Körper", 'body_spider_desc': "Acht haarige Beine und ein runder Körper.",
            'body_mummy_name': "Mumien-Körper", 'body_mummy_desc': "Verbandelt und zerbrechlich, aber mit großer Widerstandsfähigkeit.",
            'arms_robot_name': "Roboter-Arme", 'arms_robot_desc': "Stark, aber langsam, aus Metall.",
            'arms_monkey_name': "Affen-Arme", 'arms_monkey_desc': "Agil, aber schwach, mit Daumen.",
            'arms_dragon_name': "Drachen-Arme", 'arms_dragon_desc': "Langsam, aber stark, mit scharfen Krallen.",
            'arms_tentacle_name': "Tentakel-Arme", 'arms_tentacle_desc': "Flexibel und lang, um Objekte zu greifen.",
            'legs_human_name': "Humanoide Beine", 'legs_human_desc': "Ausbalanciert und vielseitig.",
            'legs_centaur_name': "Zentauren-Beine", 'legs_centaur_desc': "Stark und schnell, mit Hufen.",
            'legs_lizard_name': "Eidechsen-Beine", 'legs_lizard_desc': "Können vertikale Oberflächen erklimmen.",
            'legs_spider_name': "Spinnen-Beine", 'legs_spider_desc': "Mehrere Beine für überlegene Mobilität.",
        }
    }

    # Asigna las traducciones a las listas de partes
    opciones_cabeza = [
        (part_translations[current_language]['head_cyclops_name'], part_translations[current_language]['head_cyclops_desc'], "  _.-.\n  /  _ \\\n |  (o)  |\n  \\  _  /\n   `---'"),
        (part_translations[current_language]['head_dragon_name'], part_translations[current_language]['head_dragon_desc'], "  /vvvvv\\\n ( O   O )\n  \\  ^  /\n   \\___/"),
        (part_translations[current_language]['head_alien_name'], part_translations[current_language]['head_alien_desc'], "  /\\_/\\\n | `~` |\n  \\___/"),
        (part_translations[current_language]['head_demon_name'], part_translations[current_language]['head_demon_desc'], " .-'--'-.\n/        \\\n|  O    O  |\n \\    --   /\n  `--__--'")
    ]
    
    opciones_cuerpo = [
        (part_translations[current_language]['body_golem_name'], part_translations[current_language]['body_golem_desc'], "  [O.O]\n  /   \\\n /_____\\"),
        (part_translations[current_language]['body_slime_name'], part_translations[current_language]['body_slime_desc'], "  ~~~~~\n /     \\\n|_______|"),
        (part_translations[current_language]['body_spider_name'], part_translations[current_language]['body_spider_desc'], "  /\\__/\\\n /      \\\n |______|"),
        (part_translations[current_language]['body_mummy_name'], part_translations[current_language]['body_mummy_desc'], " |---o---|\n |-------|\n  \\-----/")
    ]
        
    opciones_brazos = [
        (part_translations[current_language]['arms_robot_name'], part_translations[current_language]['arms_robot_desc'], "  _|_|_\n (_____)"),
        (part_translations[current_language]['arms_monkey_name'], part_translations[current_language]['arms_monkey_desc'], "  /\\ /\\\n ( (o) )\n  \\   /"),
        (part_translations[current_language]['arms_dragon_name'], part_translations[current_language]['arms_dragon_desc'], "  || ||\n  \\ //\n   V V"),
        (part_translations[current_language]['arms_tentacle_name'], part_translations[current_language]['arms_tentacle_desc'], " ()()()()\n (      )\n  \\____/")
    ]

    opciones_piernas = [
        (part_translations[current_language]['legs_human_name'], part_translations[current_language]['legs_human_desc'], "  |_|  |_|\n  | |  | |"),
        (part_translations[current_language]['legs_centaur_name'], part_translations[current_language]['legs_centaur_desc'], "  | |  | |\n (  ) (  )"),
        (part_translations[current_language]['legs_lizard_name'], part_translations[current_language]['legs_lizard_desc'], "  /  \\  /  \\\n (____)(____)"),
        (part_translations[current_language]['legs_spider_name'], part_translations[current_language]['legs_spider_desc'], "  / \\ / \\\n /   \   \\\n  -   -")
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
    
    rival_translations = {
        'es': {
            'rivals': ["Goro el Implacable", "Sombra de la Furia", "Gólem Dorado", "Lama Tóxica", "El Guerrero Oxidado", "Besta de las Profundidades", "El Acechador Sombrío", "El Vigilante de la Cripta"],
            'bosses': ["El Devorador de Mundos", "El Dragón Espectral", "El Titán Ancestral", "La Reina Silente", "El Amo de las Sombras"],
        },
        'en': {
            'rivals': ["Goro the Relentless", "Shadow of Fury", "Golden Golem", "Toxic Slime", "The Rusted Warrior", "Beast of the Depths", "The Shrouded Stalker", "The Crypt Watcher"],
            'bosses': ["The World Eater", "The Spectral Dragon", "The Ancestral Titan", "The Silent Queen", "The Master of Shadows"],
        },
        'de': {
            'rivals': ["Goro der Unerbittliche", "Schatten der Wut", "Goldener Golem", "Toxischer Schleim", "Der Rostige Krieger", "Bestie der Tiefen", "Der Verhüllte Stalker", "Der Krypta-Wächter"],
            'bosses': ["Der Weltenfresser", "Der Spektraldrache", "Der Urtitan", "Die Stille Königin", "Der Meister der Schatten"],
        }
    }
    nombres_rivales = rival_translations[current_language]['rivals']
    nombres_jefes = rival_translations[current_language]['bosses']

    # --- Funciones de Juego ---
    def limpiar_pantalla():
        """Limpia la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_encabezado():
        """Muestra el título del programa."""
        limpiar_pantalla()
        print(Fore.CYAN + Style.BRIGHT + "=" * 60)
        print("== " + translations[current_language]['mbc_title_1'].center(54) + " ==")
        print("=" * 60)
        print(Style.RESET_ALL)
        print(Fore.WHITE + translations[current_language]['mbc_intro_1'] + Style.RESET_ALL)
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
            
            eleccion = input(f"\n{translations[current_language]['mbc_choice_prompt']} (1, 2, 3 {translations[current_language]['invalid_option_song']} 4): ")
            
            try:
                indice = int(eleccion) - 1
                if 0 <= indice < len(opciones):
                    return opciones[indice]
                else:
                    print(Fore.RED + translations[current_language]['invalid_option'] + Style.RESET_ALL)
                    time.sleep(2)
            except ValueError:
                print(Fore.RED + translations[current_language]['invalid_option'] + Style.RESET_ALL)
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
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{translations[current_language]['mbc_health']}{Style.RESET_ALL} {Fore.GREEN}{barra_vida_jugador}{Fore.WHITE:<10}{Fore.RED}{Style.BRIGHT}{translations[current_language]['mbc_vs']}{Style.RESET_ALL}{Fore.WHITE:>10}{Fore.RED}{barra_vida_oponente}{Fore.RED} {translations[current_language]['mbc_health']}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{translations[current_language]['mbc_energy']}{Style.RESET_ALL} {Fore.BLUE}{barra_energia}{Style.RESET_ALL}")
        
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
            print(f"\n{translations[current_language]['mbc_prompt_defense'].format(Fore.YELLOW + key1 + Style.RESET_ALL, Fore.YELLOW + key2 + Style.RESET_ALL, tiempo_espera)}")
        else:
            print(f"\n{translations[current_language]['mbc_prompt_attack'].format(Fore.YELLOW + key1 + Style.RESET_ALL, Fore.YELLOW + key2 + Style.RESET_ALL, tiempo_espera)}")

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

        print(Fore.CYAN + translations[current_language]['mbc_battle_start'] + Style.RESET_ALL)
        input(translations[current_language]['mbc_press_to_continue'])
        
        while vida_jugador > 0 and vida_oponente > 0:
            limpiar_pantalla()
            mostrar_barras(vida_jugador, vida_oponente, energia_jugador)
            mostrar_monstruos_en_batalla(jugador, oponente)
            
            # --- Fase de Defensa del Jugador ---
            print(Fore.RED + f"\n--- {translations[current_language]['mbc_phase_defense'].replace('---','')} ---" + Style.RESET_ALL)
            if pedir_combinacion(ronda, tipo_ataque="defensa"):
                print(Fore.GREEN + translations[current_language]['mbc_defense_success'] + Style.RESET_ALL)
                time.sleep(2)
            else:
                daño_oponente = random.randint(15, 30)
                if es_boss and ronda == 4:
                    print(translations[current_language]['mbc_boss_attack_strong'])
                    daño_oponente = vida_jugador + 10
                vida_jugador -= daño_oponente
                print(Fore.RED + translations[current_language]['mbc_defense_fail'].format(oponente['nombre'], daño_oponente) + Style.RESET_ALL)
                time.sleep(2)
            
            if vida_jugador <= 0:
                break
                
            # --- Fase de Ataque del Jugador ---
            print(Fore.BLUE + f"\n--- {translations[current_language]['mbc_phase_attack'].replace('---','')} ---" + Style.RESET_ALL)
            if pedir_combinacion(ronda, tipo_ataque="ofensiva"):
                daño_jugador = random.randint(20, 40)
                vida_oponente -= daño_jugador
                print(Fore.GREEN + translations[current_language]['mbc_attack_success'].format(oponente['nombre'], daño_jugador) + Style.RESET_ALL)
                time.sleep(2)
            else:
                print(Fore.RED + translations[current_language]['mbc_attack_fail'] + Style.RESET_ALL)
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
        print(Fore.YELLOW + Style.BRIGHT + translations[current_language]['mbc_trophy_room_title'] + Style.RESET_ALL)
        print(Fore.WHITE + translations[current_language]['mbc_trophies_won_count'].format(progreso['victorias']) + "\n" + Style.RESET_ALL)
        
        if "leyenda" in progreso['trofeos']:
            print(Fore.CYAN + translations[current_language]['mbc_trophy_legend_title'] + Style.RESET_ALL)
            print(Fore.CYAN + TROFEO_LEYENDA + Style.RESET_ALL)
            print(Fore.WHITE + translations[current_language]['mbc_trophy_legend_desc'] + "\n" + Style.RESET_ALL)
        
        if "veterano" in progreso['trofeos']:
            print(Fore.GREEN + translations[current_language]['mbc_trophy_veteran_title'] + Style.RESET_ALL)
            print(Fore.GREEN + TROFEO_VETERANO + Style.RESET_ALL)
            print(Fore.WHITE + translations[current_language]['mbc_trophy_veteran_desc'] + "\n" + Style.RESET_ALL)

        if "campeon" in progreso['trofeos']:
            print(Fore.YELLOW + translations[current_language]['mbc_trophy_champion_title'] + Style.RESET_ALL)
            print(Fore.YELLOW + TROFEO_CAMPEON + Style.RESET_ALL)
            print(Fore.WHITE + translations[current_language]['mbc_trophy_champion_desc'] + "\n" + Style.RESET_ALL)
        
        if not progreso['trofeos']:
            print(Fore.WHITE + translations[current_language]['mbc_no_trophies'] + "\n" + Style.RESET_ALL)
        
        input(Fore.BLUE + translations[current_language]['mbc_return_to_menu'] + Style.RESET_ALL)
    
    # Bucle principal del juego Monster Battle Creator
    while True:
        progreso = cargar_progreso()
        
        limpiar_pantalla()
        print(Fore.CYAN + Style.BRIGHT + "=" * 60)
        print("== " + translations[current_language]['mbc_menu_title'].center(54) + " ==")
        print("=" * 60)
        print(Style.RESET_ALL)
        print(Fore.WHITE + translations[current_language]['mbc_option_1'] + Style.RESET_ALL)
        print(Fore.YELLOW + translations[current_language]['mbc_option_2'] + Style.RESET_ALL)
        print(Fore.RED + translations[current_language]['mbc_option_3'] + Style.RESET_ALL)
        
        opcion = input(translations[current_language]['mbc_choice_prompt'])
        
        if opcion == '1':
            mostrar_encabezado()
            time.sleep(1)
            
            print(Fore.GREEN + f"\n--- {translations[current_language]['mbc_intro_2'].replace('---','')} ---" + Style.RESET_ALL)
            _, descripcion_cabeza, arte_cabeza = seleccionar_parte(translations[current_language]['mbc_select_head'], opciones_cabeza)
            _, descripcion_cuerpo, arte_cuerpo = seleccionar_parte(translations[current_language]['mbc_select_body'], opciones_cuerpo)
            _, descripcion_brazos, arte_brazos = seleccionar_parte(translations[current_language]['mbc_select_arms'], opciones_brazos)
            _, descripcion_piernas, arte_piernas = seleccionar_parte(translations[current_language]['mbc_select_legs'], opciones_piernas)
            
            nombre_jugador = input(translations[current_language]['mbc_prompt_name'])

            monstruo_jugador = generar_monstruo_aleatorio(nombre_jugador)
            monstruo_jugador["partes"] = {
                "cabeza": ("Cabeza", descripcion_cabeza, arte_cabeza),
                "cuerpo": ("Cuerpo", descripcion_cuerpo, arte_cuerpo),
                "brazos": ("Brazos", descripcion_brazos, arte_brazos),
                "piernas": ("Piernas", descripcion_piernas, arte_piernas)
            }

            limpiar_pantalla()
            print(Fore.GREEN + Style.BRIGHT + "=" * 50)
            print("== " + translations[current_language]['mbc_created_title'].center(44) + " ==")
            print("=" * 50 + Style.RESET_ALL)
            mostrar_monstruo(monstruo_jugador)
            print(Fore.WHITE + f"\n--- {translations[current_language]['mbc_char_title'].replace('---','')} ---" + Style.RESET_ALL)
            print(f"{Fore.WHITE}{translations[current_language]['mbc_head_char'].format(descripcion_cabeza)}")
            print(f"{Fore.WHITE}{translations[current_language]['mbc_body_char'].format(descripcion_cuerpo)}")
            print(f"{Fore.WHITE}{translations[current_language]['mbc_arms_char'].format(descripcion_brazos)}")
            print(f"{Fore.WHITE}{translations[current_language]['mbc_legs_char'].format(descripcion_piernas)}{Style.RESET_ALL}")
            input(Fore.BLUE + translations[current_language]['mbc_press_to_start'] + Style.RESET_ALL)
            
            # --- TUTORIAL DE JUEGO ---
            limpiar_pantalla()
            print(Fore.CYAN + Style.BRIGHT + translations[current_language]['mbc_tutorial_title'] + Style.RESET_ALL)
            print(Fore.WHITE + translations[current_language]['mbc_tutorial_intro'])
            print(translations[current_language]['mbc_tutorial_phases'])
            print(f"\n{Fore.RED}{Style.BRIGHT}{translations[current_language]['mbc_tutorial_defense']}{Style.RESET_ALL} {translations[current_language]['mbc_tutorial_defense_desc']}")
            print(f"\n{Fore.BLUE}{Style.BRIGHT}{translations[current_language]['mbc_tutorial_attack']}{Style.RESET_ALL} {translations[current_language]['mbc_tutorial_attack_desc']}")
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}{translations[current_language]['mbc_tutorial_important']}{Style.RESET_ALL} {translations[current_language]['mbc_tutorial_important_desc']}")
            input(Fore.BLUE + translations[current_language]['mbc_tutorial_continue'] + Style.RESET_ALL)

            # --- FASE 2: EL TORNEO ---
            rivales_torneo = random.sample(nombres_rivales, 3)
            nombre_jefe_final = random.choice(nombres_jefes)
            rivales_torneo.append(nombre_jefe_final)
            
            torneo_ganado = False
            
            for i, nombre_rival in enumerate(rivales_torneo):
                es_boss = (nombre_rival == nombre_jefe_final)
                limpiar_pantalla()
                if es_boss:
                    print(Fore.RED + f"--- {translations[current_language]['mbc_win_final_boss'].replace('!!!','').replace('YOU HAVE DEFEATED THE FINAL BOSS AND WON THE TOURNAMENT','FINAL BOSS').upper().replace('DEFEATED THE FINAL BOSS AND WON THE TOURNAMENT','').replace('HAVE','').replace('AND','').replace('WON','').replace('THE','').replace('FINAL','').replace('BOSS','') } ---" + Style.RESET_ALL)
                    oponente = generar_monstruo_aleatorio(nombre_rival, es_boss=True)
                else:
                    print(Fore.YELLOW + f"--- {translations[current_language]['invalid_upgrade_id'].replace('invalid upgrade id',f'BATTLE {i+1} OF {len(rivales_torneo)}') } ---" + Style.RESET_ALL)
                    oponente = generar_monstruo_aleatorio(nombre_rival)

                print(f"\n{translations[current_language]['mbc_intro_1'].replace('Create your monster for the tournament!','Your monster {} faces {}!').format(monstruo_jugador['nombre'], oponente['nombre'])}")
                input(translations[current_language]['press_enter_to_continue'])

                ganador = simular_batalla_street_fighter(monstruo_jugador, oponente, es_boss, i+1)

                if ganador['nombre'] == monstruo_jugador['nombre']:
                    print(Fore.GREEN + translations[current_language]['mbc_win_battle'].format(oponente['nombre']) + Style.RESET_ALL)
                    if es_boss:
                        print(Fore.YELLOW + Style.BRIGHT + translations[current_language]['mbc_win_final_boss'] + Style.RESET_ALL)
                        torneo_ganado = True
                        break
                    input(translations[current_language]['press_enter_to_continue'])
                else:
                    print(Fore.RED + translations[current_language]['mbc_lose_battle'].format(oponente['nombre']) + Style.RESET_ALL)
                    break

            # Actualizar el progreso al final del torneo
            if torneo_ganado:
                progreso['victorias'] += 1
                if "campeon" not in progreso['trofeos']:
                    progreso['trofeos'].append('campeon')
                if progreso['victorias'] >= 5 and "veterano" not in progreso['trofeos']:
                    progreso['trofeos'].append('veterano')
                    print(Fore.GREEN + translations[current_language]['mbc_win_trophy_veteran'] + Style.RESET_ALL)
                if progreso['victorias'] >= 10 and "leyenda" not in progreso['trofeos']:
                    progreso['trofeos'].append('leyenda')
                    print(Fore.CYAN + translations[current_language]['mbc_win_trophy_legend'] + Style.RESET_ALL)
            
            guardar_progreso(progreso)

            # Comprobar el resultado final del juego
            if monstruo_jugador['vida'] > 0:
                limpiar_pantalla()
                print(Fore.YELLOW + Style.BRIGHT + "=" * 50)
                print("== " + translations[current_language]['mbc_final_victory'].center(44) + " ==")
                print("=" * 50 + Style.RESET_ALL)
                mostrar_monstruo(monstruo_jugador)
                print(Fore.GREEN + translations[current_language]['mbc_final_victory_desc'] + Style.RESET_ALL)
            
            print(translations[current_language]['mbc_play_again'])
            input()
            
        elif opcion == '2':
            mostrar_sala_trofeos(progreso)
            
        elif opcion == '3':
            print(translations[current_language]['mbc_exit_game'])
            break
            
        else:
            print(Fore.RED + translations[current_language]['mbc_invalid_menu_option'] + Style.RESET_ALL)
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
