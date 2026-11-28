import json
from pathlib import Path

from retrieve_file.semantic_search import semantic_search


def evaluate(dataset_path, top_k=3):
    with open(dataset_path, encoding="utf-8") as file:
        dataset = json.load(file)

    hits = 0
    positive_queries = 0
    negative_queries = 0
    correct_rejections = 0

    for item in dataset:
        query = item["query"]
        expected = set(item["expected_files"])

        # Negative queries need a rejection metric,
        # which we'll add after thresholding.
        if not expected:
            negative_queries += 1

            results = semantic_search(query, top_k=top_k)

            if not results:
                correct_rejections += 1

            continue

        positive_queries += 1

        results = semantic_search(query, top_k=top_k)

        retrieved = {
            Path(result["path"]).as_posix()
            for result in results
        }

        # Exact path matching avoids filename collisions.
        matched = any(
            actual == expected_path
            or actual.endswith("/" + expected_path)
            for actual in retrieved
            for expected_path in expected
        )

        if matched:
            hits += 1

        print(f"Query: {query}")
        print(f"Hit: {matched}")
        print("-" * 40)

    hit_rate = (
        hits / positive_queries
        if positive_queries else 0
    )

    print(f"Hit@{top_k}: {hit_rate:.2%}")
    
    rejection_rate = (
        correct_rejections / negative_queries
        if negative_queries else 0
    )

    print(f"Negative Rejection Rate: {rejection_rate:.2%}")
    
    return hit_rate


if __name__ == "__main__":
    evaluate("evaluation/queries.json")