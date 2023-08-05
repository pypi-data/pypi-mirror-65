# mkdocs-paginate-plugin
Plugin for Mkdocs to support pagination for blog like layouts.

This is a _special_ kind of plugin that requires support by your mkdocs theme
to fully taken advantage of it.

## Setup

```
pip install mkdocs-paginage-plugin
```

In your mkdocs.yml

```
plugins:
    - paginate
```

Set the number of items per page (defaults to 6):

```
plugins:
    - paginate:
        max_items: 12
```

