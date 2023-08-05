"""
:py:class:`Model` is an abstract class representing
a Transformers model.
"""

import logging
import os
from typing import Any, Dict, Optional, Type, TypeVar

import torch
from transformers import AutoConfig, AutoModel, PreTrainedModel

from ..data import Vocabulary
from ..nn import utils
from ..training.metrics.metric import Metric
from .model_parameters import ModelParams

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# When training a model, many sets of weights are saved. By default we want to
# save/load this set of weights.
_DEFAULT_WEIGHTS = "model.th"

T = TypeVar("T", bound="Model")


class Model(torch.nn.Module):  # type: ignore
    """
    This abstract class represents a model to be trained. Rather than relying completely
    on the Pytorch Module, we modify the output spec of ``forward`` to be a dictionary.
    Models built using this API are still compatible with other pytorch models and can
    be used naturally as modules within other models - outputs are dictionaries, which
    can be unpacked and passed into other layers. One caveat to this is that if you
    wish to use an AllenNLP model inside a Container (such as nn.Sequential), you must
    interleave the models with a wrapper module which unpacks the dictionary into
    a list of tensors.
    In order for your model to be trained using the :class:`~allennlp.training.Trainer`
    api, the output dictionary of your Model must include a "loss" key, which will be
    optimised during the training process.
    Finally, you can optionally implement :func:`Model.get_metrics` in order to make use
    of early stopping and best-model serialization based on a validation metric in
    :class:`~vtorch.training.Trainer`. Metrics that begin with "_" will not be logged
    to the progress bar by :class:`~vtorch.training.Trainer`.
    """

    MODEL_NAME = "default"

    def __init__(
        self,
        transformer: PreTrainedModel,
        vocab: Vocabulary,
        model_params: ModelParams,
        labels_namespace: Any = "labels",
    ) -> None:
        super().__init__()
        self._transformer = transformer
        self._transformer_output_size = (
            self._transformer.config.emb_dim
            if hasattr(self._transformer.config, "emb_dim")
            else self._transformer.config.hidden_size
        )
        self.vocab = vocab
        self._model_params = model_params
        self.labels_namespace = labels_namespace
        self.metrics: Optional[Dict[str, Metric]] = None

    def forward(self, *args: Any, **kwargs: Any) -> Dict[str, torch.Tensor]:  # type: ignore
        """
        Defines the forward pass of the model. In addition, to facilitate easy training,
        this method is designed to compute a loss function defined by a user.
        The input is comprised of everything required to perform a
        training update, `including` labels - you define the signature here!
        It is down to the user to ensure that inference can be performed
        without the presence of these labels. Hence, any inputs not available at
        inference time should only be used inside a conditional block.
        The intended sketch of this method is as follows::
            def forward(self, input1, input2, targets=None):
                ....
                ....
                output1 = self.layer1(input1)
                output2 = self.layer2(input2)
                output_dict = {"output1": output1, "output2": output2}
                if targets is not None:
                    # Function returning a scalar torch.Tensor, defined by the user.
                    loss = self._compute_loss(output1, output2, targets)
                    output_dict["loss"] = loss
                return output_dict
        Parameters
        ----------
        inputs:
            Tensors comprising everything needed to perform a training update, `including` labels,
            which should be optional (i.e have a default value of ``None``).  At inference time,
            simply pass the relevant inputs, not including the labels.
        Returns
        -------
        output_dict: ``Dict[str, torch.Tensor]``
            The outputs from the model. In order to train a model using the
            :class:`~allennlp.training.Trainer` api, you must provide a "loss" key pointing to a
            scalar ``torch.Tensor`` representing the loss to be optimized.
        """
        raise NotImplementedError

    def postprocess_output(
        self,
        logits: torch.Tensor,
        serial_index: Optional[torch.Tensor] = None,
        additional_output: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Takes the result of :func:`forward` and runs inference / decoding / whatever
        post-processing you need to do your model.  The intent is that ``model.forward()`` should
        produce potentials or probabilities, and then ``model.decode()`` can take those results and
        run some kind of beam search or constrained inference or whatever is necessary.  This does
        not handle all possible decoding use cases, but it at least handles simple kinds of
        decoding.
        This method `modifies` the input dictionary, and also `returns` the same dictionary.
        By default in the base class we do nothing.  If your model has some special decoding step,
        override this method.
        """

        output = dict() if additional_output is None else additional_output.copy()
        output["logits"] = logits
        if serial_index is not None:
            output["serial_index"] = serial_index
        return output

    def get_metrics(self, reset: bool = False) -> Dict[str, float]:
        """
        Returns a dictionary of metrics. This method will be called by
        :class:`vtorch.training.Trainer` in order to compute and use model metrics for early
        stopping and model serialization.  We return an empty dictionary here rather than raising
        as it is not required to implement metrics for a new model.  A boolean `reset` parameter is
        passed, as frequently a metric accumulator will have some state which should be reset
        between epochs. This is also compatible with :class:`~vtorch.training.Metric`s. Metrics
        should be populated during the call to ``forward``, with the
        :class:`~vtorch.training.Metric` handling the accumulation of the metric until this
        method is called.
        """
        # pylint: disable=unused-argument,no-self-use
        return {}

    @classmethod
    def load(
        cls: Type[T],
        model_params: ModelParams,
        serialization_dir: str,
        weights_file: Optional[str] = None,
        cuda_device: int = -1,
        **kwargs: Any,
    ) -> T:
        """
        Instantiates an already-trained model, based on the experiment
        configuration and some optional overrides.
        """
        weights_file = weights_file or os.path.join(serialization_dir, _DEFAULT_WEIGHTS)

        vocab = Vocabulary.from_files(os.path.join(serialization_dir, "vocabulary"))

        config = AutoConfig.from_pretrained(serialization_dir)

        model = cls(transformer=AutoModel.from_config(config), vocab=vocab, model_params=model_params,)
        model_state = torch.load(  # type: ignore
            weights_file, map_location=utils.device_mapping(cuda_device)
        )
        model.load_state_dict(model_state, strict=False)
        cls._model_to_device(model, cuda_device)

        return model

    @classmethod
    def _model_to_device(cls: Type[T], model: T, cuda_device: int) -> None:
        if cuda_device != -1:
            model.to(cuda_device)
        else:
            model.cpu()

    @classmethod
    def from_config(cls: Type[T], config: ModelParams, vocab: Vocabulary, cuda_device: int = -1) -> T:
        model = cls(
            transformer=AutoModel.from_pretrained(config.transformer_model_name), vocab=vocab, model_params=config,
        )
        cls._model_to_device(model, cuda_device)

        return model

    def save(self, path: str) -> None:
        self.vocab.save_to_files(os.path.join(path, "vocabulary"))
        self._transformer.config.save_pretrained(path)
