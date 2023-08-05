"""
    The brain of IR algorithms. This module are responsible to execute one model and return the resulted
    scored document list.
"""
from typing import List

from matchup.structure.solution import Result
from matchup.structure.weighting.idf import InverseFrequency
from matchup.structure.weighting.tf import LogNormalization

from matchup.models.model import Model
from matchup.models.algorithms.vector_space import Vector

from matchup.presentation.text import Term


class NoSuchInputException(RuntimeError):
    pass


class ModelMissingParameters(RuntimeError):
    pass


class Orchestrator:

    def __init__(self, vocabulary):
        self._vocabulary = vocabulary
        self._input = List[Term]

    def search(self, model: Model = None, idf=None, tf=None) -> List[Result]:
        """
            Core function. Execute one IR model based in vocabulary and input(query)
        :param model: IR model to execute
        :param idf: IDF class to weighting IR model
        :param tf: TF class to weighting IR model
        :return: list of solution -> (document, score)
        """

        # setting algorithms IDF weighting
        self._vocabulary.tf = tf if tf is not None else LogNormalization()
        self._vocabulary.idf = idf if idf is not None else InverseFrequency()

        model = model if model else Vector()

        if self._input:
            return model.run(self._input, self._vocabulary)
        else:
            raise NoSuchInputException("You should to put some search. Try again!")

    @property
    def entry(self) -> List[Term]:
        """
            Property getter entry(user input)
        :return: user input
        """
        return self._input

    @entry.setter
    def entry(self, etr: List[Term]) -> None:
        """
            Setter attribute input.
        :param etr: input terms
        :return: None
        """
        self._input = etr

