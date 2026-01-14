<h2 id="styling">
Styling</h2>

<h3 id="StylingUsingCSS">Styling SVG content using CSS</h3>

<p>Elements in an SVG document can be styled using CSS.
Most visual characteristics and some aspects of element
geometry are controlled using CSS <dfn id="TermProperty" data-dfn-type="dfn">properties</dfn>.
For example, the {{fill}} property controls the paint used to
fill the inside of a shape, and the {{width}} and
{{height}} properties are used to control the size
of a <{rect}> element.

<p>SVG user agents must support all of the CSS styling
mechanisms described in this chapter.

Note: In SVG 1.1, support for inline style sheets
using the {{style element}} element and
{{style attribute}} was not required.  In SVG 2,
these are required.


<h3 id="StyleElement">Inline style sheets: the <span class='element-name'>style</span> element</h3>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Add HTML5 <span class='element-name'>style</span> element attributes to SVG's {{style element}} element.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/28-svg-irc#T18-45-45">SVG 2 <span class='element-name'>style</span> element shall be aligned with the HTML5 <span class='element-name'>style</span> element.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To not surprise authors with different behavior for the <span class='element-name'>style</span> element in HTML and SVG content.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3277">ACTION-3277</a>)</td>
    </tr>
  </table>
</div>

<p>The {{style element}} element allows
style sheets to be embedded directly within SVG content.
SVG's {{style element}} element has the same
attributes as the
<a href="https://html.spec.whatwg.org/multipage/semantics.html#the-style-element">corresponding
element in HTML</a>.

    <div class="element-summary">
      <div class="element-summary-name"><span class="element-name">‘<dfn data-dfn-type="element"
               data-export=""
               id="styling-elementdef-style">style</dfn>’</span></div>
      <dl>
        <dt>Categories:</dt>
        <dd><a href="#render-TermNeverRenderedElement">Never-rendered element</a></dd>
        <dt>Content model:</dt>
        <dd>Character data.</dd>
        <dt>Attributes:</dt>
        <dd>
          <ul class="no-bullets">
            <li><a href="#struct-TermCoreAttribute">core attributes</a><span class="expanding"> — <span
                      class="attr-name">‘<a href="#struct-IDAttribute"><span>id</span></a>’</span>, <span
                      class="attr-name">‘<a
                     href="#struct-SVGElementTabindexAttribute"><span>tabindex</span></a>’</span>, <span
                      class="attr-name">‘<a
                     href="#struct-SVGElementAutofocusAttribute"><span>autofocus</span></a>’</span>, <span
                      class="attr-name">‘<a href="#struct-LangAttribute"><span>lang</span></a>’</span>, <span
                      class="attr-name">‘<a href="#struct-XMLSpaceAttribute"><span>xml:space</span></a>’</span>, <span
                      class="attr-name">‘<a href="#styling-ClassAttribute"><span>class</span></a>’</span>, <span
                      class="attr-name">‘<a href="#styling-StyleAttribute"><span>style</span></a>’</span></span></li>
            <li><a href="https://html.spec.whatwg.org/multipage/webappapis.html#globaleventhandlers">global event
                attributes</a><span class="expanding"> — <span class="attr-name">‘<a
                     href="#interact-EventAttributes"><span>oncancel</span></a>’</span>, <span class="attr-name">‘<a
                     href="#interact-EventAttributes"><span>oncanplay</span></a>’</span>, <span class="attr-name">‘<a
                     href="#interact-EventAttributes"><span>oncanplaythrough</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onchange</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onclick</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onclose</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>oncopy</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>oncuechange</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>oncut</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondblclick</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondrag</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondragend</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondragenter</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondragexit</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondragleave</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondragover</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondragstart</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondrop</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ondurationchange</span></a>’</span>,
                <span class="attr-name">‘<a href="#interact-EventAttributes"><span>onemptied</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onended</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onerror</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onfocus</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>oninput</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>oninvalid</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onkeydown</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onkeypress</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onkeyup</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onload</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onloadeddata</span></a>’</span>,
                <span class="attr-name">‘<a href="#interact-EventAttributes"><span>onloadedmetadata</span></a>’</span>,
                <span class="attr-name">‘<a href="#interact-EventAttributes"><span>onloadstart</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onmousedown</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onmouseenter</span></a>’</span>,
                <span class="attr-name">‘<a href="#interact-EventAttributes"><span>onmouseleave</span></a>’</span>,
                <span class="attr-name">‘<a href="#interact-EventAttributes"><span>onmousemove</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onmouseout</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onmouseover</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onmouseup</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onpaste</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onpause</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onplay</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onplaying</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onprogress</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onratechange</span></a>’</span>,
                <span class="attr-name">‘<a href="#interact-EventAttributes"><span>onreset</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onresize</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onscroll</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onseeked</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onseeking</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onselect</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onshow</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onstalled</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onsubmit</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onsuspend</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>ontimeupdate</span></a>’</span>,
                <span class="attr-name">‘<a href="#interact-EventAttributes"><span>ontoggle</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onvolumechange</span></a>’</span>,
                <span class="attr-name">‘<a href="#interact-EventAttributes"><span>onwaiting</span></a>’</span>, <span
                      class="attr-name">‘<a href="#interact-EventAttributes"><span>onwheel</span></a>’</span></span>
            </li>
            <li><span class="attr-name">‘<a href="#styling-StyleElementTypeAttribute"><span>type</span></a>’</span></li>
            <li><span class="attr-name">‘<a href="#styling-StyleElementMediaAttribute"><span>media</span></a>’</span>
            </li>
            <li><span class="attr-name">‘<a href="#styling-StyleElementTitleAttribute"><span>title</span></a>’</span>
            </li>
          </ul>
        </dd>
        <dt>DOM Interfaces:</dt>
        <dd>
          <ul class="no-bullets">
            <li><a class="idlinterface"
                 href="#styling-InterfaceSVGStyleElement">SVGStyleElement</a></li>
          </ul>
        </dd>
      </dl>
    </div>

<p><em>Attribute definitions:</em>

<dl class="attrdef-list">
  <dt>
    <table class="attrdef def">
      <tr>
        <th>Name</th>
        <th>Value</th>
        <th>Initial value</th>
        <th>Animatable</th>
      </tr>
      <tr>
        <td><dfn id="StyleElementTypeAttribute" data-dfn-type="element-attr" data-dfn-for="style" data-export="">type</dfn></td>
        <td>(see below)</td>
        <td>text/css</td>
        <td>no</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>This attribute specifies the style sheet language of
    the element's contents, as a <a href="http://www.ietf.org/rfc/rfc2046.txt">media type</a>.
    [<a href="refs.html#ref-rfc2046">rfc2046</a>].
    If the attribute is not specified, then the
    style sheet language is assumed to be CSS.
  </dd>
  <dt>
    <table class="attrdef def">
      <tr>
        <th>Name</th>
        <th>Value</th>
        <th>Initial value</th>
        <th>Animatable</th>
      </tr>
      <tr>
        <td><dfn id="StyleElementMediaAttribute" data-dfn-type="element-attr" data-dfn-for="style" data-export="">media</dfn></td>
        <td>(see below)</td>
        <td>all</td>
        <td>no</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>This attribute specifies a media query that must be
    matched for the style sheet to apply.  Its value is parsed
    as a <a href="https://www.w3.org/TR/css3-mediaqueries/#syntax">media_query_list</a>.
    If not specified, the style sheet applies unconditionally.
  </dd>
  <dt>
    <table class="attrdef def">
      <tr>
        <th>Name</th>
        <th>Value</th>
        <th>Initial value</th>
        <th>Animatable</th>
      </tr>
      <tr>
        <td><dfn id="StyleElementTitleAttribute" data-dfn-type="element-attr" data-dfn-for="style" data-export="">title</dfn></td>
        <td>(see below)</td>
        <td>(none)</td>
        <td>no</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>This attribute specifies a title for the style sheet,
    which is used when exposing and selecting between alternate
    style sheets.  The attribute takes any value.
  </dd>
</dl>

<p>The semantics and processing of a {{style element}} and its
attributes must be the same as is defined for the
<a href="https://html.spec.whatwg.org/multipage/semantics.html#the-style-element">HTML
<span class='element-name'>style</span> element</a>.

<p>The style sheet's text content is never directly rendered;
the 'display' value for the {{style element}} element
must always be set to <span class="prop-value">none</span>
by the [=user agent style sheet=],
and this declaration must have importance over any other CSS rule or presentation attribute.



<h3 id="LinkElement">External style sheets: the effect of the HTML <span class='element-name'>link</span> element</h3>

<p>An <a href="https://html.spec.whatwg.org/multipage/semantics.html#the-link-element">HTML
<span class='element-name'>link</span> element</a> in an SVG document (that is,
an element in the HTML namespace with local name "link")
with its <span class="attr-name">rel</span>
attribute set to <code class='attr-value'>stylesheet</code> must be processed
as defined in the HTML specification and cause external style sheets to be
loaded and applied to the document.  Such elements in HTML documents outside
of an inline SVG fragment must also apply to the SVG content.

<p class='note'>Because the element is required to be in the HTML namespace, it
is not possible for an <a href="https://html.spec.whatwg.org/multipage/semantics.html#the-link-element">HTML
<span class='element-name'>link</span> element</a> to be parsed as
part of an inline SVG fragment in a text/html document.  However, when
parsing an SVG document using XML syntax, XML namespace declarations
can be used to place the element in the HTML namespace.

<div class='note'>
  <p>Note that an alternative way to reference external style sheets
  without using the <a href="https://html.spec.whatwg.org/multipage/semantics.html#the-link-element">HTML
  <span class='element-name'>link</span> element</a> is to use an @import
  rule in an inline style sheet.  For example:

<xmp>
<svg xmlns="http://www.w3.org/2000/svg">
  <style>
    @import url(mystyles.css);
  </style>
  <rect .../>
</svg>
</xmp>

  <p>would behave similarly to:

<xmp>
<svg xmlns="http://www.w3.org/2000/svg">
  <link xmlns="http://www.w3.org/1999/xhtml" rel="stylesheet" href="mystyles.css" type="text/css"/>
  <rect .../>
</svg>
</xmp>

  <p>Or, in XML documents, external CSS style sheets may be included using the
  <a href="https://www.w3.org/TR/xml-stylesheet">&lt;?xml-stylesheet?&gt;</a>
  processing instruction [<a href='refs.html#ref-xml-stylesheet'>xml-stylesheet</a>].
</div>

<h3 id="StyleSheetsInHTMLDocuments">Style sheets in HTML documents</h3>

<p>When an SVG {{style element}} or an HTML
<span class="attr-name">style</span> element is used in an HTML
document, those style sheets must apply to all HTML and
inline SVG content in the document.  Similarly, any HTML
<span class="attr-name">style</span> element used in an SVG
document must also apply its style sheet to the document.

<h3 id="ElementSpecificStyling">Element-specific styling: the <span class="attr-name">class</span> and <span class="attr-name">style</span> attributes</h3>

<p>As with HTML, SVG supports the <a element-attr for="core-attributes">class</a> and {{style attribute}}
attributes on all elements to support element-specific styling.

<p><em>Attribute definitions:</em>

<dl class='attrdef-list'>
  <dt>
    <table class="attrdef def">
      <tr>
        <th>Name</th>
        <th>Value</th>
        <th>Initial value</th>
        <th>Animatable</th>
      </tr>
      <tr>
        <td><dfn id="ClassAttribute" data-dfn-for="core-attributes" data-dfn-type="element-attr">class</dfn></td>
        <td>[=set of space-separated tokens=] <span class="syntax">&bs[;HTML]</span></td>
        <td>(none)</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>The <a element-attr for="core-attributes">class</a> attribute assigns one or more class names to an element,
    which can then be used for addressing by the styling language.
  </dd>
  <dt>
    <table class="attrdef def">
      <tr>
        <th>Name</th>
        <th>Value</th>
        <th>Initial value</th>
        <th>Animatable</th>
      </tr>
      <tr>
        <td><dfn id="StyleAttribute" data-dfn-for="core-attributes" data-dfn-type="element-attr">style</dfn></td>
        <td>(see below)</td>
        <td>(none)</td>
        <td>no</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>The {{style attribute}} attribute is used to supply a
    CSS declaration of an element.  The attribute is
    <a href="https://www.w3.org/TR/2013/REC-css-style-attr-20131107/#syntax">parsed as a declaration-list</a>.
  </dd>
</dl>

<p>Aside from the way that the <a element-attr for="core-attributes">class</a> attribute is reflected in the
SVG DOM (in the <a href="types.html#__svg__SVGElement__className">className</a>
IDL attribute on [[#InterfaceSVGElement|SVGElement]]), the semantics and behavior of the
<a element-attr for="core-attributes">class</a> and {{style attribute}} attributes must be the same
as that for <a href="https://html.spec.whatwg.org/multipage/dom.html#global-attributes">the corresponding
attributes in HTML</a>.

<div class='example'>
  <p>In the following example, the {{text}} element is used in
  conjunction with the <a element-attr for="core-attributes">class</a>
  attribute to markup document messages. Messages appear in both
  English and French versions.

  <pre>
&lt;!-- English messages --&gt;
&lt;text class="info" lang="en"&gt;Variable declared twice&lt;/text&gt;
&lt;text class="warning" lang="en"&gt;Undeclared variable&lt;/text&gt;
&lt;text class="error" lang="en"&gt;Bad syntax for variable name&lt;/text&gt;
&lt;!-- French messages --&gt;
&lt;text class="info" lang="fr"&gt;Variable déclarée deux fois&lt;/text&gt;
&lt;text class="warning" lang="fr"&gt;Variable indéfinie&lt;/text&gt;
&lt;text class="error" lang="fr"&gt;Erreur de syntaxe pour variable&lt;/text&gt;</pre>

  <p>The following CSS style
  rules would tell visual user agents to display informational
  messages in green, warning messages in yellow, and error
  messages in red:

  <pre>
text.info    { fill: green; }
text.warning { fill: yellow; }
text.error   { fill: red; }</pre>
</div>

<div class='example'>
  <p>This example shows how the {{style attribute}} attribute can be
  used to style {{text}} elements similarly to the previous example:

  <pre>
&lt;text style="fill: green;" lang="en"&gt;Variable declared twice&lt;/text&gt;
&lt;text style="fill: yellow;" lang="en"&gt;Undeclared variable&lt;/text&gt;
&lt;text style="fill: red;" lang="en"&gt;Bad syntax for variable name&lt;/text&gt;</pre>
</div>


<h3 id="PresentationAttributes">Presentation attributes</h3>

<p>Some styling properties can be specified not only in style sheets
and {{style attribute}} attributes, but also in
<dfn id="TermPresentationAttribute" data-dfn-type="dfn" data-export="">presentation attributes</dfn>.
These are attributes whose name matches (or is similar to) a given CSS property
and whose value is parsed as a value of that property. Presentation
attributes contribute to the
<a href="https://drafts.csswg.org/css-cascade-3/#preshint">author level</a>
of the cascade, followed by all other author-level style sheets,
and have specificity 0.

<p>Since presentation attributes are parsed as CSS values, not declarations, an
<a href="https://www.w3.org/TR/2011/REC-CSS2-20110607/cascade.html#important-rules"><span class="prop-value">!important</span> declaration</a>
within a presentation attribute will cause it to have an [=invalid value=].
See <a href="types.html#presentation-attribute-css-value">Attribute syntax</a>
for details on how presentation attributes are parsed.

<p>Not all style properties that can affect SVG rendering have a corresponding
presentation attribute.
Other attributes (which happen to share the name of a style property) must not be parsed as a
presentation attribute and must not affect CSS cascading and inheritance.
Also, only elements in the SVG namespace support presentation attributes.
Most SVG presentation attributes may be specified on any element in the SVG namespace
where there is not a name clash with an existing attribute.
However, the [=geometry properties=] only have equivalent presentation attributes
on designated elements.
Attributes of the same name on other elements must not affect CSS cascading and inheritance.

<p>
Except as noted in the table for the [[#TransformProperty|transform]] presentation attributes,
the presentation attribute name is the same as the property name, in lower-case letters.


<table class="vert" style="font-size: 90%">
  <tr>
    <th style="width: 50%">Properties with a presentation attribute</th>
    <th style="width: 50%">Elements that support the presentation attribute</th>
  </tr>
   <tr>
    <td>
      {{cx}},
      {{cy}}
    </td>
    <td>
      {{circle}} and {{ellipse}}
    </td>
  </tr>
  <tr>
    <td>
      {{height}}, {{width}}, {{x}}, {{y}}
    </td>
    <td>
      <{foreignObject}>,
      {{image}},
      <{rect}>,
      <{svg}>,
      <{symbol}>, and
      <{use}>
    </td>
  </tr>
  <tr>
    <td>
      {{r}}
    </td>
    <td>
      {{circle}}
    </td>
  </tr>
  <tr>
    <td>
      {{rx}}, {{ry}}
    </td>
    <td>
      {{ellipse}} and <{rect}>
    </td>
  </tr>
  <tr>
    <td>
      {{d}}
    </td>
    <td>
      {{path}}
    </td>
  </tr>
  <tr>
    <td>
      {{fill}}
    </td>
    <td>
      Any element in the SVG namespace except for <a href="https://svgwg.org/specs/animations/#TermAnimationElement">animation elements</a>,
      which have a different <{animate/fill}> attribute.
    </td>
  </tr>
  <tr>
    <td>
      [[#TransformProperty|transform]]
    </td>
    <td>
      For historical reasons, the [[#TransformProperty|transform]] property gets represented by different presentation attributes depending on the SVG element it applies to:
      <dl>
        <dt>[[#TransformProperty|transform]]</dt>
        <dd>
          Any element in the SVG namespace with the exception of the {{pattern}},
          {{linearGradient}} and {{radialGradient}} elements.
        </dd>
        <dt><{pattern/patternTransform}></dt>
        <dd>
            <{pattern}}. {{pattern/patternTransform}> gets mapped to the
            [[#TransformProperty|transform]] CSS property
            [<a href='refs.html#ref-css-transforms-1'>css-transforms-1</a>].
        </dd>
        <dt><{linearGradient/gradientTransform}></dt>
        <dd>
            {{linearGradient}} and {{radialGradient}} elements.
            <{linearGradient/gradientTransform}> gets mapped to the [[#TransformProperty|transform]]
            CSS property [<a href='refs.html#ref-css-transforms-1'>css-transforms-1</a>].
        </dd>
      </dl>
    </td>
  </tr>
  <tr>
    <td>
      {{alignment-baseline}},
      {{baseline-shift}},
      {{clip-path}},
      {{clip-rule}},
      {{color}},
      {{color-interpolation}},
      {{color-interpolation-filters}},
      {{cursor property}},
      {{direction}},
      'display',
      {{dominant-baseline}},
      'fill-opacity',
      'fill-rule',
      {{filter property}},
      {{flood-color}},
      {{flood-opacity}},
      {{font-family}},
      {{font-size}},
      {{font-size-adjust}},
      {{font-stretch}},
      {{font-style}},
      {{font-variant}},
      {{font-weight}},
      {{glyph-orientation-vertical}},
      [[SVG2#ImageRendering|image-rendering]],
      {{letter-spacing}},
      {{lighting-color}},
      {{marker-end}},
      {{marker-mid}},
      {{marker-start}},
      {{mask property}},
      {{mask-type}},
      {{opacity}},
      [[#OverflowAndClipProperties|overflow]],
      [=paint-order=],
      {{pointer-events}},
      {{shape-rendering}},
      {{stop-color}},
      'stop-opacity',
      {{stroke}},
      {{stroke-dasharray}},
      {{stroke-dashoffset}},
      {{stroke-linecap}},
      {{stroke-linejoin}},
      {{stroke-miterlimit}},
      'stroke-opacity',
      {{stroke-width}},
      {{text-anchor}},
      {{text-decoration}},
      {{text-overflow}},
      {{text-rendering}},
      {{transform-origin}},
      {{unicode-bidi}},
      {{vector-effect}},
      'visibility',
      {{white-space}},
      {{word-spacing}},
      {{writing-mode}}
    </td>
    <td>
      Any element in the SVG namespace.
    </td>
  </tr>
</table>

<p class='note'>Note that
<span class="attr-name">cx</span>,
<span class="attr-name">cy</span>,
<span class="attr-name">r</span>,
<span class="attr-name">x</span>,
<span class="attr-name">y</span>,
<span class="attr-name">width</span> and
<span class="attr-name">height</span> attributes are not
always presentation attributes.
For example, the <{tspan/x}> attribute on {{text}} and {{tspan}}
is not a presentation attribute for the {{x}} property,
and the <{radialGradient/r}> attribute on a {{radialGradient}}
is not a presentation attribute for the {{r}} property.


<!--
<p>The following table lists the presentation attributes whose
names are different from their corresponding property.  All
other presentation attributes have names that do match
their property.

<table class='vert' style='font-size: 90%'>
  <tr><th>Property</th><th>Element</th><th>Presentation attribute name</th></tr>
  <tr><td>[[#TransformProperty|transform]]</td><td>{{linearGradient}} and {{radialGradient}}</td><td><span class="attr-name">gradientTransform</span></td></tr>
  <tr><td>[[#TransformProperty|transform]]</td><td>{{pattern}}</td><td><span class="attr-name">patternTransform</span></td></tr>
</table>
-->

<p class='note'>In the future, any new properties that apply
to SVG content will not gain presentation attributes.  Therefore,
authors are suggested to use styling properties, either through
inline {{style attribute}} properties or style sheets,
rather than presentation attributes, for styling SVG content.

<p>Animation of presentation attributes is equivalent to
animating the corresponding property.

<h3 id="RequiredProperties">Required properties</h3>

<p>The following properties must be supported by all SVG user agents:

<ul>
  <li>all properties defined in this specification</li>

  <li>the 'display', [[#OverflowAndClipProperties|overflow]] and 'visibility' properties
    [<a href='refs.html#ref-css2'>CSS2</a>]</li>

  <li>the {{cursor property}} and {{text-overflow}} property
    [<a href='refs.html#ref-css-overflow-3'>css-overflow-3</a>]</li>

  <li>the {{clip-path}}, {{clip-rule}} and
    {{mask property}} properties
    [<a href='refs.html#ref-css-masking-1'>css-masking-1</a>]</li>

  <li>the {{color}} and {{opacity}} properties
    [<a href='refs.html#ref-css-color-3'>css-color-3</a>]</li>

  <li>the {{color-interpolation-filters}}, {{filter property}},
    {{flood-color}}, {{flood-opacity}}
    and {{lighting-color}} properties
    [<a href='refs.html#ref-filter-effects-1'>filter-effects-1</a>]</li>

  <li>the {{isolation property}} property
    [<a href='refs.html#ref-compositing-1'>compositing-1</a>]</li>

  <li>the [[#TransformProperty|transform]], {{transform-box}} and {{transform-origin}} properties
    [<a href='refs.html#ref-css-transforms-1'>css-transforms-1</a>]</li>

  <li>the {{letter-spacing}}, {{text-align}},
    {{text-align-last}}, {{text-indent}}
    and {{word-spacing}} properties
    [<a href='refs.html#ref-css-text-3'>css-text-3</a>]</li>

  <li>the {{white-space}} property
    [<a href='refs.html#ref-css-text-4'>css-text-4</a>]</li>

  <li>the {{vertical-align}}, {{dominant-baseline}},
    {{alignment-baseline}}, and {{baseline-shift}} properties
    [<a href='refs.html#ref-css-inline-3'>css-inline-3</a>]</li>

  <li>the {{direction}}, {{text-orientation}} and
    {{writing-mode}} properties
    [<a href='refs.html#ref-css-writing-modes-3'>css-writing-modes-3</a>]</li>

  <li>the {{font}}, {{font-family}}, {{font-feature-settings}},
    {{font-kerning}}, {{font-size}}, {{font-size-adjust}},
    {{font-stretch}}, {{font-style}}, {{font-variant}} (along with its subproperties)
    and {{font-weight}} properties
    [<a href='refs.html#ref-css-fonts-3'>css-fonts-3</a>]</li>

  <li>the {{text-decoration}}, {{text-decoration-line}}, {{text-decoration-style}}
    and {{text-decoration-color}} properties
    [<a href='refs.html#ref-css-text-decor-3'>css-text-decor-3</a>]</li>

</ul>


<h3 id="UAStyleSheet">User agent style sheet</h3>

<p>The following <a href="https://www.w3.org/TR/2011/REC-CSS2-20110607/cascade.html#cascade">user
agent style sheet</a> must be applied in all SVG user agents.

<pre>
@namespace url(http://www.w3.org/2000/svg);
@namespace xml url(http://www.w3.org/XML/1998/namespace);

svg:not(:root), image, marker, pattern, symbol { overflow: hidden; }

*:not(svg),
*:not(foreignObject) > svg {
  transform-origin: 0 0;
}

*[xml|space=preserve] {
  white-space-collapse: preserve-spaces;
}

defs,
clipPath, mask, marker,
desc, title, metadata,
pattern, linearGradient, radialGradient,
script, style,
symbol {
  display: none !important;
}
:host(use) > symbol {
  display: inline !important;
}
:link, :visited {
  cursor: pointer;
}
</pre>

<p>
  In addition,
  all interactive user agents are required
  to apply distinctive styles to
  the <code>:focus</code> pseudo-class
  (normally using the <code>outline</code> property)
  and the <code>::selection</code> pseudo-element
  (using an appropriate highlighting technique,
    such as redrawing the selected glyphs with inverse colors).


Note: 
An <code>!important</code> rule in a user agent stylesheet
<a href="https://www.w3.org/TR/css-cascade-4/#importance">over-rides all user and author styles</a>
[<a href="refs.html#ref-css-cascade-4">css-cascade-4</a>].
The display value for [=never-rendered elements=]
and for <{symbol}> elements
can therefore not be changed.
A symbol must only be rendered if it is the direct child
of a shadow root whose host is a <{use}> element
(and must always be rendered if the host <{use}> element is rendered).
The other elements, and their child content, are never rendered directly.


<p class='note'>CSS Transforms defines that the initial value for
{{transform-origin}} is <span class='prop-value' style='white-space: nowrap'>50% 50%</span>.
Since elements in SVG must, by default, transform around their origin at (0, 0),
{{transform-origin}} is overridden and set to a default value of
<span class='prop-value' style='white-space: nowrap'>0 0</span> for all SVG elements
(except for root <{svg}> elements and <{svg}> elements that are the child of a
<{foreignObject}> element or an element in a non-SVG namespace; these elements
must transform around their center).
[<a href="refs.html#ref-css-transforms-1">css-transforms-1</a>]

<div class="note">
  <p>The OpenType specification
    <a href="https://www.microsoft.com/typography/otspec/svg.htm">requires an additional user agent style sheet</a>
    to be applied when processing
    [<a href="refs.html#ref-opentype">OPENTYPE</a>].
    It is as follows:
  

  <pre style="background-color: #eee; padding: 0.5em">@namespace svg url(http://www.w3.org/2000/svg);

svg|text, svg|foreignObject {
  display: none !important;
}

:root {
  fill: context-fill;
  fill-opacity: context-fill-opacity;
  stroke: context-stroke;
  stroke-opacity: context-stroke-opacity;
  stroke-width: context-value;
  stroke-dasharray: context-value;
  stroke-dashoffset: context-value;
}</pre>

  <p>The [=context-fill=] and [=context-stroke=] keywords
    are as defined in this specification,
    where the [=context element=] for a font glyph
    is the corresponding [=text content element=].
    The other keywords are as defined in the OpenType specification,
    and ensure that the style values from the [=text content element=]
    are propagated to the font glyphs,
    with appropriate adjustments for the change in the coordinate system
    [<a href="refs.html#ref-opentype">OPENTYPE</a>].
  
</div>

<h3 id="RequiredCSSFeatures">Required CSS features</h3>

<p>Besides the features described above, the following CSS features must be
also supported in SVG user agents:

<ul>
  <li>in XML documents, external CSS style sheets using the
  <a href="https://www.w3.org/TR/xml-stylesheet">&lt;?xml-stylesheet?&gt;</a>
  processing instruction [<a href='refs.html#ref-xml-stylesheet'>xml-stylesheet</a>]</li>

  <li><a href="https://www.w3.org/TR/2011/REC-CSS2-20110607/media.html#at-media-rule">@media</a>,
  <a href="https://www.w3.org/TR/2011/REC-CSS2-20110607/cascade.html#at-import">@import</a>
  and <a href="https://www.w3.org/TR/2011/REC-CSS2-20110607/syndata.html#charset">@charset</a>
  rules within style sheets, as defined in CSS 2.1</li>

  <li><a href="https://www.w3.org/TR/2011/WD-css3-fonts-20111004/#font-face-rule">@font-face</a> rules
  within style sheets [<a href="refs.html#ref-css-fonts-3">css-fonts-3</a>]</li>

  <li>all pseudo-classes defined in CSS 2.1 (including :hover, :link, :active, :visited, :focus, :first-child and :lang)</li>

  <li>the ::first-letter and ::first-line pseudo-elements defined in CSS 2.1 (on {{text}} elements)</li>
</ul>



<h3 id="DOMInterfaces">DOM interfaces</h3>

<h4 id="InterfaceSVGStyleElement">Interface SVGStyleElement</h4>



<p>An [[#InterfaceSVGStyleElement|SVGStyleElement]] object represents a {{style element}} element
in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGStyleElement</b> : <a>SVGElement</a> {
  attribute DOMString <a href="styling.html#__svg__SVGStyleElement__type">type</a>;
  attribute DOMString <a href="styling.html#__svg__SVGStyleElement__media">media</a>;
  attribute DOMString <a href="styling.html#__svg__SVGStyleElement__title">title</a>;
  attribute boolean <a href="styling.html#__svg__SVGStyleElement__disabled">disabled</a>;
};

<a>SVGStyleElement</a> includes <a>LinkStyle</a>;
</pre>

<p>The <b id="__svg__SVGStyleElement__type">type</b>,
<b id="__svg__SVGStyleElement__media">media</b> and
<b id="__svg__SVGStyleElement__title">title</b> IDL attributes
[=reflect=] the {{type}}, {{media}} and {{title}}
content attributes, respectively.
