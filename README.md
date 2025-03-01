# Notion-GitHub Page Sync Action

This GitHub Action synchronizes markdown files from your repository with Notion pages, maintaining the directory structure as the page hierarchy in Notion. It provides a seamless way to keep your documentation in sync between GitHub and Notion.

## Features

- 🔄 Bi-directional synchronization between GitHub markdown files and Notion pages
- 📁 Preserves directory structure as Notion page hierarchy
- 🔍 Supports multiple directory monitoring
- 🎯 Selective synchronization based on file patterns
- 📝 Maintains markdown formatting compatibility
- 🔒 Secure handling of Notion API credentials

## Prerequisites

- A Notion account with admin access to the workspace
- Notion API key ([Get one here](https://www.notion.so/my-integrations))
- GitHub repository containing markdown files
- Notion parent page where the content will be synchronized

## Setup

1. Create a new Notion integration in your workspace
2. Add your Notion API key as a GitHub secret named `NOTION_API_KEY`
3. Share your Notion parent page with the integration
4. Get your Notion parent page ID
5. Configure the action in your workflow

## Usage

Add the following workflow to your repository (e.g., `.github/workflows/notion-sync.yml`):

```yaml
name: Sync to Notion
on:
  push:
    paths:
      - '**.md'
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Notion GitHub Page Sync
        uses: watchpointlabs/notion-github-page-sync-action@v1
        with:
          notion_api_key: ${{ secrets.NOTION_API_KEY }}
          notion_parent_page_id: 'your-parent-page-id'
          source_path: 'docs/'  # Directory containing markdown files
```

## Configuration Options

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `notion_api_key` | Notion API key for authentication | Yes | - |
| `notion_parent_page_id` | ID of the parent page in Notion | Yes | - |
| `source_path` | Path to directory containing markdown files | No | `.` |
| `file_patterns` | Glob patterns for files to sync | No | `**/*.md` |
| `sync_direction` | Direction of sync (github-to-notion, notion-to-github, or bidirectional) | No | `github-to-notion` |

## Example Directory Structure

```
docs/
├── getting-started/
│   ├── installation.md
│   └── configuration.md
├── guides/
│   ├── basic-usage.md
│   └── advanced-features.md
└── README.md
```

This will create a corresponding structure in Notion:

```
Parent Page
├── Getting Started
│   ├── Installation
│   └── Configuration
├── Guides
│   ├── Basic Usage
│   └── Advanced Features
└── README
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository. 