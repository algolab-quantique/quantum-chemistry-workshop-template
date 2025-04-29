from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

from quantum_chemistry.pauli import Operator, PauliString


def creation_annihilation_operators_with_jordan_wigner(num_states: int) -> Tuple[List[Operator], List[Operator]]:
    """
    Builds the annihilation operators as sum of two Pauli Strings for given number of fermionic states using the Jordan Wigner mapping.

    Args:
        num_states (int): Number of fermionic states.

    Returns:
        Tuple[List[Operator], List[Operator]]: The creation and annihilation operators
    """

    creation_operators = []
    annihilation_operators = []

    for i in range(num_states):
        x_str = "I" * (num_states - i - 1) + "X" + "Z" * i  # III..X..ZZ
        y_str = "I" * (num_states - i - 1) + "Y" + "Z" * i  # III..X..ZZ
        creation_operators.append(0.5 * PauliString.from_str(x_str) - 0.5j * PauliString.from_str(y_str))
        annihilation_operators.append(0.5 * PauliString.from_str(x_str) + 0.5j * PauliString.from_str(y_str))

    return creation_operators, annihilation_operators


def build_one_body_qubit_hamiltonian(
    one_body: NDArray[np.complex128],
    creation_operators: Operator,
    annihilation_operators: Operator,
) -> Operator:
    """
    Convert a one body fermionic Hamiltonian (square matrix) into a qubit Hamiltonian (Operator) given the annihilation and creation operators (Operator)

    Args:
        one_body (NDArray[np.complex128]): The matrix for the one body Hamiltonian
        annihilation_operators (Operator): Sum of two Pauli strings
        creation_operators (Operator): Sum of two Pauli strings (adjoint of annihilation_operators)

    Returns:
        Operator: The one body Hamiltonian as a sum of Pauli strings
    """

    num_qubits = one_body.shape[0]

    one_body_qubit_hamiltonian = 0 * PauliString.from_str("I" * num_qubits)

    for idx in np.ndindex(one_body.shape):
        one_body_qubit_hamiltonian += float(one_body[idx]) * creation_operators[idx[0]] * annihilation_operators[idx[1]]

    return one_body_qubit_hamiltonian


def build_two_body_qubit_hamiltonian(
    two_body: NDArray[np.complex128],
    creation_operators: Operator,
    annihilation_operators: Operator,
) -> Operator:
    """
    Convert a two body fermionic Hamiltonian (four dimensions square array) into a qubit Hamiltonian (Operator) given the annihilation and creation operators (Operator)

    Args:
        one_body (NDArray[np.complex128]): The array for the two body Hamiltonian
        annihilation_operators (Operator): Sum of two Pauli strings
        creation_operators (Operator): Sum of two Pauli strings (adjoint of annihilation_operators)

    Returns:
        Operator: The two body Hamiltonian as a sum of Pauli strings
    """

    num_qubits = two_body.shape[0]

    two_body_qubit_hamiltonian = 0 * PauliString.from_str("I" * num_qubits)

    for idx in np.ndindex(two_body.shape):
        two_body_qubit_hamiltonian += (
            float(two_body[idx])
            * creation_operators[idx[0]]
            * creation_operators[idx[1]]
            * annihilation_operators[idx[2]]
            * annihilation_operators[idx[3]]
        )

    return two_body_qubit_hamiltonian


def build_qubit_hamiltonian(
    one_body: NDArray[np.complex128],
    two_body: NDArray[np.complex128],
    creation_operators: Operator,
    annihilation_operators: Operator,
) -> Operator:
    """
    Build a qubit Hamiltonian from the one body and two body fermionic Hamiltonians.

    Args:
        one_body (NDArray[np.complex128]): The matrix for the one body Hamiltonian
        two_body (NDArray[np.complex128]): The array for the two body Hamiltonian
        annihilation_operators (Operator): Sum of two Pauli strings
        creation_operators (Operator): Sum of two Pauli strings (adjoint of annihilation_operators)

    Returns:
        Operator: The total Hamiltonian as a sum of Pauli strings
    """

    one_body_ham = build_one_body_qubit_hamiltonian(one_body, creation_operators, annihilation_operators)
    two_body_ham = build_two_body_qubit_hamiltonian(two_body, creation_operators, annihilation_operators)

    qubit_hamiltonian = (one_body_ham + 0.5 * two_body_ham).simplify().sort()

    return qubit_hamiltonian
