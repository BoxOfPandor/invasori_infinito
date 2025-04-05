import argparse
import subprocess
import os
import pygame
import random
import sys

def main():
    os.environ['PYTHONWARNINGS'] = "ignore"
    parser = argparse.ArgumentParser(description='Controls: Use the arrow keys to move')
    args = parser.parse_args()
    if os.isatty(1) and 'DISPLAY' not in os.environ:
        subprocess.run(["python3", "flame_game_tty.py"])
    else:
        subprocess.run(["python3", "flame_game.py"])

if __name__ == "__main__":
    main()