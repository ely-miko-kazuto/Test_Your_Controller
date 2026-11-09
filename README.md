# Test Your Controller

A lightweight, cross-platform desktop app for checking live game-controller input. It currently supports DualShock 4 and Xbox 360 wireless controllers, along with other controllers recognized by Pygame.

## Features

- Detect and select connected controllers
- View live left- and right-stick positions
- Monitor trigger values, face and shoulder buttons, and D-pad input
- Refresh the device list after connecting a controller

## Requirements

- Python 3
- Tkinter, usually included with Python (some Linux distributions provide it as a separate package)
- Pygame

## Run

1. Connect your controller to your computer.
2. Install Pygame if needed:

   ```bash
   python -m pip install pygame
   ```

3. Start the tester from the project directory:

   ```bash
   python Tester.py
   ```

4. Select your controller if necessary. If it was connected after the app started, click **REFRESH**.

The app updates controller input while it is open. Axis and button layouts can vary by device, so some controls may be reported differently depending on the controller and operating system.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
