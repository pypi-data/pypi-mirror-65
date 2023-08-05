from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional

import torch

from vtorch.training.metrics import Metric


class ModelParams:
    _FIELDS_TO_DELETE_BEFORE_SAVING: List[str] = ["metrics", "loss"]

    def __init__(
        self,
        transformer_model_name: str,
        head_dropout: float,
        activation: Callable[[torch.Tensor], torch.Tensor],
        loss: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
        metrics: Optional[Dict[str, Metric]] = None,
        torchscript: bool = False,
    ) -> None:
        self.transformer_model_name = transformer_model_name
        self.head_dropout = head_dropout
        self.activation = activation
        self.metrics = metrics
        self.loss = loss
        self.torchscript = torchscript

    def get_attributes_as_dict(self) -> Dict[str, Any]:
        """save just values, without objects (we don't need to import any modules)"""
        model_params = deepcopy(self.__dict__)
        for arg in self._FIELDS_TO_DELETE_BEFORE_SAVING:
            model_params.pop(arg, None)
        return model_params
