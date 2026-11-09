# Test Your Controller 🎮

**Give your gamepad a quick checkup—no boss fight required.**

Test Your Controller is a lightweight desktop app that shows live input from connected game controllers. Watch your sticks move, squeeze your triggers, tap your buttons, and see what your D-pad is reporting—all in one tidy window.

> Built with Python, Tkinter, and Pygame. Currently supports DualShock 4 and Xbox 360 wireless controllers, as well as other controllers recognized by Pygame.

## What you can test

- **Analog sticks:** See left and right stick positions update live, with normalized axis values.
- **Triggers:** Track trigger input with percentage indicators.
- **Buttons:** Check face buttons, shoulders, sticks, and other common controls.
- **D-pad:** See reported directions at a glance.
- **Connected devices:** Select a detected controller or refresh the device list after connecting one.

## Get started

### Requirements

- Python 3
- Tkinter (typically included with Python; some Linux distributions package it separately)
- Pygame

Install Pygame if it is not already available:

```bash
python -m pip install pygame
```

### Launch the tester

Connect your controller, then run this from the project directory:

```bash
python Tester.py
```

Choose your controller from the device list. If you connect it after the app opens, click **REFRESH** to scan again.

## A couple of controller quirks

Controller layouts vary across models, drivers, and operating systems. Button names or trigger axes may not line up exactly with the labels shown in the app, and some devices may not report a D-pad as a hat switch. If an input looks unexpected, the controller may simply be speaking its own dialect.

## License

Released under the [MIT License](LICENSE).
