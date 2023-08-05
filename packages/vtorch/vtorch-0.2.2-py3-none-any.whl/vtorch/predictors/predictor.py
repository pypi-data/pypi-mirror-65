from typing import Any, Callable, Dict, List, Optional

import torch

from vtorch.common.utils import sanitize
from vtorch.data import Instance
from vtorch.data.dataset_readers import DatasetReader
from vtorch.data.iterators import DataIterator
from vtorch.models import Model
from vtorch.nn import utils as nn_util


class Predictor:
    """
    a ``Predictor`` is a thin wrapper around an AllenNLP model that handles JSON -> JSON predictions
    that can be used for serving models through the web API or making predictions in bulk.
    """

    def __init__(
        self,
        model: Model,
        dataset_reader: DatasetReader,
        iterator: DataIterator,
        resort_predictions: bool = True,
        cuda_device: int = -1,
        torchscript: bool = False,
    ) -> None:
        self._model = model
        self._model.eval()
        self._dataset_reader = dataset_reader
        self._iterator = iterator
        self._iterator.index_with(self._model.vocab)
        self._resort_predictions = resort_predictions
        self._cuda_device = cuda_device
        self._torchscript = torchscript
        self._torchscript_inference: Optional[Callable[[torch.Tensor, torch.Tensor], torch.Tensor]] = None

    def _json_to_instance(self, json_dict: Dict[str, Any]) -> Instance:
        """
        Converts a JSON object into an :class:`~vtorch.data.instance.Instance`
        and a ``JsonDict`` of information which the ``Predictor`` should pass through,
        such as tokenised inputs.
        """
        raise NotImplementedError

    def predict_batch_json(self, inputs: List[Dict[str, Any]]) -> List[Any]:
        instances = self._batch_json_to_instances(inputs)
        return self.predict_batch_instance(instances)

    def predict_batch_instance(
        self, instances: List[Instance], additional_batch_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        data_iterator = self._iterator(instances, num_epochs=1, shuffle=False)
        predictions = []
        with torch.no_grad():
            for batch in data_iterator:
                batch = nn_util.move_to_device(batch, self._cuda_device)
                if additional_batch_params is not None:
                    batch.update(additional_batch_params)
                predictions.append(self._make_predictions(batch))
        sanitized_outputs = sanitize(predictions)
        unsqueezed_sanitized_outputs = []
        for batch in sanitized_outputs:
            # because we don't need to store loss
            if "loss" in batch:
                batch.pop("loss", None)
            unsqueezed_sanitized_outputs.extend(_unsqueeze_dict(batch))
        sorted_unsqueezed_sanitized_outputs = sorted(unsqueezed_sanitized_outputs, key=lambda x: x["serial_index"])
        return sorted_unsqueezed_sanitized_outputs

    def _make_predictions(self, batch: Dict[str, torch.Tensor]) -> Dict[str, Any]:
        if not self._torchscript:
            return self._model(**batch)
        if self._torchscript_inference is None:
            self._torchscript_inference = torch.jit.trace(  # type: ignore
                self._model, (batch["text"], batch["sequence_length"]),
            )
        batch_predictions = self._torchscript_inference(batch["text"], batch["sequence_length"])
        return self._model.postprocess_output(batch_predictions, batch["serial_index"])

    def _batch_json_to_instances(self, json_dicts: List[Dict[str, Any]]) -> List[Instance]:
        """
        Converts a list of JSON objects into a list of :class:`~vtorch.data.instance.Instance`s.
        By default, this expects that a "batch" consists of a list of JSON blobs which would
        individually be predicted by :func:`predict_json`. In order to use this method for
        batch prediction, :func:`_json_to_instance` should be implemented by the subclass, or
        if the instances have some dependency on each other, this method should be overridden
        directly.
        """
        instances = []
        for json_dict in json_dicts:
            instances.append(self._json_to_instance(json_dict))
        return instances

    def predict(self, inputs: List[Dict[str, Any]]) -> Any:
        raise NotImplementedError


def _unsqueeze_dict(dictionary_item: Dict[Any, Any]) -> List[Dict[Any, Any]]:
    to_right_d_values = [_unsqueeze_dict(v) if isinstance(v, dict) else v for v in dictionary_item.values()]
    return [dict(zip(dictionary_item, v)) for v in zip(*to_right_d_values)]
