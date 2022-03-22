# If you have Ubuntu uncomment the following 2 lines
# command -v python3 >/dev/null 2>&1 || { echo >&2 "python3 is not installed.  Aborting."; exit 1; } # Check if the command exist (works only on Ubuntu)
# dpkg-query -l python3-venv > /dev/null 2>&1 || { echo >&2 "python3-venv is not installed. Aborting.";exit 1;} # Check if the package is installed (works only on Ubuntu)
python3 -m venv . # Creates a virtual enviroment on the directory
source bin/activate # Activates enviroment
pip install --upgrade pip # Check if its possible to update pip
pip3 install -r requirements.txt # Install the list with pip
