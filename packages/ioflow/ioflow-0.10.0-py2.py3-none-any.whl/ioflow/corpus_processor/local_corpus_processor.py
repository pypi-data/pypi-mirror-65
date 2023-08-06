import functools

import numpy as np
from tokenizer_tools.tagset.offset.corpus import Corpus

from ioflow.corpus_processor.corpus_processor_base import CorpusProcessorBase


def generator_fn(input_file):
    return Corpus.read_from_file(input_file)


class LocalCorpusProcessor(CorpusProcessorBase):
    def __init__(self, config):
        super(LocalCorpusProcessor, self).__init__(config)

    def prepare(self):
        self.dataset_mapping[self.TRAIN] = functools.partial(
            generator_fn, self.config["train"]
        )
        self.dataset_mapping[self.EVAL] = functools.partial(
            generator_fn, self.config["test"]
        )

        self.meta_info = {
            "tags": np.loadtxt(
                self.config["tags"], dtype=np.unicode, encoding=None
            ).tolist()
            if self.config.get("tags")
            else None,
            "labels": np.loadtxt(
                self.config["labels"], dtype=np.unicode, encoding=None
            ).tolist()
            if self.config.get("labels")
            else None,
        }
