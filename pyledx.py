#!/usr/bin/env python3
# 52Pi ZP-0128 ABSMiniTowerKit Ice Tower LED Fans Custom Color Python Example
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
LED_COUNT = 4               # Number of LEDs in the strip
LED_PIN = 18                # GPIO pin to which the LED strip is connected
LED_FREQ_HZ = 800000        # Data transmission frequency for the LED strip
LED_DMA = 10                # DMA channel to be used for generating signal (Direct Memory Access)
LED_BRIGHTNESS = 255        # Set the brightness of the LEDs (0 to 255)
LED_INVERT = False          # Invert signal if needed (True or False)
LED_CHANNEL = 0             # PWM channel for generating signal (0 to 1)

# Print usage information and available color options for the LEDs
print("")  # Print an empty line for formatting
print("52Pi ZP-0128 ABSMiniTowerKit Ice Tower LED Fans Custom Color Python Example")
print("Author: Surce (surcebeats.com)")
print("Based on the work from: Tony DiCola (tony@tonydicola.com)")
print("")
print("---------------------------------------")
print("")
print('\x1B[4m' + 'Usage:' + '\x1B[0m')
print('Use ' + '\x1B[4m' + '-c' + '\x1B[0m' + ' flag to clear colors on exit while testing to avoid freezes')
print('Use ' + '\x1B[4m' + '--red' + '\x1B[0m \x1B[4m' + '--green\x1B[0m \x1B[4m--blue\x1B[0m \x1B[4m--yellow\x1B[0m \x1B[4m--cyan\x1B[0m \x1B[4m--limegreen\x1B[0m \x1B[4m--gray\x1B[0m \x1B[4m--deepgray\x1B[0m \x1B[4m--purple\x1B[0m \x1B[4m--orange\x1B[0m \x1B[4m--pink\x1B[0m \x1B[4m--white\x1B[0m for static colors')
print('Use ' + '\x1B[4m' + '--pulsate' + '\x1B[0m' + ' flag for pulsating LEDs (works combined ie: --purple --pulsate, use also ' + '\x1B[4m' + '--pvel' + '\x1B[0m' + ' % to modify velocity)')
print('Use ' + '\x1B[4m' + '--rotate' + '\x1B[0m' + ' flag to rotate color through LEDs (works combined ie: --purple --rotate)')
print('Use ' + '\x1B[4m' + '--circle' + '\x1B[0m' + ' flag to make a circle animation between all available colors')
print("")
print('\x1B[4m' + 'Examples:' + '\x1B[0m')
print('sudo python3 pyledx.py -c --red')
print('sudo python3 pyledx.py -c --purple --pulsate')
print('sudo python3 pyledx.py -c --white --pulsate --pvel 0.5 (default is 2)')
print('sudo python3 pyledx.py -c --limegreen --rotate')
print('sudo python3 pyledx.py -c --circle')
print('sudo python3 pyledx.py -c --complex_hellsgate')
print("")
print('\x1B[4m' + 'Complex animations available:' + '\x1B[0m')
print('--complex_universe, --complex_galaxy, --complex_uranium, --complex_hellsgate --complex_scientist, --complex_raspberry, --complex_mcportal')
print('')


def rotateAnimation(strip, color):
    led_order = [3, 2, 1]  # LED order to create the desired sequence (modify as needed)
    fade_steps = 40       # Number of steps for the fade effect

    for _ in range(strip.numPixels()):
        for i in led_order:
            # Fade out the previous LED
            for step in range(fade_steps):
                fade_color = Color(int(((fade_steps - step) / fade_steps) * ((color >> 16) & 255)),
                                   int(((fade_steps - step) / fade_steps) * ((color >> 8) & 255)),
                                   int(((fade_steps - step) / fade_steps) * (color & 255)))
                strip.setPixelColor(i, fade_color)
                strip.show()
                time.sleep(0.005)  # Faster fade-out

            # Turn off the previous LED
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

            # Fade in the next LED
            for step in range(fade_steps):
                fade_color = Color(int((step / fade_steps) * ((color >> 16) & 255)),
                                   int((step / fade_steps) * ((color >> 8) & 255)),
                                   int((step / fade_steps) * (color & 255)))
                strip.setPixelColor(led_order[(led_order.index(i) + 1) % len(led_order)], fade_color)
                strip.show()
                time.sleep(0.005)  # Faster fade-in

            # Turn on the next LED
            strip.setPixelColor(led_order[(led_order.index(i) + 1) % len(led_order)], color)
            strip.show()

            time.sleep(0.005)  # Adjust the duration to control the speed of the animation

        # Turn off the last LED
        strip.setPixelColor(led_order[-1], Color(0, 0, 0))
        strip.show()

# Function to set a single color for all LEDs in the strip
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms / 1000.0)

# Function to get a specific color
def get_color(color_name):
    colors = {
        'red': Color(255, 0, 0),
        'orange': Color(255, 69, 0),
        'yellow': Color(255, 255, 0),
        'green': Color(0, 255, 0),
        'cyan': Color(0, 255, 255),
        'blue': Color(0, 0, 255),
        'purple': Color(128, 0, 128),
        'white': Color(255, 255, 255),
        'limegreen': Color(150, 255, 0),
        'gray': Color(128, 128, 128),
        'deepgray': Color(64, 64, 64),
        'pink': Color(255, 0, 120),
        # Add more colors here if needed
    }
    return colors.get(color_name, Color(0, 0, 0))  # Default to off (black) color if the provided color name is not recognized

# Function to smoothly interpolate between two colors
def interpolate_color(color1, color2, steps):
    r1, g1, b1 = (color1 >> 16) & 255, (color1 >> 8) & 255, color1 & 255
    r2, g2, b2 = (color2 >> 16) & 255, (color2 >> 8) & 255, color2 & 255

    colors = []
    for step in range(steps):
        # Calculate the percentage of completion for both "fade in" and "fade out" parts
        fade_in_progress = abs(2 * step - steps) / steps
        r_val = int(r1 + (r2 - r1) * fade_in_progress)
        g_val = int(g1 + (g2 - g1) * fade_in_progress)
        b_val = int(b1 + (b2 - b1) * fade_in_progress)
        colors.append(Color(r_val, g_val, b_val))

    return colors

# Function to blink all LEDs with white color three times for one second each
def blinkTest(strip):
    for _ in range(5):  # Blink 5 times
        colorWipe(strip, Color(255, 255, 255), 100)  # White color, 100ms delay
        colorWipe(strip, Color(0, 0, 0), 100)        # Turn off, 100ms delay

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

# Function to create an animation that alternates between three colors (red, orange, and gray) in a circular pattern - Inferno Cycle
def cyclemcportal(strip, wait_ms=20, iterations=5):
    colors = ['purple', 'pink', 'purple', 'pink', 'purple', 'deepgray']  # Colors to cycle through (gray added to the sequence)
    fade_steps = 26  # Number of steps for the fade effect

    while True:
        for j in range(64 * iterations):
            for i in range(strip.numPixels()):
                # Calculate the index for each LED based on the current iteration and number of LEDs
                led_index = (i * fade_steps // strip.numPixels() + j) % fade_steps
                # Determine the current color based on the LED index
                color_index = led_index * len(colors) // fade_steps
                color1 = get_color(colors[color_index])
                color2 = get_color(colors[(color_index + 1) % len(colors)])

                # Interpolate between color1 and color2 based on the current LED index
                fade_in_progress = abs(2 * led_index - fade_steps) / fade_steps
                interpolated_color = interpolate_color(color1, color2, fade_steps)[led_index]

                # Update the LED with the current color
                strip.setPixelColor(i, interpolated_color)
            strip.show()
            time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

# Function to create an animation that alternates between two colors (purple and pink) in a circular pattern
def cycleUniverse(strip, wait_ms=20, iterations=5):
    color1 = Color(128, 0, 128)    # Purple color
    color2 = Color(255, 0, 60)    # Pink color
    fade_steps = 32  # Number of steps for the fade effect

    while True:
        for j in range(64 * iterations):
            for i in range(strip.numPixels()):
                # Calculate the index for each LED based on the current iteration and number of LEDs
                led_index = (i * fade_steps // strip.numPixels() + j) % fade_steps
                # Alternate between the colors based on the LED index
                color = interpolate_color(color1, color2, fade_steps)[led_index]
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

# Function to create an animation that alternates between two colors (blue and cyan) in a circular pattern - For my brother Anghios <3
def cycleGalaxy(strip, wait_ms=20, iterations=5):
    color1 = Color(0, 0, 255)    # Blue color
    color2 = Color(0, 255, 255)  # Cyan color
    fade_steps = 32  # Number of steps for the fade effect

    while True:
        for j in range(64 * iterations):
            for i in range(strip.numPixels()):
                # Calculate the index for each LED based on the current iteration and number of LEDs
                led_index = (i * fade_steps // strip.numPixels() + j) % fade_steps
                # Alternate between the colors based on the LED index
                color = interpolate_color(color1, color2, fade_steps)[led_index]
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

# Function to create an animation that alternates between two colors (orange and yellow) in a circular pattern
def cycleuranium(strip, wait_ms=20, iterations=5):
    color1 = Color(255, 69, 0)   # Orange color
    color2 = Color(255, 255, 0)  # Yellow color
    fade_steps = 32  # Number of steps for the fade effect

    while True:
        for j in range(64 * iterations):
            for i in range(strip.numPixels()):
                # Calculate the index for each LED based on the current iteration and number of LEDs
                led_index = (i * fade_steps // strip.numPixels() + j) % fade_steps
                # Alternate between the colors based on the LED index
                color = interpolate_color(color1, color2, fade_steps)[led_index]
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

# Function to create an animation that alternates between two colors (red and gray) in a circular pattern
def cycleHellsgate(strip, wait_ms=20, iterations=5):
    color1 = Color(255, 0, 0)   # Red color
    color2 = Color(16, 16, 16)  # Gray color
    fade_steps = 40  # Number of steps for the fade effect

    while True:
        for j in range(64 * iterations):
            for i in range(strip.numPixels()):
                # Calculate the index for each LED based on the current iteration and number of LEDs
                led_index = (i * fade_steps // strip.numPixels() + j) % fade_steps
                # Alternate between the colors based on the LED index
                if led_index < fade_steps // 2:
                    color = interpolate_color(color1, color2, fade_steps // 2)[led_index]
                else:
                    color = interpolate_color(color2, color1, fade_steps // 2)[led_index - fade_steps // 2]
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

# Function to create an animation that alternates between two colors (green and yellow) in a circular pattern
def complexScientist(strip, wait_ms=20, iterations=5):
    color1 = Color(0, 255, 0)    # Green color
    color2 = Color(255, 255, 0)  # Yellow color
    fade_steps = 40  # Number of steps for the fade effect

    while True:
        for j in range(64 * iterations):
            for i in range(strip.numPixels()):
                # Calculate the index for each LED based on the current iteration and number of LEDs
                led_index = (i * fade_steps // strip.numPixels() + j) % fade_steps
                # Alternate between the colors based on the LED index
                if led_index < fade_steps // 2:
                    color = interpolate_color(color1, color2, fade_steps // 2)[led_index]
                else:
                    color = interpolate_color(color2, color1, fade_steps // 2)[led_index - fade_steps // 2]
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

def complexraspberry(strip, wait_ms=20, iterations=5):
    color1 = Color(255, 0, 120)  # Pink color
    color2 = Color(255, 0, 0)    # Red color
    fade_steps = 36  # Number of steps for the fade effect

    while True:
        for j in range(64 * iterations):
            for i in range(strip.numPixels()):
                # Calculate the index for each LED based on the current iteration and number of LEDs
                led_index = (i * fade_steps // strip.numPixels() + j) % fade_steps
                # Alternate between the colors based on the LED index
                if led_index < fade_steps // 2:
                    color = interpolate_color(color1, color2, fade_steps // 2)[led_index]
                else:
                    color = interpolate_color(color2, color1, fade_steps // 2)[led_index - fade_steps // 2]
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)  # Increase the value of wait_ms to slow down the animation

def rainbowCircle(strip, wait_ms=20, iterations=1):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            scaled_index = int(i * 256 / 4 / strip.numPixels()) + j
            color = wheel(scaled_index & 255)
            if color == Color(0, 0, 255) or color == Color(255, 0, 0):
                strip.setPixelColor(i, color)
            else:
                strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms / 1000.0)

# Function to create a fading animation on the strip with a given color
def fadeAnimation(strip, color, duration=None, steps=100):
    """Animate the fading effect for the LEDs.

    Args:
        strip (PixelStrip): The LED strip object.
        color (int): The target color for the animation.
        duration (float, optional): The duration of the animation in seconds. If None, the --pvel
                                    command-line argument will be used. Defaults to None.
        steps (int): The number of steps for the fading effect. Larger values create smoother fading.
    """
    if duration is None:
        duration = 2  # Default pulsate velocity in seconds if no --pvel argument is provided

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

# Define las opciones de animación de color
color_animations = {
    'red': 'show red color',
    'green': 'show green color',
    'blue': 'show blue color',
    'yellow': 'show yellow color',
    'cyan': 'show cyan color',
    'purple': 'show purple color',
    'white': 'show white color',
    'orange': 'show orange color',
    'pink': 'show pink color',
    'limegreen': 'show lime green color',
    'gray': 'show gray color',
    'deepgray': 'show deepgray color'
}

# Define las opciones de animación compleja
complex_animations = {
    'universe': 'cycle between purple and pink only (Universe effect - Surce)',
    'galaxy': 'cycle between blue and cyan only (Galaxy effect - Anghios)',
    'uranium': 'cycle between orange and yellow only (uranium effect)',
    'hellsgate': 'cycle between red and gray (Hellsgate effect)',
    'scientist': 'cycle between green and yellow (Complex Scientist effect)',
    'raspberry': 'cycle between pink and red (Complex raspberry effect)',
    'mcportal': 'cycle between mc portal particles! (Complex mcportal effect)'
}

if __name__ == '__main__':
    # Command-line argument parsing
    parser = argparse.ArgumentParser()

    # Agrega las opciones adicionales al parser
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('--test', action='store_true', help='test the script and led system')
    parser.add_argument('--circle', action='store_true', help='show rainbow all colors animation')
    parser.add_argument('--pulsate', action='store_true', help='pulsate LEDs')
    parser.add_argument('--rotate', action='store_true', help='run the sprint animation with the specified color')
    parser.add_argument('--pvel', type=float, default=2, help='pulsate velocity (default is 2)')

    for color_arg, help_text in color_animations.items():
        parser.add_argument(f'--{color_arg}', action='store_true', help=help_text)

    # Agrega las opciones de animación compleja al parser
    for complex_arg, help_text in complex_animations.items():
        parser.add_argument(f'--complex_{complex_arg}', action='store_true', help=help_text)

    args = parser.parse_args()

    # Initialize the NeoPixel strip
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

try:
    while True:
        if args.test:
            blinkTest(strip)
            print("!!! If the leds blinked in white 5 times it means it is working")
            print("")
            break
        elif args.circle and args.pulsate:
            message = "!!! --circle flag doesn't accept --pulsate requests, running --circle instead..."
        elif args.pulsate and args.rotate:
            message = "!!! --pulsate flag doesn't accept --rotate requests, running --circle instead..."
        else:
            message = None

        if message:
            print(message)
            print("")
            rainbow(strip, wait_ms=20, iterations=1)
            time.sleep(1)
            rainbowCycle(strip, wait_ms=20, iterations=5)
            time.sleep(1)

        elif args.rotate and any(getattr(args, color_arg) for color_arg in color_animations):
            sprint_color_arg = [color_arg for color_arg in color_animations if getattr(args, color_arg)][0]
            sprint_color = get_color(sprint_color_arg)
            while True:
                rotateAnimation(strip, sprint_color)

        else:
            color_args = ['red', 'green', 'blue', 'yellow', 'cyan', 'purple', 'white', 'orange', 'pink', 'limegreen', 'gray', 'deepgray']
            for color_arg in color_args:
                if getattr(args, color_arg):
                    color = {
                        'red': Color(255, 0, 0),
                        'green': Color(0, 255, 0),
                        'blue': Color(0, 0, 255),
                        'yellow': Color(255, 255, 0),
                        'cyan': Color(0, 255, 255),
                        'purple': Color(128, 0, 128),
                        'white': Color(255, 255, 255),
                        'orange': Color(255, 69, 0),
                        'pink': Color(255, 0, 120),
                        'limegreen': Color(150, 255, 0),
                        'gray': Color(16, 16, 16),
                        'deepgray': Color(8, 8, 8),
                    }[color_arg]
                    if args.pulsate:
                        fadeAnimation(strip, color, duration=args.pvel, steps=40)
                    else:
                        colorWipe(strip, color)
                    break
            else:
                complex_args = ['universe', 'galaxy', 'uranium', 'hellsgate', 'scientist', 'raspberry', 'mcportal']
                complex_found = False  # Variable de control para indicar si se encontró un complex_arg válido

                for complex_arg in complex_args:
                    if getattr(args, f'complex_{complex_arg}'):
                        complex_func = {
                            'universe': cycleUniverse,
                            'galaxy': cycleGalaxy,
                            'uranium': cycleuranium,
                            'hellsgate': cycleHellsgate,
                            'scientist': complexScientist,
                            'raspberry': complexraspberry,
                            'mcportal': cyclemcportal
                        }[complex_arg]
                        if args.pulsate:
                            print(f"!!! --complex_{complex_arg} flag doesn't accept --pulsate requests, running --circle instead...")
                            print("")
                            complex_found = True  # Establecer la variable de control en True para indicar una coincidencia
                            break
                        elif args.rotate:
                            print(f"!!! --complex_{complex_arg} flag doesn't accept --rotate requests, running --circle instead...")
                            print("")
                            complex_found = True  # Establecer la variable de control en True para indicar una coincidencia
                            break
                        else:
                            wait_ms_dict = {
                                'universe': 50,
                                'galaxy': 50,
                                'uranium': 50,
                                'hellsgate': 100,
                                'scientist': 75,
                                'raspberry': 100,
                                'mcportal': 250
                            }
                            complex_func(strip, wait_ms=wait_ms_dict.get(complex_arg, 20), iterations=5)
                            complex_found = True  # Establecer la variable de control en True para indicar una coincidencia
                            break

                # Verificar si se encontró una coincidencia y si no, mostrar un mensaje de error
                if not complex_found:
                    rainbow(strip, wait_ms=20, iterations=1)
                    time.sleep(1)
                    rainbowCycle(strip, wait_ms=20, iterations=5)
                    time.sleep(1)
                else:
                    # If no specific color flag is provided, run a sequence of default animations
                    animations = [
                        (rainbow, {'wait_ms': 20, 'iterations': 1}),
                        (rainbowCycle, {'wait_ms': 20, 'iterations': 5})
                    ]
                    for animation_func, animation_args in animations:
                        animation_func(strip, **animation_args)
                        time.sleep(1)

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C) and clear the LEDs if specified
    if args.clear:
        colorWipe(strip, Color(0, 0, 0), 10)
