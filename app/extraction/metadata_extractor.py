import spacy
from typing import Dict, List
from .patterns import PatternMatcher
from .text_extractor import TextExtractor
from loguru import logger


class MetadataExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.pattern_matcher = PatternMatcher()

    def extract_authors_ner(self, text: str) -> List[str]:
        doc = self.nlp(text)
        authors = set()
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.strip()
                if len(name) > 1 and not name.isnumeric():
                    authors.add(name)
        return sorted(list(authors))

    def extract_additional_entities(self, text: str) -> Dict[str, List[str]]:
        doc = self.nlp(text)
        entities = {"organizations": [], "locations": [], "dates_ner": []}
        for ent in doc.ents:
            if ent.label_ == "ORG":
                entities["organizations"].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities["locations"].append(ent.text)
            elif ent.label_ == "DATE":
                entities["dates_ner"].append(ent.text)
        return entities

    def extract_metadata(self, filename: str, content: bytes) -> Dict[str, List[str]]:
        try:
            text = TextExtractor.extract_text(filename, content)
            if not text or len(text.strip()) < 10:
                logger.warning(f"Very little text extracted from {filename}")
                return {
                    "dates": [],
                    "authors": [],
                    "key_terms": [],
                    "organizations": [],
                    "locations": [],
                }

            dates_pattern, key_terms_pattern = self.pattern_matcher.extract_patterns(
                text
            )
            authors_ner = self.extract_authors_ner(text)
            additional_entities = self.extract_additional_entities(text)

            all_dates = set(dates_pattern + additional_entities["dates_ner"])

            logger.info(
                f"Extracted from {filename}: {len(all_dates)} dates, "
                f"{len(authors_ner)} authors, {len(key_terms_pattern)} key terms"
            )

            return {
                "dates": sorted(list(all_dates)),
                "authors": authors_ner,
                "key_terms": key_terms_pattern,
                "organizations": additional_entities["organizations"],
                "locations": additional_entities["locations"],
            }
        except Exception as e:
            logger.error(f"Error extracting metadata from {filename}: {e}")
            raise ValueError(f"Failed to extract metadata: {str(e)}")
