import numpy as np

from quantum_chemistry.pauli import Operator, PauliString


def test_init_pauli_string():

    z_bits = np.array([0, 1, 0, 1], dtype=bool)
    x_bits = np.array([0, 0, 1, 1], dtype=bool)
    pauli_string = PauliString(z_bits, x_bits)
    assert str(pauli_string) == "YXZI"

    z_bits = np.array([1, 0, 1, 1], dtype=bool)
    x_bits = np.array([1, 1, 0, 0], dtype=bool)
    pauli_string = PauliString(z_bits, x_bits)
    assert str(pauli_string) == "ZZXY"

    pauli_string = PauliString.from_str("YXZI")
    assert np.all(pauli_string.z_bits == np.array([0, 1, 0, 1]))
    assert np.all(pauli_string.x_bits == np.array([0, 0, 1, 1]))

    pauli_string = PauliString.from_str("YXZI")
    zx_bits = pauli_string.to_zx_bits()
    assert np.all(pauli_string.to_zx_bits() == np.array([0, 1, 0, 1, 0, 0, 1, 1]))
    assert np.all(pauli_string.to_xz_bits() == np.array([0, 0, 1, 1, 0, 1, 0, 1]))

    pauli_string = PauliString.from_str("YXZI")
    assert np.all(pauli_string.ids() == np.array([1, 0, 0, 0]))

    bits_1 = np.array([0, 1, 0, 1], dtype=bool)
    bits_2 = np.array([0, 1, 1, 1], dtype=bool)
    print(bits_1 + bits_2)
    print(np.sum(bits_1))


def test_compose():

    pauli_string_1 = PauliString.from_str("IYZZ")
    pauli_string_2 = PauliString.from_str("IIXZ")
    new_pauli_string, phase_factor = pauli_string_1 * pauli_string_2

    assert str(new_pauli_string) == "IYYI"
    assert phase_factor == 1j

    pauli_string_1 = PauliString.from_str("ZZZZ")
    pauli_string_2 = PauliString.from_str("XXXI")
    new_pauli_string, phase_factor = pauli_string_1 * pauli_string_2

    assert str(new_pauli_string) == "YYYZ"
    assert phase_factor == -1j


def test_to_matrix():

    pauli_string = PauliString.from_str("ZX")
    ref_matrix = np.array(
        [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, -1],
            [0, 0, -1, 0],
        ]
    )

    assert np.all(pauli_string.to_matrix() == ref_matrix)


def test_init_operator():

    coefs = np.array([0.5, 0.5])
    pauli_string_1 = PauliString.from_str("IIXZ")
    pauli_string_2 = PauliString.from_str("IYZZ")
    pauli_strings = np.array([pauli_string_1, pauli_string_2], dtype=PauliString)
    operator = Operator(coefs, pauli_strings)

    operator_single = 1 * PauliString.from_str("IIXZ")
    assert isinstance(operator_single, Operator)

    operator = 0.5 * pauli_string_1 + 0.5 * pauli_string_2
    assert isinstance(operator, Operator)


def test_compose_operators():

    operator_1 = 1 * PauliString.from_str("IIXZ")
    operator_2 = 1 * PauliString.from_str("IYZZ")
    new_operator = operator_1 * operator_2

    assert str(new_operator.paulis[0]) == "IYYI"
    assert new_operator.coefs[0] == -1j

