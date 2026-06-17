import uuid
import requests
from datetime import datetime

# === НАСТРОЙКИ ===
DNS_SERVERS = [
    "https://dns.adguard-dns.com/dns-query",      # Основной
    "https://dns.nextdns.io",                     # Запасной (можно потом свой ID вставить)
]

# Списки для скачивания (hosts-формат)
BLOCKLISTS = [
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "https://big.oisd.nl",
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/filter.txt",
]

CUSTOM_BLOCKED = [
    
    
]

def download_hosts(url):
    try:
        r = requests.get(url, timeout=30)
        domains = set()
        for line in r.text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 2:
                    domain = parts[1].lower()
                    if domain and "." in domain:
                        domains.add(domain)
        return domains
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")
        return set()

def create_profile():
    all_domains = set(CUSTOM_BLOCKED)
    
    print("Скачиваем списки блокировки...")
    for url in BLOCKLISTS:
        print(f"  → {url}")
        all_domains.update(download_hosts(url))
    
    print(f"Всего доменов для блокировки: {len(all_domains)}")

    profile_uuid = str(uuid.uuid4())
    config_uuid = str(uuid.uuid4())

    # Создаём XML профиль
    dns_settings = ""
    for i, server in enumerate(DNS_SERVERS):
        dns_settings += f"""
            <key>DNSProtocol</key>
            <string>HTTPS</string>
            <key>ServerURL</key>
            <string>{server}</string>
        """

    template = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>DNSSettings</key>
            <dict>
                {dns_settings}
            </dict>
            <key>PayloadDescription</key>
            <string>ZeroAds Shield - Enhanced</string>
            <key>PayloadDisplayName</key>
            <string>ZeroAds Enhanced</string>
            <key>PayloadIdentifier</key>
            <string>com.vercachev.dns.{profile_uuid}</string>
            <key>PayloadType</key>
            <string>com.apple.dnsSettings.managed</string>
            <key>PayloadUUID</key>
            <string>{config_uuid}</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
        </dict>
    </array>
    <key>PayloadDisplayName</key>
    <string>ZeroAds Enhanced Shield</string>
    <key>PayloadIdentifier</key>
    <string>com.vercachev.dns</string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>{profile_uuid}</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>'''

    with open("shield.mobileconfig", "w", encoding="utf-8") as f:
        f.write(template)
    
    print("Файл shield.mobileconfig обновлён!")

if __name__ == "__main__":
    create_profile()