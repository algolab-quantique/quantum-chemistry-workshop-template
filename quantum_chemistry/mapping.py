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

    ################################################################################################################
    # YOUR CODE HERE
    # TO COMPLETE
    ################################################################################################################

    raise NotImplementedError

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

    raise NotImplementedError


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

    raise NotImplementedError


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

    raise NotImplementedError
