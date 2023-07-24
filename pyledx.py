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
print('Use the following flags for static color:')
print('--red | --green | --blue | --yellow | --cyan | --purple | --white | --off ')
print("")
print('Use -c flag to clear colors on exit while testing')
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

def redAnimation(strip):
    colorWipe(strip, Color(255, 0, 0))

def greenAnimation(strip):
    colorWipe(strip, Color(0, 255, 0))

def blueAnimation(strip):
    colorWipe(strip, Color(0, 0, 255))

def yellowAnimation(strip):
    colorWipe(strip, Color(255, 255, 0))

def cyanAnimation(strip):
    colorWipe(strip, Color(0, 255, 255))

def purpleAnimation(strip):
    colorWipe(strip, Color(128, 0, 128))

def whiteAnimation(strip):
    colorWipe(strip, Color(255, 255, 255))

def offAnimation(strip):
    colorWipe(strip, Color(0, 0, 0))

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
    parser.add_argument('--off', action='store_true', help='turn off LEDs')
    args = parser.parse_args()

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    try:
        while True:
            if args.red:
                redAnimation(strip)
            elif args.green:
                greenAnimation(strip)
            elif args.blue:
                blueAnimation(strip)
            elif args.yellow:
                yellowAnimation(strip)
            elif args.cyan:
                cyanAnimation(strip)
            elif args.purple:
                purpleAnimation(strip)
            elif args.white:
                whiteAnimation(strip)
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
