<h2 id="introduction">
Introduction</h2>

<h3 id="AboutSVG">
About SVG</h3>

    This specification defines the features and syntax for
    <a href="http://www.w3.org/Graphics/SVG/">Scalable Vector Graphics
    (SVG)</a>.


    SVG is a language for describing two-dimensional graphics.
    As a standalone format or when mixed with other XML, it uses the
    XML syntax [[!xml]].
    SVG code used inside HTML documents uses the HTML syntax [[!HTML]].
    SVG allows for three types of graphic objects: vector graphic
    shapes (e.g., paths consisting of straight lines and curves),
    images and text. Graphical objects can be grouped, styled,
    transformed and composited.
    The feature set includes nested transformations, clipping
    paths, alpha masks, filter effects and template objects.

    SVG drawings can be [[#interact|interactive]]
    and [[#ScriptElement|dynamic]]. [[#animate|Animations]] can be
    defined and triggered either declaratively (i.e., by embedding SVG
    animation elements in SVG content) or via scripting.

    Sophisticated applications of SVG are possible by use of a
    supplemental scripting language which accesses
    [[#SVGDOMOverview|SVG Document Object Model (DOM)]], which provides
    complete access to all  elements, attributes and properties. A
    rich set of [[#SVGEvents|event handlers]] can be assigned to
    any SVG graphical object. Within a web page, the same scripts can
    work on both HTML and SVG elements. [[#interact|Scripting]] can occur
    in response to various events.

    SVG is useful for rich graphical presentation of information,
    including a number of [[#access|accessibility features that, used correctly]],
    ensure the content can be used by the widest possible audience. But a direct
    link to source data, where possible, is helpful for many people to understand
    the content provided.

<h3 id="W3CCompatibility">
Compatibility with other standards efforts</h3>

    SVG leverages and integrates with other W3C specifications
    and standards efforts, as described in the following:

    <ul>
        <li>
            SVG can be integrated with <a href="https://html.spec.whatwg.org/multipage/">HTML</a> either by using SVG
            in HTML or by using HTML in SVG, in both cases either by
            inclusion or reference.

        <li>
            SVG is an application of XML and is compatible with
            <a href="https://www.w3.org/TR/2008/REC-xml-20081126/">XML 1.0</a> and with the <a href="https://www.w3.org/TR/2009/REC-xml-names-20091208/">Namespaces in XML</a> specification.
            However, when SVG content is included in HTML document,
            the HTML syntax applies and may not be compatible with
            XML. See <a href="https://www.w3.org/TR/svg-integration/">SVG Integration</a> for details.

        <li>
            SVG content is styled with CSS. See [[#styling|Styling with CSS]] for
            details.

        <li>
            SVG includes a complete Document Object Model (DOM) and
            extends <a href="https://dom.spec.whatwg.org/">DOM4</a>. The SVG DOM has a high level of
            compatibility and consistency with the HTML DOM.
            Additionally, the SVG DOM supports and incorporates many
            of the facilities described in the [[cssom|CSS object model]]
            and [[uievents|event handling]].

        <li>
            SVG incorporates some features and approaches that are
            part of <a href="https://www.w3.org/TR/2008/REC-SMIL3-20081201/">SMIL 3</a>, including the <{switch}> element and the
            <{switch/systemLanguage}> attribute.

        <li>
            SVG is compatible with W3C work on internationalization.
            References (W3C and otherwise) include: [[UNICODE]] and 
            [[charmod]].

        <li>
            SVG is compatible with
            <a href="http://www.w3.org/WAI/">W3C work on Web
            Accessibility</a>. See [[#access|Accessibility Support]].
    </ul>

<h3 id="RelationshipToPrevious">
Relationship to previous versions of this standard</h3>

    This edition of the SVG standard has been developed based on, and
    built upon, the 1.1 edition released in 2003. An intermediate
    version of SVG - named <a href="https://www.w3.org/TR/SVGTiny12/">Tiny 1.2</a> - was released
    in 2008. However it did not receive wide acceptance and there have
    been very few implementations of its enhanced feature set. However
    there are some 1.2 features that have been implemented by many SVG
    implementations and those have been incorporated as part of this
    specification. But otherwise, the SVG Working Group consider
    version Tiny 1.2 to be a deprecated branch of the SVG standard.
