#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Upgrade pip
python -m pip install --upgrade pip

# Uninstall all currently installed packages
if python -m pip freeze | grep -q .; then
  python -m pip freeze | xargs python -m pip uninstall -y
  if [ $? -ne 0 ]; then
    echo "Uninstallation failed."
    exit 1
  fi
else
  echo "No packages to uninstall."
fi

# Determine the correct requirements file based on the environment
REQUIREMENTS_FILE="requirements.txt"  # Default requirements file

# If you want to add more packages for ENV_STATE=dev
# if [ -f .env ]; then
#   source .env
#   if [ "$ENV_STATE" == "dev" ]; then
#     REQUIREMENTS_FILE="requirements-dev.txt"
#   fi
# fi

# Install the required packages
python -m pip install -r $REQUIREMENTS_FILE
if [ $? -ne 0 ]; then
  echo "Installation failed."
  exit 1
fi

echo "Using requirements file: $REQUIREMENTS_FILE"

echo "Dependencies installed successfully."

if [ -f ".env" ]; then
  if [ -f "example.env" ]; then
    rm example.env
  fi

  while IFS= read -r line; do
    if [[ "$line" == *"="* ]]; then
      variable=$(echo "$line" | awk -F "=" '{print $1}')
      dummy_value="dummy_${variable}"
      line="${variable}=${dummy_value}"
    fi
    echo "$line" >> example.env
  done < .env
fi



