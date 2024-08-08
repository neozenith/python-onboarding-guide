# Documentation - MKDocs

<!--TOC-->

- [Documentation - MKDocs](#documentation---mkdocs)
  - [TODO](#todo)
  - [Resources](#resources)

<!--TOC-->

This is my personal quick start guide of preferences on generating documentation using MKDocs.

`requirements/docs.in`

```txt
# Bare minimum
mkdocs
mkdocs-material
mkdocstrings
mkdocstrings-python
mkdocs-gen-files
mkdocs-literate-nav
mkdocs-section-index
mkdocs-git-revision-date-localized-plugin
mkdocs-git-authors-plugin
mkdocs-render-swagger-plugin

# Scientific + Engineering
mkdocs-jupyter
mkdocs-plotly-plugin
mkdocs-blogging-plugin
mkdocs-drawio-exporter
```

`mkdocs.yaml`

```yaml
site_name: example-site-name
site_url: https://example-site-name.github.io/

theme:
  name: material

plugins:
- search  
- git-authors
- git-revision-date-localized

# Blogging
- blogging:
    dirs: # The directories to be included
      - blog

# Auto Documentation From Code      
- gen-files: # Generate distinct docs pages per source code file.
    scripts:
    - scripts/mkdocs/gen_ref_pages.py  
- literate-nav:
    nav_file: SUMMARY.md
- section-index
- mkdocstrings: # Generate documentation from source code.
    default_handler: python
    handlers:
      python:
        options:
          docstring_style: google
          docstring_section_style: list
          show_if_no_docstring: true
          show_submodules: true
          show_bases: true
          
          show_root_full_path: true
          show_object_full_path: false
          group_by_category: true
          show_category_heading: true
          show_source: false
          show_signature: true
          separate_signature: true
          show_signature_annotations: true

# Swagger OpenAPI doc generation
- render_swagger

# Science and Engineering
- plotly
- drawio-exporter
- mkdocs-jupyter

markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: plotly
          class: mkdocs-plotly
          format: !!python/name:mkdocs_plotly_plugin.fences.fence_plotly
nav:
- 'index.md'
- Code Reference: reference/  
```

`.readthedocs.yml`

```yml

# Read the Docs configuration file for MkDocs projects
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the version of Python and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.10"

mkdocs:
  configuration: mkdocs.yml

# Optionally declare the Python requirements required to build your docs
python:
  install:
  - requirements: docs/requirements.txt
```

`scripts/mkdocs/gen_ref_pages.py`

```python
"""Generate the code reference pages and navigation."""

# Standard Library
from pathlib import Path

# Third Party
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

src = Path(__file__).parent.parent / "src"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
```

`docs/index.md`

```md
# Index Heading

![Architecture](diagrams/architecture.drawio)
```

## TODO

 - Organise this content to be much more automated

 ## Resources
  - https://www.mkdocs.org/getting-started/
  - https://squidfunk.github.io/mkdocs-material/
  - https://github.com/mkdocs/catalog