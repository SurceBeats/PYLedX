#!/usr/bin/env python3
# ABSMiniTowerKit Custom Color Python Example
# Author: Surce (surcebeats.com)
# Based on the work from: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example. Showcases
# various animations on a strip of NeoPixels.

# Import necessary modules
import time
from rpi_ws281x import PixelStrip, Color
import argparse

# NeoPixel LED strip configuration
LED_COUNT = 4              # Number of LEDs in the strip
LED_PIN = 18                # GPIO pin to which the LED strip is connected
LED_FREQ_HZ = 800000        # Data transmission frequency for the LED strip
LED_DMA = 10                # DMA channel to be used for generating signal (Direct Memory Access)
LED_BRIGHTNESS = 255        # Set the brightness of the LEDs (0 to 255)
LED_INVERT = False          # Invert signal if needed (True or False)
LED_CHANNEL = 0             # PWM channel for generating signal (0 to 1)

# Print usage information and available color options for the LEDs
print("")  # Print an empty line for formatting
print('Use -c flag to clear colors on exit while testing to avoid freezes')
print("")
print('Use the following flags for static color:')
print('--red --green --blue --yellow --cyan --limegreen --gray --purple')
print('--orange --pink --white --off ')
print("")
print('Use --pulsate flag for pulsating LEDs (works combined ie: --purple --pulsate)')
print('When using --pulsate, use --pulsatevelocity 4 to modify pulsate velocity')
print("")
print('Use the command without color flags to roll between all available colors')
print("")
print('Examples:')
print('sudo python3 pyledx.py -c')
print('sudo python3 pyledx.py -c --red')
print('sudo python3 pyledx.py -c --purple --pulsate')
print('sudo python3 pyledx.py -c --white --pulsate --pulsatevelocity 0.1')
print('sudo python3 pyledx.py -c --blue --pulsate --pulsatevelocity 16')
print("")

# Function to set a single color for all LEDs in the strip
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms / 1000.0)

# Function to create a rainbow animation on the strip with 4 LEDs
def rainbow(strip, wait_ms=20, iterations=1):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            # Scale the index for 4 LEDs and the color palette for it to work correctly
            scaled_index = int(i * 256 / 4 / strip.numPixels()) + j
            strip.setPixelColor(i, wheel(scaled_index & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

# Function to create a rainbow cycle animation on the strip with 4 LEDs
def rainbowCycle(strip, wait_ms=20, iterations=5):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            # Scale the index for 4 LEDs and the color palette for it to work correctly
            scaled_index = int(i * 256 / 4 / strip.numPixels()) + j
            strip.setPixelColor(i, wheel(scaled_index & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

# Function to create a fading animation on the strip with a given color
def fadeAnimation(strip, color, duration=None, steps=100):
    """Animate the fading effect for the LEDs.

    Args:
        strip (PixelStrip): The LED strip object.
        color (int): The target color for the animation.
        duration (float, optional): The duration of the animation in seconds. If None, the --pulsatevelocity
                                    command-line argument will be used. Defaults to None.
        steps (int): The number of steps for the fading effect. Larger values create smoother fading.
    """
    if duration is None:
        duration = 2  # Default pulsate velocity in seconds if no --pulsatevelocity argument is provided

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

# Function to generate a color based on a position in the color wheel
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
    # Command-line argument parsing
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
    parser.add_argument('--pulsatevelocity', type=float, default=2, help='pulsate velocity in seconds (default is 2)')
    args = parser.parse_args()

    # Initialize the NeoPixel strip
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    try:
        while True:
            # Check for specific color flags and perform corresponding animations
            if args.red:
                if args.pulsate:
                    fadeAnimation(strip, Color(255, 0, 0), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for red color
                else:
                    colorWipe(strip, Color(255, 0, 0))
            elif args.green:
                if args.pulsate:
                    fadeAnimation(strip, Color(0, 255, 0), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for green color
                else:
                    colorWipe(strip, Color(0, 255, 0))
            elif args.blue:
                if args.pulsate:
                    fadeAnimation(strip, Color(0, 0, 255), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for blue color
                else:
                    colorWipe(strip, Color(0, 0, 255))
            elif args.yellow:
                if args.pulsate:
                    fadeAnimation(strip, Color(255, 255, 0), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for yellow color
                else:
                    colorWipe(strip, Color(255, 255, 0))
            elif args.cyan:
                if args.pulsate:
                    fadeAnimation(strip, Color(0, 255, 255), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for cyan color
                else:
                    colorWipe(strip, Color(0, 255, 255))
            elif args.purple:
                if args.pulsate:
                    fadeAnimation(strip, Color(128, 0, 128), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for purple color
                else:
                    colorWipe(strip, Color(128, 0, 128))
            elif args.white:
                if args.pulsate:
                    fadeAnimation(strip, Color(255, 255, 255), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for white color
                else:
                    colorWipe(strip, Color(255, 255, 255))
            elif args.orange:
                if args.pulsate:
                    fadeAnimation(strip, Color(255, 69, 0), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for orange color
                else:
                    colorWipe(strip, Color(255, 69, 0))
            elif args.pink:
                if args.pulsate:
                    fadeAnimation(strip, Color(255, 0, 120), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for pink color
                else:
                    colorWipe(strip, Color(255, 0, 120))
            elif args.limegreen:
                if args.pulsate:
                    fadeAnimation(strip, Color(150, 255, 0), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for lime green color
                else:
                    colorWipe(strip, Color(150, 255, 0))
            elif args.gray:
                if args.pulsate:
                    fadeAnimation(strip, Color(16, 16, 16), duration=args.pulsatevelocity, steps=100)  # Pulsating effect for gray color
                else:
                    colorWipe(strip, Color(16, 16, 16))
            elif args.off:
                colorWipe(strip, Color(0, 0, 0))
            else:
                # If no specific color flag is provided, run a sequence of default animations
                rainbow(strip, wait_ms=20, iterations=1)
                time.sleep(1)
                rainbowCycle(strip, wait_ms=20, iterations=5)
                time.sleep(1)

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) and clear the LEDs if specified
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
