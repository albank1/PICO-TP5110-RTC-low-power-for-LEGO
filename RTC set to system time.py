import RTC_DS3231
import time

def dec_to_bcd(val):
    """Convert decimal to BCD"""
    return (val // 10 << 4) + (val % 10)

# Initialise RTC
rtc = RTC_DS3231.RTC()

# Get system time from PC (via Thonny etc.)
t = time.localtime()
# time.localtime() → (year, month, day, hour, minute, second, weekday, yearday)

sec = dec_to_bcd(t[5])
minute = dec_to_bcd(t[4])
hour = dec_to_bcd(t[3])
weekday = dec_to_bcd((t[6] + 1) % 7 or 7)  # Convert Python weekday (0–6) to DS3231 (1–7)

day = dec_to_bcd(t[2])
month = dec_to_bcd(t[1])
year = dec_to_bcd(t[0] - 2000)  # Store only last two digits

# Create the 7-byte sequence
data = bytes([sec, minute, hour, 1, day, month, year])

print("Setting DS3231 RTC to:", t)
print("Encoded data:", data)

# Set RTC to current system time
rtc.DS3231_SetTime(data)

# Confirm it’s working
while True:
    print(rtc.DS3231_ReadTime(1))
    time.sleep(1)
