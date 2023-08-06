# readme-md-docstrings

This script updates module, class, and function docs in a README.md file,
based on their corresponding docstrings (so that documentation does not need to
be manually written in two places).

## Install

```shell script
pip3 install readme-md-docstrings
```

## Modules

### readme_md_docstrings

#### ReadMe

This class parses a markdown-formatted README file and updates sections
to reflect a corresponding package's class, method, and function
docstrings.

Parameters:

    - markdown (str): Markdown text

#### update

Update an existing README.md file located at `path`.

```python
import readme_md_docstrings
readme_md_docstrings.update('./README.md')
```

This can also be run from the command line:
```shell script
python3 -m readme_md_docstrings ./README.md
```

If no path is provided, the default is "./README.md":
```shell script
python3 -m readme_md_docstrings
```
