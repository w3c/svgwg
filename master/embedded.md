<h2>Embedded Content</h2>

<h3 id="Overview">Overview</h3>
<p>Embedded content is content that imports another resource into the document, or content from another vocabulary that is inserted into the document.
This is the same definition as <a href="https://html.spec.whatwg.org/multipage/">HTML's</a> <a href="https://html.spec.whatwg.org/multipage/embedded-content.html#embedded-content">embedded content</a>.

<p>SVG supports embedded content with the use of {{image}} and <{foreignObject}> elements.

Note: Content embedded with {{image}} is compatible with <a href="https://www.w3.org/TR/resource-hints/">Resource Hints</a> for prioritizing downloading of external resources. 

<h3 id="Placement">Placement of the embedded content</h3>

  <p>
    The {{x}}, {{y}}, {{width}}, and {{height}} geometry properties specify the rectangular region into which the embedded content is positioned
    (the <dfn id="TermPositioningRectangle"  data-dfn-type="dfn" data-export="">positioning rectangle</dfn>).
    The [=positioning rectangle=] is used as the bounding box of the element;
    note, however, that graphics may overflow the positioning rectangle,
    depending on the value of the [[#OverflowAndClipProperties|overflow]] property.
  

  <p>
    When the embedded content consists of a single referenced resource
    (e.g., an {{image}}),
    the dimensions of the [=positioning rectangle=],
    in the current coordinate system after applying all transforms,
    define the [=specified size=] for the embedded object.
    A [=concrete object size=] and final position must be determined for the object using the
    [=Default Sizing Algorithm=]
    defined for replaced elements in CSS layout [<a href="refs.html#ref-css-images-3">css-images-3</a>].
    The {{object-fit}} and {{object-position}} affect the final
    position and size of the object,
    and may cause it to be extend beyond the [=positioning rectangle=].
    In that case, the [[#OverflowAndClipProperties|overflow]] property determines whether
    the rendered object should be clipped to its [=positioning rectangle=].
  
  <p>
    When the embedded content consists of a document fragment
    (e.g., a <{foreignObject}>),
    the [=positioning rectangle=] defines the bounds of a
    <a href="https://www.w3.org/TR/CSS21/visuren.html#containing-block">containing block</a> for laying out the child content using CSS.
    The scale of the containing block is defined in the current coordinate system,
    including all explicit and implicit (e.g., [[#ViewBoxAttribute|viewBox]]) transformations.
    The <{foreignObject}>, or other element that is positioned using SVG layout attributes,
    is implicitly <a href="https://www.w3.org/TR/CSS21/visuren.html#propdef-position">absolutely-positioned</a> for the purposes of CSS layout.
    As a result, any absolutely-positioned child elements
    are positioned relative to this containing block.
    Again, the [[#OverflowAndClipProperties|overflow]] property determines
    whether content that extends outside the [=positioning rectangle=] will be hidden.
  
  <p>
    A value of zero for either {{width}} or {{height}} disables rendering of the element and its embedded content.
  
  <p>
    The <span class="attr-value">'auto'</span> value for {{width}} or {{height}} is used to size the corresponding element automatically based on the [=intrinsic dimensions=] or [=intrinsic aspect ratio=] of the referenced resource.
    Computation of automatically-sized values follows the
    [=Default Sizing Algorithm=]
    defined for replaced elements in CSS layout [<a href="refs.html#ref-css-images-3">css-images-3</a>].
    In particular, when the referenced resource does not have an intrinsic size
    (such as image types with no defined dimensions),
    it is assumed to have a width of 300px and a height of 150px.
  
  <p>
    CSS positioning properties (e.g. <span class="prop-name">top</span> and <span class="prop-name">margin</span>) have no effect when positioning the embedded content element in the SVG coordinate system.
    They can, however, be used to position child elements of a <{foreignObject}> or HTML embedding element.
  

<h3 id="ImageElement">The <span class="element-name">image</span> element</h3>



@@elementsummary image@@

<p>The {{image}} element
indicates that the contents of a complete file are to be
rendered into a given rectangle within the current user
coordinate system. The {{image}} element can refer to raster
image files such as PNG or JPEG or to files with MIME type of
"image/svg+xml". <a
href="conform.html#ConformingSVGViewers">Conforming SVG
viewers</a> need to support at least PNG, JPEG and SVG format
files.
SVG files must be processed in [[#secure-animated-mode]]
if the current document supports animation,
or in [[#secure-static-mode]] if the current document is static.


<p>The result of processing an {{image}} is always a four-channel
RGBA result. When an {{image}}
element references an image (such as many PNG or JPEG
files) which only has three channels (RGB), then the effect is
as if the object were converted into a 4-channel RGBA image
with the alpha channel uniformly set to 1. For a single-channel (grayscale)
raster image, the effect is as if the object were converted
into a 4-channel RGBA image, where the single channel from the
referenced object is used to compute the three color channels
and the alpha channel is uniformly set to 1.

<p>The [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attribute
determines how the referenced image is scaled and positioned to fit
into the [=concrete object size=] determined from the
[=positioning rectangle=] and the {{object-fit}} and {{object-position}} properties.
The result of applying this attribute defines an <dfn id="TermImageRenderingRectangle"  data-dfn-type="dfn" data-export="">image-rendering rectangle</dfn>
used for actual image rendering.
When the referenced image is an SVG,
the [=image-rendering rectangle=] defines
the [=SVG viewport=] used for rendering that SVG.


Note: 
  The [[#PreserveAspectRatioAttribute|preserveAspectRatio]] calculations
  are applied <em>after</em> determining the [=concrete object size=],
  and only have an effect if that size does not match the
  [=intrinsic aspect ratio=] of the embedded image.
  If a value of {{object-fit}} is used that
  ensures that the concrete object size matches the intrinsic aspect ratio
  (i.e., any value other than the default <span class="prop-value">fill</span>),
  then the [[#PreserveAspectRatioAttribute|preserveAspectRatio]] value will have no effect;
  the [=image-rendering rectangle=] will be that determined
  when scaling and positioning the object with CSS.
  The [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attribute can therefore be safely used
  as a fallback for most values of {{object-fit}} and {{object-position}};
  it must be explicitly set to <span class="attr-value">none</span>
  to turn off aspect ratio control, regardless of {{object-fit}} value.


<p>
The aspect ratio to use when
evaluating the [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attribute is
defined by the [=intrinsic aspect ratio=] of the referenced content.
For an SVG file, the aspect ratio is defined
in <a href="coords.html#SizingSVGInCSS">Intrinsic sizing properties of SVG content"</a>.
For most raster content (PNG, JPEG) the pixel width and height of the image file
define an intrinsic aspect ratio.
Where the embedded image does not have an [=intrinsic aspect ratio=]
(e.g. an SVG file with neither [[#ViewBoxAttribute|viewBox]] attribute nor explicit dimensions for the
[=outermost svg element=]) the [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attribute is
ignored;
the embedded image is drawn to fill the [=positioning rectangle=] defined by the geometry properties
on the {{image}} element.


<p>For example, if the image element referenced a PNG or JPEG
and <span class="attr-value">preserveAspectRatio="xMinYMin
meet"</span>, then the aspect ratio of the raster would be
preserved (which means that the scale factor from image's
coordinates to current user space coordinates would be the same
for both X and Y), the raster would be sized as large as
possible while ensuring that the entire raster fits within the
viewport, and the top/left of the raster would be aligned with
the top/left of the viewport as defined by the attributes {{x}}, {{y}}, {{width}} and {{height}} on the {{image}} element.  If the value
of [[#PreserveAspectRatioAttribute|preserveAspectRatio]] was <code class='attr-value'>none</code>
then aspect ratio of the image would not be preserved. The
image would be fit such that the top/left corner of the
raster exactly aligns with coordinate ({{x}}, {{y}}) and the bottom/right corner of
the raster exactly aligns with coordinate ({{x}}+{{width}}, {{y}}+{{height}}).

<p>
For {{image}} elements embedding an SVG image,
the [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attribute on the root
element in the referenced SVG image must be ignored,
and instead treated as if it had a value of <span class="attr-value">none</span>.
(see [[#PreserveAspectRatioAttribute|preserveAspectRatio]] for details).
This ensures that the [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attribute on
the referencing {{image}} has its intended effect,
even if it is <span class="attr-value">none</span>.


Note: 
When the value of the [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attribute on the {{image}}
is <em>not</em> <span class="attr-value">none</span>,
the [=image-rendering rectangle=] determined
from the properties of the {{image}} element
will exactly match the embedded SVG's intrinsic aspect ratio.
Ignoring the [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attribute from the embedded SVG
will therefore not usually have any effect.
The exception is if the aspect ratio of that image
is determined from absolute values for the {{width}} and {{height}} attributes
which <em>do not</em> match its [[#ViewBoxAttribute|viewBox]] aspect ratio.
This is an unusual situation that authors are advised to avoid, for many reasons.


<p>
The user agent stylesheet sets the value of the [[#OverflowAndClipProperties|overflow]] property
on {{image}} element to <span class="prop-value">hidden</span>.
Unless over-ridden by the author, images will therefore be clipped to
the [=positioning rectangle=] defined by the geometry properties.


<p>
For {{image}} elements embedding an SVG image,
two different [[#OverflowAndClipProperties|overflow]] values apply.
The value specified on the {{image}} element determines
whether the [=image-rendering rectangle=] is clipped to the [=positioning rectangle=].
The value on the root element of the referenced SVG
determines whether the graphics are clipped to the [=image-rendering rectangle=].


Note: 
New in SVG 2.
Previous versions of SVG required that the [[#OverflowAndClipProperties|overflow]] (and also {{clip}})
property on the embedded SVG be ignored.
The new rules ensure that an overflowing <span class="attr-value">slice</span> layout
can be safely used without compromising the overflow control from the referenced image.


<p>
  To link into particular view of an embedded SVG image,
  authors can use media fragments as defined in <a href="linking.html#LinksIntoSVG">Linking into SVG content</a>.
  To crop to a specific section of a raster image,
  authors can use <em>Basic media fragments identifiers</em> [<a href="refs.html#ref-media-frags">Media Fragments URI 1.0 (basic)</a>].
  Either type of fragment may affect the [=intrinsic dimensions=] and/or [=intrinsic aspect ratio=] of the image.


<p>The resource referenced by the {{image}} element represents a
separate document which generates its own parse tree and
document object model (if the resource is XML). Thus, there is
no inheritance of properties into the image.

<p>Unlike <{use}>, the {{image}} element cannot reference
elements within an SVG file.

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Support auto-sized images.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/27-svg-irc#T18-52-24">We will allow auto-sized images in SVG 2.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To allow raster images to use their own size without the need to set width and height.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3340">ACTION-3340</a>)</td>
    </tr>
  </table>
</div>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Support selecting part of an {{image}} for display.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/27-svg-irc#T18-45-13">We will have a method for <span class="element-name">image</span> to select a part of an image to display, maybe by allowing <span class="attr-name">viewBox</span> on it.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To allow selection of part of an image without requiring the author to manually slice the image.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Nobody</td>
    </tr>
  </table>
</div>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Support the <span class="property">object-fit</span> and <span class="property">object-position</span> properties from css-images-3.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/07/29-svg-minutes.html#item08">SVG 2 will depend on CSS3 Image Values and CSS4 Image Values.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To align with the CSS way of specifying image fitting that [[#PreserveAspectRatioAttribute|preserveAspectRatio]] provides.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron or Erik (no action)</td>
    </tr>
  </table>
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
        <td><dfn id="ImageElementCrossoriginAttribute" data-dfn-type="element-attr" data-dfn-for="image" data-export="">crossorigin</dfn></td>
        <td>[ anonymous | use-credentials ]?</td>
        <td>(see HTML definition of attribute)</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>The crossorigin attribute is a [=CORS settings attribute=], and unless otherwise specified follows the same processing rules as in HTML [[!HTML]].
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
        <td><dfn id="ImageElementHrefAttribute" data-dfn-type="element-attr" data-dfn-for="image" data-export="">href</dfn></td>
        <td>URL <a href="types.html#attribute-url" class="syntax">&bs[;URL]</a></td>
        <td>(none)</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>An [=URL Reference=]
    identifying the image to render.
    Refer to the common handling defined for <a
    href="linking.html#linkRefAttrs">URL reference attributes</a> and
    <a href="linking.html#XLinkRefAttrs">deprecated XLink attributes</a>.
    <p>
        The URL is processed and the resource is fetched
        <a href="linking.html#processingURL">as described in the Linking chapter</a>.
    
  </dd>
</dl>

<div class="example">
<pre>
&lt;?xml version="1.0" standalone="no"?&gt;
&lt;svg width="4in" height="3in"
     xmlns="http://www.w3.org/2000/svg"&gt;
  &lt;desc&gt;This graphic links to an external image
  &lt;/desc&gt;
  &lt;image x="200" y="200" width="100px" height="100px"
         href="myimage.png"&gt;
    &lt;title&gt;My image&lt;/title&gt;
  &lt;/image&gt;
&lt;/svg&gt;
</pre>
</div>

<p>
  Since image references always refer to a complete document,
  a target-only URL is treated as a link to the same file,
  which is rendered again as an independent embedded image.
  Since the embedded image is processed in a secure mode,
  its own embedded references are not processed,
  preventing infinite recursion.


<pre class=include-code>
path: images/embedded/recursive-image.svg
highlight: xml
</pre>
<!--
@@fix
<pre class=include>
path: images/embedded/recursive-image.svg
</pre>
-->


<h3 id="ForeignObjectElement">The <span class="element-name">foreignObject</span> element</h3>

@@elementsummary foreignObject@@

<p>SVG is designed to be compatible with other XML languages
for describing and rendering other types of content.
The <{foreignObject}>
element allows for inclusion of elements in a non-SVG namespace which
is rendered within a region of the SVG graphic using other user agent processes. The
included foreign graphical content is subject to SVG
transformations, filters, clipping, masking and compositing.
Examples include
inserting a <a
href="https://www.w3.org/TR/2003/REC-MathML2-20031021/">MathML</a> expression into
an SVG drawing [<a href="refs.html#ref-mathml3">MathML3</a>],
or adding a block of complex CSS-formatted HTML text or form inputs.


Note: 
  The HTML parser treats elements inside the <{foreignObject}>
  equivalent to elements inside an HTML document fragment.
  Any <code>svg</code> or <code>math</code> element,
  and their descendents,
  will be parsed as being in the SVG or MathML namespace, respectively;
  all other tags will be parsed as being in the HTML namespace.


<p>
SVG-namespaced elements within a <{foreignObject}> will not be rendered,
except in the situation where a properly defined SVG
fragment, including a root <{svg}> element is
defined as a descendent of the <{foreignObject}>.

<p>A <{foreignObject}>
may be used in conjunction with the <{switch}> element and
the {{requiredExtensions}} attribute to
provide proper checking for user agent support and provide an
alternate rendering in case user agent support is not
available.

Note: 
  This specification does not define how {{requiredExtensions}}
  values should be mapped to support for different XML languages;
  a future specification may do so.


<p>It is not required that SVG user agents support the ability
to invoke other arbitrary user agents to handle embedded
foreign object types; however, all conforming SVG user agents
would need to support the <{switch}> element and
must be able to render valid SVG elements when they appear as
one of the alternatives within a <{switch}>
element.

<p>It is expected that commercial Web browsers will
support the ability for SVG to embed
CSS-formatted HTML and also MathML content,
with the rendered content subject to transformations and compositing defined in the SVG fragment.
At this time, such a capability is not a requirement.

<div class="example">

<xmp>
<?xml version="1.0" standalone="yes"?>
<svg width="4in" height="3in"
 xmlns = 'http://www.w3.org/2000/svg'>
  <desc>This example uses the 'switch' element to provide a
        fallback graphical representation of an paragraph, if
        XMHTML is not supported.</desc>
  <!-- The 'switch' element will process the first child element
       whose testing attributes evaluate to true.-->
  <switch>
    <!-- Process the embedded XHTML if the requiredExtensions attribute
         evaluates to true (i.e., the user agent supports XHTML
         embedded within SVG). -->
    <foreignObject width="100" height="50"
                   requiredExtensions="http://example.com/SVGExtensions/EmbeddedXHTML">
      <!-- XHTML content goes here -->
      <body xmlns="http://www.w3.org/1999/xhtml">
        <p>Here is a paragraph that requires word wrap
      </body>
    </foreignObject>
    <!-- Else, process the following alternate SVG.
         Note that there are no testing attributes on the 'text' element.
         If no testing attributes are provided, it is as if there
         were testing attributes and they evaluated to true.-->
    <text font-size="10" font-family="Verdana">
      <tspan x="10" y="10">Here is a paragraph that</tspan>
      <tspan x="10" y="20">requires word wrap.</tspan>
    </text>
  </switch>
</svg>
</xmp>
</div>


<div class='ready-for-wider-review'>
<h3 id="DOMInterfaces">DOM interfaces</h3>

<h4 id="InterfaceSVGImageElement">Interface SVGImageElement</h4>



<p>An [[#InterfaceSVGImageElement|SVGImageElement]] object represents an {{image}} element in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGImageElement</b> : <a>SVGGraphicsElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="embedded.html#__svg__SVGImageElement__x">x</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="embedded.html#__svg__SVGImageElement__y">y</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="embedded.html#__svg__SVGImageElement__width">width</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="embedded.html#__svg__SVGImageElement__height">height</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedPreserveAspectRatio</a> <a href="embedded.html#__svg__SVGImageElement__preserveAspectRatio">preserveAspectRatio</a>;
  attribute DOMString? <a href="embedded.html#__svg__SVGImageElement__crossOrigin">crossOrigin</a>;
};

<a>SVGImageElement</a> includes <a>SVGURIReference</a>;
</pre>

<p>The
<b id="__svg__SVGImageElement__x">x</b>,
<b id="__svg__SVGImageElement__y">y</b>,
<b id="__svg__SVGImageElement__width">width</b> and
<b id="__svg__SVGImageElement__height">height</b> IDL attributes
[=reflect=] the computed values of the {{x}}, {{y}}, {{width}} and
{{height}} properties and their corresponding
presentation attributes, respectively.

<p>The <b id="__svg__SVGImageElement__preserveAspectRatio">preserveAspectRatio</b>
IDL attribute [=reflects=] the [[#PreserveAspectRatioAttribute|preserveAspectRatio]] content attribute.

<p>The <b id="__svg__SVGImageElement__crossOrigin">crossOrigin</b> IDL attribute
[=reflects=] the {{crossorigin}} content attribute.



<h4 id="InterfaceSVGForeignObjectElement">Interface SVGForeignObjectElement</h4>



<p>An [[#InterfaceSVGForeignObjectElement|SVGForeignObjectElement]] object represents a <{foreignObject}>
in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGForeignObjectElement</b> : <a>SVGGraphicsElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="embedded.html#__svg__SVGForeignObjectElement__x">x</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="embedded.html#__svg__SVGForeignObjectElement__y">y</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="embedded.html#__svg__SVGForeignObjectElement__width">width</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="embedded.html#__svg__SVGForeignObjectElement__height">height</a>;
};
</pre>

<p>The
<b id="__svg__SVGForeignObjectElement__x">x</b>,
<b id="__svg__SVGForeignObjectElement__y">y</b>,
<b id="__svg__SVGForeignObjectElement__width">width</b> and
<b id="__svg__SVGForeignObjectElement__height">height</b> IDL attributes
[=reflect=] the computed values of the {{x}}, {{y}}, {{width}} and
{{height}} properties and their corresponding
presentation attributes, respectively.


</div>
