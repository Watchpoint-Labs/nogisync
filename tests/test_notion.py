from unittest import TestCase
from unittest.mock import MagicMock, patch

from nogisync.notion import (
    create_notion_page,
    find_notion_page,
    get_notion_client,
    update_notion_page,
)


class TestNotion(TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_page_id = "test-page-id"
        self.mock_title = "Test Page"
        self.mock_content = "Test content"

    @patch("notion_client.Client")
    def test_get_notion_client(self, mock_client):
        token = "test-token"
        client = get_notion_client(token)
        mock_client.assert_called_once_with(auth=token)
        self.assertIsNotNone(client)

    def test_find_notion_page(self):
        mock_results = [{"id": "page1", "properties": {"title": {"title": [{"text": {"content": "Test Page"}}]}}}]
        self.mock_client.search.return_value = {"results": mock_results}

        result = find_notion_page(self.mock_client, self.mock_title)

        self.mock_client.search.assert_called_once()
        self.assertEqual(result["id"], "page1")

    def test_find_notion_page_not_found(self):
        self.mock_client.search.return_value = {"results": []}

        result = find_notion_page(self.mock_client, self.mock_title)

        self.assertIsNone(result)

    def test_create_notion_page(self):
        create_notion_page(self.mock_client, self.mock_page_id, self.mock_title, self.mock_content)

        self.mock_client.pages.create.assert_called_once()
        call_args = self.mock_client.pages.create.call_args[1]

        self.assertEqual(call_args["parent"]["page_id"], self.mock_page_id)
        self.assertEqual(call_args["properties"]["title"][0]["text"]["content"], self.mock_title)

    def test_update_notion_page(self):
        update_notion_page(self.mock_client, self.mock_page_id, self.mock_content)

        self.mock_client.blocks.children.append.assert_called_once()
        call_args = self.mock_client.blocks.children.append.call_args[1]

        self.assertEqual(call_args["block_id"], self.mock_page_id)
        self.assertIn("children", call_args)

    def test_find_notion_page_with_parent(self):
        mock_results = [
            {
                "id": "page1",
                "parent": {"page_id": "parent-id"},
                "properties": {"title": {"title": [{"text": {"content": "Test Page"}}]}},
            }
        ]
        self.mock_client.search.return_value = {"results": mock_results}
        parent_id = "parent-id"

        result = find_notion_page(self.mock_client, self.mock_title, parent_id=parent_id)

        self.mock_client.search.assert_called_once()
        search_args = self.mock_client.search.call_args[1]
        self.assertIn("filter", search_args)
        self.assertEqual(search_args["filter"]["property"], "object")
        self.assertEqual(search_args["filter"]["value"], "page")
        self.assertEqual(result["id"], "page1")
        
    def test_find_notion_page_with_parent_with_dashes(self):
        mock_results = [
            {
                "id": "page1",
                "parent": {"page_id": "dashes-should-be-ignored"},
                "properties": {"title": {"title": [{"text": {"content": "Test Page"}}]}},
            }
        ]
        self.mock_client.search.return_value = {"results": mock_results}
        parent_id = "dashesshouldbeignored"

        result = find_notion_page(self.mock_client, self.mock_title, parent_id=parent_id)

        self.mock_client.search.assert_called_once()
        search_args = self.mock_client.search.call_args[1]
        self.assertIn("filter", search_args)
        self.assertEqual(search_args["filter"]["property"], "object")
        self.assertEqual(search_args["filter"]["value"], "page")
        self.assertEqual(result["id"], "page1")
