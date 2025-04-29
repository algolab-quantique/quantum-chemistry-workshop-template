# %%
from typing import Callable, Mapping, Iterable

import numpy as np
from qiskit.circuit import Parameter, QuantumCircuit
from qiskit.providers import Backend

from quantum_chemistry.pauli import Operator
from quantum_chemistry.estimation import estimate_observable_expectation_value


def h2_ansatz_circuit() -> QuantumCircuit:
    """
    The simplest Ansatz for the H2 molecule, preparing a state with only two basis state (0101 and 1010)

    Returns:
        QuantumCircuit: The state circuit ansatz
    """

    raise NotImplementedError


def minimize_expectation_value(hamiltonian: Operator, ansatz_circuit: QuantumCircuit, backend: Backend, minimizer: Callable, starting_params: Mapping[Parameter:] | Iterable = None):
    """_summary_

    Args:
        hamiltonian (Operator): Hamiltonian from which to get the expectation values
        ansatz_circuit (QuantumCircuit): Circuit that prepare the variational ansatz
        backend (Backend): The backend on which the circuits will be executed 
        minimizer (Callable): Classical optimizer that will be called as `minimizer(cost_function, starting_params)`
        starting_params (_type_, optional): Initial values of the parameters passed to optimizer. Defaults to None.
    
    Returns:
        results (Any): Results from the minimization (ex: scipy.minimize Results object)
    
    """
    raise NotImplementedError
