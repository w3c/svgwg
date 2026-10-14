"""Load the SVG definitions files and answer "what does this <a> point to?".

This is a Python port of two pieces of the old build:

  tools/publish/definitions.js  (loadInto, resolve, the format*Link helpers)
  tools/publish/processing.js   (processLinks, lines 999-1057)

The port follows the JavaScript closely, including its quirks (which file
wins when a name is defined twice, the order attributes are listed in, the
visible text each kind of link gets), because the goal is that every link
lands exactly where it lands today. Nothing here decides Bikeshed syntax:
the resolver only says "this is an element/attribute/property/... called X,
whose old href is Y, shown as Z". convert.py turns that into Bikeshed.

Standard library only. Python 3.9 or later.
"""

import os
import re
import xml.etree.ElementTree as ET

DEFS_NS = "http://mcc.id.au/ns/local"
EDIT_NS = "http://xmlns.grorg.org/SVGT12NG/"
XHTML_NS = "http://www.w3.org/1999/xhtml"

LQUOTE = "‘"
RQUOTE = "’"


def split_list(s):
    # utils.splitList: split on commas followed by any spaces.
    if not s:
        return []
    return re.split(r",\s*", s)


def resolve_url(base, url):
    # utils.resolveURL
    if url is None:
        return None
    if not base:
        return url
    if url.startswith("/"):
        raise ValueError("can't handle absolute paths: " + url)
    if ":" in url:
        return url
    if url.startswith("#"):
        return re.sub(r"(#.*)?$", "", base, count=1) + url
    return re.sub(r"[^/]*$", "", base, count=1) + url


def normalize_term_name(name):
    return re.sub(r"\s+", " ", name.lower()).strip()


class Thing(object):
    """One definition: element, attribute, property, interface, symbol, term,
    element category or attribute category. Attributes are set freely, like
    the JavaScript objects they mirror."""

    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)

    def __repr__(self):
        return "<%s %s %s>" % (self.kind, getattr(self, "name", "?"), getattr(self, "href", "?"))


class Definitions(object):
    def __init__(self):
        self.elements = {}
        self.element_categories = {}
        self.attribute_categories = {}
        self.properties = {}
        self.interfaces = {}
        self.symbols = {}
        self.terms = {}
        self.common_attributes_for_elements = []
        self.common_attributes = {}
        self.presentation_attributes = {}


def _children(el, local):
    for c in el:
        if isinstance(c.tag, str) and c.tag == "{%s}%s" % (DEFS_NS, local):
            yield c


def _load_into(path, base, specid, defs):
    tree = ET.parse(path)
    root = tree.getroot()

    for e in _children(root, "element"):
        element = Thing(
            "element",
            name=e.get("name"),
            href=resolve_url(base, e.get("href")),
            content_model=e.get("contentmodel"),
            element_categories=split_list(e.get("elementcategories")),
            elements=split_list(e.get("elements")),
            attribute_categories=split_list(e.get("attributecategories")),
            common_attribute_names=split_list(e.get("attributes")),
            interfaces=split_list(e.get("interfaces")),
            specific_attributes=[],
            geometry_properties=split_list(e.get("geometryproperties")),
            categories={},
            content_model_description=None,
            specid=specid,
        )
        for c in _children(e, "attribute"):
            element.specific_attributes.append(Thing(
                "attribute",
                name=c.get("name"),
                href=resolve_url(base, c.get("href")),
                animatable=c.get("animatable") == "yes",
                specific=True,
                property=None,
                specid=specid,
            ))
        for c in _children(e, "contentmodel"):
            # Hand-written content model: keep the XHTML children as is.
            element.content_model_description = c
        defs.elements[element.name] = element

    for ec in _children(root, "elementcategory"):
        defs.element_categories[ec.get("name")] = Thing(
            "elementcategory",
            name=ec.get("name"),
            href=resolve_url(base, ec.get("href")),
            elements=split_list(ec.get("elements")),
            specid=specid,
        )

    for a in _children(root, "attribute"):
        attribute = Thing(
            "attribute",
            name=a.get("name"),
            href=resolve_url(base, a.get("href")),
            animatable=a.get("animatable") == "yes",
            common=True,
            property=None,
            specid=specid,
        )
        if a.get("elements") is not None:
            attribute.elements = dict((n, True) for n in split_list(a.get("elements")))
            defs.common_attributes_for_elements.append(attribute)
        else:
            defs.common_attributes[attribute.name] = attribute

    for ac in _children(root, "attributecategory"):
        category = Thing(
            "attributecategory",
            name=ac.get("name"),
            href=resolve_url(base, ac.get("href")),
            attributes=[],
            common_attribute_names=split_list(ac.get("attributes")),
            presentation_attribute_names=split_list(ac.get("presentationattributes")),
            specid=specid,
        )
        for a in _children(ac, "attribute"):
            category.attributes.append(Thing(
                "attribute",
                name=a.get("name"),
                href=resolve_url(base, a.get("href")),
                animatable=a.get("animatable") == "yes",
                category=category,
                property=None,
                specid=specid,
            ))
        defs.attribute_categories[category.name] = category

    for p in _children(root, "property"):
        prop = Thing("property", name=p.get("name"), href=resolve_url(base, p.get("href")), specid=specid)
        defs.properties[prop.name] = prop
        defs.presentation_attributes[prop.name] = Thing(
            "attribute", name=prop.name, href=prop.href, property=prop.name, specid=specid)

    for i in _children(root, "interface"):
        defs.interfaces[i.get("name")] = Thing(
            "interface", name=i.get("name"), href=resolve_url(base, i.get("href")), specid=specid)

    for s in _children(root, "symbol"):
        defs.symbols[s.get("name")] = Thing(
            "symbol", name=s.get("name"), href=resolve_url(base, s.get("href")), specid=specid)

    for t in _children(root, "term"):
        term = Thing("term", name=t.get("name"), href=resolve_url(base, t.get("href")),
                     markup=t if len(t) or (t.text and t.text.strip()) else None, specid=specid)
        defs.terms[term.name] = term
        norm = normalize_term_name(term.name)
        if norm not in defs.terms:
            defs.terms[norm] = term


def _resolve(defs, main=None):
    for element in defs.elements.values():
        element.attributes = {}
        element.attribute_order = []

        def add(attr):
            element.attributes[attr.name] = attr
            element.attribute_order.append(attr.name)

        for cat_name in element.attribute_categories:
            cat = defs.attribute_categories.get(cat_name) or (main and main.attribute_categories.get(cat_name))
            if cat:
                for a in cat.attributes:
                    add(a)
        if main:
            for a in main.common_attributes_for_elements:
                if element.name in a.elements:
                    add(a)
        for a in defs.common_attributes_for_elements:
            if element.name in a.elements:
                add(a)
        for name in element.common_attribute_names:
            ca = defs.common_attributes.get(name) or (main and main.common_attributes.get(name))
            if ca:
                add(ca)
        for a in element.specific_attributes:
            add(a)

    if main:
        for name, cat in main.element_categories.items():
            for e in cat.elements:
                if e in defs.elements:
                    defs.elements[e].categories[name] = cat
    for name, cat in defs.element_categories.items():
        for e in cat.elements:
            elt = defs.elements.get(e) or (main and main.elements.get(e))
            if elt:
                elt.categories[name] = cat


def load(infos):
    """infos: list of dicts with keys path, base, specid, mainspec, in the
    order publish.xml lists them. Returns (defs, defs_by_spec)."""
    defs = Definitions()
    by_spec = {}
    infos = list(reversed(infos))  # definitions.js:554, the first listed file wins
    for info in infos:
        _load_into(info["path"], info.get("base"), info.get("specid"), defs)
        if info.get("specid"):
            by_spec[info["specid"]] = Definitions()
            _load_into(info["path"], info.get("base"), info.get("specid"), by_spec[info["specid"]])
    for info in infos:
        sid = info.get("specid")
        if sid:
            ms = info.get("mainspec")
            _resolve(by_spec[sid], by_spec.get(ms) if ms else None)
    _resolve(defs)
    return defs, by_spec


# -- What a resolved link looks like -----------------------------------------

class Link(object):
    """The old build's answer for one link.

    kind     element | attribute | property | presentationattribute | symbol |
             term | interface | member | elementcategory | error
    name     the defined name
    href     the old href (relative 'page.html#id', '#id' or absolute URL)
    wrap     class of the <span> that wraps the link, or None
    quotes   True when curly quotes go around the link inside the span
    a_class  class on the <a>, or None
    title    title attribute on the <a>, or None
    text     visible text (string), or None when markup is used
    markup   an ElementTree element whose children are the visible content
    message  for kind == error, the old build's warning
    """

    def __init__(self, kind, name, href=None, wrap=None, quotes=False, a_class=None,
                 title=None, text=None, markup=None, message=None, thing=None):
        self.kind = kind
        self.name = name
        self.href = href
        self.wrap = wrap
        self.quotes = quotes
        self.a_class = a_class
        self.title = title
        self.text = text if text is not None else (None if markup is not None else name)
        self.markup = markup
        self.message = message
        self.thing = thing


def format_thing(thing, omit_quotes=False, capitalize=False):
    k = thing.kind
    if k == "element":
        return Link("element", thing.name, thing.href, wrap="element-name", quotes=not omit_quotes, thing=thing)
    if k == "attribute":
        title = None
        if getattr(thing, "property", None):
            title = "Presentation attribute for property " + LQUOTE + thing.property + RQUOTE
        return Link("attribute", thing.name, thing.href, wrap="attr-name", quotes=not omit_quotes, title=title, thing=thing)
    if k == "property":
        return Link("property", thing.name, thing.href, a_class="property", thing=thing)
    if k == "symbol":
        return Link("symbol", thing.name, thing.href, text="<" + thing.name + ">", thing=thing)
    if k == "term":
        if thing.markup is not None:
            return Link("term", thing.name, thing.href, markup=thing.markup, thing=thing)
        return Link("term", thing.name, thing.href, thing=thing)
    if k == "interface":
        return Link("interface", thing.name, thing.href, a_class="idlinterface", thing=thing)
    if k == "elementcategory":
        n = thing.name
        if capitalize:
            n = n[:1].upper() + n[1:]
        return Link("elementcategory", thing.name, thing.href, text=n + " element", thing=thing)
    if k == "attributecategory":
        return Link("attributecategory", thing.name, thing.href, text=thing.name + " attributes", thing=thing)
    raise ValueError(k)


def error(message, warnings, where):
    warnings.append((where, message))
    return Link("error", message, text="@@ " + message, message=message)


class Resolver(object):
    """Answers for untyped <a> elements. `ctx` objects passed in must offer:
         ctx.with_element()        nearest <edit:with element=...> value, or None
         ctx.closest_interface()   name from the nearest preceding 'Interface X' heading
         ctx.page_has_id(id)       does the current source page contain this id
         ctx.edit_format()         value of edit:format on the <a>, or None
         ctx.in_proptable_th()     the <a> is in a <th> of <table class=proptable>
    """

    def __init__(self, defs, warnings=None):
        self.d = defs
        self.warnings = warnings if warnings is not None else []

    def _element_context(self, ctx):
        name = ctx.with_element()
        if name and name in self.d.elements:
            return name
        if name:
            self.warnings.append((ctx.where(), 'unknown element "%s" in edit:with' % name))
        return None

    def element(self, name, ctx, omit_quotes=False):
        if name not in self.d.elements:
            return error('unknown element "%s"' % name, self.warnings, ctx.where())
        return format_thing(self.d.elements[name], omit_quotes)

    def element_attribute(self, elt, attr, ctx):
        e = self.d.elements.get(elt)
        if not e or attr not in e.attributes:
            return error('unknown attribute "%s" on element "%s"' % (attr, elt), self.warnings, ctx.where())
        return format_thing(e.attributes[attr])

    def _attrs_in_categories(self, name):
        out = []
        for cat in self.d.attribute_categories.values():
            for a in cat.attributes:
                if a.name == name:
                    out.append(a)
        return out

    def _common_for_elements(self, name):
        return [a for a in self.d.common_attributes_for_elements if a.name == name]

    def attribute(self, name, ctx):
        elt = self._element_context(ctx)
        if elt and name in self.d.elements[elt].attributes:
            return format_thing(self.d.elements[elt].attributes[name])
        if name in self.d.common_attributes:
            return format_thing(self.d.common_attributes[name])
        attrs = self._attrs_in_categories(name) + self._common_for_elements(name)
        if len(attrs) == 1:
            return format_thing(attrs[0])
        if len(attrs) > 1:
            return error('ambiguous attribute "%s"' % name, self.warnings, ctx.where())
        return error('unknown attribute "%s"' % name, self.warnings, ctx.where())

    def property(self, name, ctx, omit_quotes=False):
        if name not in self.d.properties:
            return error('unknown property "%s"' % name, self.warnings, ctx.where())
        return format_thing(self.d.properties[name], omit_quotes)

    def presentation_attribute(self, name, ctx):
        if name not in self.d.presentation_attributes:
            return error('unknown presentation attribute "%s"' % name, self.warnings, ctx.where())
        return format_thing(self.d.presentation_attributes[name])

    def symbol(self, name, ctx):
        if name not in self.d.symbols:
            return error('unknown symbol "%s"' % name, self.warnings, ctx.where())
        return format_thing(self.d.symbols[name])

    def interface(self, name, ctx):
        if name not in self.d.interfaces:
            return error('unknown interface "%s"' % name, self.warnings, ctx.where())
        return format_thing(self.d.interfaces[name])

    def term(self, name, ctx):
        if name in self.d.terms:
            return format_thing(self.d.terms[name])
        norm = normalize_term_name(name)
        if norm in self.d.terms:
            return format_thing(self.d.terms[norm])
        if name in self.d.interfaces:
            return format_thing(self.d.interfaces[name])
        iface = ctx.closest_interface()
        if iface and ctx.page_has_id("__svg__%s__%s" % (iface, name)):
            prefix = iface + "::" if ctx.edit_format() == "expanded" else ""
            return Link("member", iface + "/" + name, "#__svg__%s__%s" % (iface, name), text=prefix + name)
        return error('unknown term "%s"' % name, self.warnings, ctx.where())

    def name(self, name, ctx, omit_quotes=False):
        # definitions.js formatNameLink
        elt = self._element_context(ctx)
        element = self.d.elements.get(name)
        attribute = (elt and self.d.elements[elt].attributes.get(name)) or self.d.common_attributes.get(name)
        prop = self.d.properties.get(name)
        if elt and attribute:
            element = None
            prop = None
        if not attribute and not prop:
            attrs = self._attrs_in_categories(name) + self._common_for_elements(name)
            if len(attrs) > 1:
                return error('ambiguous name "%s" (matches multiple attributes)' % name, self.warnings, ctx.where())
            attribute = attrs[0] if attrs else None
        types = [t for t, v in (("element", element), ("attribute", attribute), ("property", prop)) if v]
        if not types:
            return error('unknown element, attribute or property "%s"' % name, self.warnings, ctx.where())
        if len(types) > 1:
            return error('ambiguous name "%s" (matches %s)' % (name, " and ".join(types)), self.warnings, ctx.where())
        return format_thing(element or attribute or prop, omit_quotes)

    def resolve(self, text, ctx):
        """processing.js processLinks, one untyped <a> with text content `text`."""
        omit = ctx.in_proptable_th()
        m = re.match(r"^'(\S+)\s+element'$", text)
        if m:
            return self.element(m.group(1), ctx)
        m = re.match(r"^'(\S+)\s+attribute'$", text)
        if m:
            return self.attribute(m.group(1), ctx)
        m = re.match(r"^'(\S+)\s+property'$", text)
        if m:
            return self.property(m.group(1), ctx, omit)
        m = re.match(r"^'(\S+)\s+presentationattribute'$", text)
        if m:
            return self.presentation_attribute(m.group(1), ctx)
        m = re.match(r"^'([^/]+)/([^/]+)'$", text)
        if m:
            return self.element_attribute(m.group(1), m.group(2), ctx)
        m = re.match(r"^'(\S+)'$", text)
        if m:
            return self.name(m.group(1), ctx, omit)
        m = re.match(r"^([^:]+)::([^:]+)$", text)
        if m:
            iface, member = m.group(1), m.group(2)
            i = self.d.interfaces.get(iface)
            if i and "#" in (i.href or ""):
                before = i.href.split("#")[0]
                prefix = iface + "::" if ctx.edit_format() == "expanded" else ""
                return Link("member", iface + "/" + member, "%s#__svg__%s__%s" % (before, iface, member),
                            text=prefix + member)
            return error('unknown interface name "%s"' % iface, self.warnings, ctx.where())
        m = re.match(r"^<(.*)>$", text, re.S)
        if m:
            return self.symbol(m.group(1), ctx)
        return self.term(text, ctx)


def english_list(items):
    """utils.englishList: [a, b, c] -> a, b and c (as a list of pieces)."""
    out = []
    for i, it in enumerate(items):
        if i:
            out.append(" and " if i == len(items) - 1 else ", ")
        out.append(it)
    return out


def comma_list(items):
    out = []
    for i, it in enumerate(items):
        if i:
            out.append(", ")
        out.append(it)
    return out
