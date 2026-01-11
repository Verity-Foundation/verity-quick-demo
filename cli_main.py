"""
Docstring for main
"""
from src.cli import VerityDemoCLI


if __name__ == "__main__":
    v = VerityDemoCLI()
    try:
        v.run()
    except SystemExit:
        pass
