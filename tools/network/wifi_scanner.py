#!/usr/bin/env python3
"""
REVERS OS v3.0 — WiFi Scanner
Сканирование точек доступа (без root)
"""

import os
import subprocess
import re
from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

def run_wifi_scanner(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         📶 WiFi SCANNER{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    networks = []
    
    # Android (Termux)
    if os.path.exists("/data/data/com.termux"):
        try:
            result = subprocess.run(["termux-wifi-scaninfo"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout:
                print(f"{C_INFO}Сети поблизости:{C_RESET}\n")
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    if "SSID" in line or "BSSID" in line or "rssi" in line:
                        print(f"  {line}")
                return
        except:
            pass
        
        # Fallback: dumpsys
        try:
            result = subprocess.run(["dumpsys", "wifi"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                ssids = re.findall(r'SSID: (.+)', result.stdout)
                bssids = re.findall(r'BSSID: ([0-9a-f:]+)', result.stdout, re.IGNORECASE)
                signals = re.findall(r'signal: (-\d+)', result.stdout)
                
                if ssids:
                    print(f"{C_INFO}Сети поблизости:{C_RESET}\n")
                    for i, ssid in enumerate(ssids[:20]):
                        bssid = bssids[i] if i < len(bssids) else "N/A"
                        signal = signals[i] if i < len(signals) else "N/A"
                        print(f"  {C_BRIGHT}{ssid}{C_RESET}")
                        print(f"  ├─ BSSID: {bssid}")
                        print(f"  └─ Сигнал: {signal} dBm\n")
                    return
        except:
            pass
    
    # Linux
    try:
        result = subprocess.run(["nmcli", "-t", "-f", "SSID,BSSID,SIGNAL,SECURITY", "dev", "wifi", "list"],
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout:
            print(f"{C_INFO}Сети поблизости:{C_RESET}\n")
            for line in result.stdout.strip().split("\n")[:20]:
                parts = line.split(":")
                if len(parts) >= 3:
                    print(f"  {C_BRIGHT}{parts[0]}{C_RESET}")
                    print(f"  ├─ BSSID: {parts[1]}")
                    print(f"  ├─ Сигнал: {parts[2]}%")
                    print(f"  └─ Защита: {parts[3] if len(parts) > 3 else 'N/A'}\n")
            return
    except:
        pass
    
    # Windows
    try:
        result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=Bssid"],
                               capture_output=True, text=True, timeout=10, shell=True)
        if result.returncode == 0:
            ssids = re.findall(r'SSID \d+ : (.+)', result.stdout)
            bssids = re.findall(r'BSSID \d+ : ([0-9a-f:]+)', result.stdout, re.IGNORECASE)
            signals = re.findall(r'Signal : (\d+)%', result.stdout)
            
            if ssids:
                print(f"{C_INFO}Сети поблизости:{C_RESET}\n")
                for i, ssid in enumerate(ssids[:20]):
                    bssid = bssids[i] if i < len(bssids) else "N/A"
                    signal = signals[i] if i < len(signals) else "N/A"
                    print(f"  {C_BRIGHT}{ssid}{C_RESET}")
                    print(f"  ├─ BSSID: {bssid}")
                    print(f"  └─ Сигнал: {signal}%\n")
                return
    except:
        pass
    
    print(f"{C_ERROR}[!] Не удалось просканировать WiFi. Установите nmcli или termux-api.{C_RESET}")
