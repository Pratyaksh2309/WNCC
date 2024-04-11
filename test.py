# test.py
import os
import random

def get_random_script_output():
    scripts_folder = 'user_files/'
    scripts = [f for f in os.listdir(scripts_folder) if os.path.isfile(os.path.join(scripts_folder, f))]
    
    if len(scripts) < 1:
        return None  # Not enough scripts for testing
    
    random_script = random.choice(scripts)
    with open(os.path.join(scripts_folder, random_script), 'r') as file:
        return file.read()
