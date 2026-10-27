# PICO-TP5110-RTC-low-power-for-LEGO
Using a TP5110 with a PI PICO and a DS3231 RTC to power LEGO USB lights for a set time period

The idea is that I want to be able to power USB powered LED sets for LEGO. I have a number of light sets but they do not get used as they need to connect to a mains powered USB power brick due to the current draw.

However, I only want them on for about 1 hr a night so see a circuit that can be battery powered that normally only takes about 20uA and then turns the LEDs on at the set time and off at a set time.

A TP5110 board can be set to turn on a PICO (the period is determined by an onboard potentiometer) and USB connector and the PICO can then turn off the TP5110 with by applying a pulse to the DONE PIN. The TP5110 has VCC, GND, DRV (the pin that goes high after the specified period), DELAY (not used if you want to use the onboard pot) and DONE (tells the TP5110 to turn off and start the timer).

I found that when the TP5110 was connected to the PICO I was damaging it when programming the PICO. A diode 1N5817 / 1N5819 / SS14 connected between the DRV pin and the VBUS or VSYS on the PICO stops the back feeding of the 5V to the TP5110. Also putting a 4.7 kΩ between the GPIO and DONE pin prevents too high a current flowing.

This works with the TP5110 drawing only a few nA (not measurable) and the PICO and LED at about 200 mA. As is every time the TP5110 activates the LED lights up for about 1s and turns off. This wastes power and does not look good. If I put a NPN transistor in the path of the LED to GND I can stop this. I used a BC337 with 100k pulldown resistor and a 10k resistor to GPIO 11.

<img width="1023" height="559" alt="image" src="https://github.com/user-attachments/assets/65638415-d02d-443e-9c56-bab5a3dce306" />

I have had issues with this locking up. After a couple of days after removing the power it works again. It might be that the charging circuit on the RTC is trying to charge the CR2032 battery. I have removed the 201 resistor on the RTC (see red box)
<img width="283" height="165" alt="image" src="https://github.com/user-attachments/assets/9db46d00-58e1-4b6c-8988-7e9ab6c5487f" />

The battery setup uses a 4x 18650 battery holder connected to a TP4056 charging breakout board. The output of this is connected to a USB A female breakout board. To be able to assess the battery charge I have connected a LED battery charge indicator circuit to a tactile switch. Pressing the switch will show the battery charge status.
<img width="877" height="682" alt="image" src="https://github.com/user-attachments/assets/5a9742ea-d24b-45e8-a22e-38cec05614cf" />
