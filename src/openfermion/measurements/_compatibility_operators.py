#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Tools to construct compatible operators."""

import itertools
import numpy

from openfermion.ops import QubitOperator


def _compatibility_pauli_operators(operator1, operator2):
    """
    Check the compatibility of two Pauli strings.

    Args:
        operator1 (QubitOperator or tuple): Pauli operator to compare
                if tuple it must have the structure of QubitOperator.terms
        operator2 (QubitOperator or tuple): Pauli operator to compare
                if tuple it must have the structure of QubitOperator.terms
    Return:
        (boolean): Whether the operators are compatible.

    Raises:
        TypeError: if the input is not a QubitOperator or tuple.

    Notes:
        This function assumes compatibility with a harder constrain
        than commutability.
        Operators are considered compatible if they do not share any qubit,
        or the shared qubits are acted with the same Pauli matrix.

        Additionaly it considers the identity and itself as incompatible.
    """
    if not (isinstance(operator1, (QubitOperator, tuple)) and
            isinstance(operator2, (QubitOperator, tuple))):
        raise TypeError(
            'Input Pauli operators as valid OpenFermion data structures.')
    if isinstance(operator1, QubitOperator):
        operator1 = list(operator1.terms.keys())[0]
    if isinstance(operator2, QubitOperator):
        operator2 = list(operator2.terms.keys())[0]

    if operator1 == operator2 or operator1 == () or operator2 == ():
        return False
    for (qbt1, pau1), (qbt2, pau2) in itertools.product(operator1, operator2):
        if qbt1 == qbt2 and pau1 != pau2:
            return False
    else:
        return True


def construct_adjacency_matrix(hamiltonian):
    """
    Construct the adjacency matrix of operators of a Hamiltonian.

    Args:
        hamiltonian (QubitOperator): Hamiltonian to construct the adjacency
            matrix from its Pauli operators.
            Each Pauli operator is a node of a graph in which the adjacency
            matrix represent its edges.

    Return:
        adj_matrix (numpy.ndarray): N x N matrix of 0s and 1s.
            N is the number of Pauli operators of the Hamiltonian.

    Raises:
        TypeError: if hamiltonian is not QubitOperator.

    Notes:
        In the adjacency matrix a 0 represents the incompatibility between
        the ith and jth Pauli operator.
        This functions assumes that the order of the Pauli operators in the
        Hamiltonian will not change.
    """
    if not isinstance(hamiltonian, QubitOperator):
        raise TypeError('This function takes a QubitOperator.')

    # Define the adjacency matrix
    num_ops = len(hamiltonian.terms.keys())
    adj_matrix = numpy.zeros((num_ops, num_ops), dtype=int)

    for i, term1 in enumerate(hamiltonian.terms.keys()):
        for j, term2 in enumerate(hamiltonian.terms.keys()):
            if _compatibility_pauli_operators(term1, term2):
                adj_matrix[i, j] = 1
            else:
                adj_matrix[i, j] = 0
    return adj_matrix
