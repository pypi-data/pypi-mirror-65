from __future__ import absolute_import
import argparse
import importlib
import re
import urllib.parse
import pydoc
from typing import Optional, Iterable, List, Pattern

README_PATH: str = urllib.parse.urljoin(__file__, '../README.md')


MARKDOWN_SECTIONS_RE: str = (
    # Group 1: Text preceding a header
    r'(.*?(?:\n|^))'
    # Group 2: Markup indicating the start of a header
    r'(#+)'
    # Group 3: Spaces, punctuation, etc. preceding the name-space key
    r'([^\w]*'
    # Group 3: ...include any tags wrapping the name-space in group 3
    r'(?:<[^\>]+>[^\w]*)?)'
    # Group 4: The name-space key (module/class/function name)
    r'([A-Za-z][A-Za-z_\.]*)'
    # Group 5: The remainder of the header line
    r'([^\n]*(?:\n|$))'
    # Group 6: Text up to (but not including) the next header of the same level
    r'(.*?(?=(?:\n\2[^#]|$)))'

)
MARKDOWN_SECTIONS_PATTERN: Pattern = re.compile(
    MARKDOWN_SECTIONS_RE,
    re.DOTALL
)


def get_name_space(path: str) -> Optional[object]:
    """
    Get a name-space from a fully-qualified path
    """
    name_space: Optional[object] = None
    parts: List[str] = path.split('.')
    index: int
    attribute_name: str
    # Iterate over indices in reverse: 0, -1, -2, -3, ...
    for index in range(0, -len(parts), -1):
        # When the index is `0`--we use the whole path, otherwise
        # we split at `index`
        module_path: str = (
            '.'.join(parts[:index])
            if index else
            path
        )
        # Check to see if `module_path` is valid, and if it is not--continue
        # to shift the split index until we find a module path which *is*
        # valid, or come to the beginning of the path
        try:
            name_space = importlib.import_module(
                module_path
            )
            # If the module path is a valid namespace, but the `path`
            # was pointing to an attribute of the module and not the module
            # itself--resolve that attribute path
            if index < 0:
                for attribute_name in parts[index:]:
                    try:
                        name_space = getattr(name_space, attribute_name)
                    except AttributeError:
                        name_space = None
            break
        except ModuleNotFoundError:
            pass
    return name_space


class ReadMe:
    """
    This class parses a markdown-formatted README file and updates sections
    to reflect a corresponding package's class, method, and function
    docstrings.

    Parameters:

        - markdown (str): Markdown text
    """

    def __init__(
        self,
        markdown: str
    ) -> None:
        self.markdown = markdown
        self.name_space_path: str = ''
        self.before: str = ''
        self.header: str = ''
        self.name: str = ''

    @property
    def text(self) -> str:
        """
        This is the text preceding any sub-sections
        """
        docstring: str = ''
        if self.name_space_path:
            name_space: Optional[object] = get_name_space(
                self.name_space_path
            )
            if name_space:
                docstring: str = pydoc.getdoc(name_space).strip() or ''
                if docstring:
                    docstring = f'\n{docstring}\n'
        return docstring

    @classmethod
    def _new_section(
        cls,
        markdown: str,
        before: str,
        start_header: str,
        before_name: str,
        name: str,
        after_name: str,
        parent_name_space_path: str
    ) -> 'ReadMe':
        section: cls = cls(markdown=markdown)
        section.before = before
        section.header = (
            start_header +
            before_name + name +
            after_name + (
                ''
                if after_name.endswith('\n') else
                '\n'
            )
        )
        # Assign a name-space path to the section
        if parent_name_space_path and get_name_space(parent_name_space_path):
            concatenated_name_space_path: str = (
                f'{parent_name_space_path}.{name}'
                if name else
                parent_name_space_path
            )
            section.name_space_path = concatenated_name_space_path
        else:
            section.name_space_path = name
        return section

    def __iter__(self) -> Iterable['ReadMe']:
        """
        Yield an iterable collection of `ReadMe` instances representing
        sub-sections of this document or document-section.
        """
        # Only include the first "before" if it's not being replaced by a
        # docstring
        include_before: bool = False if self.text else True
        before: str
        start_header: str
        before_name: str
        name: str
        after_name: str
        body: str
        for (
            before,
            start_header,
            before_name,
            name,
            after_name,
            body
        ) in self._split():
            yield self._new_section(
                markdown=body,
                before=before if include_before else '\n',
                start_header=start_header,
                before_name=before_name,
                name=name,
                after_name=after_name,
                parent_name_space_path=self.name_space_path
            )
            # Only exclude before for the first section
            include_before = True

    def _split(self) -> List[str]:
        """
        Split the markdown into sections
        """
        return MARKDOWN_SECTIONS_PATTERN.findall(
            self.markdown
        )

    def __str__(self) -> str:
        """
        Render the document as markdown, updated to reflect any docstrings
        that were found
        """
        body: str = ''.join(
            str(section)
            for section in self
        )
        text: str = self.text
        if not (body or text):
            body = self.markdown
        return (
            f'{self.before}'
            f'{self.header}'
            f'{text}'
            f'{body}'
        )


def update(path: str = './README.md') -> None:
    """
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
    """
    # Read the existing markdown
    with open(path, 'r') as readme_io:
        read_me: ReadMe = ReadMe(readme_io.read())
    read_me_str: str = str(read_me)
    # Update and save
    if read_me_str:
        with open(path, 'w') as readme_io:
            readme_io.write(read_me_str)


if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Parse command-line arguments'
    )
    parser.add_argument(
        'path',
        default='./README.md',
        nargs=argparse.OPTIONAL,
        help='Where is the README file (defaults to "./README.md")?'
    )
    arguments = parser.parse_args()
    update(arguments.path)
