<h2>Rendering Model</h2>

<div class="annotation">
  <p>
    The SVG 2 rendering model will follow the rules defined by the <a href="https://www.w3.org/TR/compositing/">Compositing and Blending specification</a>.
  
  <p>
    Resolution: <a href="http://www.w3.org/2012/07/24-svg-minutes.html#item09">Seattle/Paris 2012 F2F day 3</a>.
  
  <p>
    Owner: Nikos (Action 3332).
  
  <p>
    Status: Done.
  
</div>

<h3 id="Introduction">Introduction</h3>
<p>
Implementations of SVG must implement the rendering model as described in this
chapter, as modified in the appendix on <a href="conform.html">conformance
requirements</a> which describes
situations where an implementation may deviate.
In practice variability is allowed based on limitations of the output device
(e.g. only a limited range of colors might be supported) and because of practical
limitations in implementing a precise mathematical model (e.g. for realistic
performance curves are approximated by straight lines, the approximation need
only be sufficiently precise to match the conformance requirements).


<p>The appendix on <a href="conform.html">conformance
requirements</a> describes the extent to which an actual
implementation may deviate from this description. In practice
an actual implementation <span class="ready-for-wider-review">may</span>
deviate slightly because of
limitations of the output device (e.g. only a limited range of
colors might be supported) and because of practical limitations
in implementing a precise mathematical model (e.g. for
realistic performance curves are approximated by straight
lines, the approximation need only be sufficiently precise to
match the conformance requirements).


<div class='ready-for-wider-review'>
<h3 id="RenderingTree">The rendering tree</h3>

<p> The components of the final rendered representation of an SVG document
    do not have a one-to-one relationship with the underlying
    elements in the document model.
    The appearance of the graphic instead reflects a parallel structure,
    the rendering tree,
    in which some elements are excluded and others are repeated.


<p> Many elements in the SVG namespace do not directly represent
    a component of the graphical document.
    Instead, they define graphical effects, metadata,
    content to be used to represent other elements,
    or alternatives to be displayed under certain conditions.
    In dynamic documents, certain components of the graphic
    may be rendered or not, depending on interaction or animation.
    These non-rendered elements are not directly included
    in the [=rendering tree=].

<p>
    Because SVG supports the reuse of graphical sub-components,
    some elements are rendered multiple times.
    The individual renderings may have context-dependent styling
    and may be rasterized at different scales or transformations.


<h4 id="Definitions">Definitions</h4>

<dl class="definitions">
    <dt><dfn id="TermRenderingTree" data-dfn-type="dfn" data-export="">rendering tree</dfn></dt>
    <dd>
    <p>
        The rendering tree is the set of elements being rendered
        in an [=SVG document fragment=].
        It is generated from the document tree
        by excluding [=non-rendered elements=]
        and inserting additional fragments for [=re-used graphics=].
        Graphics are painted and composited in rendering-tree order,
        subject to re-ordering based on the
        {{paint-order}} property.
        Note that elements that have no visual paint may still be in the rendering tree.
    
  </dd>
  <dt><dfn id="TermRenderedElement" data-dfn-type="dfn" data-export="">rendered element</dfn></dt>
  <dd>
    <p>
        An element that has a direct representation in the
        [=rendering tree=] for the current document.
        Includes a rendered [=instance=] of an element in a [=use-element shadow tree=].
        Does not include elements that affect rendering
        as the source definition of re-used graphics
        but are not directly rendered themselves.
        See <a href="#Rendered-vs-NonRendered">Rendered versus non-rendered elements</a>
    
  </dd>
  <dt><dfn id="TermNonRenderedElement" data-dfn-type="dfn" data-export="">non-rendered element</dfn></dt>
  <dd>
    <p>
        An element that does not have a direct representation in the
        [=rendering tree=] for the current document.
        It may nonetheless affect the rendering tree as re-used graphics
        or graphical effects.
        See <a href="#Rendered-vs-NonRendered">Rendered versus non-rendered elements</a>.
    
  </dd>
  <dt><dfn id="TermReusedGraphics" data-dfn-type="dfn" data-export="">re-used graphics</dfn></dt>
  <dd>
    <p>
        Graphical components that are included in the rendering tree
        but do not have a single direct equivalent element
        in the document model.
        They may be represented through shadow DOM elements
        (as in graphics re-used with a {{use}} element),
        or as image fragments generated as part of a graphical effect
        (as in patterns or masks).
    
  </dd>

  <dt><dfn id="TermNeverRenderedElement" data-dfn-type="dfn" data-export="">never-rendered element</dfn></dt>
  <dd>
      <p>
          Any element type that is <em>never directly rendered</em>,
          regardless of context or {{display}} style value.
          It includes the following elements:
          @@never-rendered@@;
          it also includes a {{symbol}} element that is not
          the [=instance root=] of a [=use-element shadow tree=].
      
  </dd>
  <dt><dfn id="TermRenderableElement" data-dfn-type="dfn" data-export="">renderable element</dfn></dt>
  <dd>
    <p>
        Any element type that <em>can</em> have a direct representation
        in the [=rendering tree=],
        as a graphic, container, text, audio, or animation.
        It includes the following elements:
        @@renderable@@;
        it also includes a {{symbol}} element that <em>is</em>
        the [=instance root=] of a [=use-element shadow tree=].
    
    <p> A renderable element may or may not be rendered
        in a given document or point in time.
    
  </dd>

</dl>

<h4 id="Rendered-vs-NonRendered">Rendered versus non-rendered elements</h4>

<p> At any given time, every SVG element
    (or [=element instance=] in a [=use-element shadow tree=])
    is either rendered or non-rendered.
    Whether an element is currently rendered or not affects
    not only its visual display but also interactivity
    and geometric calculations.


<p>
    An element is <em>not rendered</em> in any of these five situations:

<ul>
    <li>[=never-rendered element=] types</li>
    <li>elements excluded because of [=conditional processing attributes=]
        or {{switch}} structures
    </li>
    <li>elements with a computed style value of <code>none</code>
        for the {{display}} property
    </li>
    <li>detached from the DOM tree</li>
    <li>descendent elements of other non-rendered elements
    </li>
</ul>

<p> Non-rendered elements:

<ul>
  <li>have no visual effect on the graphic,
      except when they are used in the rendering of another element
      that references them.</li>

  <li>do not contribute to the net geometry of
      [=clipping paths=] or [=masks=]
      when they are descendants of a
      {{clipPath}} or {{mask element}} </li>

  <li>are not sensitive to <a href="interact.html#UIEvents">pointer events</a></li>

  <li>cannot receive [=focus=]</li>

  <li>do not contribute to <a href="coords.html#ObjectBoundingBox">bounding box
  calculations</a></li>

  <li>are not considered when performing <a href="text.html#TextLayout">text layout</a></li>
</ul>

<p> Non-rendered elements are not represented in the document accessibility tree.
    Nonetheless, they remain part of the document model, and
    participate in <a href="styling.html">style inheritance and cascade</a>.



<h4 id="VisibilityControl">Controlling visibility: the effect of the <span class="property">'display'</span> and <span class="property">visibility</span> properties</h4>

<p>
    SVG uses two properties to toggle the visible display of
    elements that are normally rendered:
    {{display}} and {{visibility}}.
    Although they have a similar visible effect in static documents,
    they are conceptually distinct.


Note: See the CSS 2.1 specification for the definitions
of {{display}} and {{visibility}}.
[[CSS2]]

<p>
    Setting  {{display}} to <span class="prop-value">none</span>
    results in the element not being rendered.
    When applied to
    [=graphics elements=],
    [=text content elements=],
    and [=container elements=] that are normally rendered,
    setting {{display}} to <span class="prop-value">none</span>
    results in the element (and all its descendents)
    not becoming part of the [=rendering tree=].
    Note that {{display}} is not an inherited property.

<p>
    Elements that have any other {{display}} value than
<span class="prop-value">none</span> are rendered as normal.

<p>
    The {{display}} property only applies to [=renderable elements=].
    Setting <code>display: none</code> on an element
    that is [=never directly rendered=]
    or [=not rendered=] based on conditional processing
    has no effect.


<p>
    The {{display}} property affects the direct processing
    of a given element, but it does not prevent it from
    being referenced by other elements.
    For example, setting
    <span class="prop-value">display: none</span> on a {{path}} element
    will prevent that element from getting rendered directly onto the
    canvas, but the {{path}} element can still be referenced by a
    {{textPath}} element and its geometry will be used
    in text-on-a-path processing.


<p>
    When applied to a [=graphics element=] or {{use}} element,
    setting {{visibility}} to <span class="prop-value">hidden</span>
    or <span class="prop-value">collapse</span>
    results in the element not being painted.
    It is, however, still part of the [=rendering tree=].
    It may be sensitive to pointer events
    (depending on the value of {{pointer-events}}),
    may receive focus (depending on the value of {{tabindex}}),
    contributes to bounding box calculations and clipping paths,
    and does affect text layout.


<p>
    The {{visibility}} property only directly affects the rendering of
    [=graphics elements=], [=text content elements=], and the
    {{a}} element when it is a child of [=text content element=].
    Since {{visibility}} is an inherited property, however,
    although it has no effect on a {{use}} element or [=container element=] itself,
    its inherited value can affect descendant elements.


<h4 id="ReusedGraphics">Re-used graphics</h4>

<p> Graphical content defined in one part of the document
    (or in another document)
    may be used to render other elements.
    There are two types of re-used graphics from a rendering perspective:

<ul>
  <li>
    shadow DOM elements,
    such as those generated by {{use}} elements
    or by cross-references between paint servers;
  </li>
  <li>
    content re-used as part of a graphical effect on another element,
    including the child content of
    [=markers=], [=paint server elements=],
    {{clipPath}}, and {{mask element}}.
  </li>
</ul>

<p>
  Shadow DOM elements are rendered in the same way as normal elements,
  as if the host element (e.g., the {{use}} element)
  was a container and the shadow content was its descendents.
  Style and geometry properties on the shadow DOM elements
  are resolved independently from those on their [=corresponding element=]
  in the source document.
  The {{display}} property has its normal effect on shadow elements,
  except for special rules that apply to the {{symbol}} element.

<p>
  For blending purposes, the {{use}} element forms a [=non-isolated group=].


<p>
  In contrast,
  graphical effects elements generate a self-contained SVG fragment
  which is rendered independently as a [=stacking context=]
  and an [=isolated group=].
  The canvas for this fragment is scaled

  The graphical effect element's child content
  is rendered and composited into this canvas.
  The flattened canvas as a whole is treated as a vector image
  when compositing and blending with other paint layers

<p>
  The {{display}} property on any child content of a graphical effects element
  has its normal effect when set to <code>none</code>,
  excluding that subtree from being used in rendering.
  However, the graphical effect is not altered
  by a value of <code>display: none</code>
  on the graphical effect element or an ancestor.

</div>

<div class="ready-for-wider-review">

<h3 id="PaintersModel">The painters model</h3>

<p>SVG uses a "painters model" of rendering. [=Paint=]
is applied in successive operations to the output device such
that each operation paints onto some area of the output device,
possibly obscuring paint that has previously been laid down.

After each object or group is painted, it becomes part of the background
for the next painting operation.

SVG 2 supports advanced blending modes and compositing operations that
control how each painting operation interacts with the background.
The rules governing these painting operations are outlined in the
<a href="https://www.w3.org/TR/compositing/">Compositing and Blending Specification</a>.


<h3 id="RenderingOrder">Rendering order</h3>
<p>Elements in SVG are positioned in three dimensions. In addition to their
position on the x and y axis of the [=SVG viewport=], SVG elements are also
positioned on the z axis. The position on the z-axis defines the order that
they are painted.

<p>Along the z axis, elements are grouped into <dfn id="TermStackingContext" data-dfn-type="dfn" data-export="">stacking contexts</dfn>.
</div>

<h4 id="EstablishingStackingContex">Establishing a stacking context in SVG</h4>
<p>A new stacking context must be established at an SVG element for its descendants if:

<ul>
  <li>it is the root element</li>

  <li>the element is an [=outermost svg element=], or a <{foreignObject}>,
  {{image}}, {{marker element}}, {{mask element}}, {{pattern}},
  {{symbol}} or {{use}} element</li>

  <li>the element is an inner <{svg}> element and the computed value of its
  {{overflow}} property is a value other than <span class='prop-value'>visible</span></li>

  <li>the element is subject to explicit clipping:
    <ul>
      <li>the {{clip}} property applies to the element and it has a
      computed value other than <span class='prop-value'>auto</span></li>

      <li>the {{clip-path}} property applies to the element and it has a
      computed value other than <span class='prop-value'>none</span></li>
    </ul>
  </li>

  <li>the {{opacity}} property applies to the element and it has a
  computed value other than <span class='prop-value'>1</span></li>

  <li>the {{mask property}} property applies to the element and it has a computed
  value other than <span class='prop-value'>none</span></li>

  <li>the {{filter property}} property applies to the element and it has a
  computed value other than <span class='prop-value'>none</span></li>

  <li class="ready-for-wider-review">a property defined in another specification is
  applied and that property is defined to establish a stacking context in SVG</li>
</ul>

<p>Stacking contexts are conceptual tools used to describe the
order in which elements must be painted one on top of the other when the
document is rendered, and for determining which element is highest when
determining the target of a pointer event. Stacking contexts do
not affect the position of elements in the DOM tree, and their presence or
absence does not affect an element's position, size or orientation in the
canvas' X-Y plane - only the order in which it is painted.

<p>Stacking contexts can contain further stacking contexts. A stacking context is
atomic from the point of view of its parent stacking context; elements in
ancestor stacking contexts may not come between any of its elements.

<p>Each element belongs to one stacking context. Elements in a stacking context
must be stacked according to document order.

<p>With the exception of the <{foreignObject}> element, the back to front
stacking order for a stacking context created by an SVG element is:

<ol>
  <li>the background and borders of the element forming the stacking
  context, if any</li>

  <li>descendants, in tree order</li>
</ol>

<p>Since the <{foreignObject}> element creates a "fixed position containing block" in
CSS terms, the normative rules for the stacking order of the stacking context
created by <{foreignObject}> elements are the rules in Appendix E of CSS 2.1.

<h3 id="Elements">How elements are rendered</h3>
<div class="ready-for-wider-review">
<p>
Individual [=graphics elements=] are treated as if they are a [=non-isolated group=],
the components (fill, stroke, etc) that make up a graphic element
(See  <a href="#PaintingShapesAndText">Painting shapes and text</a>) being
members of that group. See <a href="#Grouping">How groups are rendered</a>.

</div>

<h3 id="Grouping">How groups are rendered</h3>
<div class="ready-for-wider-review">
</div>
<div class="ready-for-wider-review">
<p>
Grouping elements, such as the {{g}} element (see [=container elements=]
) create a [=compositing group=].
Similarly, a {{use}} element creates a compositing group for its shadow content.
The [=Compositing and Blending=]
specification normatively describes how to render [=compositing groups=].
In SVG, effects may be applied to a group. For example, opacity, filters
or masking. These effects are applied to the rendered result of the group
immediately before any transforms on the group are applied, which are applied
immediately before the group is blended and composited with the
[=group backdrop=]. Applying any such effects to a group makes that
group isolated.
<br/><br/>
Thus, rendering a [=compositing group=] follows the following steps:<br/>
If the group is isolated:

<ol>
<li>The [=initial backdrop=] is set to a new buffer initialised with
rgba(0,0,0,0)</li>
<li>The contents of the group that are [=graphics elements=] or
{{g element}} elements are rendered
<a href="#RenderingOrder">in order</a>, onto the
[=initial backdrop=]</li>
<li>filters and other effects that modify the group canvas are applied
<div class="note">
<p class='ready-for-wider-review'>To provide for high quality rendering, filter
primitives and other bitmap effects must be applied in the
[=operating coordinate space=].
</div>
</li>
<li>Group transforms are applied</li>
<li>The group canvas is blended and composited with the [=group backdrop=]</li>
</ol>
else (the group is not isolated):
<ol>
<li>The [=initial backdrop=] is set to the [=group backdrop=]</li>
<li>The contents of the group that are [=graphics elements=] or
{{g element}} elements are rendered
<a href="#RenderingOrder">in order</a>, onto the
[=initial backdrop=]. The group transforms are applied to each element
as they are rendered.</li>
</ol>
</div>

<h4 id="ObjectAndGroupOpacityProperties">Object and group opacity: the effect of the <span class="property">opacity</span> property</h4>

Note: See the CSS Color Module Level 3 for the definition
of {{opacity}}. [<a href="refs.html#ref-css-color-3">css-color-3</a>]

<p>The {{opacity}} property specifies how opaque a given
graphical element or container element will be when it is
painted to the canvas.  When applied to a container element,
this is known as <em>group opacity</em>, and when applied to
an individual rendering element, it is known as <em>object
opacity</em>.  The principle for these two operations however
is the same.

<p>There are several other opacity-related properties in SVG:

<ul>
<li>{{fill-opacity}}, which specifies the opacity of a fill
operation;</li>

<li>{{stroke-opacity}}, which specifies the opacity of a stroking
operation; and</li>

<li>{{stop-opacity}}, which specifies the opacity of a gradient stop.</li>
</ul>

<p>These four opacity properties are involved in intermediate rendering operations.
Object and group opacity however can be thought of as a post-processing operation.
Conceptually, the object or group to which {{opacity}} applies
is rendered into an RGBA offscreen image.  The offscreen image as whole is then blended
into the canvas with the specified {{opacity}} value used uniformly
across the offscreen image.
<span class="ready-for-wider-review">
Thus, the presence of {{opacity property}} causes the group to be
[=isolated=].
</span>


<p>The {{opacity}} property applies to the following SVG elements:
{{svg}}, {{g}}, {{symbol}}, {{marker element}},
{{a}}, {{switch}}, {{use}} and [=graphics elements=].

<div class="example">
<p>The following example illustrates various usage of the {{opacity}}
property on objects and groups.

<pre class=include>
path: images/masking/opacity01.svg
</pre>

<div class='figure'>
<img class='bordered' src='images/masking/opacity01.svg' alt='Image showing different groups of circles blended into the background.'>
<p class='caption'>Each group of red and green circles is first rendered
to an offscreen image before being blended with the background
blue rectangle as a whole, with the given {{opacity}} values.
</div>

<p>In the example, the top row of circles have differing opacities,
ranging from 1.0 to 0.2. The bottom row illustrates five {{g}} elements,
each of which contains overlapping red and green circles, as follows:

<ul>
<li>The first group shows the opaque case for reference. The group has
opacity of 1, as do the circles.</li>

<li>The second group shows group opacity when the elements in the group are
opaque.</li>

<li>The third and fourth group show that opacity is not commutative. In the
third group (which has opacity of 1), a semi-transparent green circle is
drawn on top of a semi-transparent red circle, whereas in the fourth group a
semi-transparent red circle is drawn on top of a semi-transparent green
circle. Note that area where the two circles intersect display different
colors. The third group shows more green color in the intersection area,
whereas the fourth group shows more red color.</li>

<li>The fifth group shows the multiplicative effect of opacity settings.
Both the circles and the group itself have opacity settings of .5. The
result is that the portion of the red circle which does not overlap with the
green circle (i.e., the top/right of the red circle) will blend into the
blue rectangle with accumulative opacity of .25 (i.e., .5*.5), which, after
blending into the blue rectangle, results in a blended color which is 25%
red and 75% blue.</li>
</ul>
</div>

<h3 id="TypesOfGraphicsElements">Types of graphics elements</h3>

<p>SVG supports three fundamental types of [=graphics elements=]
that can be rendered onto the canvas:

<ul>
<li>[=Shapes=], which represent some combination of straight line
and curves</li>
<li>Text, which represents some combination of character glyphs</li>
<li>Raster images, which represent an array of values that
specify the paint color and opacity (often termed alpha) at a
series of points on a rectangular grid. (SVG requires support
for specified raster image formats under
<a href="conform.html">conformance requirements</a>.)</li>
</ul>

<h4 id="PaintingShapesAndText">Painting shapes and text</h4>

<p>Shapes and text can be [=filled=] (i.e., apply paint to the
interior of the shape) and [=stroked=] (i.e., apply paint
along the outline of the shape).

<p>For certain types of shapes, <a href="painting.html#Markers">marker
symbols</a> (which themselves can consist of any combination of shapes,
text and images) can be drawn at positions along the
shape boundary. Each marker symbol
is painted as if its graphical content were expanded into the
SVG document tree just after the shape object which is using
the given marker symbol. The graphical contents of a marker
symbol are rendered using the same methods as graphics
elements. Marker symbols are not applicable to text.

<p>The order in which fill, stroke and markers are painted is determined
by the {{paint-order}} property. The default is that
fill is painted first, then the stroke, and then the
marker symbols. The marker symbols are rendered in order along
the outline of the shape, from the start of the shape to the
end of the shape.

<p>The fill and stroke operations are entirely independent;
for instance, each fill or stroke operation has its own opacity setting.

<p>SVG supports numerous built-in types of paint which can
be used in fill and stroke operations. These are described in
<a href="pservers.html">Paint Servers</a>.

<h4 id="PaintingRasterImages">Painting raster images</h4>

<p>When a raster image is rendered, the original samples are
"resampled" using standard algorithms to produce samples at the
positions required on the output device. Resampling
requirements are discussed under
<a href="conform.html">conformance requirements</a>.
<p class="ready-for-wider-review">
As in HTML [<a href="refs.html#ref-html">HTML</a>, 10.4.2],
all animated images with the same absolute URL and the same image
data are expected to be rendered synchronised to the same timeline as a group,
with the timeline starting at the time of the least recent addition to the
group.

<p class="ready-for-wider-review">
When a user agent is to restart the animation for an img element showing an
animated image, all animated images with the same absolute URL and the same
image data in that img element's node document are expected to restart their
animation from the beginning.


<h3 id="FilteringPaintRegions">Filtering painted regions</h3>
<p>SVG allows any painting operation to be filtered. (See
<a href="https://www.w3.org/TR/filter-effects/">Filter Effects</a>.)

<p>In this case the result must be as though the paint
operations had been applied to an intermediate canvas
initialized to transparent black, of a size determined by the
rules given in <a href="https://www.w3.org/TR/filter-effects/">Filter Effects</a> then
filtered by the processes defined in
<a href="https://www.w3.org/TR/filter-effects/">Filter Effects</a>.

<div class="ready-for-wider-review">
<h3 id="ClippingAndMasking">Clipping and masking</h3>

<p>SVG supports the following clipping/masking features:

<ul>
<li>clipping paths, which either uses
any combination of {{path}}, {{text}} and
[=basic shapes=] or basic shapes to serve as
the outline of a (in the absence of anti-aliasing) 1-bit
mask, where everything on the "inside" of the outline is
allowed to show through but everything on the outside is
masked out</li>

<li>masks, which are
[=container elements=]
which can contain [=graphics elements=]
or other container elements which define a set of graphics
that is to be used as a semi-transparent mask for compositing
foreground objects into the current background.</li>
</ul>

<p>Both, clipping and masking, are specified in the module CSS Masking
[<a href="refs.html#ref-css-masking-1">css-masking-1</a>].
</div>

<h3 id="ParentCompositing">Parent compositing</h3>
<p>SVG document fragments can be semi-opaque.
<p class="ready-for-wider-review">
In accordance with the [=Compositing and Blending=] specification,
the <{svg}> element always creates an [=isolated=] group.
When an SVG document is a top-level document,
meaning it is not embedded in another document,
the root <{svg}> element
is considered to be the [=Page Group=] and is composited with
a backdrop of white with 100% opacity.
In all other cases, the SVG document or document fragment is composited into the parent
document with opacity preserved.


<h3 id="OverflowAndClipProperties">The effect of the <span class="property">overflow</span> property</h3>

Note: See the Cascading Style Sheets Level 2 Revision 1 (CSS 2.1)
Specification [[CSS2]] for the definition of
{{overflow}}.
<div class="ready-for-wider-review">
<table class="data compact">
<caption>A summary of the behavior of the {{overflow}} property in SVG.
</caption>
<thead>
<tr>
<th>element</th>
<th>initial</th>
<th>ua stylesheet</th>
<th>auto</th>
<th>visible</th>
<th>hidden</th>
<th>scroll</th>
</tr>
</thead>
<tbody>
<tr>
<th>document root svg</th><td>visible</td><td>n/a</td><td>visible | scroll</td><td>visible</td><td>hidden</td><td>scroll</td>
</tr>
<tr>
<th>other svg</th><td>visible</td><td>hidden</td><td>visible | scroll</td><td>visible</td><td>hidden</td><td>scroll</td>
</tr>
<tr>
<th>text</th><td>visible</td><td>hidden</td><td>visible</td><td>visible</td><td>hidden</td><td>hidden</td>
</tr>
<tr>
<th>pattern</th><td>visible</td><td>hidden</td><td>visible</td><td>visible</td><td>hidden</td><td>hidden</td>
</tr>
<tr>
<th>marker</th><td>visible</td><td>hidden</td><td>visible</td><td>visible</td><td>hidden</td><td>hidden</td>
</tr>
<tr>
<th>symbol</th><td>visible</td><td>hidden</td><td>visible</td><td>visible</td><td>hidden</td><td>hidden</td>
</tr>
<tr>
<th>image</th><td>visible</td><td>hidden</td><td>visible</td><td>visible</td><td>hidden</td><td>hidden</td>
</tr>
<tr>
<th>foreignObject</th><td>visible</td><td>hidden</td><td>visible | scroll</td><td>visible</td><td>hidden</td><td>scroll</td>
</tr>
</tbody>
</table>

<p>The {{overflow}} property has the same parameter values and has the
same meaning <a href="https://www.w3.org/TR/2011/REC-CSS2-20110607/visufx.html#propdef-overflow">as defined in CSS 2.1</a>
([[CSS2]], section 11.1.1);
however, the following additional points apply:

<ul>
  <li>
  If the {{overflow}} property has a value of 'visible',
  the property has no effect (i.e., a clipping rectangle is not created).
  </li>

  <li>For those elements to which the {{overflow}} property can apply.
  If the {{overflow}} property has the value <span class='prop-value'>
  hidden</span> or <span class='prop-value'>scroll</span>, a clip,
  the exact size of the SVG viewport is applied.
  </li>

  <li>
  When <span class='prop-value'>scroll</span> is specified on an
  <{svg}> element and if the user agent uses a scrolling mechanism that
  is visible on the screen (such as a scroll bar or a panner), that mechanism
  should be displayed for the SVG viewport whether or not any of its content is clipped.
  </li>

  <li>
  Within SVG content, the value <span class='prop-value'>auto</span> implies
  that all rendered content for child elements must be
  <span class='prop-value'>visible</span>, either through a scrolling
  mechanism, or by rendering with no clip.
  For elements where the value of <span class='prop-value'>scroll</span> results
  in a scrolling mechanism being used by the user agent, then a value of
  <span class='prop-value'>auto</span> may be treated as
  <span class='prop-value'>scroll</span>. If the user agent has no scrolling
  mechanism, the content would not be clipped, or the value 'scroll' is treated
  as <span class='prop-value'>hidden</span>, then the value
  <span class='prop-value'>auto</span> must be treated as
  <span class='prop-value'>visible</span>
  </li>
</ul>

<div class="note">
Although the initial value for {{overflow}} is auto. In the User Agent style sheet,
overflow is overridden for the <{svg}> element when it is not the root
element of a stand-alone document, the {{pattern}} element, and the {{marker element}} element to be hidden by default.
</div>
</div> <!-- ready-for-wider-review -->
