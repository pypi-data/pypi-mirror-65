"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
from abc import ABCMeta, abstractmethod
import logging
from typing import Iterable, Mapping, Optional, Union

from gs_quant.base import PricingKey
from gs_quant.risk import ErrorValue, Formatters, RiskRequest


_logger = logging.getLogger(__name__)


class RiskApi(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def calc(cls, request: RiskRequest) -> Union[Iterable, str]:
        raise NotImplementedError('Must implement calc')

    @classmethod
    @abstractmethod
    def get_results(cls, ids_to_requests: Mapping[str, RiskRequest], poll: bool, timeout: Optional[int] = None)\
            -> Mapping[str, dict]:
        raise NotImplementedError('Must implement get_results')

    @classmethod
    def _handle_results(cls, request: RiskRequest, results: Iterable) -> dict:
        formatted_results = {}

        pricing_key = PricingKey(
            request.pricing_and_market_data_as_of,
            request.pricing_location.value,
            request.parameters,
            request.scenario
        )

        for measure_idx, position_results in enumerate(results):
            risk_measure = request.measures[measure_idx]
            formatter = Formatters.get(risk_measure) if not request.parameters.raw_results else None
            for position_idx, result in enumerate(position_results):
                position = request.positions[position_idx]

                try:
                    result = formatter(result, pricing_key, position.instrument) if formatter else result
                except Exception as e:
                    error_string = str(e)
                    result = ErrorValue(pricing_key, error_string)
                    _logger.error(error_string)

                formatted_results.setdefault(risk_measure, {})[position] = result

        return formatted_results
