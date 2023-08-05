import os
import sys
import copy
import shutil
import logging

from operator import attrgetter, itemgetter

from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File
from mkdocs.structure.nav import Section
from mkdocs.commands.build import _build_page


log = logging.getLogger(__name__)

DEBUG=False

class PaginatePlugin(BasePlugin):

    config_scheme = (
        ('max_items', mkdocs.config.config_options.Type(int, default=6))
    )

    def do_paginate(self, items, **kwargs):
        if DEBUG:
            print("------------")
            print('do_paginate')
            print(items)
            print(kwargs)
            print("NUMPAGES: ", self.num_pages)
            
        page = kwargs.get('page')

        if hasattr(page, 'page_num'):
            #pages_sorted = sorted(items, key=attrgetter(sort_key), reverse=True)
            #pages_sorted = sorted(nav.pages, key=lambda x: x.url, reverse=True)
            #chunks = [pages_sorted[i:i + max_items] for i in range(0, len(pages_sorted), max_items)]
            chunks = [items[i:i + self.max_items] for i in range(0, len(items), self.max_items)]
            if DEBUG: 
                print("NUM CHUNKS: ", len(chunks))
                print("PAGE NUM: ", (page.page_num-1))
            out_items = chunks[page.page_num-1]
        else:
            out_items = items

        return out_items

    def on_config(self, config):
        self.max_items = self.config.get('max_items', 6)

    def on_env(self, env, config, files):
        self.config = config
        env.filters['paginate'] = self.do_paginate

        self._env = env
        return env

    def on_nav(self, nav, config, files):
        if DEBUG: 
            print("------------")
            print("on_nav")
            print(nav)
        num_items = len(nav.pages)
        num_pages = num_items / self.max_items
        if num_items % self.max_items:
            num_pages += 1

        self.num_pages = int(num_pages)

        homepage = None
        for page in nav.pages:
            if page.is_homepage:
                page.page_num = 1
                homepage = page

                for i in range(1, self.num_pages):
                    # i+1 since we want to start with page2, etc.
                    new_pagenum = i+1
                    newfile = File(
                        path = homepage.file.src_path,
                        src_dir = homepage.file.abs_src_path.rstrip(homepage.file.src_path),
                        dest_dir = homepage.file.abs_dest_path.rstrip(homepage.file.dest_path),
                        use_directory_urls = True
                    )
                    newfile.abs_dest_path = os.path.join(
                        newfile.abs_dest_path.rstrip(newfile.dest_path),
                        "page",
                        str(new_pagenum),
                        "index.html"
                    )
                    newfile.url = "page/%s/" % new_pagenum
                    newpage = Page(
                        title='page%s' % new_pagenum,
                        file=newfile,
                        config=config
                    )
                    newpage.page_num = new_pagenum
                    newpage.generated = True
                    if i == (self.num_pages-1):
                        newpage.last_page = True

                    nav.pages.append(newpage)
                    nav.items.append(newpage)
                    files.append(newfile)

        return nav
