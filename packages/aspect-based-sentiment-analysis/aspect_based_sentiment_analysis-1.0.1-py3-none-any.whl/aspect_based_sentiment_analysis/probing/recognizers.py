from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import List
from typing import Tuple

import numpy as np
import numpy.ma as ma
import tensorflow as tf

from ..data_types import AspectSpan
from ..data_types import AspectRepresentation
from ..data_types import Pattern


class PatternRecognizer(ABC):
    """ The Pattern Recognizer's aim is to discover and
    name patterns which a model uses in a prediction. """

    @abstractmethod
    def __call__(
            self,
            aspect_span: AspectSpan,
            hidden_states: tf.Tensor,
            attentions: tf.Tensor,
            attention_grads: tf.Tensor
    ) -> Tuple[AspectRepresentation, List[Pattern]]:
        """ To recognize patterns, we provide detailed information about a
        prediction, including hidden states after each layer, attentions from
        each head in each layer, and attention gradients with respect to the
        model output. The Recognizer returns the `AspectRepresentation` (the
        words describing the aspect) and the most significant `Pattern`s. """


@dataclass
class AttentionPatternRecognizer(PatternRecognizer):
    """ The Attention Pattern Recognizer uses attentions and their gradients
    to discover the most significant patterns. The key idea is to use
    attention activations and scale them by their gradients (with respect to
    the model output). The language model constructs an enormous amount of
    various relations between words. However, only some of them are crucial
    in the aspect-based sentiment classification. Thanks to gradients,
    we can filter unnecessary patterns out. This heuristic is a rough
    approximation (e.g. we take the mean activation over model heads).
    Nonetheless, it gives a good intuition about how model reasoning works.

    Parameters:
        `keep_key_weights` mask weights which are under the weight
        magnitude percentile. Default is turn off.
        `information_in_patterns` returns the key patterns which coverts the
        percentile of the total information. Default 80% of weights magnitude.
    """
    keep_key_weights: int = 100
    information_in_patterns: int = 80

    def __call__(
            self,
            aspect_span: AspectSpan,
            hidden_states: tf.Tensor,
            attentions: tf.Tensor,
            attention_grads: tf.Tensor
    ) -> Tuple[AspectRepresentation, List[Pattern]]:
        interest = self.get_interest(attentions, attention_grads)
        patterns = self.get_patterns(aspect_span, interest)
        aspect = self.get_aspect_representation(aspect_span, interest)
        return aspect, patterns

    def get_interest(
            self,
            attentions: tf.Tensor,
            attention_grads: tf.Tensor
    ) -> np.ndarray:
        """ Calculate the mean of the scaled attentions over model heads,
        called the model `interest`. Mask unnecessary weights. """
        interest = (attentions * attention_grads).numpy()
        interest = np.sum(interest, axis=(0, 1))
        interest = self.mask_noise(interest, percentile=self.keep_key_weights)
        return interest

    def get_patterns(
            self,
            aspect_span: AspectSpan,
            interest: np.ndarray
    ) -> List[Pattern]:
        """ The method tries to discover the most significant patterns.
        Briefly, the model encodes needed information in the class token
        representation and use them to classify the sentiment. Throughout the
        transformer's layers, the model creates contextual word embeddings,
        which we can interpret as the word mixtures. Because of the interest
        includes a gradient part, the first row represents how particular
        mixtures, not words, of the class token representation impact to the
        prediction on average. The approximation of these word `mixtures` are
        rows of the interest matrix. Select only key patterns. """
        cls_id, text_ids, aspect_id = self.get_indices(aspect_span)
        # Note that the gradient comes from the loss function, and it is why
        # we have to change the sign to get a direction of the improvement.
        impacts = interest[cls_id, text_ids] * -1
        mixtures = np.abs(interest[text_ids, :][:, text_ids])
        impacts = self.scale(impacts)
        mixtures = self.scale(mixtures)
        key_impacts, key_mixtures = self.get_key_mixtures(
            impacts, mixtures, percentile=self.information_in_patterns)
        patterns = self.construct_patterns(
            aspect_span, key_impacts, key_mixtures)
        return patterns

    def get_aspect_representation(
            self,
            aspect_span: AspectSpan,
            interest: np.ndarray
    ) -> AspectRepresentation:
        """ The presented sentiment classification is aspect-based, so it is
        worth to know the relation between the aspect and words in the text.
        In this case, we distinguish two sets of weights. As for the other
        patterns, the `come_from` tells us how each word appeals to the
        aspect representation on average. Also, we add the `look_at` weights
        to check what it is interesting for the aspect to look at. """
        cls_id, text_ids, aspect_id = self.get_indices(aspect_span)
        come_from = np.abs(interest[aspect_id, text_ids])
        look_at = np.abs(interest[text_ids, aspect_id])
        come_from = self.scale(come_from).tolist()
        look_at = self.scale(look_at).tolist()
        aspect_representation = AspectRepresentation(
            aspect_span.text_tokens, come_from, look_at)
        return aspect_representation

    @staticmethod
    def mask_noise(interest: np.ndarray, percentile: int) -> np.ndarray:
        """ Keep the key weights which coverts the `percentile` of
        the total information (the sum of the weight magnitudes). """
        magnitudes = np.abs(interest)
        information = np.sum(magnitudes)
        increasing_magnitudes = np.sort(magnitudes.ravel())
        magnitude_sorted = increasing_magnitudes[::-1]
        cumsum = np.cumsum(magnitude_sorted)

        min_information = information * percentile / 100
        index = np.searchsorted(cumsum, min_information, 'right')
        index = index - 1 if index == len(magnitude_sorted) else index
        threshold = magnitude_sorted[index]

        mx = ma.masked_array(interest, magnitudes < threshold)
        clean_interest = mx.filled(0)
        return clean_interest

    @staticmethod
    def get_indices(aspect_span: AspectSpan) -> Tuple[int, List[int], int]:
        """ Get indices for the class token, text words, and the aspect word
        according to the BERT input structure. """
        indices = np.arange(len(aspect_span.tokens))
        cls_id, *text_ids, sep1_id, aspect_id, sep2_id = indices
        return cls_id, text_ids, aspect_id

    @staticmethod
    def scale(x: np.ndarray, epsilon: float = 1e-16) -> np.ndarray:
        """ Scale the array so that the max magnitude equals one. """
        scaled = x / np.max(np.abs(x) + epsilon)
        return scaled

    @staticmethod
    def get_key_mixtures(
            impacts: np.ndarray,
            mixtures: np.ndarray,
            percentile: int
    ) -> Tuple[List[float], List[List[float]]]:
        """ Get the most important mixtures, weights of patterns. """
        increasing_order = np.argsort(np.abs(impacts))
        order = increasing_order[::-1]
        results = []
        magnitude = 0
        total_magnitude = np.sum(np.abs(impacts))
        for i in order:
            impact = impacts[i]
            weights = mixtures[i].tolist()
            results.append((impact, weights))
            magnitude += np.abs(impact)
            if magnitude / total_magnitude * 100 >= percentile:
                key_impacts, key_mixtures = zip(*results)
                return key_impacts, key_mixtures

    @staticmethod
    def construct_patterns(
            aspect_span: AspectSpan,
            impacts: List[float],
            mixtures: List[List[float]]
    ) -> List[Pattern]:
        patterns = [Pattern(impact, aspect_span.text_tokens, weights)
                    for impact, weights in zip(impacts, mixtures)]
        return patterns
