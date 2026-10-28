# Facilitator runbook

## Schedule (3 h 45 min including break)

| Time | Block | Notebook | Notes |
|---|---|---|---|
| 0:00 | Introduction | Quirk (algassert.com/quirk) | Bits vs. qubits. Have attendees drag H and a measurement onto a wire, then add a CNOT. |
| 0:20 | Lab 1: One qubit | `01_one_qubit` | First 5 minutes go to Colab install. Exercise 1.2 (interference) is the key moment; discuss before moving on. |
| 0:50 | Lab 2: Entanglement | `02_entanglement` | Lead the "can entanglement send a message?" discussion. It sets up Lab 5. |
| 1:30 | Break | | Start the live hardware job now so it is through the queue by 2:10. |
| 1:40 | Lab 3: Noise and randomness | `03_noise_and_randomness` | Exercise 3.1 shows errors growing with circuit size. |
| 2:10 | Live hardware demo | `facilitator/hardware_demo.ipynb` | Show the job started at the break, or the backup job. Compare with the Lab 3 noisy simulator. |
| 2:30 | Lab 4: Grover search | `04_grover_search` | Bit ordering (rightmost character is qubit 0) trips people up in Exercise 4.1. |
| 3:15 | Lab 5: Teleportation | `05_teleportation` | Buffer block: if behind, walk through the solution on screen instead. |
| 3:40 | Wrap-up | | How to get a free IBM account, resources, `06_bb84_optional` as take-home. |

## One week before

- [ ] Set `REPO` in `tools/build_notebooks.py`, rebuild, push to GitHub, and confirm the Colab badges open the right notebooks.
- [ ] Open every solution notebook in Colab and run all cells. Fix any version breakage before the day.
- [ ] Send `pre_workshop_email.md` to attendees.
- [ ] Confirm the current IBM Open Plan limits (about 10 minutes of QPU time per month as of 2026) and that your account works.
- [ ] Check the venue Wi-Fi allows Colab and pip installs (pypi.org, files.pythonhosted.org).

## Day before

- [ ] Run `hardware_demo.ipynb` with `USE_FAKE = False`. Paste the job ID into `BACKUP_JOB_ID` and save.
- [ ] Rehearse the demo once with `USE_FAKE = True`.
- [ ] Screenshot the key result of every lab as a fallback.

## Fallbacks

| Problem | Response |
|---|---|
| Hardware job still queued at 2:10 | Show the backup job, then check the live one again at the end. |
| IBM service down | Run the demo with `USE_FAKE = True` and explain it uses real device error rates. |
| Colab slow or blocked | Attendees pair up on working laptops. Show solutions from your own machine. |
| An attendee's install fails | Runtime > Disconnect and delete runtime, then run all again. |
| Running behind | Skip the Lab 2 stretch exercise and Exercise 4.2, then present Lab 5 as a walkthrough. |

## Notes on the code

- Qiskit 2.x removed `c_if`. Lab 5 uses `with qc.if_test(...)` for Bob's corrections.
- `SamplerV2` in the hardware demo is deprecated as of qiskit-ibm-runtime 0.50 but works with the pinned 0.51.0. Recheck if you upgrade.
- The simulator's "quantum random numbers" in Lab 3 come from a pseudo-random generator. Say so; the physics only applies on real hardware.
