# Hands-On Quantum Computing Workshop

Build and run quantum circuits in Python with [Qiskit](https://www.ibm.com/quantum/qiskit). Every lab runs in Google Colab on a simulator: no installation, no paid account.

## Labs

| Notebook | Topic | Time |
|---|---|---|
| `00_setup` | Check that everything works (do this before the workshop) | 5 min |
| `01_one_qubit` | Gates, the Bloch sphere, measurement, interference | 30 min |
| `02_entanglement` | Bell and GHZ states | 40 min |
| `03_noise_and_randomness` | Realistic hardware noise, quantum random numbers | 30 min |
| `04_grover_search` | Find a marked item in one query | 45 min |
| `05_teleportation` | Move a qubit state with entanglement and two classical bits | 30 min |
| `06_bb84_optional` | Quantum key distribution and catching an eavesdropper | extra |

Attendee notebooks are in `notebooks/` and have exercises marked `TODO`. Worked answers are in `solutions/`.

## Running in Colab (recommended)

Open a notebook from `notebooks/` and click the **Open in Colab** badge at the top, or go to https://colab.research.google.com, choose **File > Open notebook > GitHub**, and paste this repository's URL. The first code cell installs Qiskit.

## Running locally

Requires Python 3.10 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt jupyterlab
jupyter lab
```

## Real hardware (optional)

The labs never need an account. To run your own circuits on a real IBM quantum computer afterwards, create a free Open Plan account at https://quantum.cloud.ibm.com, store your API key as a Colab secret named `IBM_QUANTUM_TOKEN`, and follow `facilitator/hardware_demo.ipynb`. Never paste an API key into a notebook cell.

## For facilitators

- `facilitator/RUNBOOK.md`: schedule, preparation checklist and fallbacks.
- `facilitator/hardware_demo.ipynb`: the live hardware demo.
- `facilitator/pre_workshop_email.md`: setup instructions to send attendees.

### Editing the notebooks

The notebooks are generated from `tools/build_notebooks.py`, which defines each lab once and writes both the attendee and solution versions. Edit that file, not the notebooks, then rebuild:

```bash
python tools/build_notebooks.py
```

Before publishing, set `REPO` at the top of that script to your GitHub `owner/name` and rebuild, so the Colab badges point at your copy.

### Versions

Package versions are pinned because the Qiskit API changes often. The notebooks were tested with Qiskit 2.6.1, Qiskit Aer 0.18.2 and qiskit-ibm-runtime 0.51.0. If you upgrade, rerun every solution notebook first.
