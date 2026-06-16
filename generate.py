import uuid

# КОНФИГ: Сюда можно добавить любые DNS-over-HTTPS сервера, которые не заблочены
# Мы будем использовать проверенные бесплатные движки, но с фильтрацией
DNS_SERVER_URL = "https://dns.adguard-dns.com/dns-query" 

def create_profile(name, domain):
    profile_uuid = str(uuid.uuid4())
    config_uuid = str(uuid.uuid4())
    
    template = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>DNSSettings</key>
            <dict>
                <key>DNSProtocol</key>
                <string>HTTPS</string>
                <key>ServerURL</key>
                <string>{DNS_SERVER_URL}</string>
            </dict>
            <key>PayloadDescription</key>
            <string>ZeroAds System Shield</string>
            <key>PayloadDisplayName</key>
            <string>{name}</string>
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
    <string>{name}</string>
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
    return template

with open("shield.mobileconfig", "w") as f:
    f.write(create_profile("ZeroAds_Shield", "github.com"))