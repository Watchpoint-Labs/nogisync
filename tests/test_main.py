from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from nogisync.__main__ import get_content, get_title, main, process_page_hierarchy


class TestMain(TestCase):
    def test_get_title_with_frontmatter(self):
        post = {"attributes": {"title": "Test Title"}}
        md_file = Path("test_file.md")
        self.assertEqual(get_title(md_file, post), "Test Title")

    def test_get_title_without_frontmatter(self):
        post = {}
        md_file = Path("test_file_name.md")
        self.assertEqual(get_title(md_file, post), "Test File Name")

    def test_get_title_with_empty_frontmatter(self):
        post = {"attributes": {}}
        md_file = Path("test_file.md")
        self.assertEqual(get_title(md_file, post), "Test File")

    def test_get_content_with_frontmatter(self):
        post = {"body": "Test content"}
        md_file = Path("test.md")
        self.assertEqual(get_content(md_file, post), "Test content")

    @patch("nogisync.notion.find_notion_page")
    @patch("nogisync.notion.create_notion_page")
    def test_process_page_hierarchy_creates_new_pages(self, mock_create_page, mock_find_page):
        mock_find_page.return_value = None
        mock_create_page.side_effect = lambda client, parent_id, title, content: {"id": f"new_page_id_{title}"}

        path = Path("dir1/dir2/file.md")
        base_parent_id = "base_id"

        result = process_page_hierarchy(None, base_parent_id, path)

        self.assertEqual(mock_create_page.call_count, 2)
        mock_create_page.assert_any_call(None, "base_id", "Dir1", "")
        mock_create_page.assert_any_call(None, "new_page_id_Dir1", "Dir2", "")
        self.assertEqual(result, "new_page_id_Dir2")

    @patch("nogisync.notion.find_notion_page")
    @patch("nogisync.notion.create_notion_page")
    def test_process_page_hierarchy_uses_existing_pages(self, mock_create_page, mock_find_page):
        mock_find_page.side_effect = lambda client, title, parent_id: {"id": f"existing_page_id_{title}"}

        path = Path("dir1/dir2/file.md")
        base_parent_id = "base_id"

        result = process_page_hierarchy(None, base_parent_id, path)

        mock_create_page.assert_not_called()
        self.assertEqual(result, "existing_page_id_Dir2")

    @patch("nogisync.notion.find_notion_page")
    @patch("nogisync.notion.create_notion_page")
    def test_process_page_hierarchy_mixed_existing_and_new(self, mock_create_page, mock_find_page):
        def mock_find(client, title, parent_id):
            if title == "Dir1":
                return {"id": "existing_dir1"}
            return None

        mock_find_page.side_effect = mock_find
        mock_create_page.side_effect = lambda client, parent_id, title, content: {"id": f"new_page_id_{title}"}

        path = Path("dir1/dir2/file.md")
        base_parent_id = "base_id"

        result = process_page_hierarchy(None, base_parent_id, path)

        mock_create_page.assert_called_once_with(None, "existing_dir1", "Dir2", "")
        self.assertEqual(result, "new_page_id_Dir2")

    def test_process_page_hierarchy_single_level(self):
        path = Path("file.md")
        base_parent_id = "base_id"

        result = process_page_hierarchy(None, base_parent_id, path)

        self.assertEqual(result, base_parent_id)

    @patch("builtins.open")
    def test_get_content_without_frontmatter(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = "File content"
        post = {}
        md_file = Path("test.md")
        self.assertEqual(get_content(md_file, post), "File content")
        mock_open.assert_called_once_with(md_file, "r")

    @patch("sys.argv", ["nogisync"])
    def test_main_without_required_args(self):
        with self.assertRaises(TypeError):
            main()

    @patch("sys.argv", ["nogisync", "--help"])
    def test_main_with_help_flag(self):
        with self.assertRaises(SystemExit):
            main()

    @patch("sys.argv", ["nogisync", "--invalid", "value"])
    def test_main_with_invalid_args(self):
        with self.assertRaises(SystemExit):
            main()

    @patch("sys.argv", ["nogisync", "--version"])
    def test_main_with_version_flag(self):
        with self.assertRaises(SystemExit):
            main()
