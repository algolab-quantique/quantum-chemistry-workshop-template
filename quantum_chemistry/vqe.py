# %%
import numpy as np
from qiskit.circuit import Parameter, QuantumCircuit

from quantum_chemistry.estimation import estimate_observable_expectation_value


def h2_ansatz_circuit() -> QuantumCircuit:
    """
    The simplest Ansatz for the H2 molecule, preparing a state with only two basis state (0101 and 1010)

    Returns:
        QuantumCircuit: The state circuit ansatz
    """

    param_a = Parameter("a")

    ansatz_circuit = QuantumCircuit(4)
    ansatz_circuit.x(0)
    ansatz_circuit.ry(param_a, 1)
    ansatz_circuit.cx(1, 0)
    ansatz_circuit.cx(0, 2)
    ansatz_circuit.cx(1, 3)

    return ansatz_circuit


def minimize_expectation_value(hamiltonian, ansatz_circuit, backend, minimizer, starting_params=None):

    def cost_function(params):

        state_circuit = ansatz_circuit.assign_parameters(params)
        hamiltonian_expectation_value = estimate_observable_expectation_value(hamiltonian, state_circuit, backend)

        return hamiltonian_expectation_value.real

    if starting_params is None:
        starting_params = np.zeros(len(ansatz_circuit.parameters))

    minimization_result = minimizer(cost_function, starting_params)

    return minimization_result
