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

## Explanation

This plugin has two main components: Homepage duplication, and a filter to
return groups of pages from a collection.

This is designed to be used with themes that intend to show child pages on the
homepage.  Though you may find other uses, perhaps.

## Usage

This plugin will gather the set of mkdocs pages and determine how many should
be grouped based on the 'max_items' allowed.  The homepage is detected and
duplicated by the number of groups to display.  A 'page_num' attribue is
injected into each Page object, and can be referenced later.  A 'last_page'
attribute is injected into the last generated page.

Your theme would then use the filter like so:

```
{% for nav_item in nav_item.children|paginate(page=page) %}
  {{ nav_item.content }}
{% endfor %}
```

The items for just the matching 'page_num' will be returned.

Duplicated homepages will be accessible at `<site_url>/page/<num>/` where
`<site_url>` is the URL of your site and `<num>` is the number of the page.
For instance a site of example.com will have the second page at
`http://example.com/page/2/`

You can use logic to add 'next' and 'previous' buttons based on the current
page_num.  For example:

```
{% if not page.last_page %}
<div class="nav-previous">
    <a href="{{ config.site_url|url }}page/{{ page.page_num + 1 }}/">
        "Older posts"
    </a>
</div>
{% endif %}
```


