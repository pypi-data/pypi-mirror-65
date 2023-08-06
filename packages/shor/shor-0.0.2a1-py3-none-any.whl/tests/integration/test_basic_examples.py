
    # Accounting for random noise, results won't be exact
    assert result.counts.get(bin(0)) > 450
    assert result.counts.get(bin(1)) > 450


def test_entanglement():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(Hadamard(0))
    circuit.add(CNOT(0, 1))
    circuit.add(Measure(0, 1))

    sess = QSession(backend=QuantumSimulator())
    result = sess.run(circuit, num_shots=1024)

    # Accounting for random noise, results won't be exact
    # For result index:
    #     - int('10',2)
    #     - 0b10
    #     - 2
    # are all equivalant ways to get the index for '|10>'
    assert result.counts.get(bin(1)) == 0
    assert result.counts.get(0b10) == 0
    assert result.counts.get('00') > 450
    assert result.counts.get(3) > 450


def test_unitary_symmetry_does_nothing():
    symmetric_circuit_1 = Circuit()
    symmetric_circuit_1.add(Qubits(2))
    symmetric_circuit_1.add(Hadamard(0))
    symmetric_circuit_1.add(Hadamard(0))
    symmetric_circuit_1.add(CNOT(0, 1))
    symmetric_circuit_1.add(CNOT(0, 1))
    symmetric_circuit_1.add(Measure(0, 1))

    symmetric_circuit_2 = Circuit()
    symmetric_circuit_2.add(Qubits(2, state=1))
    symmetric_circuit_2.add(Hadamard(0))
    symmetric_circuit_2.add(CNOT(0, 1))
    symmetric_circuit_2.add(CNOT(0, 1))
    symmetric_circuit_2.add(Hadamard(0))
    symmetric_circuit_2.add(Measure(0, 1))

    sess = QSession(backend=QuantumSimulator())
    result_1 = sess.run(symmetric_circuit_1, num_shots=1024)
    result_2 = sess.run(symmetric_circuit_2, num_shots=1024)

    assert result_1.counts.get(0) == 1024
    assert result_2.counts.get(3) == 1024
