"""svgdefs.py: reading the definitions files and resolving untyped links the
way tools/publish/definitions.js and processing.js do."""

import unittest

from . import helpers

svgdefs = helpers.load("svgdefs.py")

MASTER = helpers.fixture("src", "master")
INFOS = [
    dict(path=MASTER + "/definitions.xml", base=None, specid=None, mainspec=None),
    dict(path=MASTER + "/definitions-other.xml",
         base="https://drafts.csswg.org/filter-effects-1/", specid="FX", mainspec=None),
]


class FakeCtx(object):
    """Stands in for convert.Ctx: what the resolver may ask about one <a>."""

    def __init__(self, with_element=None, interface=None, page_ids=(), fmt=None, proptable_th=False):
        self._with = with_element
        self._iface = interface
        self._ids = set(page_ids)
        self._fmt = fmt
        self._th = proptable_th

    def where(self):
        return "test.html"

    def with_element(self):
        return self._with

    def closest_interface(self):
        return self._iface

    def page_has_id(self, i):
        return i in self._ids

    def edit_format(self):
        return self._fmt

    def in_proptable_th(self):
        return self._th


class HelperTests(unittest.TestCase):
    def test_split_list(self):
        self.assertEqual(svgdefs.split_list("a, b,c"), ["a", "b", "c"])
        self.assertEqual(svgdefs.split_list(""), [])
        self.assertEqual(svgdefs.split_list(None), [])

    def test_resolve_url(self):
        r = svgdefs.resolve_url
        self.assertEqual(r(None, "shapes.html#x"), "shapes.html#x")
        self.assertEqual(r("https://example.org/spec/", "#frag"), "https://example.org/spec/#frag")
        self.assertEqual(r("https://example.org/spec/a.html#old", "#new"), "https://example.org/spec/a.html#new")
        self.assertEqual(r("https://example.org/spec/a.html", "b.html#x"), "https://example.org/spec/b.html#x")
        self.assertEqual(r("https://example.org/", "https://other.org/#x"), "https://other.org/#x")
        self.assertIsNone(r("https://example.org/", None))
        with self.assertRaises(ValueError):
            r("https://example.org/", "/absolute")

    def test_normalize_term_name(self):
        self.assertEqual(svgdefs.normalize_term_name("  User\n  Agent "), "user agent")

    def test_english_and_comma_lists(self):
        self.assertEqual("".join(svgdefs.english_list(["a"])), "a")
        self.assertEqual("".join(svgdefs.english_list(["a", "b"])), "a and b")
        self.assertEqual("".join(svgdefs.english_list(["a", "b", "c"])), "a, b and c")
        self.assertEqual("".join(svgdefs.comma_list(["a", "b", "c"])), "a, b, c")


class LoadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defs, cls.by_spec = svgdefs.load(INFOS)

    def test_elements(self):
        d = self.defs
        self.assertEqual(sorted(d.elements), ["circle", "desc", "rect", "script"])
        rect = d.elements["rect"]
        self.assertEqual(rect.href, "shapes.html#RectElement")
        self.assertEqual(rect.content_model, "anyof")
        self.assertEqual(rect.element_categories, ["descriptive"])
        self.assertEqual(rect.elements, ["script"])
        self.assertEqual(rect.attribute_categories, ["core", "presentation"])
        self.assertEqual(rect.geometry_properties, ["x", "width"])
        self.assertEqual(rect.interfaces, ["SVGRectElement"])
        self.assertEqual([a.name for a in rect.specific_attributes], ["rx"])
        self.assertTrue(rect.specific_attributes[0].animatable)
        self.assertIsNone(rect.content_model_description)
        # a hand-written content model is kept as an XML element
        self.assertIsNotNone(d.elements["script"].content_model_description)

    def test_attribute_order_on_element(self):
        # categories first, then attributes common to listed elements, then
        # the element's common attributes, then its own (definitions.js)
        self.assertEqual(self.defs.elements["rect"].attribute_order,
                         ["id", "class", "dup", "x", "pathLength", "rx"])

    def test_element_categories_resolved_on_elements(self):
        d = self.defs
        self.assertEqual(sorted(d.element_categories), ["descriptive", "shape"])
        self.assertEqual(d.element_categories["shape"].elements, ["rect", "circle"])
        self.assertIn("shape", d.elements["rect"].categories)
        self.assertNotIn("shape", d.elements["desc"].categories)

    def test_common_attributes(self):
        d = self.defs
        self.assertEqual(list(d.common_attributes), ["pathLength"])
        self.assertEqual([a.name for a in d.common_attributes_for_elements], ["x"])
        self.assertEqual(d.common_attributes_for_elements[0].elements, {"rect": True})

    def test_attribute_categories(self):
        d = self.defs
        core = d.attribute_categories["core"]
        self.assertEqual([a.name for a in core.attributes], ["id", "class", "dup"])
        self.assertIs(core.attributes[0].category, core)
        pres = d.attribute_categories["presentation"]
        self.assertEqual(pres.presentation_attribute_names, ["fill"])

    def test_properties_and_presentation_attributes(self):
        d = self.defs
        self.assertIn("filter", d.properties)
        pa = d.presentation_attributes["fill"]
        self.assertEqual(pa.kind, "attribute")
        self.assertEqual(pa.property, "fill")

    def test_base_url_applied(self):
        self.assertEqual(self.defs.properties["filter"].href,
                         "https://drafts.csswg.org/filter-effects-1/#FilterProperty")

    def test_first_listed_file_wins(self):
        # 'fill' is in both files; definitions.xml is listed first in publish.xml
        self.assertEqual(self.defs.properties["fill"].href, "shapes.html#FillProperty")

    def test_interfaces_symbols_terms(self):
        d = self.defs
        self.assertEqual(d.interfaces["SVGRectElement"].href, "shapes.html#InterfaceSVGRectElement")
        self.assertEqual(d.symbols["length"].href, "intro.html#DataTypeLength")
        self.assertIn("user agent", d.terms)
        self.assertIn("anim.", d.terms)            # normalized copy
        self.assertIsNone(d.terms["user agent"].markup)
        self.assertIsNotNone(d.terms["CTM"].markup)  # term with its own markup

    def test_definitions_by_spec(self):
        self.assertEqual(sorted(self.by_spec), ["FX"])
        self.assertEqual(sorted(self.by_spec["FX"].properties), ["fill", "filter"])


class ResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.defs, _ = svgdefs.load(INFOS)

    def setUp(self):
        self.warnings = []
        self.r = svgdefs.Resolver(self.defs, self.warnings)

    def resolve(self, text, **kw):
        return self.r.resolve(text, FakeCtx(**kw))

    def test_quoted_element_name(self):
        link = self.resolve("'rect'")
        self.assertEqual((link.kind, link.name, link.href), ("element", "rect", "shapes.html#RectElement"))
        self.assertEqual(link.wrap, "element-name")
        self.assertTrue(link.quotes)

    def test_quoted_property_name(self):
        link = self.resolve("'fill'")
        self.assertEqual((link.kind, link.a_class), ("property", "property"))
        self.assertEqual(link.href, "shapes.html#FillProperty")

    def test_quoted_attribute_name(self):
        link = self.resolve("'pathLength'")
        self.assertEqual((link.kind, link.wrap), ("attribute", "attr-name"))
        self.assertEqual(link.href, "shapes.html#PathLengthAttribute")
        # an attribute found in exactly one category
        self.assertEqual(self.resolve("'lone'").href, "intro.html#LoneAttribute")

    def test_name_that_is_attribute_and_property(self):
        # 'x' is an attribute of rect only and a property: outside
        # <edit:with element=rect> it is the property, inside it the attribute
        link = self.resolve("'x'")
        self.assertEqual((link.kind, link.href), ("property", "shapes.html#XProperty"))
        link = self.resolve("'x'", with_element="rect")
        self.assertEqual((link.kind, link.href), ("attribute", "shapes.html#RectElementXAttribute"))

    def test_ambiguous_attribute_in_two_categories(self):
        link = self.resolve("'dup'")
        self.assertEqual(link.kind, "error")
        self.assertTrue(self.warnings)
        self.assertEqual(link.text, "@@ " + link.message)

    def test_element_slash_attribute(self):
        link = self.resolve("'rect/rx'")
        self.assertEqual((link.kind, link.href), ("attribute", "shapes.html#RectElementRXAttribute"))
        self.assertEqual(self.resolve("'rect/nope'").kind, "error")

    def test_explicit_kind_forms(self):
        self.assertEqual(self.resolve("'rect element'").kind, "element")
        self.assertEqual(self.resolve("'fill property'").kind, "property")
        self.assertEqual(self.resolve("'lone attribute'").href, "intro.html#LoneAttribute")
        pa = self.resolve("'fill presentationattribute'")
        self.assertEqual(pa.kind, "attribute")
        self.assertIn("Presentation attribute for property", pa.title)

    def test_proptable_header_omits_quotes(self):
        link = self.resolve("'rect'", proptable_th=True)
        self.assertFalse(link.quotes)

    def test_terms(self):
        link = self.resolve("user agent")
        self.assertEqual((link.kind, link.href), ("term", "intro.html#TermUserAgent"))
        # case and spaces do not matter
        self.assertEqual(self.resolve("User\n Agent").href, "intro.html#TermUserAgent")
        # a term with its own markup keeps it, and has no plain text
        ctm = self.resolve("CTM")
        self.assertIsNotNone(ctm.markup)
        self.assertIsNone(ctm.text)

    def test_interface_name_as_term(self):
        link = self.resolve("SVGRectElement")
        self.assertEqual((link.kind, link.a_class), ("interface", "idlinterface"))

    def test_interface_member(self):
        link = self.resolve("SVGRectElement::x")
        self.assertEqual((link.kind, link.href), ("member", "shapes.html#__svg__SVGRectElement__x"))
        self.assertEqual(link.text, "x")
        expanded = self.resolve("SVGRectElement::x", fmt="expanded")
        self.assertEqual(expanded.text, "SVGRectElement::x")
        self.assertEqual(self.resolve("NoSuch::x").kind, "error")

    def test_member_found_through_closest_interface(self):
        link = self.resolve("frob", interface="SVGRectElement",
                            page_ids=["__svg__SVGRectElement__frob"])
        self.assertEqual((link.kind, link.href), ("member", "#__svg__SVGRectElement__frob"))

    def test_symbol(self):
        link = self.resolve("<length>")
        self.assertEqual((link.kind, link.text), ("symbol", "<length>"))
        self.assertEqual(self.resolve("<nosuch>").kind, "error")

    def test_failure(self):
        link = self.resolve("no such words")
        self.assertEqual(link.kind, "error")
        self.assertEqual(link.message, 'unknown term "no such words"')
        self.assertEqual(self.warnings[-1], ("test.html", 'unknown term "no such words"'))
        self.assertEqual(self.resolve("'nosuchthing'").kind, "error")

    def test_unknown_with_element_warns_and_is_ignored(self):
        link = self.resolve("'pathLength'", with_element="nosuch")
        self.assertEqual(link.kind, "attribute")
        self.assertIn('unknown element "nosuch" in edit:with', self.warnings[0][1])

    def test_element_category_link_text(self):
        cat = self.defs.element_categories["shape"]
        self.assertEqual(svgdefs.format_thing(cat).text, "shape element")
        self.assertEqual(svgdefs.format_thing(cat, capitalize=True).text, "Shape element")
        acat = self.defs.attribute_categories["core"]
        self.assertEqual(svgdefs.format_thing(acat).text, "core attributes")


if __name__ == "__main__":
    unittest.main()
