import argparse
from rich.console import Console
from rich.table import Table

from retrieve_file.database import create_database
from retrieve_file.scanner import scan_folder
from retrieve_file.vector_store import build_index
from retrieve_file.semantic_search import (
    semantic_search,
    group_by_project
)

def main():
    parser = argparse.ArgumentParser(
        description="AI-powered semantic file retriever"
    )

    parser.add_argument(
        "command",
        choices=["index", "search"],
        help="Choose index or search"
    )

    parser.add_argument(
        "value",
        help="Folder path for indexing or query for searching"
    )

    args = parser.parse_args()

    if args.command == "index":
        try:
            create_database()
            scan_folder(args.value)
            build_index()
            
        except(FileNotFoundError, NotADirectoryError, ValueError) as e:
            parser.error(str(e))

    elif args.command == "search":
        query = args.value.strip()

        if not query:
            parser.error("Search query cannot be empty")

        try:
            results = semantic_search(args.value, top_k=5)
        except (FileNotFoundError, ValueError) as e:
            parser.error(str(e))

        projects = group_by_project(results)

        # for project in projects:
        #     print(f"\nProject: {project['project_name']}")
        #     print(f"Location: {project['project_path']}")
        #     print(f"Cosine Similarity: {project['score']:.4f}")

        #     for file in project["files"]:
        #         print(f" -{file['name']}")
        console = Console()

        table = Table(title="FileRetriever — Search Results")

        table.add_column("Project", style="cyan")
        table.add_column("Filename", style="green")
        table.add_column("Cosine Similarity", justify="right")
        table.add_column("Location", style="dim")

        for project in projects:
            for file in project["files"]:
                table.add_row(
                    project["project_name"],
                    file["name"],
                    f'{file["score"]:.4f}',
                    file["path"]
                )

        console.print()
        console.print(f"[bold]Search query:[/bold] {query}")
        console.print(table)

if __name__ == "__main__":
    main()