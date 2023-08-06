from pangeamt_nlp.processor.base.validator_base import ValidatorBase
from pangeamt_nlp.seg import Seg


class EndsWithPunctVal(ValidatorBase):
    NAME = "ends_with_punct_val"

    DESCRIPTION_TRAINING = """
        Checks if src and target lines both end in punctuation (.?!) and that it is the same.
    """

    DESCRIPTION_DECODING = """
        Validators do not apply to decoding.
    """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)
        self.valid_punct = ["?", "!", "."]

    def _is_valid(self, src, tgt):
        if src[-1] in self.valid_punct:
            if src[-1] == tgt[-1]:
                return True
        return False

    def validate(self, seg: Seg) -> bool:
        return self._is_valid(seg.src, seg.tgt)
