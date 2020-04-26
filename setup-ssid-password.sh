#!/bin/bash
echo "HoverCamera wifi config: "
#adb wait-for-device shell cat /etc/hostapd.conf | grep ssid
#adb shell cat /etc/hostapd.conf | grep wpa_passphrase
adb shell "cat data/misc/wifi/hostapd.conf | grep ^ssid="
adb shell "cat data/misc/wifi/hostapd.conf | grep wpa_passphrase="
echo ""
echo "HoverCamera wi-fi only take effect at softap mode."
read -p "ssid: " SSID
read -p "password: " PASS

#adb shell "cat data/misc/wifi/hostapd.conf | grep wpa_passphrase=.* | sed -i 's/wpa_passphrase=.*/wpa_passphrase=1234567898/g'"
## ^ssid.*
#adb shell "sed -i 's/wpa_passphrase=.*/wpa_passphrase=1234567898/g' data/misc/wifi/hostapd.conf"
cp -a data/misc/wifi/hostapd.conf ./hostapd.conf

sed -i 's/SSIDTEMP/'$SSID'/g' hostapd.conf
sed -i 's/PASSTEMP/'$PASS'/g' hostapd.conf

adb push ./hostapd.conf data/misc/wifi/hostapd.conf

echo ""
echo "HoverCamera wifi change to: "
adb shell "cat data/misc/wifi/hostapd.conf | grep ^ssid="
adb shell "cat data/misc/wifi/hostapd.conf | grep wpa_passphrase="

#
#rm ./hostapd.conf
#
#adb shell sync
exit 2
