"""
MaxTechFix Software Protector
Developer: Zulfiqar Ali | www.maxtechfix.com

Entry point for the Software Protector application.
"""
import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from protector.app import run_app

if __name__ == "__main__":
    run_app()
