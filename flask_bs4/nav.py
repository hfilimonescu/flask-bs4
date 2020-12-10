from hashlib import sha1

from dominate import tags
from visitor import Visitor


class BootstrapRenderer(Visitor):
    def __init__(self, html5=True, id=None):
        self.html5 = html5
        self._in_dropdown = False
        self.id = id

    def visit_Navbar(self, node):
        # create a navbar id that is somewhat fixed, but do not leak any
        # information about memory contents to the outside
        node_id = self.id or sha1(str(id(node)).encode()).hexdigest()

        nav_root = tags.nav() if self.html5 else tags.div(role='navigation')
        nav_root['class'] = 'navbar navbar-expand-lg navbar-light bg-light'

        root = tags.div(_class="container-fluid")

        # title may also have a 'get_url()' method, in which case we render
        # a brand-link
        if node.title is not None:
            if hasattr(node.title, 'get_url'):
                root.add(tags.a(node.title.text, _class='navbar-brand',
                                href=node.title.get_url()))
            else:
                root.add(tags.span(node.title, _class='navbar-brand'))

        btn = root.add(tags.button())
        btn['class'] = 'navbar-toggler'
        btn['type'] = 'button'
        btn['data-bs-toggle'] = 'collapse'
        btn['data-bs-target'] = '#' + node_id
        btn['aria-controls'] = node_id
        btn['aria-expanded'] = 'false'
        btn['aria-label'] = 'Toogle Navigation'

        btn.add(tags.span(_class='navbar-toggler-icon'))

        bar = root.add(tags.div(
            _class='navbar-collapse collapse',
            id=node_id,
        ))

        bar_list = bar.add(tags.ul(_class='navbar-nav mr-auto'))

        for item in node.items:
            bar_list.add(self.visit(item))

        nav_root.add(root)

        return nav_root

    def visit_Text(self, node):
        if not self._in_dropdown:
            return tags.span(node.text, _class='navbar-text')
        return tags.li(node.text, _class='dropdown-header')

    def visit_Link(self, node):
        if hasattr(node, '_in_dropdown'):
            item = tags.a(node.text, href=node.get_url(),
                          _class="dropdown-item")
        else:
            item = tags.li(_class="nav-item")
            item.add(tags.a(node.text, href=node.get_url(), _class="nav-link"))

        return item

    def visit_Separator(self, node):
        if not self._in_dropdown:
            raise RuntimeError('Cannot render separator outside Subgroup.')
        return tags.div(role='separator', _class='dropdown-divider')

    def visit_Subgroup(self, node):
        if not self._in_dropdown:
            li = tags.li(_class='nav-item dropdown')
            if node.active:
                li['class'] += ' active'
            a = li.add(tags.a(node.title, href='#',
                              _class='nav-link dropdown-toggle'))
            a['data-bs-toggle'] = 'dropdown'
            a['role'] = 'button'
            a['aria-haspopup'] = 'true'
            a['aria-expanded'] = 'false'
            a.add(tags.span(_class='caret'))

            ul = li.add(tags.ul(_class='dropdown-menu'))

            self._in_dropdown = True
            for item in node.items:
                item._in_dropdown = True
                ul.add(self.visit(item))
            self._in_dropdown = False

            return li
        else:
            raise RuntimeError('Cannot render nested Subgroups')

    def visit_View(self, node):
        if hasattr(node, '_in_dropdown'):
            item = tags.a(node.text, href=node.get_url(),
                          title=node.text, _class="dropdown-item")
            if node.active:
                item['class'] += ' active'
        else:
            item = tags.li(_class="nav-item")
            sub_item = tags.a(node.text, href=node.get_url(),
                              _class="nav-link")

            if node.active:
                sub_item['class'] += ' active'

            item.add(sub_item)

        return item
