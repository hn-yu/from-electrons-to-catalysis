# Input contract

`example.json` contains the experiment name and all model parameters. Energies are eV and distances angstrom unless a key or the README explicitly specifies atomic/reduced units. Random experiments have a fixed seed.

Change parameters in a copy, record a new prediction, and pass `--input your.json`. The result embeds the exact input and its SHA-256 hash.
