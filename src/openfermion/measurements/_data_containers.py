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
"""
Classes for data storage.
"""
from collections import Counter


class ShotData(Counter):
    '''A ShotData container is a counter
    of the various shots recorded (in big endian order),
    as well as a list of the qubit order and a dictionary
    for any metadata.

    Attributes:
        qubits (tuple) : a list of the labels of the qubits, in order.
        meta (dic) : any metadata associated with the experiment
    '''

    def __init__(self, qubits, meta=None, **kwargs):
        super().__init__(**kwargs)
        self.qubits = tuple(qubits)
        self.meta = meta if meta else {}
