from typing import Dict, List, Sequence, Union

import torch


class Metric:
    """
    A very general abstract class representing a metric which can be
    accumulated.
    """

    NAMES: List[str] = []

    def __call__(self, predictions: torch.Tensor, gold_labels: torch.Tensor) -> None:
        """
        Parameters
        ----------
        predictions : ``torch.Tensor``, required.
            A tensor of predictions.
        gold_labels : ``torch.Tensor``, required.
            A tensor corresponding to some gold label to evaluate against.
        """
        raise NotImplementedError

    def get_metric(self, reset: bool) -> Dict[str, Union[float, List[float]]]:
        """
        Compute and return the metric. Optionally also call :func:`self.reset`.
        """
        raise NotImplementedError

    def reset(self) -> None:
        """
        Reset any accumulators or internal state.
        """
        raise NotImplementedError

    @staticmethod
    def unwrap_to_tensors(*tensors: torch.Tensor) -> Sequence[torch.Tensor]:
        """
        If you actually passed gradient-tracking Tensors to a Metric, there will be
        a huge memory leak, because it will prevent garbage collection for the computation
        graph. This method ensures that you're using tensors directly and that they are on
        the CPU.
        """
        return [x.detach().cpu() if isinstance(x, torch.Tensor) else x for x in tensors]
