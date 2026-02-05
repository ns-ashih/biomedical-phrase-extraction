import os
import re
from Bio import Entrez
from collections import Counter

Entrez.email = os.getenv("ENTREZ_EMAIL", "anonymous@example.com")

handle = Entrez.esearch(
    db="pubmed",
    term="cholera[Title/Abstract]",
    retmax=100
)
search_result = Entrez.read(handle)
handle.close()

pmids = search_result["IdList"]
#print("PMIDs:", pmids)

handle = Entrez.efetch(
    db="pubmed",
    id=",".join(pmids),
    rettype="abstract",
    retmode="xml"
)
records = Entrez.read(handle)
handle.close()

texts = []

for article in records["PubmedArticle"]:
    medline = article["MedlineCitation"]
    article_data = medline["Article"]

    title = article_data.get("ArticleTitle", "")
    abstract = ""
    if "Abstract" in article_data:
        abstract = " ".join(
            str(p) for p in article_data["Abstract"]["AbstractText"]
        )

    full_text = f"{title} {abstract}"
    texts.append(full_text)

    # print("\n" + "=" * 60)
    # print("PMID:", medline["PMID"])
    # print("TITLE:", title)
    # print("ABSTRACT:", abstract[:500])

def find_constructions(
    texts,
    constant="of",
    target="cholera",
    distance=0,
    window=2,
):
    """
    Find constructions where `constant` occurs `distance` tokens
    away from `target`, either on the left or the right.

    distance = number of tokens BETWEEN constant and target
    """

    counts = Counter()
    contexts = {}

    for text in texts:
        tokens = text.lower().split()
        lower = [t.lower() for t in tokens]

        for i, tok in enumerate(tokens):
            if tok != target:
                continue
            
            target_idx = i

            # ----- CASE 1: constant on the LEFT of target -----
            # pattern: constant ... target
            const_idx_left = target_idx - distance - 1
            if const_idx_left >= 0 and lower[const_idx_left] == constant.lower():
                # span from constant to target (inclusive)
                span_start = const_idx_left
                span_end = target_idx

                phrase_tokens = tokens[span_start:span_end + 1]
                phrase = " ".join(phrase_tokens)
                phrase_key = phrase.lower()

                # context window around the span
                ctx_start = max(0, span_start - window)
                ctx_end = min(len(tokens), span_end + window + 1)
                context_snippet = " ".join(tokens[ctx_start:ctx_end])

                counts[phrase_key] += 1
                contexts.setdefault(phrase_key, []).append(context_snippet)

            # ----- CASE 2: constant on the RIGHT of target -----
            # pattern: target ... constant
            const_idx_right = target_idx + distance + 1
            if const_idx_right < len(tokens) and lower[const_idx_right] == constant.lower():
                span_start = target_idx
                span_end = const_idx_right

                phrase_tokens = tokens[span_start:span_end + 1]
                phrase = " ".join(phrase_tokens)
                phrase_key = phrase.lower()

                ctx_start = max(0, span_start - window)
                ctx_end = min(len(tokens), span_end + window + 1)
                context_snippet = " ".join(tokens[ctx_start:ctx_end])

                counts[phrase_key] += 1
                contexts.setdefault(phrase_key, []).append(context_snippet)

    return counts, contexts

counts, contexts = find_constructions(
    texts,
    constant="of",
    target="cholera",
    distance=0,
    window=2,
)

print("\nTop constructions around 'of cholera':")
for phrase, freq in counts.most_common():
    print(f"{phrase!r} has {freq} hits")
    for ex in contexts[phrase]:
        print("   context:", ex)
    print()

