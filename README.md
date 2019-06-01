# aerolibb
Aerospace package for Python in progress.
This will be a tool to help design spacecrafts and plan space missions. Notes:
- Spacecrafts are defined as classes and each subsystem (propulsion, power, comms, ADCS, etc.) are classes which can generate objects within the main spacecraft class.
- Aside from system classes, files with functions for simple orbital mechanics, controls, etc. will also be provided for use independently or with a spacecraft.

WARNING:
DO NOT RUN any files with the text "test". This includes: aerotest.py, test1.py, testpower.py, testkalman.py.
These are just for internal tests and are not part of the library.
