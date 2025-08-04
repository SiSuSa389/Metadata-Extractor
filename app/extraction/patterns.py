import spacy
from spacy.matcher import Matcher
from typing import List, Tuple


class PatternMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        self._setup_patterns()

    def _setup_patterns(self):
        # Date patterns (various common date formats)
        date_patterns = [
            [
                {"SHAPE": "dddd"},
                {"TEXT": "-"},
                {"SHAPE": "dd"},
                {"TEXT": "-"},
                {"SHAPE": "dd"},
            ],  # 2025-07-28
            [
                {"SHAPE": "dd"},
                {"TEXT": "/"},
                {"SHAPE": "dd"},
                {"TEXT": "/"},
                {"SHAPE": "dddd"},
            ],  # 28/07/2025
            [
                {"POS": "PROPN", "IS_TITLE": True},
                {"SHAPE": "dd"},
                {"TEXT": ","},
                {"SHAPE": "dddd"},
            ],  # July 28, 2025
            [
                {"SHAPE": "dd"},
                {"POS": "PROPN", "IS_TITLE": True},
                {"SHAPE": "dddd"},
            ],  # 28 July 2025
            [{"POS": "PROPN", "IS_TITLE": True}, {"SHAPE": "dddd"}],  # July 2025
            [{"SHAPE": "dddd"}],  # Year only
        ]

        # Key term patterns (domain-specific)
        key_term_patterns = [
            [{"LOWER": "machine"}, {"LOWER": "learning"}],
            [{"LOWER": "artificial"}, {"LOWER": "intelligence"}],
            [{"LOWER": "natural"}, {"LOWER": "language"}, {"LOWER": "processing"}],
            [{"LOWER": "deep"}, {"LOWER": "learning"}],
            [{"LOWER": "neural"}, {"LOWER": "network"}],
            [{"LOWER": "data"}, {"LOWER": "science"}],
            [{"LOWER": "computer"}, {"LOWER": "vision"}],
            [{"LOWER": "reinforcement"}, {"LOWER": "learning"}],
            [{"LOWER": "supervised"}, {"LOWER": "learning"}],
            [{"LOWER": "unsupervised"}, {"LOWER": "learning"}],
            [{"LOWER": "big"}, {"LOWER": "data"}],
            [{"LOWER": "data"}, {"LOWER": "mining"}],
            [{"LOWER": "predictive"}, {"LOWER": "analytics"}],
            [{"LOWER": "statistical"}, {"LOWER": "analysis"}],
            [{"LOWER": "regression"}, {"LOWER": "analysis"}],
            [{"LOWER": "classification"}],
            [{"LOWER": "clustering"}],
            [{"LOWER": "cloud"}, {"LOWER": "computing"}],
            [{"LOWER": "blockchain"}],
            [{"LOWER": "internet"}, {"LOWER": "of"}, {"LOWER": "things"}],
            [{"LOWER": "cybersecurity"}],
            [{"LOWER": "software"}, {"LOWER": "engineering"}],
            [{"LOWER": "digital"}, {"LOWER": "transformation"}],
            [{"LOWER": "business"}, {"LOWER": "intelligence"}],
            [{"LOWER": "enterprise"}, {"LOWER": "resource"}, {"LOWER": "planning"}],
            [{"LOWER": "customer"}, {"LOWER": "relationship"}, {"LOWER": "management"}],
            [{"LOWER": "research"}, {"LOWER": "methodology"}],
            [{"LOWER": "literature"}, {"LOWER": "review"}],
            [{"LOWER": "case"}, {"LOWER": "study"}],
            [{"LOWER": "empirical"}, {"LOWER": "analysis"}],
            [{"LOWER": "quantitative"}, {"LOWER": "research"}],
            [{"LOWER": "qualitative"}, {"LOWER": "research"}],
        ]

        self.matcher.add("DATE_PATTERN", date_patterns)
        self.matcher.add("KEY_TERM", key_term_patterns)

    def extract_patterns(self, text: str) -> Tuple[List[str], List[str]]:
        doc = self.nlp(text)
        matches = self.matcher(doc)
        dates = set()
        key_terms = set()

        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            span_text = doc[start:end].text

            if label == "DATE_PATTERN":
                dates.add(span_text)
            elif label == "KEY_TERM":
                key_terms.add(span_text.lower())

        return sorted(list(dates)), sorted(list(key_terms))
