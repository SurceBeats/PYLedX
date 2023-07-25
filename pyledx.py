#!/usr/bin/env python3
# ABSMiniTowerKit Custom Color Python Example
# Author: Surce (surcebeats.com)
# Based on the work from: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
import argparse

LED_COUNT = 16
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

print("")
print('Use -c flag to clear colors on exit while testing to avoid freezes')
print("")
print('Use the following flags for static color:')
print('--red --green --blue --yellow --cyan --limegreen --gray --purple')
print('--orange --pink --white --off ')
print("")
print('Use --pulsate flag for pulsating LEDs (works combined ie: --purple --pulsate)')
print("")
print('Use the command without color flags to roll between all available colors')
print("")

def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms / 1000.0)

def rainbow(strip, wait_ms=20, iterations=1):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def redAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(255, 0, 0), duration=2, steps=100)  # Pulsating effect for red color
    else:
        colorWipe(strip, Color(255, 0, 0))

def greenAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(0, 255, 0), duration=2, steps=100)  # Pulsating effect for green color
    else:
        colorWipe(strip, Color(0, 255, 0))

def blueAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(0, 0, 255), duration=2, steps=100)  # Pulsating effect for blue color
    else:
        colorWipe(strip, Color(0, 0, 255))

def yellowAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(255, 255, 0), duration=2, steps=100)  # Pulsating effect for yellow color
    else:
        colorWipe(strip, Color(255, 255, 0))

def cyanAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(0, 255, 255), duration=2, steps=100)  # Pulsating effect for cyan color
    else:
        colorWipe(strip, Color(0, 255, 255))

def purpleAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(128, 0, 128), duration=2, steps=100)  # Pulsating effect for purple color
    else:
        colorWipe(strip, Color(128, 0, 128))

def whiteAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(255, 255, 255), duration=2, steps=100)  # Pulsating effect for white color
    else:
        colorWipe(strip, Color(255, 255, 255))

def orangeAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(255, 69, 0), duration=2, steps=100)  # Pulsating effect for orange color
    else:
        colorWipe(strip, Color(255, 69, 0))

def pinkAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(255, 0, 120), duration=2, steps=100)  # Pulsating effect for pink color
    else:
        colorWipe(strip, Color(255, 0, 120))

def limeGreenAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(150, 255, 0), duration=2, steps=100)  # Pulsating effect for lime green color
    else:
        colorWipe(strip, Color(150, 255, 0))

def grayAnimation(strip, pulsate=False):
    if pulsate:
        fadeAnimation(strip, Color(16, 16, 16), duration=2, steps=100)  # Pulsating effect for gray color
    else:
        colorWipe(strip, Color(16, 16, 16))

def offAnimation(strip):
    colorWipe(strip, Color(0, 0, 0))

def fadeAnimation(strip, color, duration=2, steps=100):
    """Animate the fading effect for the LEDs."""
    initial_color = [strip.getPixelColor(i) for i in range(strip.numPixels())]
    target_r, target_g, target_b = (color >> 16) & 255, (color >> 8) & 255, color & 255

    for step in range(steps):
        for i in range(strip.numPixels()):
            r_val = int(initial_color[i] >> 16) & 255
            g_val = int(initial_color[i] >> 8) & 255
            b_val = int(initial_color[i]) & 255

            r_val += int((target_r - r_val) * step / steps)
            g_val += int((target_g - g_val) * step / steps)
            b_val += int((target_b - b_val) * step / steps)

            strip.setPixelColor(i, Color(r_val, g_val, b_val))
        strip.show()
        time.sleep(duration / steps)

    for step in range(steps, -1, -1):
        for i in range(strip.numPixels()):
            r_val = int(initial_color[i] >> 16) & 255
            g_val = int(initial_color[i] >> 8) & 255
            b_val = int(initial_color[i]) & 255

            r_val += int((target_r - r_val) * step / steps)
            g_val += int((target_g - g_val) * step / steps)
            b_val += int((target_b - b_val) * step / steps)

            strip.setPixelColor(i, Color(r_val, g_val, b_val))
        strip.show()
        time.sleep(duration / steps)

def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('--red', action='store_true', help='show red animation')
    parser.add_argument('--green', action='store_true', help='show green animation')
    parser.add_argument('--blue', action='store_true', help='show blue animation')
    parser.add_argument('--yellow', action='store_true', help='show yellow animation')
    parser.add_argument('--cyan', action='store_true', help='show cyan animation')
    parser.add_argument('--purple', action='store_true', help='show purple animation')
    parser.add_argument('--white', action='store_true', help='show white animation')
    parser.add_argument('--orange', action='store_true', help='show orange animation')
    parser.add_argument('--pink', action='store_true', help='show pink animation')
    parser.add_argument('--limegreen', action='store_true', help='show lime green animation')
    parser.add_argument('--gray', action='store_true', help='show gray animation')
    parser.add_argument('--off', action='store_true', help='turn off LEDs')
    parser.add_argument('--pulsate', action='store_true', help='pulsate LEDs')
    args = parser.parse_args()

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    try:
        while True:
            if args.red:
                redAnimation(strip, args.pulsate)
            elif args.green:
                greenAnimation(strip, args.pulsate)
            elif args.blue:
                blueAnimation(strip, args.pulsate)
            elif args.yellow:
                yellowAnimation(strip, args.pulsate)
            elif args.cyan:
                cyanAnimation(strip, args.pulsate)
            elif args.purple:
                purpleAnimation(strip, args.pulsate)
            elif args.white:
                whiteAnimation(strip, args.pulsate)
            elif args.orange:
                orangeAnimation(strip, args.pulsate)
            elif args.pink:
                pinkAnimation(strip, args.pulsate)
            elif args.limegreen:
                limeGreenAnimation(strip, args.pulsate)
            elif args.gray:
                grayAnimation(strip, args.pulsate)
            elif args.off:
                offAnimation(strip)
            else:
                rainbow(strip, wait_ms=20, iterations=1)
                time.sleep(1)
                rainbowCycle(strip, wait_ms=20, iterations=5)
                time.sleep(1)
                theaterChaseRainbow(strip, wait_ms=50)
                time.sleep(1)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
