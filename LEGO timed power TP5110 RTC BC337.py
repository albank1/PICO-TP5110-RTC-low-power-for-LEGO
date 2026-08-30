from machine import Pin
from RTC_DS3231 import RTC
import time


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

STARTTIME = 21       # Pico remains powered from this time
STOPTIME = 22       # Pico powers off at this time

RTC_SDA_PIN = 4
RTC_SCL_PIN = 5

LED_PIN = "LED"

TP5110_DONE_PIN = 19
TRANSISTOR_PIN = 11

CHECK_INTERVAL_SECONDS = 10


# ---------------------------------------------------------
# Hardware setup
# ---------------------------------------------------------

# GPIO 4 and GPIO 5 use I2C0 on the Raspberry Pi Pico.
rtc = RTC(
    sda_pin=RTC_SDA_PIN,
    scl_pin=RTC_SCL_PIN,
    port=0
)

done = Pin(TP5110_DONE_PIN, Pin.OUT)
done.value(0)
led = Pin(LED_PIN, Pin.OUT)
led.value(0)

transistor = Pin(TRANSISTOR_PIN, Pin.OUT)
transistor.value(0)

# --------------------------------------------------------
# Functions
# ---------------------------------------------------------

def power_off():
    """
    Pulse the TP5110 DONE pin high.

    The TP5110 should then remove power from the Pico.
    """
    print("Setting TP5110 DONE pin")

    led.value(0)
    done.value(1)
    time.sleep_ms(500)
    done.value(0)

    # The Pico should lose power during the pulse.
    # Stay here if power is not removed immediately.
    while True:
        time.sleep(1)


def read_rtc_time():
    """
    Read and return the RTC hour, minute and second.
    """
    rtc_time = rtc.DS3231_ReadTime(mode=0)

    # The supplied driver returns an error as a string.
    if isinstance(rtc_time, str):
        raise RuntimeError(rtc_time)

    second, minute, hour, weekday, day, month, year = rtc_time

    return int(hour), int(minute), int(second)


def within_operating_period(hour):
    """
    Return True when the current hour is between
    STARTTIME and STOPTIME.

    STARTTIME is inclusive.
    STOPTIME is exclusive.
    """
    return STARTTIME <= hour < STOPTIME


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

try:
    hour, minute, second = read_rtc_time()

    print(
        "RTC time: {:02d}:{:02d}:{:02d}".format(
            hour, minute, second
        )
    )
    led.toggle()
    time.sleep(1)
    led.toggle()
    time.sleep(1)    
    led.toggle()
    time.sleep(1)
    
    if not within_operating_period(hour):
        print(
            "Outside operating period "
            "({:02d}:00 to {:02d}:00)".format(
                STARTTIME, STOPTIME
            )
        )
        power_off()

    print("Within operating period - remaining powered")
    transistor.value(1)
    
    while True:
        hour, minute, second = read_rtc_time()

        print(
            "RTC time: {:02d}:{:02d}:{:02d}".format(
                hour, minute, second
            )
        )
        led.toggle()
        
        if not within_operating_period(hour):
            print("STOPTIME reached")
            power_off()

        time.sleep(CHECK_INTERVAL_SECONDS)

except Exception as error:
    print("RTC error:", error)

    # Do not leave the device permanently powered if the RTC fails.
    while True:
        led.toggle(0)
        time.sleep(1)