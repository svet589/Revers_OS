#!/usr/bin/env python3
"""
REVERS OS v3.0 — Меню пентест-утилит
"""

from core.utils import (
    C_ERROR, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET,
    clear_screen, select_option, confirm_action
)

def tools_menu():
    while True:
        clear_screen()
        print(f"""
{C_WARNING}╔══════════════════════════════════════════════╗
║         🔧 ПЕНТЕСТ-УТИЛИТЫ REVERS              ║
╠══════════════════════════════════════════════╣
║                                                ║
║  {C_INFO}🌐 СЕТЕВАЯ РАЗВЕДКА{C_WARNING}                       ║
║  {C_BRIGHT}1.{C_RESET}  WiFi Scanner                           {C_WARNING}║
║  {C_BRIGHT}2.{C_RESET}  Host Discovery                         {C_WARNING}║
║  {C_BRIGHT}3.{C_RESET}  DNS Lookup                             {C_WARNING}║
║  {C_BRIGHT}4.{C_RESET}  Traceroute                             {C_WARNING}║
║  {C_BRIGHT}5.{C_RESET}  HTTP Headers                           {C_WARNING}║
║  {C_BRIGHT}6.{C_RESET}  Port Scanner                           {C_WARNING}║
║                                                ║
║  {C_INFO}🔍 OSINT{C_WARNING}                                   ║
║  {C_BRIGHT}7.{C_RESET}  KRAKEN (цифровой профиль)              {C_WARNING}║
║  {C_BRIGHT}8.{C_RESET}  Username Search                        {C_WARNING}║
║  {C_BRIGHT}9.{C_RESET}  Email Breach                           {C_WARNING}║
║  {C_BRIGHT}10.{C_RESET} Phone Lookup                           {C_WARNING}║
║  {C_BRIGHT}11.{C_RESET} IP Intelligence                        {C_WARNING}║
║  {C_BRIGHT}12.{C_RESET} Image Metadata                         {C_WARNING}║
║  {C_BRIGHT}13.{C_RESET} Social Media Scraper                   {C_WARNING}║
║                                                ║
║  {C_ERROR}⚡ DOS ТЕСТИРОВАНИЕ{C_WARNING}                       ║
║  {C_BRIGHT}14.{C_RESET} SYN Flood                              {C_WARNING}║
║  {C_BRIGHT}15.{C_RESET} UDP Flood                              {C_WARNING}║
║  {C_BRIGHT}16.{C_RESET} HTTP Flood                             {C_WARNING}║
║  {C_BRIGHT}17.{C_RESET} Slowloris                              {C_WARNING}║
║  {C_BRIGHT}18.{C_RESET} DNS Amplification                      {C_WARNING}║
║                                                ║
║  {C_WARNING}🛠 ПРОЧЕЕ{C_WARNING}                                ║
║  {C_BRIGHT}19.{C_RESET} Payload Generator                       {C_WARNING}║
║  {C_BRIGHT}20.{C_RESET} Hash Cracker                            {C_WARNING}║
║  {C_BRIGHT}21.{C_RESET} CipherForge                             {C_WARNING}║
║                                                ║
║  {C_DIM}0.{C_RESET} Выход                                      {C_WARNING}║
╚══════════════════════════════════════════════╝{C_RESET}
""")
        
        try:
            choice = input(f"{C_INFO}Выберите утилиту (0-21): {C_RESET}").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                from tools.network.wifi_scanner import run_wifi_scanner
                run_wifi_scanner([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "2":
                from tools.network.host_discovery import run_host_discovery
                run_host_discovery([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "3":
                from tools.network.dns_lookup import run_dns_lookup
                run_dns_lookup([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "4":
                from tools.network.traceroute import run_traceroute
                run_traceroute([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "5":
                from tools.network.http_headers import run_http_headers
                run_http_headers([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "6":
                from tools.network.port_scanner import run_port_scanner
                run_port_scanner([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "7":
                from tools.osint.kraken import run_kraken
                run_kraken([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "8":
                from tools.osint.username_search import run_username_search
                run_username_search([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "9":
                from tools.osint.email_breach import run_email_breach
                run_email_breach([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "10":
                from tools.osint.phone_lookup import run_phone_lookup
                run_phone_lookup([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "11":
                from tools.osint.ip_intel import run_ip_intel
                run_ip_intel([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "12":
                from tools.osint.image_meta import run_image_meta
                run_image_meta([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "13":
                from tools.osint.social_scraper import run_social_scraper
                run_social_scraper([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "14":
                if confirm_action("⚠️ SYN Flood — только для своих систем! Продолжить? (y/n): "):
                    from tools.dos.syn_flood import run_syn_flood
                    run_syn_flood([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "15":
                if confirm_action("⚠️ UDP Flood — только для своих систем! Продолжить? (y/n): "):
                    from tools.dos.udp_flood import run_udp_flood
                    run_udp_flood([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "16":
                if confirm_action("⚠️ HTTP Flood — только для своих систем! Продолжить? (y/n): "):
                    from tools.dos.http_flood import run_http_flood
                    run_http_flood([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "17":
                if confirm_action("⚠️ Slowloris — только для своих систем! Продолжить? (y/n): "):
                    from tools.dos.slowloris import run_slowloris
                    run_slowloris([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "18":
                if confirm_action("⚠️ DNS Amplification — только для своих систем! Продолжить? (y/n): "):
                    from tools.dos.dns_amp import run_dns_amp
                    run_dns_amp([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "19":
                from tools.other.payload_gen import run_payload_gen
                run_payload_gen([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "20":
                from tools.other.hash_crack import run_hash_crack
                run_hash_crack([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            elif choice == "21":
                from tools.other.cipher_forge import run_cipher_forge
                run_cipher_forge([])
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
            else:
                print(f"{C_ERROR}[!] Неверный выбор.{C_RESET}")
                input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"{C_ERROR}[!] Ошибка: {e}{C_RESET}")
            input(f"\n{C_DIM}Нажмите Enter для продолжения...{C_RESET}")
