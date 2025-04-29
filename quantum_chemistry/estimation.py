from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray
from qiskit.circuit import QuantumCircuit
from qiskit.providers import Backend
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler

from quantum_chemistry.pauli import Operator, PauliString


def bitstring_to_bits(bit_string: str) -> NDArray[np.bool]:
    """
    Convert a bitstring (str) into a numpy.ndarray of bools

    Args:
        bit_string (str): String of '0' and '1'. Little endian assumed.

    Returns:
        NDArray[np.bool_]: Array of bits as bools
    """

    bits = np.array([int(bitchar) for bitchar in reversed(bit_string)], dtype=np.bool)

    return bits


def diagonal_pauli_with_circuit(pauli: PauliString) -> Tuple[PauliString, QuantumCircuit]:
    """
    Diagonalize a Pauli string using single qubit operations. Also returns the circuit that performs this transformation.

    Args:
        pauli (PauliString): A Pauli string

    Returns:
        PauliString: A diagonal Pauli string
        QuantumCircuit: Circuit which transform the orginal Pauli into the diagonale Pauli
    """

    num_qubits = len(pauli)

    circuit = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        if pauli.x_bits[i]:
            if pauli.z_bits[i]:
                circuit.sdg(i)
            circuit.h(i)

    new_z_bits = np.logical_or(pauli.x_bits, pauli.z_bits)
    diagonal_pauli = PauliString(new_z_bits, np.zeros_like(new_z_bits))

    return diagonal_pauli, circuit


def diagonal_pauli_eigenvalue(pauli: PauliString, bits: NDArray[np.bool]) -> float:

    assert np.all(pauli.x_bits == 0)

    return np.prod(np.choose(np.mod(pauli.z_bits * bits, 2), [1, -1]))


def diagonal_pauli_expectation_value(pauli: PauliString, counts: dict) -> float:
    """
    Computes the expectation value of a digaonal Pauli string based on counts.

    Args:
        pauli (PauliString): A diagonal Pauli string
        counts (dict): Keys : basis state bitstring (ex : '1100'),
                       Values : number of times this state was obtained

    Returns:
        float: The expectation value
    """

    assert np.all(~pauli.x_bits)  # is diagonal

    weighted_count = 0
    total_count = 0
    for bitstring, count in counts.items():
        weighted_count += count * diagonal_pauli_eigenvalue(pauli, bitstring_to_bits(bitstring))
        total_count += count

    return float(weighted_count / total_count)


def prepare_estimation_circuits_and_diagonal_paulis(
    paulis: List[PauliString], state_circuit: QuantumCircuit
) -> Tuple[List[QuantumCircuit], List[PauliString]]:
    """
    Assemble the quantum circuit to be executed to compute the expectation values of all the Pauli string in paulis. Also returns the diagonal Paulis required to compute the expectation values.

    Args:
        paulis (List[PauliString]): An ensemble on Pauli string
        state_circuit (QuantumCircuit): A quantum circuit which prepare a quantum state

    Returns:
        List[QuantumCircuit]: The quantum circuits which allow to compute the expectation values of the Paulis
        List[PauliString]: The diagonal Paulis required to compute the expectation values
    """

    diagonal_paulis = list()
    estimation_circuits = list()
    for pauli in paulis:
        diagonal_pauli, diagonalizing_circuit = diagonal_pauli_with_circuit(pauli)
        diagonal_paulis.append(diagonal_pauli)
        circuit = state_circuit.copy(str(pauli)).compose(diagonalizing_circuit)
        circuit.measure_all()
        estimation_circuits.append(circuit)

    return estimation_circuits, diagonal_paulis


def estimate_paulis_expectation_values(
    paulis: List[PauliString], state_circuit: QuantumCircuit, backend: Backend
) -> NDArray[np.float64]:
    """
    Estimates the expectation values for an ensemble of Pauli strings (paulis) for a given quantum state (state_circuit) using a given backend.

    Args:
        paulis (List[PauliString]): An ensemble on Pauli string
        state_circuit (QuantumCircuit): A quantum circuit which prepare a quantum state
        backend (Backend): The backend on which the circuits will be executed
        execute_opts (dict, optional): Execution options, will be passed to the execute function.

    Returns:
        NDArray[np.float64]: The estimated expectation values
    """

    estimation_circuits, diagonal_paulis = prepare_estimation_circuits_and_diagonal_paulis(paulis, state_circuit)

    sampler = Sampler(mode=backend)
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuits = pass_manager.run(estimation_circuits)
    job = sampler.run(isa_circuits)
    results = job.result()

    expectation_values = np.zeros(len(estimation_circuits))
    for i, diagonal_pauli in enumerate(diagonal_paulis):
        counts = results[i].data.meas.get_counts()
        expectation_values[i] = diagonal_pauli_expectation_value(diagonal_pauli, counts)

    return expectation_values


def estimate_observable_expectation_value(
    observable: Operator, state_circuit: QuantumCircuit, backend: Backend
) -> float:

    paulis_expectation_values = estimate_paulis_expectation_values(observable.paulis, state_circuit, backend)

    return np.sum(observable.coefs * paulis_expectation_values)
