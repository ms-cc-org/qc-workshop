"""Build the workshop notebooks.

Every lab is defined once below. Running this script writes two copies of
each lab:

    notebooks/   attendee version, exercises replaced with TODO stubs
    solutions/   facilitator version, exercises filled in

Usage:
    python tools/build_notebooks.py

Set REPO to your GitHub "owner/name" before building so the
"Open in Colab" badges point at your copy of the repository.
"""

from pathlib import Path
from textwrap import dedent

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

REPO = "ms-cc-org/qc-workshop"
BRANCH = "main"
ROOT = Path(__file__).resolve().parent.parent

INSTALL = dedent(
    """\
    # Install pinned versions (takes about a minute in Colab; already done locally)
    %pip install -q qiskit==2.6.1 qiskit-aer==0.18.2 qiskit-ibm-runtime==0.51.0 matplotlib pylatexenc
    """
)

HELPERS = dedent(
    """\
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    from qiskit.visualization import plot_histogram

    sim = AerSimulator()

    def run(qc, shots=1000, backend=sim):
        \"\"\"Run a circuit and return the measurement counts.\"\"\"
        return backend.run(transpile(qc, backend), shots=shots).result().get_counts()
    """
)


def md(text):
    return ("md", dedent(text).strip())


def code(text):
    return ("code", dedent(text).strip())


def ex(attendee, solution):
    """Exercise cell: attendees get `attendee`, solutions get `solution`."""
    return ("ex", dedent(attendee).strip(), dedent(solution).strip())


def badge(folder, name):
    url = f"https://colab.research.google.com/github/{REPO}/blob/{BRANCH}/{folder}/{name}"
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"


# ---------------------------------------------------------------------------
# Lab 0: setup
# ---------------------------------------------------------------------------
LAB0 = [
    md(
        """
        # Lab 0: Setup check

        Run every cell in this notebook (Runtime > Run all). If the last cell
        prints a histogram, you are ready for the workshop.
        """
    ),
    code(INSTALL),
    code(
        """
        import sys, qiskit, qiskit_aer
        print("Python ", sys.version.split()[0])
        print("Qiskit ", qiskit.__version__)
        print("Aer    ", qiskit_aer.__version__)
        """
    ),
    code(HELPERS),
    md(
        """
        ## Hello, qubit

        This circuit puts one qubit into superposition and measures it 1000 times.
        You should see roughly 500 zeros and 500 ones. Don't worry about how it
        works yet: that is Lab 1.
        """
    ),
    code(
        """
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()
        counts = run(qc)
        print(counts)
        plot_histogram(counts)
        """
    ),
    md(
        """
        ## Optional: IBM Quantum account

        All labs run on a simulator, so you do not need an account today. To run
        on real hardware after the workshop:

        1. Create a free account at https://quantum.cloud.ibm.com (Open Plan).
        2. Copy your API key from the dashboard.
        3. In Colab, open the key icon (Secrets) in the left sidebar, add a secret
           named `IBM_QUANTUM_TOKEN`, and paste the key as its value.

        Never paste the key into a notebook cell: notebooks get shared, and the
        key would go with it.
        """
    ),
]

# ---------------------------------------------------------------------------
# Lab 1: one qubit
# ---------------------------------------------------------------------------
LAB1 = [
    md(
        """
        # Lab 1: One qubit

        **Goals:** build single-qubit circuits, see superposition on the Bloch
        sphere, and connect amplitudes to measurement statistics.
        """
    ),
    code(INSTALL),
    code(
        HELPERS
        + dedent(
            """
            from qiskit.quantum_info import Statevector
            from qiskit.visualization import plot_bloch_multivector
            import numpy as np
            """
        )
    ),
    md(
        """
        ## 1.1 The state of a qubit

        A qubit starts in $|0\\rangle$. `Statevector` shows its amplitudes
        without measuring, which only a simulator can do.
        """
    ),
    code(
        """
        qc = QuantumCircuit(1)
        state = Statevector(qc)
        print(state)
        plot_bloch_multivector(state)
        """
    ),
    md(
        """
        ## 1.2 The X gate (quantum NOT)

        X flips $|0\\rangle$ to $|1\\rangle$: the arrow moves from the north pole
        to the south pole.
        """
    ),
    code(
        """
        qc = QuantumCircuit(1)
        qc.x(0)
        plot_bloch_multivector(Statevector(qc))
        """
    ),
    md(
        """
        ## 1.3 The H gate (superposition)

        Hadamard takes $|0\\rangle$ to
        $\\frac{1}{\\sqrt{2}}(|0\\rangle + |1\\rangle)$, a point on the equator.
        Both amplitudes are $1/\\sqrt{2} \\approx 0.707$, so each outcome has
        probability $0.707^2 = 0.5$.
        """
    ),
    code(
        """
        qc = QuantumCircuit(1)
        qc.h(0)
        state = Statevector(qc)
        print(state)
        print("Probabilities:", state.probabilities_dict())
        plot_bloch_multivector(state)
        """
    ),
    md(
        """
        ## 1.4 Measurement

        Measuring collapses the qubit to 0 or 1. Repeating the circuit many times
        ("shots") reveals the probabilities.
        """
    ),
    code(
        """
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()
        display(qc.draw("mpl"))
        counts = run(qc, shots=1000)
        print(counts)
        plot_histogram(counts)
        """
    ),
    md(
        """
        Try changing `shots` to 10, then 10000. With few shots the split is
        uneven; with many it approaches 50/50.
        """
    ),
    md(
        """
        ## Exercise 1.1: Always 1

        Build a circuit that measures `1` every time.
        """
    ),
    ex(
        """
        qc = QuantumCircuit(1)
        # TODO: add one gate here

        qc.measure_all()
        counts = run(qc)
        print(counts)
        """,
        """
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.measure_all()
        counts = run(qc)
        print(counts)
        assert counts == {"1": 1000}
        """,
    ),
    md(
        """
        ## Exercise 1.2: Interference

        Apply H twice, then measure. Predict the result before you run it.
        Is it 50/50?
        """
    ),
    ex(
        """
        qc = QuantumCircuit(1)
        # TODO: apply H twice

        qc.measure_all()
        counts = run(qc)
        print(counts)
        """,
        """
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.h(0)
        qc.measure_all()
        counts = run(qc)
        print(counts)
        assert counts == {"0": 1000}
        """,
    ),
    md(
        """
        The answer is always 0. The two paths to `1` have opposite signs and
        cancel, while the paths to `0` add up. This *interference* is what
        quantum algorithms use to boost right answers and cancel wrong ones.
        A classical coin flipped twice would still be 50/50.
        """
    ),
    md(
        """
        ## Exercise 1.3: A biased quantum coin

        `qc.ry(theta, 0)` rotates the qubit by angle `theta` about the Y axis.
        The probability of measuring 0 is $\\cos^2(\\theta/2)$.

        Find `theta` so the qubit measures 0 about 75% of the time.
        """
    ),
    ex(
        """
        theta = 0  # TODO: choose theta

        qc = QuantumCircuit(1)
        qc.ry(theta, 0)
        qc.measure_all()
        counts = run(qc, shots=10000)
        print(counts)
        plot_histogram(counts)
        """,
        """
        theta = 2 * np.arccos(np.sqrt(0.75))  # = pi/3

        qc = QuantumCircuit(1)
        qc.ry(theta, 0)
        qc.measure_all()
        counts = run(qc, shots=10000)
        print(counts)
        assert abs(counts.get("0", 0) / 10000 - 0.75) < 0.03
        plot_histogram(counts)
        """,
    ),
    md(
        """
        ## Summary

        - A qubit's state is a pair of amplitudes; measurement probabilities are
          their squares.
        - H creates an equal superposition. X flips the qubit.
        - Amplitudes can cancel (interference), which has no classical analogue.
        """
    ),
]

# ---------------------------------------------------------------------------
# Lab 2: entanglement
# ---------------------------------------------------------------------------
LAB2 = [
    md(
        """
        # Lab 2: Entanglement

        **Goals:** create a Bell state, see correlations no classical coin can
        produce, and extend to three qubits.
        """
    ),
    code(INSTALL),
    code(HELPERS),
    md(
        """
        ## 2.1 The Bell state

        H puts qubit 0 into superposition. CNOT (`cx`) flips qubit 1 only when
        qubit 0 is 1. The result is
        $\\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$.

        Qiskit prints bit strings right to left: in `"01"`, qubit 0 is the
        rightmost bit.
        """
    ),
    code(
        """
        bell = QuantumCircuit(2)
        bell.h(0)
        bell.cx(0, 1)
        bell.measure_all()
        display(bell.draw("mpl"))

        counts = run(bell)
        print(counts)
        plot_histogram(counts)
        """
    ),
    md(
        """
        Only `00` and `11` appear. Each qubit on its own is a fair coin, yet the
        two always agree.
        """
    ),
    code(
        """
        # Look at each qubit separately: both are 50/50
        q0 = {"0": 0, "1": 0}
        q1 = {"0": 0, "1": 0}
        for bits, n in counts.items():
            q0[bits[1]] += n
            q1[bits[0]] += n
        print("qubit 0:", q0)
        print("qubit 1:", q1)
        """
    ),
    md(
        """
        ## Discussion: can entanglement send a message?

        No. Whoever holds qubit 1 sees a random 50/50 result whatever is done to
        qubit 0. The correlation only shows up when the two results are compared,
        and comparing them needs an ordinary (classical) channel. We use exactly
        this fact in Lab 5.
        """
    ),
    md(
        """
        ## Exercise 2.1: The anti-correlated Bell state

        Build a circuit whose results are only `01` and `10`: the qubits always
        disagree. Hint: start from the Bell circuit and add one gate.
        """
    ),
    ex(
        """
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        # TODO: add one gate

        qc.measure_all()
        counts = run(qc)
        print(counts)
        """,
        """
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.x(1)
        qc.measure_all()
        counts = run(qc)
        print(counts)
        assert set(counts) == {"01", "10"}
        """,
    ),
    md(
        """
        ## Exercise 2.2: GHZ state (three qubits)

        Entangle three qubits so the only results are `000` and `111`.
        """
    ),
    ex(
        """
        ghz = QuantumCircuit(3)
        # TODO: build the GHZ state

        ghz.measure_all()
        counts = run(ghz)
        print(counts)
        plot_histogram(counts)
        """,
        """
        ghz = QuantumCircuit(3)
        ghz.h(0)
        ghz.cx(0, 1)
        ghz.cx(1, 2)
        ghz.measure_all()
        counts = run(ghz)
        print(counts)
        assert set(counts) == {"000", "111"}
        plot_histogram(counts)
        """,
    ),
    md(
        """
        ## Stretch: how big can you go?

        Write a function `ghz_circuit(n)` for any number of qubits and run it for
        n = 10. The simulator handles this easily; at around 30 qubits a laptop
        runs out of memory, because the state has $2^n$ amplitudes.
        """
    ),
    ex(
        """
        def ghz_circuit(n):
            qc = QuantumCircuit(n)
            # TODO
            qc.measure_all()
            return qc

        print(run(ghz_circuit(10)))
        """,
        """
        def ghz_circuit(n):
            qc = QuantumCircuit(n)
            qc.h(0)
            for i in range(n - 1):
                qc.cx(i, i + 1)
            qc.measure_all()
            return qc

        counts = run(ghz_circuit(10))
        print(counts)
        assert set(counts) == {"0" * 10, "1" * 10}
        """,
    ),
]

# ---------------------------------------------------------------------------
# Lab 3: noise and randomness
# ---------------------------------------------------------------------------
LAB3 = [
    md(
        """
        # Lab 3: Noise and randomness

        **Goals:** see how real hardware errors change results, and build a
        quantum random number generator.
        """
    ),
    code(INSTALL),
    code(
        HELPERS
        + dedent(
            """
            from qiskit_ibm_runtime.fake_provider import FakeManilaV2

            # A simulator that copies the measured error rates of a real 5-qubit IBM device
            noisy = AerSimulator.from_backend(FakeManilaV2())
            """
        )
    ),
    md(
        """
        ## 3.1 Ideal versus noisy

        Real qubits are disturbed by heat, stray fields and imperfect control
        pulses. The "fake backend" reproduces those error rates.
        """
    ),
    code(
        """
        bell = QuantumCircuit(2)
        bell.h(0)
        bell.cx(0, 1)
        bell.measure_all()

        ideal_counts = run(bell, shots=4000)
        noisy_counts = run(bell, shots=4000, backend=noisy)
        print("ideal:", ideal_counts)
        print("noisy:", noisy_counts)
        plot_histogram([ideal_counts, noisy_counts], legend=["ideal", "noisy"])
        """
    ),
    md(
        """
        The noisy run shows some `01` and `10`. Those outcomes are impossible in
        theory, so every one of them is an error.
        """
    ),
    md(
        """
        ## Exercise 3.1: Does noise grow with size?

        Write `success_rate(counts, good)`: the fraction of shots whose result is
        in the list `good`. Then compare GHZ states of 2, 3, 4 and 5 qubits on
        the noisy simulator.
        """
    ),
    ex(
        """
        def success_rate(counts, good):
            # TODO: return the fraction of shots whose result is in `good`
            ...

        def ghz_circuit(n):
            qc = QuantumCircuit(n)
            qc.h(0)
            for i in range(n - 1):
                qc.cx(i, i + 1)
            qc.measure_all()
            return qc

        for n in range(2, 6):
            counts = run(ghz_circuit(n), shots=4000, backend=noisy)
            print(n, "qubits:", success_rate(counts, ["0" * n, "1" * n]))
        """,
        """
        def success_rate(counts, good):
            return sum(counts.get(g, 0) for g in good) / sum(counts.values())

        def ghz_circuit(n):
            qc = QuantumCircuit(n)
            qc.h(0)
            for i in range(n - 1):
                qc.cx(i, i + 1)
            qc.measure_all()
            return qc

        rates = []
        for n in range(2, 6):
            counts = run(ghz_circuit(n), shots=4000, backend=noisy)
            rates.append(success_rate(counts, ["0" * n, "1" * n]))
            print(n, "qubits:", round(rates[-1], 3))
        assert rates[0] > rates[-1]
        """,
    ),
    md(
        """
        More qubits and more gates mean more chances for error. This is why
        today's machines are called *noisy intermediate-scale* (NISQ) devices,
        and why quantum error correction is a major research area.
        """
    ),
    md(
        """
        ## 3.2 A quantum random number generator

        A qubit in equal superposition gives a 0 or 1 that, on real hardware, no
        one can predict, even in principle. Eight qubits give a random byte.

        `memory=True` returns the result of each shot in order instead of totals.

        Caveat: on a simulator the randomness comes from an ordinary
        pseudo-random generator. The physics is only real on real hardware.
        """
    ),
    code(
        """
        def random_bits(n_bits):
            qc = QuantumCircuit(n_bits)
            qc.h(range(n_bits))
            qc.measure_all()
            result = sim.run(qc, shots=1, memory=True).result()
            return result.get_memory()[0]

        bits = random_bits(8)
        print(bits, "=", int(bits, 2))
        """
    ),
    md(
        """
        ## Exercise 3.2: Quantum dice

        Write `roll_die()` that returns a fair number from 1 to 6. Three qubits
        give 0 to 7, which is two too many. Throw those results away and roll
        again (this is called rejection sampling); taking the result modulo 6
        would make some faces more likely than others.
        """
    ),
    ex(
        """
        def roll_die():
            # TODO: use random_bits(3) and reject values that don't map to 1-6
            ...

        rolls = [roll_die() for _ in range(60)]
        print(rolls)
        """,
        """
        def roll_die():
            while True:
                value = int(random_bits(3), 2)
                if value < 6:
                    return value + 1

        rolls = [roll_die() for _ in range(60)]
        print(rolls)
        assert set(rolls) <= {1, 2, 3, 4, 5, 6}
        """,
    ),
    md(
        """
        Up next: the facilitator runs the Bell circuit on a real IBM quantum
        computer. Compare its results with the noisy simulator above.
        """
    ),
]

# ---------------------------------------------------------------------------
# Lab 4: Grover search
# ---------------------------------------------------------------------------
LAB4 = [
    md(
        """
        # Lab 4: Grover search

        **Goal:** find a marked item among four in a single query.

        Classically, with four unlabelled boxes and one prize, you need up to
        three looks. Grover's algorithm uses interference to find it with one
        query to the "oracle". For $N$ items it needs about $\\sqrt{N}$ queries
        instead of about $N$.
        """
    ),
    code(INSTALL),
    code(
        HELPERS
        + dedent(
            """
            from qiskit.quantum_info import Statevector
            """
        )
    ),
    md(
        """
        ## 4.1 The pieces

        1. **Superposition:** H on both qubits gives equal amplitude to 00, 01,
           10 and 11.
        2. **Oracle:** flips the sign of the marked state's amplitude. The
           probabilities don't change yet, so measuring now tells you nothing.
        3. **Diffuser:** reflects every amplitude about the average. The marked
           state's amplitude grows and the others cancel.

        Here is the oracle for the marked state `11`. CZ flips the sign of
        $|11\\rangle$ only.
        """
    ),
    code(
        """
        oracle_11 = QuantumCircuit(2, name="oracle")
        oracle_11.cz(0, 1)

        qc = QuantumCircuit(2)
        qc.h([0, 1])
        qc.compose(oracle_11, inplace=True)
        print(Statevector(qc))  # the |11> amplitude is now negative
        """
    ),
    code(
        """
        def diffuser():
            qc = QuantumCircuit(2, name="diffuser")
            qc.h([0, 1])
            qc.x([0, 1])
            qc.cz(0, 1)
            qc.x([0, 1])
            qc.h([0, 1])
            return qc

        def grover(oracle):
            qc = QuantumCircuit(2)
            qc.h([0, 1])
            qc.compose(oracle, inplace=True)
            qc.compose(diffuser(), inplace=True)
            qc.measure_all()
            return qc

        qc = grover(oracle_11)
        display(qc.draw("mpl"))
        counts = run(qc)
        print(counts)
        plot_histogram(counts)
        """
    ),
    md(
        """
        Every shot returns `11`: one query, certain answer.
        """
    ),
    md(
        """
        ## Exercise 4.1: Mark any state

        Write `make_oracle(marked)` that flips the sign of any two-bit state,
        for example `"01"`.

        Hint: CZ only reacts to `11`. Apply X to each qubit that should be 0 in
        the marked state, apply CZ, then undo the X gates. Remember that the
        rightmost character is qubit 0.
        """
    ),
    ex(
        """
        def make_oracle(marked):
            qc = QuantumCircuit(2, name=f"oracle {marked}")
            # TODO
            return qc

        for marked in ["00", "01", "10", "11"]:
            counts = run(grover(make_oracle(marked)))
            print(marked, "->", counts)
        """,
        """
        def make_oracle(marked):
            qc = QuantumCircuit(2, name=f"oracle {marked}")
            zeros = [i for i, bit in enumerate(reversed(marked)) if bit == "0"]
            if zeros:
                qc.x(zeros)
            qc.cz(0, 1)
            if zeros:
                qc.x(zeros)
            return qc

        for marked in ["00", "01", "10", "11"]:
            counts = run(grover(make_oracle(marked)))
            print(marked, "->", counts)
            assert counts == {marked: 1000}
        """,
    ),
    md(
        """
        ## Exercise 4.2: Grover on noisy hardware

        Run your search on the noisy simulator from Lab 3. Does the marked state
        still win?
        """
    ),
    ex(
        """
        from qiskit_ibm_runtime.fake_provider import FakeManilaV2
        noisy = AerSimulator.from_backend(FakeManilaV2())

        # TODO: run grover(make_oracle("01")) on `noisy` and plot the histogram
        """,
        """
        from qiskit_ibm_runtime.fake_provider import FakeManilaV2
        noisy = AerSimulator.from_backend(FakeManilaV2())

        counts = run(grover(make_oracle("01")), shots=4000, backend=noisy)
        print(counts)
        assert max(counts, key=counts.get) == "01"
        plot_histogram(counts)
        """,
    ),
    md(
        """
        ## Why this matters

        With two qubits the speed-up is small. For a million items, Grover needs
        about 1,000 queries where a classical search needs up to a million. The
        same amplify-the-right-answer idea appears in many quantum algorithms.
        """
    ),
]

# ---------------------------------------------------------------------------
# Lab 5: teleportation
# ---------------------------------------------------------------------------
LAB5 = [
    md(
        """
        # Lab 5: Quantum teleportation

        **Goal:** move an unknown qubit state from Alice to Bob using one shared
        Bell pair and two classical bits.

        Nothing travels faster than light: Bob's qubit is useless until the two
        classical bits arrive. And the original is destroyed, so the state is
        moved, not copied.
        """
    ),
    code(INSTALL),
    code(
        HELPERS
        + dedent(
            """
            from qiskit import ClassicalRegister, QuantumRegister
            import numpy as np
            """
        )
    ),
    md(
        """
        ## 5.1 The state to send

        Alice's qubit gets an arbitrary state from two rotations. Later we undo
        these rotations on Bob's qubit: if teleportation worked, Bob always
        measures 0.
        """
    ),
    code(
        """
        theta, phi = 1.1, 0.7   # any values work; try your own

        def prepare(qc, q):
            qc.ry(theta, q)
            qc.rz(phi, q)

        def unprepare(qc, q):
            qc.rz(-phi, q)
            qc.ry(-theta, q)
        """
    ),
    md(
        """
        ## 5.2 The protocol

        | Step | Who | What |
        |---|---|---|
        | 1 | Both | Share a Bell pair: qubit 1 for Alice, qubit 2 for Bob |
        | 2 | Alice | CNOT from her message qubit (0) to qubit 1, then H on qubit 0 |
        | 3 | Alice | Measure qubits 0 and 1, send the two bits to Bob |
        | 4 | Bob | If bit 1 is 1, apply X. If bit 0 is 1, apply Z |

        `qc.if_test(...)` applies a gate only when a measured bit has a given
        value, the way Bob reacts to Alice's message.
        """
    ),
    ex(
        """
        msg, alice, bob = QuantumRegister(1, "msg"), QuantumRegister(1, "alice"), QuantumRegister(1, "bob")
        c_alice = ClassicalRegister(2, "alice_bits")
        c_bob = ClassicalRegister(1, "bob_result")
        qc = QuantumCircuit(msg, alice, bob, c_alice, c_bob)

        prepare(qc, msg[0])
        qc.barrier()

        # Step 1: Bell pair between alice and bob
        qc.h(alice[0])
        qc.cx(alice[0], bob[0])
        qc.barrier()

        # Step 2-3: Alice's operations and measurements
        qc.cx(msg[0], alice[0])
        qc.h(msg[0])
        qc.measure(msg[0], c_alice[0])
        qc.measure(alice[0], c_alice[1])
        qc.barrier()

        # Step 4: TODO Bob's corrections
        # with qc.if_test((c_alice[1], 1)):
        #     ...

        # Check: undo the preparation, Bob should always see 0
        unprepare(qc, bob[0])
        qc.measure(bob[0], c_bob[0])

        display(qc.draw("mpl"))
        counts = run(qc, shots=2000)
        print(counts)
        """,
        """
        msg, alice, bob = QuantumRegister(1, "msg"), QuantumRegister(1, "alice"), QuantumRegister(1, "bob")
        c_alice = ClassicalRegister(2, "alice_bits")
        c_bob = ClassicalRegister(1, "bob_result")
        qc = QuantumCircuit(msg, alice, bob, c_alice, c_bob)

        prepare(qc, msg[0])
        qc.barrier()

        # Step 1: Bell pair between alice and bob
        qc.h(alice[0])
        qc.cx(alice[0], bob[0])
        qc.barrier()

        # Step 2-3: Alice's operations and measurements
        qc.cx(msg[0], alice[0])
        qc.h(msg[0])
        qc.measure(msg[0], c_alice[0])
        qc.measure(alice[0], c_alice[1])
        qc.barrier()

        # Step 4: Bob's corrections
        with qc.if_test((c_alice[1], 1)):
            qc.x(bob[0])
        with qc.if_test((c_alice[0], 1)):
            qc.z(bob[0])

        # Check: undo the preparation, Bob should always see 0
        unprepare(qc, bob[0])
        qc.measure(bob[0], c_bob[0])

        display(qc.draw("mpl"))
        counts = run(qc, shots=2000)
        print(counts)
        """,
    ),
    md(
        """
        ## 5.3 Reading the results

        Each key reads `bob_result alice_bits`. Alice's two bits are random
        (all four combinations appear), but Bob's bit, the leftmost, should be 0
        in every shot.
        """
    ),
    ex(
        """
        bob_ones = sum(n for key, n in counts.items() if key.split()[0] == "1")
        print("Shots where Bob measured 1:", bob_ones)
        """,
        """
        bob_ones = sum(n for key, n in counts.items() if key.split()[0] == "1")
        print("Shots where Bob measured 1:", bob_ones)
        assert bob_ones == 0
        """,
    ),
    md(
        """
        ## Exercise 5.1: Skip the corrections

        Comment out Bob's corrections and run again. How often does Bob measure
        1 now? What does that say about using entanglement without the classical
        message?
        """
    ),
    md(
        """
        ## Summary

        - Teleportation moves a state using entanglement plus two classical bits.
        - Without the classical bits, Bob's qubit is random noise, so no
          information travels faster than light.
        - The same idea underlies quantum networks and some error-correction
          schemes.

        Finished early? Try the optional BB84 notebook.
        """
    ),
]

# ---------------------------------------------------------------------------
# Lab 6: BB84 (optional)
# ---------------------------------------------------------------------------
LAB6 = [
    md(
        """
        # Optional: BB84 quantum key distribution

        **Goal:** Alice and Bob build a shared secret key, and an eavesdropper
        reveals herself through the errors she causes.

        1. Alice picks a random bit and a random basis (Z or X) and sends a qubit.
        2. Bob measures in his own random basis.
        3. They publicly compare *bases* (not bits) and keep only the positions
           where the bases matched.
        4. They compare a sample of the kept bits. Errors mean someone measured
           the qubits in transit.
        """
    ),
    code(INSTALL),
    code(
        HELPERS
        + dedent(
            """
            import random

            N = 200  # qubits Alice sends
            """
        )
    ),
    code(
        """
        def bb84_round(alice_bit, alice_basis, bob_basis, eve_basis=None):
            \"\"\"Send one qubit. Bases: 0 = Z (standard), 1 = X (Hadamard).\"\"\"
            qc = QuantumCircuit(1, 1)
            if alice_bit:
                qc.x(0)
            if alice_basis:
                qc.h(0)
            if eve_basis is not None:
                eavesdrop(qc, eve_basis)
            if bob_basis:
                qc.h(0)
            qc.measure(0, 0)
            return qc

        def eavesdrop(qc, eve_basis):
            pass  # replaced in Exercise 6.1

        def run_protocol(with_eve=False):
            alice_bits = [random.randint(0, 1) for _ in range(N)]
            alice_bases = [random.randint(0, 1) for _ in range(N)]
            bob_bases = [random.randint(0, 1) for _ in range(N)]
            eve_bases = [random.randint(0, 1) if with_eve else None for _ in range(N)]

            circuits = [bb84_round(*args) for args in zip(alice_bits, alice_bases, bob_bases, eve_bases)]
            results = sim.run(transpile(circuits, sim), shots=1, memory=True).result()
            bob_bits = [int(results.get_memory(i)[0]) for i in range(N)]

            kept = [i for i in range(N) if alice_bases[i] == bob_bases[i]]
            errors = sum(alice_bits[i] != bob_bits[i] for i in kept)
            return len(kept), errors

        kept, errors = run_protocol()
        print(f"Kept {kept} of {N} bits, errors: {errors}")
        """
    ),
    md(
        """
        With no eavesdropper there are no errors, so the kept bits form a shared
        secret key. About half of the bits survive, because the bases match
        half the time.
        """
    ),
    md(
        """
        ## Exercise 6.1: Add Eve

        Eve intercepts each qubit, measures it in her own random basis, and sends
        on what she saw. Fill in `eavesdrop`: rotate into her basis, measure,
        then rotate back so the qubit continues in her basis.
        """
    ),
    ex(
        """
        def eavesdrop(qc, eve_basis):
            # TODO: if eve_basis is 1, apply H; measure qubit 0 into bit 0;
            #       if eve_basis is 1, apply H again
            pass

        kept, errors = run_protocol(with_eve=True)
        print(f"Kept {kept} bits, errors: {errors} ({errors / kept:.0%})")
        """,
        """
        def eavesdrop(qc, eve_basis):
            if eve_basis:
                qc.h(0)
            qc.measure(0, 0)
            if eve_basis:
                qc.h(0)

        kept, errors = run_protocol(with_eve=True)
        print(f"Kept {kept} bits, errors: {errors} ({errors / kept:.0%})")
        assert 0.1 < errors / kept < 0.4
        """,
    ),
    md(
        """
        Eve guesses the wrong basis half the time, and each wrong guess gives
        Bob a random bit, so about 25% of the kept bits disagree. Alice and Bob
        compare a sample, see the errors and throw the key away. Eve cannot
        measure without leaving a trace: that is the security guarantee.
        """
    ),
]

# ---------------------------------------------------------------------------
# Facilitator: live hardware demo
# ---------------------------------------------------------------------------
DEMO = [
    md(
        """
        # Facilitator: live hardware demo

        Runs the Lab 2 Bell circuit on a real IBM quantum computer.

        **Before the workshop**
        - Add your IBM Quantum API key as a Colab secret named `IBM_QUANTUM_TOKEN`
          (or set the `IBM_QUANTUM_TOKEN` environment variable when running locally).
        - Run this notebook the day before and write down the job ID as a backup.
        - Rehearse with `USE_FAKE = True`, which uses a local noisy simulator and
          needs no account.
        """
    ),
    code(INSTALL),
    code(
        """
        USE_FAKE = False        # True = rehearse offline with a simulated device
        BACKUP_JOB_ID = ""      # paste the job ID from your day-before run
        """
    ),
    code(
        """
        import os, warnings
        from qiskit import QuantumCircuit
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
        from qiskit.visualization import plot_histogram
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

        # SamplerV2 is deprecated in qiskit-ibm-runtime 0.50+ but still works with the pinned version
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        def get_token():
            try:
                from google.colab import userdata
                return userdata.get("IBM_QUANTUM_TOKEN")
            except ImportError:
                return os.environ["IBM_QUANTUM_TOKEN"]

        if USE_FAKE:
            from qiskit_ibm_runtime.fake_provider import FakeManilaV2
            backend = FakeManilaV2()
        else:
            service = QiskitRuntimeService(channel="ibm_quantum_platform", token=get_token())
            backend = service.least_busy(operational=True, simulator=False)
        print("Backend:", backend.name, "-", backend.num_qubits, "qubits")
        """
    ),
    code(
        """
        bell = QuantumCircuit(2)
        bell.h(0)
        bell.cx(0, 1)
        bell.measure_all()

        # Rewrite the circuit into the device's native gates and physical qubits
        isa = generate_preset_pass_manager(backend=backend, optimization_level=1).run(bell)
        print("Gates after transpiling:", dict(isa.count_ops()))
        """
    ),
    code(
        """
        job = Sampler(mode=backend).run([isa], shots=1000)
        print("Job ID:", job.job_id())
        """
    ),
    md(
        """
        The next cell waits for the job. If the queue is long, interrupt it and
        show the backup job instead.
        """
    ),
    code(
        """
        counts = job.result()[0].data.meas.get_counts()
        print(counts)
        plot_histogram(counts, title=f"Bell state on {backend.name}")
        """
    ),
    code(
        """
        # Backup: results from the day-before run
        if BACKUP_JOB_ID and not USE_FAKE:
            old = service.job(BACKUP_JOB_ID)
            backup_counts = old.result()[0].data.meas.get_counts()
            print(old.backend().name, backup_counts)
            display(plot_histogram(backup_counts, title="Backup run"))
        """
    ),
]

LABS = {
    "00_setup.ipynb": (LAB0, False),
    "01_one_qubit.ipynb": (LAB1, True),
    "02_entanglement.ipynb": (LAB2, True),
    "03_noise_and_randomness.ipynb": (LAB3, True),
    "04_grover_search.ipynb": (LAB4, True),
    "05_teleportation.ipynb": (LAB5, True),
    "06_bb84_optional.ipynb": (LAB6, True),
}


def build(cells, folder, name, solution):
    nb_cells = []
    for i, cell in enumerate(cells):
        kind = cell[0]
        if kind == "md":
            text = cell[1]
            if i == 0:
                text += "\n\n" + badge(folder, name)
                if solution:
                    text += "\n\n**Solution notebook.**"
            nb_cells.append(new_markdown_cell(text))
        elif kind == "code":
            nb_cells.append(new_code_cell(cell[1]))
        else:
            nb_cells.append(new_code_cell(cell[2] if solution else cell[1]))
    nb = new_notebook(cells=nb_cells)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["colab"] = {"provenance": []}
    return nb


def main():
    for name, (cells, has_solution) in LABS.items():
        out = ROOT / "notebooks" / name
        out.parent.mkdir(exist_ok=True)
        nbformat.write(build(cells, "notebooks", name, False), out)
        if has_solution:
            out = ROOT / "solutions" / name
            out.parent.mkdir(exist_ok=True)
            nbformat.write(build(cells, "solutions", name, True), out)
    out = ROOT / "facilitator" / "hardware_demo.ipynb"
    out.parent.mkdir(exist_ok=True)
    nbformat.write(build(DEMO, "facilitator", out.name, False), out)
    print("Notebooks written to", ROOT / "notebooks", "and", ROOT / "solutions")


if __name__ == "__main__":
    main()
