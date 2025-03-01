import notion_client


def convert_markdown_to_blocks(content: str) -> list[dict]:
    """Convert a markdown string to a list of blocks."""
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]},
        }
    ]


def get_notion_client(token: str) -> notion_client.Client:
    """Get a Notion client."""
    return notion_client.Client(auth=token)


def get_notion_parent_page(client: notion_client.Client, parent_page_id: str) -> dict | None:
    """Get a Notion parent page."""
    return (
        client.pages.retrieve(page_id=parent_page_id).get("results", [])[0]  # type: ignore
        if client.pages.retrieve(page_id=parent_page_id).get("results")  # type: ignore
        else None
    )


def find_notion_page(client: notion_client.Client, title: str) -> dict | None:
    """Find a Notion page by its title."""
    response = client.search(query=title, filter_properties={"property": "title", "title": {"equals": title}})
    return response.get("results", [])[0] if response.get("results") else None  # type: ignore


def create_notion_page(client: notion_client.Client, parent_page_id: str, title: str, content: str) -> dict:
    """Create a new page in Notion."""
    blocks = convert_markdown_to_blocks(content)

    # Create the page
    new_page = client.pages.create(
        parent={"page_id": parent_page_id},
        properties={"title": [{"text": {"content": title}}]},
        children=blocks,
    )
    return new_page  # type: ignore


def update_notion_page(client: notion_client.Client, page_id: str, content: str) -> None:
    """Update an existing Notion page."""
    blocks = convert_markdown_to_blocks(content)

    # First, delete existing blocks
    existing_blocks = client.blocks.children.list(block_id=page_id)
    for block in existing_blocks.get("results", []):  # type: ignore
        client.blocks.delete(block_id=block["id"])

    # Then add new blocks
    client.blocks.children.append(block_id=page_id, children=blocks)
