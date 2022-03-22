# If you're on Ubuntu uncomment the following 2 lines
# command -v python3 >/dev/null 2>&1 || { echo >&2 "python3 is not installed.  Aborting."; exit 1; } # Check if the command exist (Ubuntu only)
# dpkg-query -l python3-venv > /dev/null 2>&1 || { echo >&2 "python3-venv is not installed. Aborting.";exit 1;} # Check if the package is installed (Ubuntu only)
python3 -m venv . # Creates a virtual environment on the directory
source bin/activate # Activates environment
pip install --upgrade pip # Try to update pip if its possible
pip3 install -r requirements.txt # Install the list in the file with pip
