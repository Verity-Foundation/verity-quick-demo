"""
Docstring for main
"""
import sys
from src.cli import main

if __name__ == "__main__":
    #main()
    sys.path.append('.')
    # Simulate CLI arguments for headless mode
    sys.argv = ['cli.py', '--message',
                'Test claim', '--issuer', 'did:verity:gov:demo-election-comm']
    try:
        main()
    except SystemExit:
        pass
