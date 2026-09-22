"""Explicitly regenerate the reviewable Cantera YAML from state/TS CSV tables."""
from pathlib import Path
import argparse
from catalysis.cantera_reference import write_mechanism
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).parent/'input')
write_mechanism(p.parse_args().input)
