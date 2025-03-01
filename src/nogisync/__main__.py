import sys
from pathlib import Path

import click
from frontmatter import Frontmatter

sys.path.append("src")

from nogisync import notion  # noqa: E402


@click.command()
@click.option("--token", "-t", type=str, help="Notion API token")
@click.option("--parent-page-id", "-parentid", type=str, help="Notion parent page ID")
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True, file_okay=False, readable=True, resolve_path=True, path_type=Path),
    help="Path to the markdown files",
)
def main(token: str, parent_page_id: str, path: Path):
    """
    Sync GitHub markdown files to Notion
    """
    markdown_files = Path(path).glob("*.md")

    for md_file in markdown_files:
        # Read the markdown file
        post = Frontmatter.read_file(md_file)
        title = post.get("attributes").get("title", md_file.stem)
        content = post.get("body")

        client = notion.get_notion_client(token)

        # Check if page exists in Notion
        existing_page = notion.find_notion_page(client, title)

        if existing_page:
            print(f"Updating existing page: {title}")
            notion.update_notion_page(client, existing_page["id"], content)
        else:
            print(f"Creating new page: {title}")
            notion.create_notion_page(client, parent_page_id, title, content)


if __name__ == "__main__":
    main()
