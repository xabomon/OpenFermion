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

"""Base classes for processing data from quantum experiments"""


class Estimator:
    """Base class for QPEEstimator and StateEstimator

    An estimator processes a set of data from a quantum processor
    to obtain an estimate of some target parameter, including
    uncertainties.

    It may contain methods for calculating the next set of
    quantum experiments to be performed.

    Attributes:
    update: a function to process a set of input data
    estimate: a function to provide an estimate of the desired quantity
    next_experiment: a function to provide details of required
        subsequent experiments
    """

    def update(self):
        ''' Updates with given data
        '''
        pass

    def estimate(self):
        ''' Returns estimate of target
        '''
        pass

    def uncertainty(self):
        ''' Returns uncertainty in estimate
        '''
        pass
