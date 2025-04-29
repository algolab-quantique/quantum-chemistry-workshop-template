import numpy as np

from quantum_chemistry.mapping import creation_annihilation_operators_with_jordan_wigner
from quantum_chemistry.pauli import Operator


def assert_zero_operator(operator: Operator):

    assert np.all(operator.coefs == 0)


def assert_identity_operator(operator: Operator):

    assert len(operator.coefs) == 1
    assert operator.coefs[0] == 1
    assert np.all(operator.paulis[0].z_bits == 0)
    assert np.all(operator.paulis[0].x_bits == 0)


def anti_commutator(operator_1: Operator, operator_2: Operator) -> Operator:

    return operator_1 * operator_2 + operator_2 * operator_1


def test_commutation_relation_with_jordan_wigner():
    """
    Test if the annihilation and creation operators respect anticommutation relations.
    """
    states = 4

    creation_operators, annihilation_operators = creation_annihilation_operators_with_jordan_wigner(states)
    creation_operators = [op.adjoint() for op in annihilation_operators]

    for i, ann_op_1 in enumerate(annihilation_operators):
        for j, ann_op_2 in enumerate(annihilation_operators[i:]):
            assert_zero_operator(anti_commutator(ann_op_1, ann_op_2).simplify())

    for i, cre_op_1 in enumerate(creation_operators):
        for j, cre_op_2 in enumerate(creation_operators[i:]):
            assert_zero_operator(anti_commutator(cre_op_1, cre_op_2).simplify())

    for i, ann_op in enumerate(annihilation_operators):
        for j, cre_op in enumerate(creation_operators):
            if i == j:
                assert_identity_operator(anti_commutator(ann_op, cre_op).simplify())
            else:
                assert_zero_operator(anti_commutator(ann_op, cre_op).simplify())
