<h2 id="linking">Linking</h2>

<div class="ready-for-WG-review">
<h3 id="URLReference">References</h3>
<h4 id="HeadOverview">Overview</h4>

    On the Web, resources are identified using [=URLs=]
    (Internationalized Resource Identifiers). For
    example, an SVG file called <code>someDrawing.svg</code> located 
    at <code>http://example.com</code> might have the following 
    [=URL=]:

    <pre>
    http://example.com/someDrawing.svg
    </pre>

    An [=URL=] can also address a particular element within an XML
    document by including an [=URL=] fragment identifier as part of
    the [=URL=]. An [=URL=] which includes an [=URL=] 
    fragment identifier consists of an optional base [=URL=], 
    followed by a "<code>#</code>" character, followed by the 
    [=URL=] fragment identifier. For example, the following 
    [=URL=] can be used to specify the element whose 
    <code>ID</code> is "<code>Lamppost</code>" within file <code>someDrawing.svg</code>:

    <pre>
    http://example.com/someDrawing.svg#Lamppost
    </pre>

<!-- from 1.2T - add this too?

<h5 id="AlteringHref">Altering the <span class="attr-name">href</span> attribute</h5>

<p>If the <a href="https://svgwg.org/specs/animations/#HrefAttribute"><span class="attr-name">href</span></a>
attribute of an element in the tree is altered by any means (e.g. script, declarative
animation) such that a new resource is referenced, the new resource must replace
the existing resource, and must be rendered as appropriate.  For specific effects
on the scripting context when a {{script}} element's
{{script/href}} attribute is altered, see
<a href="interact.html#ScriptContentProcessing">Script processing</a>.

-->

<h4 id="linking-definitions">
Definitions</h4>

    <dl class='definitions'>
        <dt><dfn dfn export>URL reference</dfn>
        <dd>
            An URL reference is an Internationalized Resource 
            Identifier, as defined in Internationalized Resource 
            Identifiers [[rfc3987]]. See [=URL reference=] and
    <a href="struct.html#Head">References and the
    <span class="element-name">defs</span> element</a>.</dd>

    <dt><dfn id="TermURLReferenceWithFragmentIdentifier" data-dfn-type="dfn" data-export="">URL reference with fragment identifier</dfn></dt>
    <dd>An Internationalized Resource Identifier [<a href="refs.html#ref-rfc3987">rfc3987</a>] that
    can include an &lt;absoluteURL&gt; or
    &lt;relativeURL&gt; and a identifier of the fragment in that resource. See <a href="struct.html#Head">References and the
    <span class="element-name">defs</span> element</a>. URL reference with fragment identifiers are commonly used to reference <a href="pservers.html">paint servers</a>.</dd>

    <dt><dfn export>external file reference</dfn>
    <dd>A [=URL reference=] or [=URL reference with fragment identifier=]
      which refers to a resource that is not part of the current document.
    </dd>

    <dt><dfn id="TermSameDocumentURL" data-dfn-type="dfn" data-export="">same-document URL reference</dfn></dt>
    <dd>A [=URL reference with fragment identifier=]
      where the non-fragment part of the URL refers to the current document.
    </dd>

    <dt><dfn>data URL</dfn></dt>
    <dd>A [=URL reference=] to an embedded document
      specified using the [[rfc2397#section-2|the "data" URL scheme]]
    [[rfc2397]].
      Data URL references are neither
      [=external file references=] nor [=same-document URL references=].

      [=data URL=] references, as defined by
                    [[rfc2397#section-2|the "data" URL scheme]],
                    [[rfc2397]]
    </dd>

    <dt><dfn id="TermCircularReference" data-dfn-type="dfn" data-export="">circular reference</dfn></dt>
    <dd>[=URL references=] that directly or indirectly reference
    themselves are treated as invalid circular references.
      What constitutes a circular reference will depend on how the referenced resource is used,
      and may include a reference to an ancestor of the current element.
    </dd>

    <dt><dfn id="TermUnresolvedReference" data-dfn-type="dfn" data-export="">unresolved reference</dfn></dt>
    <dd>A reference that is still being processed,
      and has not yet resulted in either an error or an identified resource.
    </dd>

    <dt><dfn id="TermInvalidReference" data-dfn-type="dfn" data-export="">invalid reference</dfn></dt>
    <dd>
      <p>Any of the following are invalid references:
      <ul>
        <li>A circular reference.</li>
        <li>
          A <a href="[=URL references=]">URL reference</a> that results in an error
          during <a href="#processingURL">processing</a>.
        </li>
        <li>
          A <a href="[=URL references=]">URL reference</a> that cannot be resolved.
        </li>
        <li>
          A [=URL references=] to elements which are
          inappropriate targets for the given reference shall be treated as invalid
          references
          (see <a href="#processingURL-validity">Valid URL targets</a>
          for appropriate targets).
          For example, the {{clip-path}} property can only refer to
          <a element spec="css-masking">clipPath</a> elements. The property setting
          <span class="attr-value">clip-path:url(#MyElement)</span> is an
          invalid reference if the referenced element is not a <a element spec="css-masking">clipPath</a>.</li>
      </ul>
      <p>Invalid references may or may not be an error
        (see <a href="conform.html#ErrorProcessing">Error processing</a>),
        depending on whether the referencing property or attribute defines fallback behavior.
      
    </dd>
    </dl>

<h4 id="URLandURI">URLs and URIs</h4>
<p>Internationalized Resource Identifiers ([=URLs=]) are a more generalized
complement to Uniform Resource Identifiers (URIs). An [=URL=] is a sequence
of characters from the Universal Character Set [[UNICODE]].
A URI is constructed from a much more restricted set of characters. All URIs are
already conformant [=URLs=]. A mapping from [=URLs=] to URIs is defined by
the [=URL=] specification, which means that URLs can be used instead of URIs
in XML documents, to identify resources. [=URLs=] can be converted to URIs
for resolution on a network, if the protocol does not support [=URLs=]
directly.

<p>Previous versions of SVG, following XLink, defined an URL reference type
as a URI <em>or as a sequence of characters which must result in an URL after a
particular escaping procedure was applied</em>. The escaping procedure was repeated in the
XLink 1.0 specification [<a href="refs.html#ref-xlink">xlink</a>], and in the
W3C XML Schema Part 2: Datatypes specification [<a href="refs.html#ref-xmlschema-2">xmlschema-2</a>].
This copying introduced the possibility of error and divergence, but was done
because the [=URL=] specification was not yet standardized.

<p>In this specification, the correct term [=URL=] is used for this "URI or sequence of characters
plus an algorithm" and the escaping method, which turns URLs into URIs, is defined by reference to the
<a href="http://www.ietf.org/rfc/rfc3987.txt">URL specification</a> [<a href="refs.html#ref-rfc3987">rfc3987</a>],
which has since become an IETF Proposed Standard. Other W3C specifications are
expected to be revised over time to remove these duplicate descriptions of the
escaping procedure and to refer to [=URL=] directly.

<h4 id="URLforms">Syntactic forms: URL and &lt;url&gt;</h4>

<p>In SVG, most structural relationships between two elements
are specified using a [=URL=] value in an <a href="#linkRefAttrs"><span class="attr-name">href</span></a> attribute.

<p>To describe linking relationships,
this specification uses two different data types in attribute and property values:
[=URL=] and <a>&lt;url&gt;</a>.
The linking guidelines in this chapter apply to URLs specified with either syntax.


<p>The [=URL=] data type is a simple URL string.
In SVG, most structural relationships between two elements
are specified using a [=URL=] value in an <a href="#linkRefAttrs"><span
class="attr-name">href</span></a> attribute.


<p><a>&lt;url&gt;</a> is different from [=URL=] and represents a CSS <code>url()</code> function value.
(See CSS Values and Units for further details [<a href="refs.html#ref-css-values-3">css-values</a>]). <a>&lt;url&gt;</a>s
may be used for [=presentation attributes=] and their corresponding CSS properties
[<a href="refs.html#ref-css-values-3">css-values</a>].

<p>[=URL=] is not a valid value for [=presentation attributes=] for structural
relationships purposes. No non-[=presentation attribute=] allows <a>&lt;url&gt;</a> as value.

<p>SVG makes extensive use of [=URL=] references, both absolute and relative,
to other objects.
For example, a {{linearGradient}} element
may be based on another gradient element,
so that only the differences between the two need to be specified,
by referencing the source gradient with a URL in the {{linearGradient/href}} attribute:


<pre class=include-raw>
path: images/linking/05_07.xml
</pre>

<p>
To fill a rectangle with that gradient,
the value of the rectangle's {{fill}} property may be set so as to
include a URL reference to the relevant {{linearGradient}} element;
here is an example:


<pre class=include-raw>
path: images/linking/05_08.xml
</pre>


<!-- old stuff from 1.1 for checking

<p id="URLReference">URL references are defined in either of the
following forms:

<pre class='grammar'><![CDATA[
<URL-reference> = [ <absoluteURL> | <relativeURL> ] [ "#" <elementID> ]    -or-
<URL-reference> = [ <absoluteURL> | <relativeURL> ] [ "#xpointer(id(" <elementID> "))" ]
</xmp>

<p>where <span class="grammar">&lt;elementID&gt;</span>
is the ID of the referenced element.

<p>(Note that the two forms above (i.e.,
<span class="attr-value">#&lt;elementID&gt;</span> and
<span class="attr-value">#xpointer(id(&lt;elementID&gt;))</span>)
are formulated in syntaxes compatible with "XML Pointer Language (XPointer)"
[<a href="https://www.w3.org/TR/xptr">XPTR</a>]. These two formulations of URL
references are the only XPointer formulations that are required in SVG 1.1 user
agents.)

-->

<h4 id="linkRefAttrs">URL reference attributes</h4>

<p id="linkRefAttrsEmbed">[=URL references=] are normally specified with an
<span class="attr-name">href</span> attribute.
The value of this attribute forms a reference for the desired resource (or
secondary resource, if there is a fragment identifier).
The value of the <span class="attr-name">href</span>
attribute must be a URL.

<p>Because it is impractical for any application to check that
a value is an [=URL reference=], this specification follows the lead
of the <a href="http://www.ietf.org/rfc/rfc3986.txt">URL Specification</a>
in this matter and imposes no such conformance testing
requirement on [=SVG authoring tools=].
An invalid URL does not make an SVG document non-conforming.
SVG user agents are only required to process URLs when needed,
as specified in <a href="#processingURL">Processing of URL references</a>.



<h4 id="XLinkRefAttrs">Deprecated XLink URL reference attributes</h4>

<p>In previous versions of SVG, the <span class="attr-name">href</span>
attribute was specified in the XLink namespace [<a
href="refs.html#ref-xlink">xlink</a>] namespace.
This usage is now deprecated and instead [=URL references=] should be
specified using the <span class="attr-name">href</span> attribute without
a namespace.

<p>For backwards compatibility, the deprecated {{xlink:href}} attribute
is defined below along with the {{xlink:title}} attribute which has also
been deprecated.

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
        <td><dfn id="XLinkHrefAttribute" data-dfn-type="element-attr" data-dfn-for="a, image, linearGradient, pattern, radialGradient, script, textPath, use" data-export="">xlink:href</dfn></td>
        <td>URL <a href="types.html#attribute-url" class="syntax">&bs[;URL]</a></td>
        <td>(none)</td>
        <td>(see below)</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>For backwards compatibility, elements with an <span
    class="attr-name">href</span> attribute also recognize an <span
    class="attr-name">href</span> attribute in the XLink namespace [<a
    href="refs.html#ref-xlink">xlink</a>].

    <p>When the <span class="attr-name">href</span> attribute is present in
    <em>both</em> the XLink namespace and without a namespace, the
    value of the attribute without a namespace shall be used. The attribute in
    the XLink namespace shall be ignored.

    <p>A [=conforming SVG generator=] must generate <span
    class="attr-name">href</span> attributes without a namespace.
    However, it may <em>also</em> generate <span class="attr-name">href</span>
    attributes in the XLink namespace to provide backwards compatibility.

    <p>This attribute is [=animatable=] if and only if the corresponding
    <span class="attr-name">href</span> attribute is defined to be
    animatable.
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
        <td><dfn id="XLinkTitleAttribute" data-dfn-type="element-attr" data-dfn-for="a, image, linearGradient, pattern, radialGradient, script, textPath, use" data-export="">xlink:title</dfn></td>
        <td>&lt;anything&gt;</td>
        <td>(none)</td>
        <td>no</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>Deprecated attribute to describe the meaning of
    a link or resource in a human-readable fashion.
    New content should use a <a href="struct.html#TitleElement"><span
    class="element-name">title</span></a> child element rather than a <span
    class="attr-name">xlink:title</span> attribute.
    <p>The use of this information is highly dependent on the type of processing
    being done. It may be used, for example, to make titles
    available to applications used by visually impaired users,
    or to create a table of links, or to present help text that
    appears when a user lets a mouse pointer hover over a
    starting resource.
    <p>The <span class="attr-name">title</span> attribute, if used, must be
    in the XLink namespace.
    Refer to the <a href="https://www.w3.org/TR/xlink/">XML Linking Language
    (XLink)</a> [<a href="refs.html#ref-xlink">xlink</a>].
  </dd>
</dl>

<p>When using the deprecated XLink attributes {{xlink:href}} or
{{xlink:title}} an explicit XLink namespace declaration must be provided
[[!xml-names]],

One simple way to provide such an XLink namespace declaration
is to include an <span class="attr-name">xmlns</span> attribute
for the XLink namespace on the <{svg}> element for content that uses
XLink attributes. For example:

<xmp>
<svg xmlns:xlink="http://www.w3.org/1999/xlink" ...>
  <image xlink:href="foo.png" .../>
</svg>
</xmp>


<h4 id="processingURL">Processing of URL references</h4>

<p>
  URLs are processed to identify a resource at the time they are needed, as follows:


<ul>
  <li>For the {{a/href}} attribute of the <a element spec="svg2">a</a> element,
    at the time the link is activated by the user.
  </li>
  <li>For all other <span class="attr-name">href</span> attributes,
    at the time the element is <a href="https://dom.spec.whatwg.org/#connected">connected</a> to a document,
    or at the time when the attribute is set, whichever is later.
  </li>
  <li>For source URLs on embedded HTML media elements,
    as required based on source selection rules
    <a href="https://html.spec.whatwg.org/multipage/media.html#media-elements">in the HTML specification</a> [[!HTML]].
  </li>
  <li>For all presentation attributes and style properties,
    at the time the property is required for rendering an element.
  </li>
</ul>

<p>
  Legacy {{xlink:href}} attributes are processed
  at the time a corresponding <span class="attr-name">href</span> attribute would be processed,
  but only if no such <span class="attr-name">href</span> attribute exists on the element.


<p>Processing a URL involves three steps:
  generating the absolute URL;
  fetching the document (if required);
  identifying the target element (if required).


<p>
  A URL reference is [=unresolved=]
  until processing either results in an [=invalid reference=]
  or in the identification of the target resource.
  Unresolved references in the non-presentation attributes of
  [=structurally external elements=] prevent the <a href="interact.html#LoadEvent">load event</a>
  from firing. User agents may place time limits on the resolution of references
  that are not [=same-document URL references=],
  after which the reference is treated as a network error
  (and therefore as an [=invalid reference=]).


<p>
  For [=same-document URL references=] in a dynamic document,
  modifications or animations of attributes or properties,
  or removal of elements from the DOM,
  may cause an URL reference to return to the [=unresolved=] state.
  The user agent must once again attempt to resolve the URI to identify the referenced resource.


<h5 id="processingURL-absolute">Generating the absolute URL</h5>

<p>If the [=URL reference=] is relative, its absolute version must be computed before use.
The absolute URL should be generated using one of the following methods:

<ul>
  <li>
    as described in <a href="https://drafts.csswg.org/css-values/#local-urls">CSS Values and Units</a> if the reference occurs in a CSS file or in a [=presentation attribute=]
[<a href="refs.html#ref-css-values-3">css-values</a>]
  </li>
  <li>
    as described in <a href="https://www.w3.org/TR/xmlbase/">XML Base</a> before use [<a href="refs.html#ref-xmlbase">xmlbase</a>]
    if the reference occurs in any other attribute in an XML document
  </li>
  <li>
    as described in the <a href="https://html.spec.whatwg.org/multipage/urls-and-fetching.html#resolving-urls">HTML specification</a>
    if the reference occurs in a non-presentation attribute
    in an HTML document that is not an XML document [[!HTML]]
  </li>
</ul>

Note: 
  The <a href="https://www.w3.org/TR/xmlbase/#syntax"><span class="attr-name">xml:base</span></a> attribute
  will only have an effect in XML documents;
  this includes SVG documents and XHTML documents but not HTML documents that are not XML.
  In contrast, a <a class="html" href="https://html.spec.whatwg.org/multipage/semantics.html#the-base-element"><code>base</code></a> element
  affects relative URLs in any SVG or HTML document,
  by altering the <a href="https://html.spec.whatwg.org/multipage/urls-and-fetching.html#document-base-url">document base URL</a>.


<p>If the protocol, such as HTTP, does not support [=URLs=] directly,
the [=URL=] must be converted to a URI by the user agent, as described
in section 3.1 of the <a href="http://www.ietf.org/rfc/rfc3987.txt">URL specification</a> [<a href="refs.html#ref-rfc3987">rfc3987</a>].

<p>After generating the absolute URL:
<ul>
  <li>
    <p>
      If the URL is being processed following the activation of a link,
      the user agent must follow the <a href="https://html.spec.whatwg.org/multipage/browsing-the-web.html#browsing-the-web">algorithm for navigating to a URL</a>
      described in the HTML specification [[!HTML]].
      The outcome of this algorithm varies depending on the
      {{a/target}} browsing context and security restrictions between browsing contexts,
      and on whether the link is to the same document as is currently contained in that browsing context
      (in which case the fragment is navigated without reloading the document).
      If the document that was navigated was an SVG document,
      then adjust the target behavior as described in
      <a href="#LinksIntoSVG">Linking into SVG content</a>.
    
  </li>
  <li>
    <p>
      If the URL being processed is only <a href="#processingURL-validity">valid</a>
      if it refers to a complete document file
      (such as the <span class="attr-name">href</span> attribute of
      an {{image}} and {{script}} element),
      continue as indicated in <a href="#processingURL-fetch">Fetching the document</a>
      (regardless of whether the URL is to the same document or not).
    
  </li>
  <li>
    <p>
      In all other cases, the URL is for a resource to be used in this SVG document.
      The user agent must parse the URL to separate out the target fragment from the rest of the URL,
      and compare it with the document base URL.
      If all parts other than the target fragment are equal,
      this is a [=same-document URL reference=],
      and processing the URL must continue
      as indicated in <a href="#processingURL-target">Identifying the target element</a>
      with the current document as the referenced document.
    
  </li>
  <li>
    <p>
      Otherwise, the URL references a separate document,
      and the user agent must continue processing the URL
      as indicated in <a href="#processingURL-fetch">Fetching the document</a>.
    
  </li>
</ul>

Note: 
  As defined in <a href="https://drafts.csswg.org/css-values/#local-urls">CSS Values and Units</a>,
  a fragment-only URL in a style property must be treated as
  a [=same-document URL reference=],
  regardless of the file in which the property was declared.



<h5 id="processingURL-fetch">Fetching the document</h5>

<p>
  SVG properties and attributes may reference other documents.
  When processing such a URL,
  the user agent should fetch the referenced document
  as described in this section,
  except under the following conditions:


<ul>
  <li>
    <p>
      If the URL reference is from
      the <span class="attr-name">href</span> attribute on <a href="https://svgwg.org/specs/animations/#TargetElement">SVG animation elements</a>,
      only [=same-document URL=] references are allowed
      [<a href="refs.html#ref-svg-animation">svg-animation</a>].
      A URL referring to a different document is invalid
      and the document must not be fetched.
    
  </li>
  <li>
    <p>
      If the document containing the reference is being processed in
      [[#secure-static-mode]] or [[#secure-animated-mode]],
      [=external file references=] are disallowed.
      Unless the reference is a [=data URL=],
      the user agent must treat the reference as if there was a network error,
      making this an [=invalid reference=].
    
  </li>
  <li>
    <p>
      If any other security restrictions
      on the browsing context or user agent prevent accessing the external file,
      then the user agent must treat the reference as if there was a network error.
    
  </li>
</ul>

<p>
  When fetching external resources from the Internet,
  user agents must use a <a href="https://html.spec.whatwg.org/multipage/urls-and-fetching.html#create-a-potential-cors-request">potentially CORS-enabled request</a>
  as defined in HTML [[!HTML]]
  with the <em>corsAttributeState</em> as follows:

<ul>
  <li>
    For an <span class="attr-name">href</span> reference on an
    {{image}} element or
    {{script}} element,
    the CORS state specified by the {{image/crossorigin}} attribute.
  </li>
  <li>
    For a reference from a style property or presentation attribute,
    the "anonymous" state.
  </li>
  <li>
    For all other references,
    the "no-cors" state.
  </li>
</ul><a class="html" href="https://html.spec.whatwg.org/multipage/semantics.html#the-base-element"><code>base</code></a>
<p>
  The request's <em>origin</em> is computed using the
  <a href="https://fetch.spec.whatwg.org/#concept-cors-check" >same rules as HTML</a>,
  with an SVG {{script}} element treated like an HTML <code>script</code> element,
  and an SVG <{image}> element treated like an HTML <code>img</code> element.
  The <em>default origin behaviour</em> must be set to <em>taint</em>.


Note: 
  A future SVG specification may enable CORS references
  on other SVG elements with <span class="attr-name">href</span> attributes.


<p>
  If the fetching algorithm results in an error or an empty response body,
  the reference URL is treated as an [=invalid reference=].

<p>
  If a valid response is returned,
  and the <a href="#processingURL-validity">valid URL targets</a> for the reference
  include specific element types,
  the user agent must continue by
  <a href="#processingURL-parsing">Processing the subresource document</a>.
  Otherwise (if only entire-document the URL references are valid),
  then the fetched document is the referenced resource.


<h5 id="processingURL-parsing">Processing the subresource document</h5>

<p>
  Otherwise, the subresource must be parsed to identify the target element.
  If the fetched document is a type that the user agent can parse
  to create a document object model,
  it must process it in [[#secure-static-mode]]
  (meaning, do not fetch any additional external resources
  and do not run scripts or play animations).
  The document model generated for an external subresource reference
  must be immutable (read-only) and cannot be modified.


<p>
  If a document object model can be generated from the fetched file,
  processing the URL must continue
  as indicated in <a href="#processingURL-target">Identifying the target element</a>
  with the parsed subresource document as the referenced document.
  The user agent may commence the target-identification process
  prior to completely parsing the document.


<p>
  User agents may maintain a list of external resource URLs
  and their associated parsed documents,
  and may re-use the documents for subsequent references,
  so long as doing so does not violate the processing mode,
  caching, and CORS requirements on the resource.


<h5 id="processingURL-target">Identifying the target element</h5>

<p>
  For URL references to a specific element,
  whether the reference is valid depends on whether
   the element can be located within the referenced document
  and whether it is of an allowed type.


<p>
  Using the referenced document identified in previous processing steps
  (either an external subresource document or the current document),
  the target element is identified as follows:

<ul>
  <li>
    <p>
      If the URL does not specify a specific element in a target fragment,
      the target element is the root element of the referenced document.
    
  </li>
  <li>
    <p>
      Otherwise, the URL targets a specific element.
      If a matching element currently exists in the referenced document,
      then it is the target element.
    
  </li>
  <li>
    <p>
      Otherwise, there is no currently matching element.
      If the referenced document is immutable,
      then the URL reference is [=invalid=].
      An external subresource document is always immutable once fully parsed;
      the current document is also immutable once parsed
      if it is being processed in any mode other than
      [[#dynamic-interactive-mode]].
    
  </li>
  <li>
    <p>
      Otherwise, observe mutations to the referenced document
      until the URL can be successfully resolved
      to define a target element,
      or until the document becomes immutable
      (e.g., a non-dynamic document finishes parsing).
    
  </li>
</ul>

<p>The target element provides the referenced resource
  if (and only if) it is a <a href="#processingURL-validity">valid URL target</a> for the reference.


<h5 id="processingURL-validity">Valid URL targets</h5>

<p>The valid target element types for <span class="attr-name">href</span> (or {{xlink:href}}) attributes are based on the element that has the attribute, as follows:

<ul>
  <li>the <a element spec="svg2">a</a> element can reference any local or non-local resource</li>
  <li>the {{image}} element must reference a document that can be processed as an image</li>
  <li>the {{linearGradient}} element must reference a different {{linearGradient}} or {{radialGradient}} element</li>
  <li>the {{pattern}} element must reference another {{pattern}} element</li>
  <li>the {{radialGradient}} element must reference a {{linearGradient}} or another {{radialGradient}} element</li>
  <li>the {{script}} element must reference an external document that provides the script content</li>
  <li>the {{textPath}} element must reference an element type
    that implements the [=SVGGeometryElement=] interface</li>
  <li>the <{use}> element must reference an SVG-namespaced element</li>
</ul>

<p>The valid target element types for style properties defined in this specification are as follows: 

<ul>
  <!--
  <li>the <a href="color.html#ColorProfileSrcProperty">src</a> descriptor on an @color-profile definition must reference an ICC profile resource</li>
  -->
  <li>the {{fill}} property (see <a href="painting.html#SpecifyingPaint">Specifying paint</a> for reference rules)</li>
  <li>the {{marker property}}, {{marker-start}}, {{marker-mid}} and {{marker-end}} properties must reference a {{marker element}} element.</li>
  <li>the {{shape-inside}} and {{shape-subtract}} properties must reference an element type
    that implements the [=SVGGeometryElement=] interface,
    or a document that can be processed as an image
  </li>
  <li>the {{stroke}} property (see <a href="painting.html#SpecifyingPaint">Specifying paint</a> for reference rules)</li>
</ul>

<p>
  For references that allow either a reference to a target element, or to an image file
  (such as the {{shape-inside}}, {{shape-subtract}}, and {{mask property}} properties),
  the user agent must identify the target element and determine whether it is a valid target.
  If the resolved target element is not an allowed element type,
  the referenced resource is the entire document file;
  the target fragment is used in processing that file as with any other image.
  

<p>In all other cases, if the resolved target element type (or document type) is not allowed for the URL reference,
  it is an [=invalid reference=].


</div>

<h3 id="Links">Links out of SVG content: the <span class="element-name">a</span> element</h3>



<p>SVG provides an <a element spec="svg2">a</a> element, to indicate links (also known
as <em>hyperlinks</em> or <em>Web links</em>).
An <a element spec="svg2">a</a> element forms a link if it has a {{href}} or {{xlink:href}} attribute; without these attributes the <a element spec="svg2">a</a> element is an inactive placeholder for a link.

Note: SVG 1.1 defined links in terms of the XLink specification ([<a href="https://www.w3.org/TR/2001/REC-xlink-20010627/">XLink</a>]),
using attributes defined in the XLink namespace.
SVG 2 uses an alternative set of attributes in the default namespace that are consistent with HTML links, and <a href="#XLinkRefAttrs">deprecates the XLink attributes</a>.

<p>The <a element spec="svg2">a</a> element may
contain any element that its parent may contain, except for another <a element spec="svg2">a</a> element;
the same element is used for both graphical and textual linked content.
Links may not be nested;
if an <a element spec="svg2">a</a> element is a descendent of another hyperlink element
(whether in the SVG namespace or another namespace),
user agents must ignore its href attribute and treat it as inactive.
The invalid <a element spec="svg2">a</a> element must still be rendered as a generic container element.


<p class="issue" data-issue="18">The rendering of invalid nested links is at risk, and will likely be synchronized with any decisions regarding the rendering of unknown elements.


<p>For pointer events processing,
a linked hit region is defined for each separate rendered element contained
within the <a element spec="svg2">a</a> element (according to the value of their {{pointer-events}} property),
rather than for the bounding box of the <a element spec="svg2">a</a> element itself.
User agents must also ensure that all links are [=focusable=] and can be activated by keyboard commands.

<p>The remote resource (the destination for the link) is defined by
a [=URL=] specified by the {{href}} attribute on the <a element spec="svg2">a</a>
element. The remote resource may be any Web resource (e.g., an image, a video
clip, a sound bite, a program, another SVG document, an HTML document, an
element within the current document, an element within a different document, etc.).
In response to user activation of a link
(by clicking with the mouse, through keyboard input, voice commands, etc.),
user agents should attempt to fetch the specified resource document and either display it or make it available as a downloaded file.

<p id="ExampleLink01"><span class="example-ref">Example link01</span> assigns
a link to an ellipse.

<pre class=include-raw>
path: images/linking/link01.svg
</pre>
<!--
<pre class=include>
path: images/linking/link01.svg
</pre>
-->
<p>If the above SVG file is viewed by a user agent that supports both
SVG and HTML, then clicking on the ellipse will cause the current window
or frame to be replaced by the W3C home page.

<div id="AElement">
@@elementsummary a@@
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
        <td><dfn id="AElementHrefAttribute" data-dfn-type="element-attr" data-dfn-for="a" data-export="">href</dfn></td>
        <td>URL <a href="types.html#attribute-url" class="syntax">&bs[;URL]</a></td>
        <td>(none)</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    The location of the referenced object, expressed as an [=URL reference=].
    Refer to the common handling defined for <a
    href="linking.html#linkRefAttrs">URL reference attributes</a>.
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
        <td><dfn id="AElementTargetAttribute" data-dfn-type="element-attr" data-dfn-for="a" data-export="">target</dfn></td>
        <td> _self | _parent | _top | _blank | &lt;XML-Name&gt;</td>
        <td>_self</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>This attribute should be used when there are multiple possible targets for
    the ending resource, such as when the parent document is embedded within an HTML
    or XHTML document, or is viewed with a tabbed browser. This attribute specifies the
    name of the browsing context
    (e.g., a browser tab or an (X)HTML iframe or object element) into
    which a document is to be opened when the link is activated:
    <dl>
      <dt><span class="attr-value">_self</span></dt>
      <dd>The current SVG image is replaced by the linked content in the
      same browsing context as the current SVG image.</dd>
      <dt><span class="attr-value">_parent</span></dt>
      <dd>The immediate parent browsing context of the SVG image is replaced by the
      linked content, if it exists and can be securely accessed from this document.</dd>
      <dt><span class="attr-value">_top</span></dt>
      <dd>The content of the full active window or tab is replaced by the linked content,
          if it exists and can be securely accessed from this document</dd>
      <dt><span class="attr-value">_blank</span></dt>
      <dd>A new un-named window or tab is requested for the display of the
      linked content, if this document can securely do so.
      If the user agent does not support multiple windows/tabs,
      the result is the same as <span class="attr-value">_top</span>.</dd>
      <dt><span class="attr-value">&lt;XML-Name&gt;</span></dt>
      <dd>Specifies the name of the browsing context (tab, inline frame, object, etc.)
      for display of the linked content. If a context with this name
      already exists, and can be securely accessed from this document, it is re-used,
      replacing the existing content.  If it does not exist, it is created
      (the same as <span class="attr-value">'_blank'</span>, except that
      it now has a name).  The name must be a valid XML Name &bs[;XML11], and should not start
      with an underscore (U+005F LOW LINE character), to meet the requirements of a
      <a href="https://html.spec.whatwg.org/multipage/browsers.html#valid-browsing-context-name">valid
      browsing context name</a> from HTML.</dd>
    </dl>
    <p> The normative definitions for browsing contexts and security
        restrictions on navigation actions between browsing contexts
        is HTML [[!HTML]], specifically
        <a href="https://html.spec.whatwg.org/multipage/browsers.html#browsers">the chapter on
            loading web pages</a>.
    
    <!--
       The SVG 1.1 text for "_blank" was:

      <dt><span class="attr-value">_blank</span></dt>
      <dd>A new un-named window or tab is requested for the display of the
      linked content. If this fails, the result is the same as <span class="attr-value">_top</span></dd>

        However, under HTML a request for a new tab may fail
        because of sandboxing/no-popups, in which case the link is simply not followed.
        The new language reflects this restriction while still supporting the old
        behavior in single-window SVG viewers (if such exist).
    -->
    <div class="note">
        <p>Previous versions of SVG defined the special target value
            <span class="attr-value">'_replace'</span>.  It was never well implemented,
            and the distinction between <span class="attr-value">'_replace'</span>
            and <span class="attr-value">'_self'</span> has been made redundant by
            changes in the HTML definition of browsing contexts.  Use
             <span class="attr-value">'_self'</span> to replace the current
            SVG document.
        <p>The value <span class="attr-value">'_new'</span> is <em>not</em> a
            legal value for target.  Use <span class="attr-value">'_blank'</span>
            to open a document in a new tab/window.
    </div>
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
        <td><dfn id="AElementDownloadAttribute" data-dfn-type="element-attr" data-dfn-for="a" data-export="">download</dfn></td>
        <td>any value (if non-empty, value represents a suggested file name)</td>
        <td>(none)</td>
        <td>no</td>
      </tr>
      <tr>
        <td><dfn id="AElementPingAttribute" data-dfn-type="element-attr" data-dfn-for="a" data-export="">ping</dfn></td>
        <td>space-separated valid non-empty URL tokens <a href="https://html.spec.whatwg.org/multipage/links.html#ping" class="syntax">&bs[;HTML]</a></td>
        <td>(none)</td>
        <td>no</td>
      </tr>
      <tr>
        <td><dfn id="AElementRelAttribute" data-dfn-type="element-attr" data-dfn-for="a" data-export="">rel</dfn></td>
        <td>space-separated keyword tokens <a href="https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#set-of-space-separated-tokens" class="syntax">&bs[;HTML]</a></td>
        <td>(none)</td>
        <td>no</td>
      </tr>
      <tr>
        <td><dfn id="AElementHreflangAttribute" data-dfn-type="element-attr" data-dfn-for="a" data-export="">hreflang</dfn></td>
        <td>A BCP 47 language tag string <a href="https://html.spec.whatwg.org/multipage/links.html#attr-hyperlink-hreflang" class="syntax">&bs[;HTML]</a></td>
        <td>(none)</td>
        <td>no</td>
      </tr>
      <tr>
        <td><dfn id="AElementTypeAttribute" data-dfn-type="element-attr" data-dfn-for="a" data-export="">type</dfn></td>
        <td>A MIME type string <a href="https://html.spec.whatwg.org/multipage/infrastructure.html#mime-type" class="syntax">&bs[;HTML]</a></td>
        <td>(none)</td>
        <td>no</td>
      </tr>
      <tr>
        <td><dfn id="AElementReferrerpolicyAttribute" data-dfn-type="element-attr" data-dfn-for="a" data-export="">referrerpolicy</dfn></td>
        <td>A referrer policy string <a href="https://w3c.github.io/webappsec-referrer-policy/#referrer-policy" class="syntax">&bs[;REFERRERPOLICY]</a></td>
        <td>(none)</td>
        <td>no</td>
      </tr>
    </table>
  </dt>
  <dd>
    These attributes further describe the targetted resource
    and its relationship to the current document.
    Allowed values and meaning are <a href="https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-a-element">as defined for the <code>a</code> element in HTML</a>.
  </dd>
</dl>


    Note: The SVG Working Group is waiting on the HTML specification 
    to clarify the processing model and algorithms for these 
    attributes. The attributes should follow the definitions and 
    algorithms <a href="https://html.spec.whatwg.org/multipage/links.html#following-hyperlinks-2">as 
    specified in the HTML specification</a>. For more details on the
    ongoing clarification effort, see the 
    <a href="https://github.com/whatwg/html/issues/11936">HTML 
    specification issue on processing model and algorithms
    for the HTML A element</a>.


<h3 id="LinksIntoSVG">Linking into SVG content: URL fragments and SVG views</h3>

<p>Because SVG content often represents a picture or drawing
of something, a common need is to link into a particular
<em>view</em> of the document, where a view indicates
the initial transformations so as to present a closeup of a particular
section of the document.

<div class="ready-for-wider-review">
<h4 id="SVGFragmentIdentifiers">SVG fragment identifiers</h4>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Merge the SVG 1.1 SE text and the SVG Tiny 1.2 text on fragment identifiers link traversal and add media fragments.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2012/03/08-svg-irc#T21-05-52">SVG 2 will have media fragment identifiers.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To align with Media Fragments URI.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cyril (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3442">ACTION-3442</a>)</td>
    </tr>
  </table>
</div>

<p>To link into a particular view of an SVG document, the <a href="#TermURLReferenceWithFragmentIdentifier">URL reference with fragment
identifier</a> needs to be a correctly formed <dfn id='svg-fragment-identifier' data-dfn-type="dfn" data-export="">SVG
fragment identifier</dfn>. An SVG fragment identifier defines the
meaning of the "selector" or "fragment identifier" portion of URLs that
locate resources of MIME media type "image/svg+xml".

<p>An SVG fragment identifier can come in the following forms:

<ul>
  <li>Shorthand <em>bare name</em> form of addressing (e.g.,
  <span class="attr-value">MyDrawing.svg#MyView</span>).  This form of
  addressing, which allows addressing an SVG element by its ID, is compatible
  with the fragment addressing mechanism for older versions of HTML.</li>

  <li>An <dfn id="SVGViewSpecification" data-dfn-type="dfn" data-export="">SVG view specification</dfn>
  (e.g., <span class="attr-value">MyDrawing.svg#svgView(viewBox(0,200,1000,1000))</span>).
  This form of addressing specifies the desired view of the
  document (e.g., the region of the document to view, the
  initial zoom level) completely within the SVG fragment
  specification. The contents of the SVG view specification are defined in
  <a href="#SVGFragmentIdentifiersDefinitions">SVG fragment identifiers definitions</a> section.
  </li>

  <li id="MediaFragments"><em>Basic media fragments identifiers</em> of type spatial or temporal
  (e.g., <span class="attr-value">MyDrawing.svg#xywh=0,200,1000,1000 or MyAnimation.svg#t=10)</span>)
  as defined in [<a href="refs.html#ref-media-frags">Media Fragments URI 1.0 (basic)</a>] and possibly combined using the &amp; sign (e.g. <span class="attr-value">MyDrawing.svg#xywh=0,200,1000,1000&amp;t=10</span>).
  </li>
</ul>

<h4 id="SVGFragmentIdentifiersDefinitions">SVG fragment identifiers definitions</h4>

<p>An SVG fragment identifier is defined as follows:

<pre class='grammar'>
SVGFragmentIdentifier ::= BareName *( "&amp;" <a href="https://www.w3.org/TR/media-frags/#timesegment">timesegment</a> ) |
                          SVGViewSpec *( "&amp;" <a href="https://www.w3.org/TR/media-frags/#timesegment">timesegment</a> ) |
                          <a href="https://www.w3.org/TR/media-frags/#spacesegment">spacesegment</a> *( "&amp;" timesegment ) |
                          <a href="https://www.w3.org/TR/media-frags/#timesegment">timesegment</a> *( "&amp;" spacesegment )

BareName ::= XML_Name
SVGViewSpec ::= 'svgView(' SVGViewAttributes ')'
SVGViewAttributes ::= SVGViewAttribute |
                      SVGViewAttribute ';' SVGViewAttributes

SVGViewAttribute ::= viewBoxSpec |
                     preserveAspectRatioSpec |
                     transformSpec
viewBoxSpec ::= 'viewBox(' ViewBoxParams ')'
preserveAspectRatioSpec = 'preserveAspectRatio(' AspectParams ')'
transformSpec ::= 'transform(' TransformParams ')'
</pre>

<p>where:

<ul>

  <li><em>ViewBoxParams</em> corresponds to the
  parameter values for the {{viewBox}} attribute on the {{view}}
  element. For example, <span class="attr-value">viewBox(0,0,200,200)</span>.</li>

  <li><em>AspectParams</em> corresponds to the
  parameter values for the {{preserveAspectRatio}} attribute on the
  {{view}} element. For example,
  <span class="attr-value">preserveAspectRatio(xMidYMid)</span>.</li>

  <li><em>TransformParams</em> corresponds to the
  parameter values for the {{transform}} property that is available on
  many elements. For example, <span class="attr-value">transform(scale(5))</span>.
  Currently additional transform styles and parameters (e.g. transform-origin, perspective) are not supported.
  </li>

</ul>

<p>SVG view box parameters are applied in order, as defined in
<a href="https://www.w3.org/TR/css3-transforms/">CSS Transforms</a> specification (e.g. SVG view is transformed as defined in <em>ViewBoxParams</em>,
then as defined in <em>TransformParams</em>).

<p>Spaces are allowed in fragment specifications. Commas
are used to separate numeric values within an SVG view specification
(e.g., <span class="attr-value">#svgView(viewBox(0,0,200,200))</span>)
and semicolons are used to separate attributes (e.g.,
<span class="attr-value">#svgView(viewBox(0,0,200,200);preserveAspectRatio(none))</span>).

<div class="note">
  <p>Fragment identifiers may be url-escaped according to the rules defined in
    <a href="https://www.w3.org/TR/cssom/#common-serializing-idioms">CSS Object Model (CSSOM)</a> specification.
    For example semicolons can be escaped as %3B to allow animating a (semi-colon separated) list of URLs because otherwise the semicolon would
    be interpreted as a list separator.
</div>

<p>The four types of <em>SVGViewAttribute</em> may occur
in any order, but each type may only occur at most one time in a correctly
formed <em>SVGViewSpec</em>.

<p>When a source document performs a link into an SVG document, for example
via an <a href="https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-a-element">HTML anchor element</a>
([[!HTML]]; i.e.,
<span class="attr-value">&lt;a href=...&gt;</span> element in HTML) or an
XLink specification [<a href="refs.html#ref-xlink">xlink</a>], then
the SVG fragment identifier specifies the initial view into the SVG document,
as follows:

<ul>
  <li>If no SVG fragment identifier is provided (e.g, the specified URL did
  not contain a "#" character, such as <span class="attr-value">MyDrawing.svg</span>),
  then the initial view into the SVG document is established using the view
  specification attributes (i.e., {{viewBox}}, etc.) on the
  [=outermost svg element=].</li>

  <li>If the SVG fragment identifier addresses a <a href="https://www.w3.org/TR/media-frags/#spacesegment">space segment</a>
  (e.g., <span class="attr-value">MyDrawing.svg#xywh=0,0,100,100</span>),then the initial
  view into the SVG document is established using the view specification attributes
  on the [=outermost svg element=] where the 'viewBox' is overriden by the
  x, y, width and height values provided by the fragment identifier.
  </li>

  <li>Media fragments can be specified as "pixel:" (default) and "percent:". In the latter case the resulting 'viewBox' transformation is
  calculated against referenced SVG resolved size (width and height). When the host document cannot resolve the width and height of the SVG document,
  the used values for width and height should be calculated according to CSS rules for
  <a href="https://www.w3.org/TR/CSS21/visudet.html#inline-replaced-width">calculating width and ratio for inline replaced elements</a>.</li>

  <li>If the SVG fragment identifier addresses a <a href="https://www.w3.org/TR/media-frags/#timesegment">time segment</a>
  (e.g., <span class="attr-value">MyDrawing.svg#t=10</span>),then the initial
  view into the SVG document is established as if no fragment identifier was
  provided. The rendering of the SVG Document shall be as if the setCurrentTime
  method on the SVG Document element had been called with the begin time value
  from the fragment identifier. Additionally, if an end time value is provided
  in the fragment identifier, the effect is equivalent to calling the pauseAnimations
  method on the SVG Document when the document time reaches the end time of the
  fragment identifier.
  </li>

  <li>If the SVG fragment identifier addresses a {{view}} element within
  an SVG document (e.g., <span class="attr-value">MyDrawing.svg#MyView</span>)
  then the root <{svg}> element is displayed in the SVG viewport.
  Any view specification attributes included on the given {{view}}
  element override the corresponding view specification attributes on the
  root <{svg}> element.</li>

  <li>If the SVG fragment identifier addresses specific SVG view (e.g.,
  <span class="attr-value">MyDrawing.svg#svgView(viewBox(0,200,1000,1000))</span>),
  then the document fragment defined by the root <{svg}>
  element is displayed in the SVG viewport using the SVG view specification
  provided by the SVG fragment identifier. Parameters of the svgView specification override
  the parameters defined on the root <{svg}> element of the referenced document.
  Unspecified parameters of the svgView specification don't reset the values defined on the root
  <{svg}> element of the referenced document.</li>

   <li>If the SVG fragment identifier addresses a combination of the above
   non-time related identifiers with a time-related identifier (i.e. a timesegment),
  the behavior of each identifier is applied.
  </li>

</ul>
</div>

<h4 id="ViewElement">Predefined views: the <span class="element-name">view</span> element</h4>



<p>The <span class="element-name">view</span> element is defined as follows:

@@elementsummary view@@


<div class="annotation">
  <p>
    We have resolved to remove viewTarget attribute.
  
  <p>
    Resolution: Paris 2015 F2F Day 3.
  
  <p>
    Owner: BogdanBrinza.
  
</div>

<h3 id="DOMInterfaces">DOM interfaces</h3>

<div class='ready-for-wider-review'>
<h4 id="InterfaceSVGAElement">Interface SVGAElement</h4>



<p>An [=SVGElement=] object represents an <a element spec="svg2">a</a> element in the DOM.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAElement</b> : <a>SVGGraphicsElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedString</a> <a href="linking.html#__svg__SVGAElement__target">target</a>;
  attribute DOMString <a href="linking.html#__svg__SVGAElement__download">download</a>;
  attribute USVString <a href="linking.html#__svg__SVGAElement__ping">ping</a>;
  attribute DOMString <a href="linking.html#__svg__SVGAElement__rel">rel</a>;
  [<a>SameObject</a>, <a>PutForwards</a>=value] readonly attribute <a>DOMTokenList</a> <a href="linking.html#__svg__SVGAElement__relList">relList</a>;
  attribute DOMString <a href="linking.html#__svg__SVGAElement__hreflang">hreflang</a>;
  attribute DOMString <a href="linking.html#__svg__SVGAElement__type">type</a>;

  attribute DOMString <a href="linking.html#__svg__SVGAElement__referrerPolicy">referrerPolicy</a>;
};

<a>SVGAElement</a> includes <a>SVGURIReference</a>;
<a>SVGAElement</a> includes <a>HTMLHyperlinkElementUtils</a>;</pre>

<p>The <b id="__svg__SVGAElement__target">target</b>,
  <b id="__svg__SVGAElement__download">download</b>,
  <b id="__svg__SVGAElement__ping">ping</b>,
  <b id="__svg__SVGAElement__rel">rel</b>,
  <b id="__svg__SVGAElement__hreflang">hreflang</b>,
  <b id="__svg__SVGAElement__type">type</b>,
  IDL attributes
[=reflect=] the content attributes of the same name.
<p>The <b id="__svg__SVGAElement__relList">relList</b>
  IDL attribute
[=reflects=] the {{rel}} content attribute.
<p>The <b id="__svg__SVGAElement__referrerPolicy">referrerPolicy</b>
  IDL attribute
[=reflects=] the {{referrerpolicy}} content attribute,
 <a href="https://html.spec.whatwg.org/multipage/common-dom-interfaces.html#limited-to-only-known-values">limited to only known values</a>.



<h4 id="InterfaceSVGViewElement">Interface SVGViewElement</h4>



<p>An [=SVGViewElement=] object represents a {{view}} element in the DOM.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGViewElement</b> : <a>SVGElement</a> {};

<a>SVGViewElement</a> includes <a>SVGFitToViewBox</a>;</pre>


</div>
