from __future__ import annotations

import re
from typing import Any, Dict, List, Set, Tuple

from dil.core.loader import LoadedPack
from dil.core.models import ConceptItem, TerminologyItem

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "to", "for", "of", "and", "or",
    "in", "on", "with", "what", "how", "does", "do", "can", "could", "would",
    "should", "my", "your", "their", "it", "this", "that", "affect", "about",
    "explain", "tell", "me", "i", "want", "know"
}


def tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


class IntelligenceMatcher:
    """
    Identifies relevant domain concepts, terminology, and ontology relationships
    from natural language questions.
    """

    def __init__(self, pack: LoadedPack):
        self.pack = pack

    def match(
        self,
        query: str,
        jurisdiction: str = "global",
        max_concepts: int = 5,
    ) -> Tuple[List[ConceptItem], List[TerminologyItem], Dict[str, float]]:
        if not query or not query.strip():
            raise ValueError("Query string cannot be empty")

        q_tokens = set(tokenize(query))
        q_norm = " ".join(tokenize(query))

        concept_scores: List[Tuple[float, ConceptItem]] = []
        jur_norm = jurisdiction.lower()

        # 1. Score Concepts
        for concept in self.pack.concepts:
            if concept.jurisdiction not in ("global", jur_norm):
                continue

            score = 0.0
            alias_matched = False

            # Match aliases (exact phrase hit with word boundaries)
            for alias in concept.aliases:
                alias_norm = " ".join(tokenize(alias))
                if alias_norm and re.search(rf"\b{re.escape(alias_norm)}\b", q_norm):
                    score += 5.0 + min(len(alias_norm.split()), 3) * 0.75
                    alias_matched = True

            # Concept Name Token Overlap
            name_tokens = set(tokenize(concept.name))
            overlap = q_tokens.intersection(name_tokens)
            score += 2.0 * len(overlap)

            # Definition & Key Points Overlap
            content_text = " ".join([concept.definition] + concept.key_points)
            content_tokens = set(tokenize(content_text))
            score += 0.3 * len(q_tokens.intersection(content_tokens))

            # Only accept concepts with an explicit alias match, at least 2 name tokens,
            # significant name overlap (>= 50% of concept name), or high aggregate score (>= 3.5)
            # to avoid false unigram homonym collisions.
            overlap_ratio = len(overlap) / len(name_tokens) if name_tokens else 0.0
            if alias_matched or len(overlap) >= 2 or overlap_ratio >= 0.5 or score >= 3.5:
                concept_scores.append((score, concept))

        concept_scores.sort(key=lambda x: (-x[0], x[1].id))

        selected_concepts: List[ConceptItem] = []
        scores_map: Dict[str, float] = {}
        detected_ids: Set[str] = set()

        for score, concept in concept_scores:
            if concept.id not in detected_ids:
                selected_concepts.append(concept)
                scores_map[concept.id] = round(score, 2)
                detected_ids.add(concept.id)
            if len(selected_concepts) >= max_concepts:
                break

        # 2. Relationship Expansion (1-hop)
        # If there is room in the context budget, expand top matched concepts' relationships
        for concept in list(selected_concepts[:2]):
            if len(selected_concepts) >= max_concepts:
                break
            for rel_id in concept.related:
                if len(selected_concepts) >= max_concepts:
                    break
                if rel_id not in detected_ids and rel_id in self.pack.concepts_by_id:
                    rel_item = self.pack.concepts_by_id[rel_id]
                    if rel_item.jurisdiction in ("global", jur_norm):
                        selected_concepts.append(rel_item)
                        scores_map[rel_id] = 0.5  # Fixed lower weight for ontology expansion
                        detected_ids.add(rel_id)

        # 3. Detect Relevant Terminology / Acronyms
        matched_terms: List[TerminologyItem] = []
        for term in self.pack.terminology:
            term_clean = term.term.lower()
            if term_clean in q_tokens or any(
                re.search(rf"\b{re.escape(syn.lower())}\b", q_norm) for syn in term.synonyms
            ):
                matched_terms.append(term)

        return selected_concepts, matched_terms, scores_map

