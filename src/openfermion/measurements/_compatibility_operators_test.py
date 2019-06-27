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

"""Test for qubit_tapering_from_stabilizer model."""

import unittest

import numpy

from openfermion.ops import QubitOperator
from openfermion.measurements._compatibility_operators import (
    _compatibility_pauli_operators, construct_adjacency_matrix)


class CompatibilityTest(unittest.TestCase):
    """Compatibility operator test class."""

    def test_function_errors(self):
        """Test error of main function."""
        with self.assertRaises(TypeError):
            test_op1 = list(QubitOperator('X0 X1', 1.0))
            test_op2 = 'Z0 Z1 X2 X3'
            _compatibility_pauli_operators(test_op1, test_op2)
        with self.assertRaises(TypeError):
            construct_adjacency_matrix('X0 X1')

    def test_different_input(self):
        """Test correct result if input are tuple and QubitOperator."""
        test_op1 = QubitOperator('X0 X1', 1.0)
        qop = QubitOperator('Z2 Z3', -1.0)
        test_op2 = list(qop.terms.keys())[0]

        self.assertTrue(_compatibility_pauli_operators(test_op1,
                                                       test_op2))

    def test_equal_operator(self):
        """Test equal operator yields to False."""
        test_op1 = QubitOperator('X0 X1', 1.0)
        test_op2 = QubitOperator('X0 X1', 1.0)

        self.assertFalse(_compatibility_pauli_operators(test_op1,
                                                        test_op2))

    def test_identity_operator(self):
        """Test identity operator yields to False."""
        test_op1 = QubitOperator('X0 X1', 1.0)
        test_op2 = QubitOperator(' ', 1.0)

        self.assertFalse(_compatibility_pauli_operators(test_op1,
                                                        test_op2))
        self.assertFalse(_compatibility_pauli_operators(test_op2,
                                                        test_op1))

    def test_incompatible_operators(self):
        """Test two incompatible operators yield to False."""
        test_op1 = QubitOperator('Z0 Z1 Z2 Z3', 1.0)
        test_op2 = QubitOperator('X0 X2', 1.0)

        self.assertFalse(_compatibility_pauli_operators(test_op2,
                                                        test_op1))

    def test_compatible_operators(self):
        """Test two compatible operators yield to True."""
        test_op1 = QubitOperator('Z0 Z1', 1.0)
        test_op2 = QubitOperator('X2 Y3', 1.0)

        self.assertTrue(_compatibility_pauli_operators(test_op2,
                                                       test_op1))

    def test_adjacency_matrix_zeros(self):
        """Test non-compatible Pauli operator adjacency matrix."""
        test_ham = (QubitOperator('Z0 Z1', 1.0) +
                    QubitOperator('X0 X1', -1.0) +
                    QubitOperator('Y0 Y1', -1.0) +
                    QubitOperator(' ', 1.0))
        num_ops = len(test_ham.terms.keys())

        test_adj = construct_adjacency_matrix(test_ham)
        zero_mat = numpy.zeros((num_ops, num_ops), dtype=int)

        self.assertTrue(numpy.allclose(test_adj, zero_mat))

    def test_adjacency_matrix_ones(self):
        """Test non-compatible Pauli operator adjacency matrix."""
        test_ham = (QubitOperator('Z0 Z1', 1.0) +
                    QubitOperator('X2 X3', -1.0) +
                    QubitOperator('Y4 Y5', -1.0))
        num_ops = len(test_ham.terms.keys())

        test_adj = construct_adjacency_matrix(test_ham)
        zero_mat = numpy.zeros((num_ops, num_ops), dtype=int)

        self.assertFalse(numpy.allclose(test_adj, zero_mat))
