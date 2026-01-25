# Repository Update Info Setup

This setup automatically tracks and displays git repository information on your Jekyll site.

## Files Created

1. **update_info.py** - Python script that generates git repository information
2. **_includes/repo-info.html** - Jekyll include component to display repository info
3. **.github/workflows/update-repo-info.yml** - GitHub Actions workflow for automatic updates

## Generated Files

- **_data/git_info.yml** - YAML file with repository information (auto-generated)
- **assets/git_info.json** - JSON file with repository information (auto-generated)

## How It Works

### Manual Update
Run this command locally to generate/update the repository information:
```bash
python3 update_info.py
```

This will create/update:
- `_data/git_info.yml` - Used by Jekyll templates
- `assets/git_info.json` - For JavaScript/API use

### Automatic Update (CI/CD)
GitHub Actions workflow automatically:
1. Runs on every push to `master` or `main` branch
2. Runs daily at midnight UTC
3. Generates updated repository info
4. Commits changes with `[skip ci]` tag to prevent infinite loops

## Including Repository Info in Pages

To display repository information in any Jekyll page or layout, add this line:

```liquid
{% include repo-info.html %}
```

This will display:
- Current branch
- Latest commit hash and message
- Commit date
- Repository status (clean/modified)
- Repository URL

## Displaying in about.md

The about page now includes repository information which shows:
- The current git branch
- Latest commit details
- Repository status
- Link to the GitHub repository

## Styling

The `_includes/repo-info.html` component includes embedded CSS styling that:
- Uses a light blue border and background
- Shows green indicator for clean repository status
- Shows red indicator for modified files
- Includes monospace font for code elements

## Information Tracked

The scripts collect:
- **branch** - Current git branch
- **commit_hash** - Short commit SHA
- **commit_msg** - Latest commit message
- **commit_date** - Commit timestamp with timezone
- **remote_url** - GitHub repository URL
- **is_dirty** - Whether there are uncommitted changes
- **ahead/behind** - Commits ahead/behind upstream branch
- **updated_at** - ISO timestamp of generation time

## Usage Examples

### Jekyll Template
```liquid
{% if site.data.git_info %}
  Last updated: {{ site.data.git_info.commit_date }}
  Branch: {{ site.data.git_info.branch }}
{% endif %}
```

### JavaScript (via JSON)
```javascript
fetch('/assets/git_info.json')
  .then(r => r.json())
  .then(info => console.log(info.commit_msg));
```

## Notes

- The repository status is determined from `git status --porcelain`
- Generated files should be committed to the repository
- The GitHub Actions workflow skips CI to avoid infinite update loops
- The Python script requires `git` to be installed and the current directory to be a git repository
