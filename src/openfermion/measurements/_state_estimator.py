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

"""Estimators for sets of expectation values of quantum states"""
"""i.e. for when estimating with a VQE etc"""
from openfermion.measurements import Estimator
from openfermion.ops import QubitOperator


class StateEstimator(Estimator):
    """abstract state estimator class - estimates a quantum
    state as a QubitOperator object, and parses ShotData
    input.

    attributes:
        qubits (tuple): ordered list of qubits
        evs (QubitOperator): expectation values
            of corresponding QubitOperator terms
        vars (QubitOperator): variances in estimates
            of corresponding QubitOperator terms
        terms (tuple): terms to estimate
    """

    def __init__(self, qubits, terms):
        """
        vars:
            qubits (tuple): ordered list of qubits
            terms (tuple or QubitOperator): terms to estimate
                if QubitOperator, takes all terms present in
                operator
        """
        self.qubits = tuple(qubits)
        self.evs = QubitOperator()
        self.vars = QubitOperator()
        if isinstance(terms, QubitOperator):
            self.terms = tuple(terms.terms.keys())
        else:
            self.terms = terms

    def update(self, shots):
        """Updates with data from shots, assuming that data
        distribution is well-approximated by a normal distribution
        

        vars:
            shots (ShotData): shots to be updated. Needs to
                contain metadata for the PauliString that was
                measured.

        raises:
        """
        if 'PauliString' not in shots.meta:
            raise ValueError('Shot data does not contain PauliString')
        num_shots = sum(shots.values())

        for term in self.terms:
            try:
                indices = self.get_indices(term, shots)
            except LookupError:
                continue
            temp_ev, temp_var = shots.get_ev_var(indices)
            if term not in self.evs:
                self.evs[term] = temp_ev
                self.vars[term] = temp_var
                continue
            old_ev = self.evs[term]
            old_var = self.vars[term]
            sum_var = old_var+temp_var
            new_ev = (old_ev*temp_var+temp_ev*old_var)/sum_var
            new_var = temp_var*old_var/sum_var
            self.evs[term] = new_ev
            self.vars[term] = new_var
