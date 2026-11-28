from .semantic_search import semantic_search
from .project_detector import detect_project_root


def project_search(query, search_root, top_k=3,
                   candidate_k=50, threshold=0.20):

    results = semantic_search(
        query,
        top_k=candidate_k,
        threshold=threshold
    )

    projects = {}

    for result in results:
        project_root = detect_project_root(
            result["path"], search_root
        )

        if project_root is None:
            continue

        project_path = str(project_root)

        if project_path not in projects:
            projects[project_path] = {
                "project_name": project_root.name,
                "project_path": project_path,
                "files": [],
                "score": 0.0
            }

        projects[project_path]["files"].append(result)

    for project in projects.values():
        scores = [
            file["score"]
            for file in project["files"]
        ]

        project["score"] = max(scores)

    return sorted(
        projects.values(),
        key=lambda project: project["score"],
        reverse=True
    )[:top_k]