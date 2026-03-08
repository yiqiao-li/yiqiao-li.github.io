# Projects

Research projects are stored as Markdown files in this folder. Each file becomes a project page at `/projects/<filename>/`.

## Adding a New Project

1. **Copy the template**  
   Copy `TEMPLATE.md` to a new file with a **descriptive slug** (e.g., `my-new-project.md`).

2. **Required frontmatter**  
   Fill in these fields in the YAML header:

   | Field         | Description                              | Example                     |
   | ------------- | ---------------------------------------- | --------------------------- |
   | `title`       | Full project title                       | `My Research Project`       |
   | `description` | Short summary for the Research page card | Include Sponsor, Role, Year |
   | `year`        | Year or range                            | `2025` or `2024-2026`       |
   | `importance`  | Display order (lower = first)            | `1`, `2`, `3`...            |
   | `category`    | `Current` or `Past`                      | `Current`                   |
   | `role`        | PI, co-PI, Researcher, etc. (optional)   | `PI`                        |
   | `img`         | Image path (optional)                    | `assets/img/project.png`    |

3. **Optional frontmatter**

   - `related_publications: true` — Shows a References section (cite papers in content with `{% cite key %}`)
   - `giscus_comments: false` — Disable comments

4. **Body content**  
   Use the structure below for consistency:

   ```
   Year: YYYY-YYYY
   PIs: Name1, Name2
   Sponsor: Funding Agency
   Description: Full project description...
   ```

5. **Add an image** (optional)  
   Put the image in `assets/img/` and reference it in `img` and in the body if needed.

## File Naming

- Use **lowercase** and **hyphens**: `urban-mobility.md`, `cross-border-truck.md`
- The filename (without `.md`) becomes the URL slug
- No need for numbers—`importance` controls display order

## Defaults

All projects inherit from `_config.yml`:

- Layout: `project`
- `related_publications: false`
- `giscus_comments: false`

Override these in frontmatter when needed.
