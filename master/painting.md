<h2 id="chap-painting">Painting: Filling, Stroking and Marker Symbols</h2>

<div class="ready-for-wider-review">
<h3 id="painting-intro">Introduction</h3>

<h4 id="painting-Definitions">Definitions</h4>
<dl class="definitions">

  <dt><dfn id="TermFill" data-dfn-type="dfn" data-export="">fill</dfn></dt>
  <dd>The operation of [=painting=] the interior of a
  [=shape=] or the interior of the
  character glyphs in a text string.</dd>

  <dt><dfn id="TermStroke" data-dfn-type="dfn" data-export="">stroke</dfn></dt>
  <dd>The operation of [=painting=] the outline
  of a [=shape=] or the outline of
  character glyphs in a text string.</dd>

</dl>

<p>Graphical elements that define a shape – <{path}> elements, [=basic shapes=],
and [=text content elements=] – are rendered by being <strong>filled</strong>,
which is painting the interior of the object, and <strong>stroked</strong>, which is
painting along the outline of the object.  Filling and stroking are both
<strong>painting</strong> operations.  SVG 2 supports a number of
different paints that the fill and stroke of a graphical element can be painted with:

<ul>
  <li>a single color,</li>
  <li>a gradient (linear or radial)</li>
  <li>a pattern (vector or raster, possibly tiled),</li>
  <li>other images as specified using CSS Image Value syntax [<a href="refs.html#ref-css-images-3">css-images-3</a>].</li>
</ul>

<p>The paint to use for filling and stroking an element is specified using the
'fill' and 'stroke' properties.  The following section describes
the different values that can be used for these properties.

<p>Other properties, such as 'fill-opacity' and 'stroke-width',
also have an effect on the way fill and stroke paint is applied to the
canvas.  The <a href='#FillProperties'>Fill properties</a> and <a href='#StrokeProperties'>Stroke properties</a>
sections below describe these properties.

<p>Some graphics elements – <{path}> elements and <a>basic
shapes</a> – can also have <strong>marker symbols</strong>
drawn at their vertices or at other positions along the path that
they describe.  The <a href='#Markers'>Markers</a> section below describes
how markers can be defined and used.

<p class="annotation">SVG 2 adds markers on shapes. Resolved at
<a href="http://www.w3.org/2013/06/03-svg-minutes.html#item03">Tokyo F2F</a>.

<!--
<p>SVG uses the general notion of a <strong>paint server</strong>. Paint
servers are specified using a [=URL Reference=]
on a 'fill' or 'stroke' property.
<a href="pservers.html">Gradients and patterns</a> are just specific types of
paint servers.
-->

<h3 id="SpecifyingPaint">Specifying paint</h3>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Add new paint values for referencing current fill paint, stroke paint, etc.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/07/29-svg-minutes.html#item02">We will add new paint values currentFillPaint, currentStrokePaint etc. to SVG 2</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>Among other things, to provide an easy way to match marker color to stroke color.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Chris (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3094">ACTION-3094</a>)</td>
    </tr>
  </table>
</div>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Addition:</th>
      <td>Allow multiple paints in fill and stroke.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2013/06/03-svg-minutes.html#item10">We will allow multiple paints in the fill and stroke properties in SVG 2.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>Useful for creating cross hatchings, putting a partially transparent pattern on top of a solid fill, etc.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Tav (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3500">ACTION-3500</a>)</td>
    </tr>
    <tr>
      <th>Deferred:</th>
      <td>This was dropped for SVG 2, but will be added later in sync with
        <a href="https://drafts.fxtf.org/paint/">CSS Fill and Stroke Level 3</a>
      </td>
    </tr>
  </table>
</div>

<p>The 'fill' and 'stroke' properties, defined below, are used to
specify the <dfn id="TermPaint" data-dfn-type="dfn" data-export="">paint</dfn> used to render the interior of and the
stroke around shapes and text. A paint specification describes a way of putting
color values on to the canvas and is composed of one or more paint layers.
Four types of paints within these paint layers are supported:
<a href="https://www.w3.org/TR/css3-values/#colors">solid colors</a>,
<a href="pservers.html#Gradients">gradients</a>, and
<a href="pservers.html#Patterns">patterns</a>.

<p>A <a>&lt;paint&gt;</a> value is defined as follows:
<p class="definition prod">
<dfn id="DataTypePaint" data-dfn-type="type" data-export="">&lt;paint&gt;</dfn>
= none
| <a>&lt;color&gt;</a>
| <a>&lt;url&gt;</a> [none | <a>&lt;color&gt;</a>]?
| context-fill | context-stroke


<p>With the possible values:
<dl>
  <dt>none</dt>
  <dd>No paint is applied in this layer.</dd>

  <dt><a>&lt;url&gt;</a> [none | <a>&lt;color&gt;</a>]?</dt>
  <dd>A URL reference to a <dfn id="TermPaintServerElement" dfn export>paint server element</dfn>,
  which is an element that defines a <a href="pservers.html">paint server</a>:
  <{linearGradient}>, <{radialGradient}> or <{pattern}>, optionally followed by a fall-back
  value that is used if the paint server reference cannot be resolved.</dd>

  <dt><a>&lt;color&gt;</a></dt>
  <dd>A solid color paint.</dd>

  <dt><dfn id="painting-context-paint" data-dfn-type="dfn" data-export="">context-fill</dfn></dt>
  <dd>Use the paint value of 'fill' from a [=context element=].</dd>

  <dt><dfn id="painting-context-stroke" data-dfn-type="dfn" data-export="">context-stroke</dfn></dt>
  <dd>Use the paint value of 'stroke' from a [=context element=].</dd>
</dl>

<p>A <a>&lt;paint&gt;</a> allows a paint server reference, to be optionally followed
by a <a>&lt;color&gt;</a> or the keyword <span class='prop-value'>none</span>.
When this optional value is given, the <a>&lt;color&gt;</a> value or the value
<span class='prop-value'>none</span> is a fallback value to use if the paint
server reference in the layer is invalid (due to pointing to an element that
does not exist or which is not a valid paint server).

Note: Note that this is slightly different from CSS background syntax, where
a background image and color specified in the final layer of a 'background'
value will result in both the image and color being rendered.

<p>If a paint server reference in a <a>&lt;paint&gt;</a> is invalid, and no
fall-back value is given, no paint is rendered for that layer.

<p class="annotation">This is changed from SVG 1.1 behavior where the document
is in error if a paint server reference is invalid and there is no fallback
color specified.

<div class="example">
  <xmp>
<rect width="100" height="100" fill="url(#MyHatch) powderblue">
  </xmp>
  <div class="figure">
    <img
no-autosize alt="An example with a fallback solid paint fill."
       src="images/painting/fallback_paint.svg">
    <p class="caption">The left rectangle shows the expected fill if MyHatch is defined.
    The right rectangle shows the expected fill if MyHatch is missing.
  </div>
</div>

<p>For any <a>&lt;color&gt;</a> value, all color syntaxes
defined in <a href="https://www.w3.org/TR/css-color-3/#colorunits">CSS Color Module Level 3</a>
must be supported, including <span class='prop-value'>rgb()</span>,
<span class='prop-value'>rgba()</span>,
<span class='prop-value'>hsl()</span>,
<span class='prop-value'>hsla()</span>,
the <a href="https://www.w3.org/TR/css-color-3/#svg-color">extended color keywords</a> and
the <span class='prop-value'>currentColor</span> value.

<p id="context-paint">The <span class='prop-value'>context-fill</span> and <span class='prop-value'>context-stroke</span>
values are a reference to the paint layers generated for the 'fill' or 'stroke'
property, respectively, of the <dfn id="TermContextElement" data-dfn-type="dfn" data-export="">context element</dfn>
of the element being painted.  The context element of an element is defined as follows:

<ul>
  <li>If the element is within a <{marker}> element, and
  is being rendered as part of that marker due to being referenced
  via a [=marker property=], then the context element
  is the element referencing that <{marker}> element.</li>
  <li>If the element is within a sub-tree that is instantiated
  with a <{use}> element, then the context element is
  that <{use}> element.</li>
  <li>Otherwise, there is no context element.</li>
</ul>

<p>If there is no context element and these keywords are used, then no paint is
applied.

<p>
When the context paint layers include paint server references, then the
coordinate space and the bounding box used
to scale the paint server elements and content are
those of the [=context element=].
In other words, any gradients and patterns referenced with these keywords
should be continuous from the main shape to the markers,
or from one element within a [=use-element shadow tree=] to another.


<p>If the referenced value of 'fill' or 'stroke' is a
<span class='prop-value'>context-fill</span> and <span class='prop-value'>context-stroke</span>
value, then those contextual referencing is recursive.

<div class="example">

<pre class=include-raw>
path: images/painting/marker-context.svg2.svg
</pre>
  
  <div class="figure">
    <img
       alt="An example of the content-stroke keyword used in a marker"
       src="images/painting/marker-context.svg11.svg" height="200">
    <p class="caption">The marker is defined using a shape whose
    'stroke' is set to <span class='prop-value'>context-stroke</span>.
    This causes the marker to take on the color of each <{path}>
    element that uses the marker.
  </div>
</div>


<h3 id="ColorProperty">The effect of the <span class="property">color</span> property</h3>

Note: See the CSS Color Module Level 3 specification for the
definition of 'color'.
[<a href="refs.html#ref-css-color-3">css-color-3</a>]

<p>The 'color' property is used to provide a potential indirect value,
<span class="prop-value">currentColor</span>, for the 'fill',
'stroke', 'stop-color', 'flood-color' and
'lighting-color' properties.  The property has no other effect
on SVG elements.

<div class="example">
  <p>The following example shows how the inherited value of the
  'color' property from an HTML document can be used to
  set the color of SVG text in an inline SVG fragment.

  <xmp>
<!DOCTYPE html>
<style>
body { color: #468; font: 16px sans-serif }
svg { border: 1px solid #888; background-color: #eee }
</style>
<p>Please see the diagram below:
<svg width="200" height="100">
  <g fill="currentColor">
    <text x="70" y="55" text-anchor="end">START</text>
    <text x="130" y="55">STOP</text>
    <path d="M 85,45 h 25 v -5 l 10,10 -10,10 v -5 h -25 z"/>
  </g>
</svg>
</xmp>

  <div class="figure">
    <div class="bordered" style="color: #468; font: 16px sans-serif; display: inline-block; text-align: left; padding: 32px 128px 32px 32px">
      <p style="margin-top: 0; margin-bottom: 1em">Please see the diagram below:
      <svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" style="border: 1px solid #888; background-color: #eee">
        <g fill="currentColor">
          <text x="70" y="55" text-anchor="end">START</text>
          <text x="130" y="55">STOP</text>
          <path d="M 85,45 h 25 v -5 l 10,10 -10,10 v -5 h -25 z"/>
        </g>
      </svg>
    </div>
    <p class="caption">The text and arrow in the SVG fragment are filled
    with the same color as the inherited 'color' property.
  </div>
</div>

<h3 id="FillProperties">Fill properties</h3>

<h4 id="SpecifyingFillPaint">Specifying fill paint: the <span class="property">fill</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="FillProperty" data-dfn-type="property" data-export="">fill</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><a>&lt;paint&gt;</a></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>black</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified, but with <a>&lt;color&gt;</a> values computed and
    <a>&lt;url&gt;</a> values made absolute</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The 'fill' property paints the interior of the given graphical
element. The area to be painted consists of any areas inside the outline
of the shape. To determine the inside of the shape, all subpaths are
considered, and the interior is determined according to the rules
associated with the current value of the 'fill-rule' property.
The zero-width geometric outline of a shape is included in the area to
be painted.

<p>The fill operation fills [=open subpaths=] by performing the fill
operation as if an additional "closepath" command were added to the
path to connect the last point of the subpath with the first point of
the subpath. Thus, fill operations apply to both [=open subpaths=] within
<{path}> elements (i.e., subpaths without a closepath command) and
<{polyline}> elements.

<h4 id="WindingRule">Winding rule: the <span class="property">fill-rule</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="FillRuleProperty" property export>fill-rule</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>nonzero | evenodd</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>nonzero</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

<p>The 'fill-rule' property indicates the algorithm (or
<em>winding rule</em>) which is to
be used to determine what parts of the canvas are included inside the
shape. For a simple, non-intersecting path, it is intuitively clear
what region lies "inside"; however, for a more complex path, such as a
path that intersects itself or where one subpath encloses another, the
interpretation of "inside" is not so obvious.

<p>The 'fill-rule' property provides two options for how the
inside of a shape is determined:

<dl>
  <dt><span class='prop-value'>nonzero</span></dt>
  <dd>
    <p>This rule determines the "insideness" of a point on the
    canvas by drawing a ray from that point to infinity in any
    direction and then examining the places where a segment of
    the shape crosses the ray. Starting with a count of zero,
    add one each time a path segment crosses the ray from left
    to right and subtract one each time a path segment crosses
    the ray from right to left. After counting the crossings,
    if the result is zero then the point is <em>outside</em>
    the path. Otherwise, it is <em>inside</em>. The following
    drawing illustrates the <span class='prop-value'>nonzero</span>
    rule:

    <div class="figure">
      <img no-autosize class="bordered" src="images/painting/fillrule-nonzero.svg" alt="Image showing nonzero fill rule">
      <p class="caption">The effect of a nonzero fill rule on paths with self-intersections
      and enclosed subpaths.
    </div>
  </dd>

  <dt><span class='prop-value'>evenodd</span></dt>
  <dd>
    <p>This rule determines the "insideness" of a point on the
    canvas by drawing a ray from that point to infinity in any
    direction and counting the number of path segments from the
    given shape that the ray crosses. If this number is odd,
    the point is inside; if even, the point is outside. The
    following drawing illustrates the <span class='prop-value'>evenodd</span>
    rule:

    <div class="figure">
      <img no-autosize class="bordered" src="images/painting/fillrule-evenodd.svg" alt="Image showing evenodd fill rule">
      <p class="caption">The effect of an evenodd fill rule on paths with self-intersections
      and enclosed subpaths.
    </div>
  </dd>
</dl>

Note: The above descriptions do not specify what to do if a path
segment coincides with or is tangent to the ray. Since any ray will do,
one may simply choose a different ray that does not have such problem
intersections.

<h4 id="FillOpacity">Fill paint opacity: the <span class="property">fill-opacity</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="FillOpacityProperty" data-dfn-type="property" data-export="">fill-opacity</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>&lt;‘'opacity'’&gt;</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>1</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>the specified value converted to a number, clamped to the range [0,1]</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>'fill-opacity' specifies the opacity of the painting operation used
to paint the fill the current object. (See
<a href="render.html#PaintingShapesAndText">Painting shapes and text</a>).

<dl>
  <dt><span class='prop-value'>&lt;number&gt;</span></dt>
  <dd>
    The opacity of the fill. Any values outside the
    range 0 (fully transparent) to 1 (fully opaque) must be
    clamped to this range.
  </dd>
  <dt><span class='prop-value'>&lt;percentage&gt;</span></dt>
  <dd>
    The opacity of the fill expressed as a percentage
    of the range 0 to 1.
  </dd>
</dl>

Note: See also the 'opacity' property, which
specifies group opacity.

<h3 id="StrokeProperties">Stroke properties</h3>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Support non-scaling stroke.</td>
    </tr>
    <tr>
      <th>Resolutions:</th>
      <td><a href="http://www.w3.org/2011/10/28-svg-irc#T17-46-34">SVG 2 will include non-scaling stroke.</a><br/>
          <a href="http://www.w3.org/2012/02/02-svg-minutes.html#item05">SVG 2 will have the <span class="property">vector-effect</span>
 property.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To support strokes whose width does not change when zooming a page, as common for example in maps.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Chris or Erik (no action)</td>
    </tr>
    <tr>
      <th>Note:</th>
      <td>Note that this could be part of more generic non-scaling features.</td>
    </tr>
  </table>
</div>

<p>In this section, we define a number of properties that allow the
author to control different aspects of a stroke, including its paint,
thickness, use of dashing, and joining and capping of
path segments.

<p>In all cases, all stroking properties which are affected by
directionality, such as those having to do with dash patterns, must be
rendered such that the stroke operation starts at the same point at
which the graphics element starts. In particular, for <{path}>
elements, the start of the path is the first point of the initial
"moveto" command.

<p>For stroking properties such as dash patterns whose computations
are dependent on progress along the outline of the graphics element,
distance calculations are required to utilize the SVG user agent's
standard <a href="paths.html#DistanceAlongAPath">Distance along a path</a>
algorithms.

<p>When stroking is performed using a complex paint server, such as a
gradient or a pattern, the stroke operation must be identical to the
result that would have occurred if the geometric shape defined by the
geometry of the current graphics element and its associated stroking
properties were converted to an equivalent <{path}> element and
then filled using the given paint server.

<h4 id="SpecifyingStrokePaint">Specifying stroke paint: the <span class="property">stroke</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="StrokeProperty" data-dfn-type="property" data-export="">stroke</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><a>&lt;paint&gt;</a></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>none</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified, but with <a>&lt;color&gt;</a> values computed and
    <a>&lt;url&gt;</a> values made absolute</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The 'stroke' property paints along the outline of the given
graphical element.

Note: Note that when stroking a <{path}> element,
any subpath consisting of a <a href="paths.html#PathDataMovetoCommands">moveto</a>
but no following line drawing command will not be stroked.
Any other type of zero-length subpath, such as
<span class="attr-value">'M 10,10 L 10,10'</span>
or <span class="attr-value">'M 30,30 Z'</span>
will also not be stroked if the 'stroke-linecap' property has a value of
<span class="prop-value">butt</span>.  See the definition of
the [=stroke shape=] below for the details of computing
the stroke of a path.

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Include a way to specify stroke position.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/28-svg-irc#T18-09-48">SVG 2 shall include a way to specify stroke position.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To allow a stroke to be inside or outside the path.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3162">ACTION-3162</a>)</td>
    </tr>
    <tr>
      <th>Note:</th>
      <td>See <a href="http://www.w3.org/Graphics/SVG/WG/wiki/Proposals/Stroke_position">proposal page</a>.</td>
    </tr>
  </table>
</div>

<h4 id="StrokeOpacity">Stroke paint opacity: the <span class="property">stroke-opacity</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="StrokeOpacityProperty" data-dfn-type="property" data-export="">stroke-opacity</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>&lt;‘'opacity'’&gt;</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>1</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>the specified value converted to a number, clamped to the range [0,1]</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The 'stroke-opacity' property specifies the opacity of the
painting operation used to stroke the current object.  (See
<a href="render.html#PaintingShapesAndText">Painting shapes and text</a>.)
As with 'fill-opacity'.

<dl>
  <dt><span class='prop-value'>&lt;number&gt;</span></dt>
  <dd>
    The opacity of the stroke. Any values outside the
    range 0 (fully transparent) to 1 (fully opaque) must be
    clamped to this range.
  </dd>
  <dt><span class='prop-value'>&lt;percentage&gt;</span></dt>
  <dd>
    The opacity of the stroke expressed as a percentage
    of the range 0 to 1.
  </dd>
</dl>

Note: See also the 'opacity' property, which specifies
group opacity.

<h4 id="StrokeWidth">Stroke width: the <span class="property">stroke-width</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="StrokeWidthProperty" data-dfn-type="property" data-export="">stroke-width</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>> | <<number>></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>1px</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the normalized diagonal of the current SVG viewport (see <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage, numbers converted to absolute lengths first</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>This property specifies the width of the stroke on the current object.
A zero value causes no stroke to be painted. A negative value
is [=invalid=]. A <<number>> value represents a value in [=user units=].

<h4 id="LineCaps">Drawing caps at the ends of strokes: the <span class="property">stroke-linecap</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="StrokeLinecapProperty" data-dfn-type="property" data-export="">stroke-linecap</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>butt | round | square</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>butt</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

<p>'stroke-linecap' specifies the shape to be used at the end of
[=open subpaths=] when they are stroked, <span class="ready-for-wider-review">
and the shape to be drawn for zero length
subpaths whether they are open or closed.</span>  The possible values are:

<dl>
  <dt><span class='prop-value'>butt</span></dt>
  <dd>This value indicates that the stroke for each subpath does not
  extend beyond its two endpoints.  A zero length subpath will therefore
  not have any stroke.</dd>

  <dt><span class='prop-value'>round</span></dt>
  <dd>
    <p>This value indicates that at each end of each subpath, the shape
    representing the stroke will be extended by a half circle with a diameter equal
    to the stroke width.  If a subpath, <span class="ready-for-wider-review">whether open or closed,</span> has zero length,
    then the resulting effect is that the stroke for that subpath consists solely
    of a full circle centered at the subpath's point.
  </dd>

  <dt><span class='prop-value'>square</span></dt>
  <dd>
    <p>This value indicates that at the end of each subpath, the shape
    representing the stroke will be extended by a rectangle with the
    same width as the stroke width and whose length is half of the stroke width.
    If a subpath, <span class="ready-for-wider-review">whether open or closed,</span> has zero length, then the resulting
    effect is that the stroke for that subpath consists solely of a square with
    side length equal to the stroke width, centered at the subpath's point, and
    oriented such that two of its sides are parallel to the effective tangent
    at that subpath's point.  See
    <a href="paths.html#PathElementImplementationNotes"><span class="element-name">path</span>
    element implementation notes</a> for details on how to determine the tangent
    at a zero-length subpath.
  </dd>
</dl>

<div class="figure">
  <img no-autosize class="bordered" src="images/painting/linecap.svg"
       alt="Image showing three paths, each with a different line cap.">
  <p class="caption">The three types of line caps.
</div>

<p>See the definition of the [=cap shape=] below for a more precise
description of the shape a line cap will have.

<h4 id="LineJoin">Controlling line joins: the <span class="property">stroke-linejoin</span> and <span class="property">stroke-miterlimit</span> properties</h4>

<p class="issue" data-issue="592">
    The values <span class="prop-value">miter-clip</span> and <span class="prop-value">arcs</span>
    of the 'stroke-linejoin' property are at risk. There are no known browser implementations.
    See issue <a href="https://github.com/w3c/svgwg/issues/592">GitHub issue #592</a>.

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="StrokeLinejoinProperty" data-dfn-type="property" data-export="">stroke-linejoin</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>miter | miter-clip | round | bevel | arcs </td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>miter</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>Animation Type:</th>
    <td>discrete</td>
  </tr>
</table>

<p>'stroke-linejoin' specifies the shape to be used at the
corners of paths or basic shapes when they are stroked. For further details see
the <a href="paths.html#PathElementImplementationNotes">path implementation notes</a>.

<dl>
  <dt><span class='prop-value'>miter</span></dt>
  <dd>This value indicates that a sharp corner is to be used to join path segments.
  The corner is formed by extending the outer edges of the stroke at the tangents
  of the path segments until they intersect. If the 'stroke-miterlimit'
  is exceeded, the line join falls back to <span class='prop-value'>bevel</span>
  (see below).</dd>

  <dt><span class='prop-value'>miter-clip</span></dt>
  <dd>This value is the same as <span class='prop-value'>miter</span> but if
    the 'stroke-miterlimit' is exceeded, the miter is clipped at a
    distance equal to half the 'stroke-miterlimit' value multiplied
    by the stroke width from the intersection of the path segments
    (see below).</dd>

  <dt><span class='prop-value'>round</span></dt>
  <dd>This value indicates that a round corner is to be used to join path segments.
  The corner is a circular sector centered on the join point.</dd>

  <dt><span class='prop-value'>bevel</span></dt>
  <dd>This value indicates that a bevelled corner is to be used to join path segments.
  The bevel shape is a triangle that fills the area between the two stroked segments.</dd>

  <dt><span class='prop-value'>arcs</span></dt>
  <dd>This value indicates that an arcs corner is to be used to join
    path segments. The arcs shape is formed by extending the outer
    edges of the stroke at the join point with arcs that have the same
    curvature as the outer edges at the join point.</dd>
</dl>

Note: 
  The <span class='prop-value'>miter-clip</span> and
  <span class='prop-value'>arcs</span> values are new in SVG 2.
  The <span class='prop-value'>miter-clip</span> value offers a more
  consistent presentation for a path with multiple joins as well as
  better behavior when a path is animated.
  The <span class='prop-value'>arcs</span> value provides a better
  looking join when the path segments at the join are curved.


<p class="annotation">
  Adding <span class="attr-value">arcs</span> line join was resolved at the
  <a href="http://www.w3.org/2012/09/19-svg-minutes.html#item08">Rigi
  Kaltbad group meeting</a>.


<p class="annotation">
  Adding <span class="attr-value">miter-clip</span> line join was resolved at the
  <a href="http://www.w3.org/2015/02/12-svg-minutes.html#item03">Sydney
  (2015) group meeting</a>.


<div class="figure">
  <img no-autosize class="bordered" src="images/painting/linejoin-four.svg"
       alt="Image showing four paths, each with a different line join.">
  <p class="caption">Four types of line joins.
</div>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="StrokeMiterlimitProperty" data-dfn-type="property" data-export="">stroke-miterlimit</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<number>></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>4</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>
  When two line segments meet at a sharp angle and a value of
  <span class='prop-value'>miter</span>,
  <span class='prop-value'>miter-clip</span>, or
  <span class='prop-value'>arcs</span> has been specified for
  'stroke-linejoin', it is possible for the join to extend
  far beyond the thickness of the line stroking the path. The
  'stroke-miterlimit' imposes a limit on the extent of the
  line join.


<dl>
  <dt><span class='prop-value'>&lt;number&gt;</span></dt>
  <dd>
    The limit on the extent of a
    <span class='prop-value'>miter</span>,
    <span class='prop-value'>miter-clip</span>, or
    <span class='prop-value'>arcs</span> line join as a multiple of
    the 'stroke-width' value.
    A negative value for 'stroke-miterlimit' is [=invalid=] and must be [=ignored=].
  </dd>
</dl>

Note: 
  Previous versions of the SVG specification
  also stated that values between 0 and 1 were in error,
  but this was not well implemented by user agent's CSS parsers.
  In practice, any miter join will exceed a miter limit between 0 and 1.


<p>
  For the <span class='prop-value'>miter</span> or the
  <span class='prop-value'>miter-clip</span> values, given
  the angle <var>θ</var> between the segments in user coordinate system,
  the miter length is calculated by:


<div role="math" aria-describedby="math-miter-length">
  <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
    <mrow>
      <mi>miter length</mi>
      <mo>=</mo>
      <mfrac>
        <mi style="font-family: sans-serif">‘stroke-width’</mi>
        <mrow>
          <mi>sin</mi>
          <mo>&#x2061;</mo>
          <mfrac>
            <mi>θ</mi>
            <mn>2</mn>
          </mfrac>
        </mrow>
      </mfrac>
    </mrow>
  </math>
  <pre id="math-miter-length">miter length = stroke-width / sin(theta / 2)</pre>
</div>

<div class="note">
  <p>
    Historically, the miter length is defined as the distance from the
    inside stroke edge of the intersecting path segments to the tip of
    the miter. In practice, this is followed only for straight path
    segments. The above definition of miter length based on angles
    depends only on the tangents to the path segments at the join and
    thus gives consistent results independent of the curvature of the
    path segments. To be consistent with this definition, the clipping
    point of the
    <span class='prop-value'>miter-clip</span> and
    <span class='prop-value'>arcs</span> line joins is at a distance
    or arc length equal to half the 'stroke-miterlimit' times
    the stroke width from the point the two path segments join.
  
  <div class="figure">
    <img no-autosize class="bordered" src="images/painting/miter-limit-def.svg"
	 alt="Image showing the definition of the stroke miter length
	      and consistency of clipping between different shaped
	      path segments.">
    <p class="caption">
      Left: Historical definition of miter length.

      Right: Two different paths with the same tangents to the path at
      the point where the path segments join. The behavior of the
      miter join (fallback to bevel or clipping position) is the same
      for both paths. It does not depend on the position where the
      inside stroked edges intersect.
    
  </div>
</div>

<p>
  If the miter length divided by the stroke width exceeds the
  'stroke-miterlimit' then for the value:

<dl>
  <dt><span class='prop-value'>miter</span></dt>
  <dd>
    the join is converted to a bevel;
  </dd>
  <dt><span class='prop-value'>miter-clip</span></dt>
  <dd>
    the miter is clipped by a line perpendicular to the line bisecting
    the angle between the two path segments at a distance of half the value
    of miter length from the intersection of the two path segments.
  </dd>
</dl>

<div class="figure">
  <img no-autosize class="bordered" src="images/painting/miter-limit.svg"
       alt="Image showing resulting stroke when stroke miter limit is exceeded.">
  <p class="caption">
    Effect on line join when 'stroke-miterlimit' is
    exceeded. The olive-green dashed lines shows the position of the
    miter limit when the 'stroke-miterlimit' value is 3. The
    gray regions shows what the joins would look like without a miter
    limit.
  
</div>

<p>
  For the <span class='prop-value'>arcs</span> value, the
  <em>miter length</em> is calculated along a circular arc that is
  tangent to the line bisecting the angle between the two segments at
  the point the two segments intersect and passes through the end
  point of the join. The line join is clipped, if necessary, by a line
  perpendicular to this arc at an arc length from the intersection
  point equal to half the value of the 'stroke-miterlimit' value
  multiplied by the stroke width.


<p class="annotation">
  The effect of 'stroke-miterlimit' on an <span class="attr-value">arcs</span> line join was resolved
  at <a href="http://www.w3.org/2015/02/12-svg-minutes.html#item12">Sydney
  (2015) group meeting</a>.


<p>
  See the definition of the [=line join shape=] below for a more
  precise description of the shape a line join will have.


<h4 id="StrokeDashing">Dashing strokes: the <span class="property">stroke-dasharray</span> and <span class="property">stroke-dashoffset</span> properties</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="StrokeDasharrayProperty" data-dfn-type="property" data-export="">stroke-dasharray</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>none | <a>&lt;dasharray&gt;</a></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>none</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the normalized diagonal of the current SVG viewport (see <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as comma separated list of absolute lengths or percentages, numbers converted to absolute lengths first, or keyword specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>See prose</td>
  </tr>
</table>

<p>where:

<p class="definition prod"><dfn id="DataTypeDasharray" data-dfn-type="type" data-export="">&lt;dasharray&gt;</dfn> =
[ [ <<length-percentage>> | <<number>> ]+ ]#

<p>The 'stroke-dasharray' property controls
the pattern of dashes and gaps used to form the shape of
a path's stroke.

<dl>
  <dt><span class='prop-value'>none</span></dt>
  <dd>Indicates that no dashing is used.</dd>

  <dt><span class='prop-value'>&lt;dasharray&gt;</span></dt>
  <dd>
    <p>Specifies a dashing pattern to use.  A <a>&lt;dasharray&gt;</a> is
    a list of comma and/or white space separated <<number>> or
    <<length-percentage>> values.
    A <<number>> value represents a value in [=user units=].
    Each value specifies a length along the path for which the stroke
    is to be painted (a <em>dash</em>) and not painted (a <em>gap</em>).
    The first value and every second value in the list after it specifies
    the length of a dash, and every other value specifies the length of a gap
    between the dashes.  If the list has an odd number of values, then it is
    repeated to yield an even number of values.  (Thus, the rendering behavior
    of <span class="prop-value">stroke-dasharray: 5,3,2</span>
    is equivalent to <span class="prop-value">stroke-dasharray: 5,3,2,5,3,2</span>.)

    <p>The resulting even-length dashing pattern is repeated along each subpath.
    The dashing pattern is reset and begins again at the start of each subpath.

    <p>If any value in the list is negative, the <a>&lt;dasharray&gt;</a> value is
    [=invalid=].  If all of the values in the list are zero,
    then the stroke is rendered as a solid line without any dashing.
  </dd>
</dl>

<div class="figure">
  <img no-autosize class="bordered" src="images/painting/dashes.svg" alt="Image showing a thick, dashed stroke.">
  <p class="caption">A dashed stroke.  The dashing pattern is <span class="prop-value">20,10</span>.
  The red line shows the actual path that is stroked.
</div>

<p>The <{path/pathLength}> attribute on a <{path}> element affects
'stroke-dasharray': each dash and gap length is interpreted relative
to the author's path length as specified by <{path/pathLength}>.

<p id="interpolationDashPattern">'stroke-dasharray' values are [=not additive=]. For interpolation,
'stroke-dasharray' values are combined as follows:
<dl class="switch">
  <dt>If either <var>start</var> or <var>end</var> compute to <span class="prop-value">none</span> or are invalid</dt>
  <dd><var>start</var> or <var>end</var> are combined using the discrete animation type.</dd>
  <dt>Otherwise</dt>
  <dd>repeat both dash patterns of <var>start</var> and <var>end</var> value list until the length of elements in
    both value lists match. Each item is then combined by computed value.</dd>
</dl>

<div class="example">
The two 'stroke-dasharray' value lists in the following example have different number
of elements:

<pre><code>path {
  stroke-dasharray: 20 40 10;
}

path:hover {
  transition-property: stroke-dasharray;
  transition-duration: 0.5s;
  stroke-dasharray: 40 20;
}
</code></pre>

To interpolate the two value lists the dash pattern gets repeated on both lists first:

<pre><code>stroke-dasharray: 20 40 10 20 40 10;
stroke-dasharray: 40 20 40 20 40 20;
</code></pre>

After that, each item is then combined by computed value.
</div>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="StrokeDashoffsetProperty" data-dfn-type="property" data-export="">stroke-dashoffset</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>> | <<number>></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>0</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the normalized diagonal of the current SVG viewport (see <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage, numbers converted to absolute lengths first</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The 'stroke-dashoffset' property specifies the distance into the repeated
dash pattern to start the stroke dashing at the beginning of the path.  If the
value is negative, then the effect is the same as dash offset <var>d</var>:

<div role="math" aria-describedby="math-dashoffset">
  <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
    <mrow>
      <mi>d</mi>
      <mo>=</mo>
      <mi>s</mi>
      <mo>-</mo>
      <mfenced open="|" close="|">
        <mi style="font-family: sans-serif">‘stroke-dashoffset’</mi>
      </mfenced>
      <mo>mod</mo>
      <mi>s</mi>
    </mrow>
  </math>
  <pre id="math-dashoffset">d = s - (abs(stroke-dashoffset) mod s)</pre>
</div>

<p>where <var ignore=''>s</var> is the sum of the dash array values.

<div class="figure">
  <img no-autosize class="bordered" src="images/painting/dashoffset.svg"
       alt="Image showing a thick, dashed stroke with a non-zero dash offset.">
  <p class="caption">A dashed stroke with a non-zero dash offset.  The dashing
  pattern is <span class="prop-value">20,10</span> and the dash offset is
  <span class="prop-value">15</span>.  The red line shows the actual path that
  is stroked.
</div>

<p>Like 'stroke-dasharray', 'stroke-dashoffset' is interpreted
relative to the author's path length as specified by the <{path/pathLength}>
attribute on a <{path}> element.

<div class="example">
  <p>The example below shows how a <{path/pathLength}> that is greatly
  different from the actual path length can be used to control stroke
  dashing more easily.

<pre class=include-raw>
path: images/painting/dash-pathlength.svg
</pre>

  <div class="figure">
    <img no-autosize src="images/painting/dash-pathlength.svg"
         alt="Image of three casino chips, each of which has a patterned border
              produced using stroke dashing.">
    <p class="caption">The four broad white dashes and the eight small circular
    dashes around each chip are placed relative to an author specified
    <{path/pathLength}> of <code class='attr-value'>80</code>, which
    makes the desired 'stroke-dasharray' and 'stroke-dashoffset'
    values easy to compute.
  </div>
</div>

<p>See the definition of [=dash positions=] below for a more precise
description of positions along a path that dashes will be placed.
</div>

<div class="ready-for-wider-review">
<h4 id="StrokeShape">Computing the shape of the stroke</h4>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Specify stroke dashing more precisely.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/28-svg-irc#T18-14-14">SVG 2 shall specify stroke dashing more precisely.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To define dash starting point on basic shapes and path segments.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (no action)</td>
    </tr>
  </table>
</div>

<div class="ready-for-wider-review">
<p>The <dfn id="TermStrokeShape" data-dfn-type="dfn" data-export="">stroke shape</dfn> of an element is the
shape that is filled by the 'stroke' property.  Since <{text}>
elements can be rendered in multiple chunks, each chunk has its own
[=stroke shape=].  The following algorithm describes the ideal stroke shape
of a <{path}>, [=basic shape=] or individual <{text}> chunk is,
taking into account the stroking properties above. The ideal stroke shape
described defines a best case implementation, but implementations are given some
leeway to deviate from this description for performance reasons.

<div class="note">
Authors should be aware that the shape of a stroke may in some cases, such as
at extremely tight curves, differ across platforms.
<div class="figure">
  <img class="bordered" src="images/painting/stroke-tight-corner-render-examples.png"
       alt="Image showing how stroke shape differs across platforms. One
            example is as described by the algorithm in this specification, the
            other is different and overall looks less correct. It is distinct in
            that the geometry created to describe the left and right sides of
            the stroke are distorted due to the proximity of the end of the
            curve to the section of high curvature.">
  <p class="caption">An example of how the shape painted for stroke may differ
  across platforms.
</div>
The above example shows the possible rendered results for the following
two SVG paths:
<pre class=include-raw>
path: images/painting/stroke-tight-corner.svg
</pre>
</div>
</div> <!-- end of class="ready-for-wider-review" -->

The ideal stroke shape is determined as follows:

<ol class="algorithm">
  <li>Let <var>shape</var> be an empty shape.</li>
  <li class="ready-for-wider-review">If 'stroke-width' > 0, then:
    <ol>
      <li>Let <var>scale</var> be a scale factor for the dash pattern.  If we are
      computing the stroke shape of a <{text}> chunk,
      or if the <{path/pathLength}> attribute is not present on the element,
      then <var>scale</var> is 1.  Otherwise, it is determined as follows:
        <ol>
          <li>Let <var>length</var> be the user agent's computed length of the
          <{path}> or [=equivalent path=] for a [=basic shape=].</li>
          <li>Let <var>authorlength</var> be the value of the <{path/pathLength}>
          attribute on the [=shape=].</li>
          <li><var>scale</var> is <var>authorlength</var> / <var>length</var>.</li>
        </ol>
      </li>
      <li>Let <var>path</var> be the [=equivalent path=] of the element (or the individual
      chunk of a <{text}> element).</li>
      <li>For each subpath of <var>path</var>:
        <ol>
          <li>Let <var>positions</var> be the [=dash positions=] for the subpath.</li>
          <li>For each pair &lt;<var>start</var>, <var>end</var>&gt; in <var>positions</var>:
            <ol>
              <li>Scale <var>start</var> and <var>end</var> by <var>scale</var>.</li>

              <li>Let <var>dash</var> be the shape that includes, for all distances
              between <var>start</var> and <var>end</var> along the subpath, all
              points that lie on the line perpendicular to the subpath at that
              distance and which are within distance 'stroke-width' of
              the point on the subpath at that position.</li>

              <li>Set <var>dash</var> to be the union of <var>dash</var> and the
              starting [=cap shape=] for the subpath at position <var>start</var>.</li>

              <li>Set <var>dash</var> to be the union of <var>dash</var> and the
              ending [=cap shape=] for the subpath at position <var>end</var>.</li>

              <li>
                Let <var>index</var> and <var>last</var> be the indexes of the
                path segments in the subpath at distance <var>start</var> and
                <var>end</var> along the subpath.

                Note: It does not matter whether any zero length segments are
                included when choosing <var>index</var> and <var>last</var>.
              </li>

              <li>While <var>index</var> &lt; <var>last</var>:
                <ol>
                  <li>Set <var>dash</var> to be the union of <var>dash</var> and the
                  [=line join shape=] for the subpath at segment index <var>index</var>.</li>

                  <li>Set <var>index</var> to <var>index</var> + 1.</li>
                </ol>
              </li>

              <li>Set <var>shape</var> to be the union of <var>shape</var> and
              <var>stroke</var>.</li>
            </ol>
          </li>
        </ol>
      </li>
    </ol>
  </li>
  <li>Return <var>shape</var>.</li>
</ol>

<p>The <dfn id="TermDashPositions" data-dfn-type="dfn" data-export="">dash positions</dfn> for a given subpath of
the [=equivalent path=] of a <{path}> or [=basic shape=] is a
sequence of pairs of values, which represent the starting and ending distance
along the subpath for each of the dashes that form the subpath's stroke.  It is
determined as follows:

<ol class="algorithm">
  <li>Let <var>pathlength</var> be the length of the subpath.</li>

  <li>Let <var>dashes</var> be the list of values of 'stroke-dasharray'
  on the element, converted to user units, repeated if necessary so that it has
  an even number of elements; if the property has the value
  <span class="prop-value">none</span>, then the list has a single value 0.</li>

  <li>Let <var>count</var> be the number of values in <var>dashes</var>.</li>
  <li>Let <var>sum</var> be the sum of the values in <var>dashes</var>.</li>

  <li>If <var>sum</var> = 0, then return a sequence with the single pair
  &lt;0, <var>pathlength</var>&gt;.</li>

  <li>Let <var>positions</var> be an empty sequence.</li>

  <li>Let <var>offset</var> be the value of the 'stroke-dashoffset'
  property on the element.</li>

  <li>If <var>offset</var> is negative, then set <var>offset</var> to
  <var>sum</var> − abs(<var>offset</var>).</li>

  <li>Set <var>offset</var> to <var>offset</var> mod <var>sum</var>.</li>

  <li>Let <var>index</var> be the smallest integer such that
  sum(<var>dashes<sub>i</sub></var>, 0 ≤ <var>i</var> ≤ <var>index</var>) ≥ <var>offset</var>.</li>

  <li>Let <var>dashlength</var> be
  min(sum(<var>dashes<sub>i</sub></var>, 0 ≤ <var>i</var> ≤ <var>index</var>) − <var>offset</var>, <var>pathlength</var>).</li>

  <li>If <var>index</var> mod 2 = 0, then append to <var>positions</var> the
  pair &lt;0, <var>dashlength</var>&gt;.</li>

  <li>Let <var>position</var> be <var>dashlength</var>.</li>

  <li>While <var>position</var> &lt; <var>pathlength</var>:
    <ol>
      <li>Set <var>index</var> to (<var>index</var> + 1) mod <var>count</var>.</li>

      <li>Let <var>dashlength</var> be
      min(<var>dashes</var><sub><var>index</var></sub>, <var>pathlength</var> − <var>position</var>).</li>

      <li>If <var>index</var> mod 2 = 0, then append to <var>positions</var> the
      pair &lt;<var>position</var>, <var>position</var> + <var>dashlength</var>&gt;.</li>

      <li>Set <var>position</var> to <var>position</var> + <var>dashlength</var>.</li>
    </ol>
  </li>

  <li>Return <var>positions</var>.</li>
</ol>

<p>The starting and ending <dfn id="TermCapShape" data-dfn-type="dfn" data-export="">cap shapes</dfn> at a given
<var>position</var> along a subpath are determined as follows:

<ol class="algorithm">
  <li>If 'stroke-linecap' is <span class="prop-value">butt</span>, then return an empty shape.</li>

  <li>Otherwise, if 'stroke-linecap' is <span class="prop-value">round</span>, then:
    <ol>
      <li>If this is a starting cap, then return a semicircle of diameter 'stroke-width' positioned such that:
        <ul>
          <li class='ready-for-wider-review'>The subpath that the semicircle is relative to is the subpath starting
          at distance <var>position</var>.</li>
          <li>Its straight edge is parallel to the line perpendicular to the subpath at distance <var>position</var> along it.</li>
          <li>The midpoint of its straight edge is at the point that is along the subpath at distance <var>position</var>.</li>
          <li>The direction from the midpoint of its arc to the midpoint of its straight edge is the same as the direction of
          the subpath at distance <var>position</var>.</li>
        </ul>
      </li>
      <li>Otherwise, this is an ending cap.  Return a semicircle of diameter 'stroke-width' positioned such that:
        <ul>
          <li class='ready-for-wider-review'>The subpath that the semicircle is relative to is the subpath ending
          at distance <var>position</var>.</li>
          <li>Its straight edge is parallel to the line perpendicular to the subpath at distance <var>position</var> along it.</li>
          <li>The midpoint of its straight edge is at the point that is along the subpath at distance <var>position</var>.</li>
          <li>The direction from the midpoint of its straight edge to the midpoint of its arc is the same as the
          direction of the subpath.</li>
        </ul>
      </li>
    </ol>
  </li>

  <li>Otherwise, 'stroke-linecap' is <span class="prop-value">square</span>:
    <ol>
      <li>If this is a starting cap, then return a rectangle with side lengths 'stroke-width' and 'stroke-width' / 2 positioned such that:
        <ul>
          <li>Its longer edges, <var>A</var> and <var>B</var>, are parallel to the line perpendicular to the subpath at distance <var>position</var> along it.</li>
          <li>The midpoint of <var>A</var> is at <var>start</var>.</li>
          <li>The direction from the midpoint of <var>B</var> to the midpoint of <var>A</var> is the same as the direction of the subpath at distance <var>position</var> along it.</li>
        </ul>
      </li>
      <li>Otherwise, this is an ending cap.  Return a rectangle with side lengths 'stroke-width' and 'stroke-width' / 2 positioned such that:
        <ul>
          <li>Its longer edges, <var>A</var> and <var>B</var>, are parallel to the line perpendicular to the subpath at distance <var>position</var> along it.</li>
          <li>The midpoint of <var>A</var> is at <var>end</var>.</li>
          <li>The direction from the midpoint of <var>A</var> to the midpoint of <var>B</var> is the same as the direction of the subpath at distance <var>position</var> along it.</li>
        </ul>
      </li>
    </ol>
  </li>
</ol>

<div class="figure">
  <img no-autosize class="bordered" src="images/painting/linecap-construction.svg"
       alt="Image showing how to construct the three types of line caps">
  <p class="caption">The three different 'stroke-linecap' values used on
  paths with a single, non-zero length subpath.  The white line is the path
  itself and the thick gray area is the stroke.  On the top row, the green lines
  indicate the perpendicular to the tangent at the path endpoints and the pink
  areas are the caps.  The bottom row shows the stroke without the perpendicular
  and cap highlighting.
</div>

<p>The <dfn id="TermLineJoinShape"  data-dfn-type="dfn" data-export="">line join shape</dfn> for a given segment of
a subpath is determined as follows:

<ol class="algorithm">
  <li>Let <var>P</var> be the point at the end of the segment.</li>

  <li>If the unit tangent vector at the end of the segment and the unit tangent vector
  at the start of the following segment are equal, then return an empty shape.
  Note: This means for example that <code class='attr-value'>M 100,100 h 100 h 100</code>
  would not produce a line join shape between the two straight line segment, but
  <code class='attr-value'>M 100,100 h 100 h -100</code> would.</li>

  <li>Let <var>A</var> be the line parallel to the tangent at the end of the segment.</li>
  <li>Let <var>B</var> be the line parallel to the tangent at the start of the following segment.</li>

  <li>Let <var>A<sub>left</sub></var> and <var>A<sub>right</sub></var> be lines
  parallel to <var>A</var> at a distance of 'stroke-width' / 2 to the
  left and to the right of <var>A</var> relative to the subpath direction, respectively.</li>

  <li>Let <var>B<sub>left</sub></var> and <var>B<sub>right</sub></var> be lines
  parallel to <var>B</var> at a distance of 'stroke-width' / 2 to the
  left and to the right of <var>B</var>, relative to the subpath direction, respectively.</li>

  <li>
    Let <var>P</var><sub>1</sub>, <var>P</var><sub>2</sub> and
    <var>P</var><sub>3</sub> be points determined as follows:

    <ol>
      <li>If the smaller angle between <var>A</var> and <var>B</var> is on the
      right of these lines, considering the direction of the subpath, then
      <var>P</var><sub>1</sub> and <var>P</var><sub>2</sub> are the points on
      <var>A<sub>left</sub></var> and <var>B<sub>left</sub></var> closest to
      <var>P</var>, and <var>P</var><sub>3</sub> is the intersection of
      <var>A<sub>left</sub></var> and <var>B<sub>left</sub></var>.</li>

      <li>Otherwise, <var>P</var><sub>1</sub> and <var>P</var><sub>2</sub> are
      the points on <var>A<sub>right</sub></var> and <var>B<sub>right</sub></var>
      closest to <var>P</var>, and <var>P</var><sub>3</sub> is the intersection
      of <var>A<sub>right</sub></var> and <var>B<sub>right</sub></var>.</li>
    </ol>
  </li>

  <li>Let <var>bevel</var> be the triangle formed from the three points
  <var>P</var>, <var>P</var><sub>1</sub> and <var>P</var><sub>2</sub>.</li>

  <li>If 'stroke-linejoin' is <span class="prop-value">round</span>, then
  return the union of <var>bevel</var> and a circular sector of diameter
  'stroke-width', centered on <var>P</var>, and which has
  <var>P</var><sub>1</sub> and <var>P</var><sub>2</sub> as the two endpoints of
  the arc.</li>

  <li>If 'stroke-linejoin' is <span class="prop-value">arcs</span>,
    then find the circles that are tangent to the stroke edges at
    <var>P</var><sub>1</sub> and <var>P</var><sub>2</sub> with the
    same curvature as the edges at those points (see below). If both
    curvatures are zero fall through to <span class="prop-value">miter-clip</span>.
    If either curvature is greater than 2/(stroke width), fallback to
    <span class="prop-value">round</span>.

    Extend the stroke edges using these circles (or a line, in the case
    of zero curvature).

    If the two circles (or circle and line) do not intersect, adjust
    the radii of the two circles by an equal amount (or just the circle
    in case of a circle and line) until they do intersect (see below).

    The line join
    region is defined by the lines that connect <var>P</var>
    with <var>P</var><sub>1</sub> and <var>P</var><sub>2</sub> and the
    arcs defined by the circles (or arc and line) between the closest
    intersection point to <var>P</var>, and <var>P</var><sub>1</sub>
    and <var>P</var><sub>2</sub>.

    Next calculate the <em>miter limit</em> as defined in
    the 'stroke-miterlimit' section. Clip any part of the line
    join region that extends past the miter limit. Return the
    resulting region.

    Note that the curvatures are calculated in user-space before any
    transforms are applied.</li>

  <li>
    If 'stroke-linejoin' is <span class="prop-value">miter</span> or
    <span class="prop-value">miter-clip</span> then the line join
    region is the union of <var>bevel</var> and the triangle formed
    from the three points <var>P</var><sub>1</sub>,
    <var>P</var><sub>2</sub> and <var>P</var><sub>3</sub>.
  </li>

  <li>
    Let <var>θ</var> be the angle between <var>A</var> and <var>B</var>.
    If 1 / sin(<var>θ</var> / 2) ≤ 'stroke-miterlimit', then return
    the line join region.
  </li>

  <li>
    If 'stroke-linejoin' is <span class="prop-value">miter-clip</span>,
    then clip any part of the line join region that extends past the
    miter limit and return this region.
  </li>

  <li>Return <var>bevel</var>.</li>
</ol>

<div class="figure">
  <img no-autosize class="bordered" src="images/painting/linejoin-construction.svg"
       alt="Image showing the lines and points computed to construct a round line join.">
  <p class="caption">Construction of a round line join shape, shown in pink.
  The white line is the original path, which has two segments that come to a
  point, and the gray region is the stroke.
</div>

<div class="figure">
  <img no-autosize class="bordered" src="images/painting/linejoin-construction-arcs.svg"
       alt="Image showing the lines and points computed to construct an arcs line join.">
  <p class="caption">Construction of an arcs line join shape, shown in
    pink. The white line is the original path, which has two segments
    that come to a point, and the dark gray region is the stroke. The
    dashed lines show circles that are tangent to and have the
    curvature of the segments at the join.  The olive-green circles
    (concentric with the dashed circles) define the join shape.
</div>

<h4 id="CurvatureCalculation">Computing the circles for the <span class="prop-value">arcs</span> 'stroke-linejoin'</h4>

<p>The <span class="prop-value">arcs</span> 'stroke-linejoin'
  requires finding circles that are both tangent to and have the same
  curvatures as the outer stroke edges at the ends of path
  segments. To find one of these circles, first calculate the
  curvature <var>&#x03BA;</var> of the path segment at its end (see
  below). Next, find the radius of a circle corresponding to this
  curvature: <var>r</var> = 1/<var>&#x03BA;</var>. Increase or
  decrease the radius by one half of the stroke width to account for
  the stroke: <var>r<sub>c</sub></var> = <var>r</var> &#x00b1; &#xbd;
  stroke-width. The center of the circle will be on a line normal to
  the path end a distance of <var>r<sub>c</sub></var> away from the
  outer stroke edge at the end.

<p>For a line: the curvature is zero. Extend the outer stroke edge by a line.

<p>For an elliptical arc:

  <div role="math" aria-describedby="math-curvature-of-ellipse">
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
      <mi>&#x03BA;<!-- κ --></mi>
      <mo stretchy="false">(</mo>
      <mi>t</mi>
      <mo stretchy="false">)</mo>
      <mo>=</mo>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mrow class="MJX-TeXAtom-ORD">
            <msub>
              <mi>r</mi>
              <mi>x</mi>
            </msub>
            <msub>
              <mi>r</mi>
              <mi>y</mi>
            </msub>
	  </mrow>
	  <mrow class="MJX-TeXAtom-ORD">
            <mo stretchy="false">(</mo>
            <msubsup>
              <mi>r</mi>
              <mi>x</mi>
              <mn>2</mn>
            </msubsup>
            <msup>
              <mi>sin</mi>
              <mn>2</mn>
            </msup>
            <mo>&#x2061;<!-- ⁡ --></mo>
            <mi>t</mi>
            <mo>+</mo>
            <msubsup>
              <mi>r</mi>
              <mi>y</mi>
              <mn>2</mn>
            </msubsup>
            <msup>
              <mi>cos</mi>
              <mn>2</mn>
            </msup>
            <mo>&#x2061;<!-- ⁡ --></mo>
            <mi>t</mi>
            <msup>
              <mo stretchy="false">)</mo>
              <mrow class="MJX-TeXAtom-ORD">
		<mn>3</mn>
		<mrow class="MJX-TeXAtom-ORD">
		  <mo>/</mo>
		</mrow>
		<mn>2</mn>
              </mrow>
            </msup>
	  </mrow>
	</mfrac>
      </mrow>
    </math>
    <pre id="math-curvature-of-ellipse">$$\kappa(t) = {{r_x r_y}\over{(r_x^2 \sin^2 t + r_y^2 \cos^2 t)^{3/2}}}$$</pre>
  </div>

  <p>where:

  <div role="math" aria-describedby="math-curvature-t">
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
      <mi>t</mi>
      <mo>=</mo>
      <mi>arctan</mi>
      <mo>&#x2061;<!-- ⁡ --></mo>
      <mrow>
        <mo>(</mo>
        <mrow>
          <mrow class="MJX-TeXAtom-ORD">
	    <mfrac>
	      <msub>
                <mi>r</mi>
                <mi>y</mi>
	      </msub>
	      <msub>
                <mi>r</mi>
                <mi>x</mi>
	      </msub>
	    </mfrac>
          </mrow>
          <mi>tan</mi>
          <mo>&#x2061;<!-- ⁡ --></mo>
          <mi>&#x03B8;<!-- θ --></mi>
        </mrow>
        <mo>)</mo>
      </mrow>
    </math>
    <pre id="math-curvature-t">$$t = \arctan \left( {r_y \over r_x} \tan \theta \right)$$</pre>
  </div>

  <p>The parameter <var>&#x03B8;</var> at the beginning or end of an
    arc segment can be found by using the formulas in
    the <a href="implnote.html#ArcImplementationNotes">Elliptical arc
    implementation notes</a>. (Note, some renderers convert elliptical
    arcs to cubic Béziers prior to rendering so the equations here may
    not be needed.)

<p>For a quadratic Bézier:

  <div role="math" aria-describedby="math-quadratic-start">
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
      <mi>&#x03BA;<!-- κ --></mi>
      <mo stretchy="false">(</mo>
      <mn>0</mn>
      <mo stretchy="false">)</mo>
      <mo>=</mo>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mn>1</mn>
	  <mn>2</mn>
	</mfrac>
      </mrow>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mrow>
            <mo stretchy="false">(</mo>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>0</mn>
            </msub>
            <mo stretchy="false">)</mo>
            <mo>&#x00D7;<!-- × --></mo>
            <mo stretchy="false">(</mo>
            <msub>
              <mi>P</mi>
              <mn>2</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo stretchy="false">)</mo>
	  </mrow>
	  <mrow>
            <mrow class="MJX-TeXAtom-ORD">
              <mo stretchy="false">|</mo>
            </mrow>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>0</mn>
            </msub>
            <msup>
              <mrow class="MJX-TeXAtom-ORD">
		<mo stretchy="false">|</mo>
              </mrow>
              <mn>3</mn>
            </msup>
	  </mrow>
	</mfrac>
      </mrow>
    </math>
    <pre id="math-quadratic-start">$$\kappa(0) = {2\over3}{(P_1-P_0)\times((P_0-P_1)+(P_2-P_1))\over|P_1-P_0|^3}$$</pre>
  </div>

  <div role="math" aria-describedby="math-quadratic-end">
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
      <mi>&#x03BA;<!-- κ --></mi>
      <mo stretchy="false">(</mo>
      <mn>1</mn>
      <mo stretchy="false">)</mo>
      <mo>=</mo>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mn>1</mn>
	  <mn>2</mn>
	</mfrac>
      </mrow>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mrow>
            <mo stretchy="false">(</mo>
            <msub>
              <mi>P</mi>
              <mn>2</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo stretchy="false">)</mo>
            <mo>&#x00D7;<!-- × --></mo>
            <mo stretchy="false">(</mo>
            <msub>
              <mi>P</mi>
              <mn>0</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo stretchy="false">)</mo>
	  </mrow>
	  <mrow>
            <mrow class="MJX-TeXAtom-ORD">
              <mo stretchy="false">|</mo>
            </mrow>
            <msub>
              <mi>P</mi>
              <mn>2</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <msup>
              <mrow class="MJX-TeXAtom-ORD">
		<mo stretchy="false">|</mo>
              </mrow>
              <mn>3</mn>
            </msup>
	  </mrow>
	</mfrac>
      </mrow>
    </math>
    <pre id="math-quadratic-end">$$\kappa(0) = {2\over3}{(P_1-P_0)\times((P_0-P_1)+(P_2-P_1))\over|P_1-P_0|^3}$$</pre>
  </div>

  <p>Where <var>&#x03BA;(0)</var> and <var>&#x03BA;(1)</var> are the
  signed curvatures at the start and end of the path segment
  respectively, and the <var>P</var>'s are the three points that
  define the quadratic Bézier.

<p>For a cubic Bézier:

  <div role="math" aria-describedby="math-cubic-start">
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
      <mi>&#x03BA;<!-- κ --></mi>
      <mo stretchy="false">(</mo>
      <mn>0</mn>
      <mo stretchy="false">)</mo>
      <mo>=</mo>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mn>2</mn>
	  <mn>3</mn>
	</mfrac>
      </mrow>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mrow>
            <mo stretchy="false">(</mo>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>0</mn>
            </msub>
            <mo stretchy="false">)</mo>
            <mo>&#x00D7;<!-- × --></mo>
            <mo stretchy="false">(</mo>
            <msub>
              <mi>P</mi>
              <mn>2</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo stretchy="false">)</mo>
	  </mrow>
	  <mrow>
            <mrow class="MJX-TeXAtom-ORD">
              <mo stretchy="false">|</mo>
            </mrow>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>0</mn>
            </msub>
            <msup>
              <mrow class="MJX-TeXAtom-ORD">
		<mo stretchy="false">|</mo>
              </mrow>
              <mn>3</mn>
            </msup>
	  </mrow>
	</mfrac>
      </mrow>
    </math>
    <pre id="math-cubic-start">$$\kappa(0) = {2\over3}{(P_1-P_0)\times((P_0-P_1)+(P_2-P_1))\over|P_1-P_0|^3}$$</pre>
  </div>

  <div role="math" aria-describedby="math-cubic-end">
    <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
      <mi>&#x03BA;<!-- κ --></mi>
      <mo stretchy="false">(</mo>
      <mn>1</mn>
      <mo stretchy="false">)</mo>
      <mo>=</mo>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mn>2</mn>
	  <mn>3</mn>
	</mfrac>
      </mrow>
      <mrow class="MJX-TeXAtom-ORD">
	<mfrac>
	  <mrow>
            <mo stretchy="false">(</mo>
            <msub>
              <mi>P</mi>
              <mn>3</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>2</mn>
            </msub>
            <mo stretchy="false">)</mo>
            <mo>&#x00D7;<!-- × --></mo>
            <mo stretchy="false">(</mo>
            <msub>
              <mi>P</mi>
              <mn>1</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>2</mn>
            </msub>
            <mo stretchy="false">)</mo>
	  </mrow>
	  <mrow>
            <mrow class="MJX-TeXAtom-ORD">
              <mo stretchy="false">|</mo>
            </mrow>
            <msub>
              <mi>P</mi>
              <mn>3</mn>
            </msub>
            <mo>&#x2212;<!-- − --></mo>
            <msub>
              <mi>P</mi>
              <mn>2</mn>
            </msub>
            <msup>
              <mrow class="MJX-TeXAtom-ORD">
		<mo stretchy="false">|</mo>
              </mrow>
              <mn>3</mn>
            </msup>
	  </mrow>
	</mfrac>
      </mrow>
    </math>
    <pre id="math-cubic-end">$$\kappa(1) = {2\over3}{(P_3-P_2)\times((P_1-P_2)+(P_3-P_2))\over|P_3-P_2|^3}$$</pre>
  </div>

  <p>Where <var>&#x03BA;(0)</var> and <var>&#x03BA;(1)</var> are the
  signed curvatures at the start and end of the path segment
  respectively, and the <var>P</var>'s are the four points that define
  the cubic Bézier. Note, if
  <var ignore="">P<sub>0</sub></var> and <var ignore="">P<sub>1</sub></var>, or
  <var ignore="">P<sub>2</sub></var> and <var ignore="">P<sub>3</sub></var> are degenerate, the
  curvature will be infinite and a line should be used in constructing the join.

<h4 id="ArcsLinejoinFallback">Adjusting the circles for the <span class="prop-value">arcs</span> 'stroke-linejoin' when the initial circles do not intersect</h4>

  <p class="annotation">
    The fallback behavior was resolved at
    the <a href="https://www.w3.org/2016/02/03-svg-minutes.html#item02">Sydney
    2016 F2F</a>. It gives a smooth transition between the fallback
    and non-fallback states.
  

  <p>
    When the initial circles calculated for the
    <span class="prop-value">arcs</span> 'stroke-linejoin' do
    not intersect, they need to be adjusted by changing both radii by
    the same magnitude (moving the circle centers to keep the circles
    tangent to the offset paths) until the circles just touch. There
    are two cases to consider. The first is when one circle encloses
    the other circle. In this case the larger circle is reduced in
    size while the smaller circle is increased in size:
  

  <div class="figure">
    <img no-autosize class="bordered" src="images/painting/linejoin-construction-fallback.svg"
	 alt="Image showing the lines and points computed to construct an arcs line join
	      when the original offset circles do not intersect.">
    <p class="caption">Construction of an arcs line join shape, shown
      in pink. The white line is the original path and the dark gray
      region is the stroke. The dashed lines show circles that are
      tangent to and have the curvature of the segments at the
      join. Note the circles do not intersect. Two new circles are
      constructed by adjusting the radii of the original circles by
      the same magnitude with the larger circle being made smaller and
      the smaller circle being made larger until the new circles just
      touch as shown by the olive-green circles. These new circles
      then define the join shape.
    
  </div>

  <p>
    The second case is when there is no overlap between the circles.
    In this case the radii of both circles are increased by the same
    amount:
  

  <div class="figure">
    <img no-autosize class="bordered" src="images/painting/linejoin-construction-fallback2.svg"
	 alt="Image showing the lines and points computed to construct an arcs line join
	      when the original offset circles do not intersect.">
    <p class="caption">Construction of an arcs line join shape, shown
      in pink. The white line is the original path and the dark gray
      region is the stroke. The dashed lines show circles that are
      tangent to and have the curvature of the segments at the
      join. Note they do not intersect. Two new circles are
      constructed by increasing the radii of the original circles by
      the same amount until the new circles just touch as shown by the
      olive-green circles. These new circles then define the join
      shape.
    
  </div>

  <p>
    If in this latter case, the tangents of the offset paths at the
    line join are parallel, the circles cannot be adjusted so that
    they touch. The line join should then be constructed as a
    rectangle whose width is the stroke width and whose length is the
    stroke width times one half of the value of the
    'stroke-miterlimit':
  

  <div class="figure">
    <img no-autosize class="bordered" src="images/painting/linejoin-construction-fallback3.svg"
	 alt="Image showing the lines and points computed to construct an arcs line join
	      when the original offset circles do not intersect.">
    <p class="caption">Construction of an arcs line join shape, shown
      in pink. The white line is the original path, which has two
      segments that come to a point, and the dark gray region is the
      stroke. The dashed lines show circles that are tangent to and
      have the curvature of the segments at the join. Note they do not
      intersect. Even if the radii of the circles are increased to infinity,
      the circles will not intersect. The line join is then a rectangle
      with the length determined by the miter limit (shown as a vertical
      dashed line).
    
  </div>

  Note: 
    There are a couple of ways to implement the fallback algorithm. The first
    way is by recursive trial and error on the magnitude of the radius change.
    The second is by an exact calculation utilizing the <em>touching circle
      condition</em> and the constraints that the centers of the circles must
    remain on lines normal to the path segments at the join. This leads to
    a quadratic equation where one solution is the required radius change.
  

</div>

<h3 id="PaintingVectorEffects">Vector effects</h3>

<p>This chapter explains 'vector-effect' related to Painting. Please refer to <a href="coords.html#VectorEffects">this</a> for the perspective of 'vector-effect'. 

<dl>
  <dt class="prop-value" id="non-scaling-stroke">non-scaling-stroke</dt>
  <dd>Modifies the way an object is stroked. Normally stroking involves calculating stroke
  outline of the shape's path in current [=user coordinate system=] and filling that outline with the
  stroke paint (color or gradient). With the non-scaling-stroke vector effect, stroke outline
  shall be calculated in the "host" coordinate space instead of [=user coordinate system=].
  More precisely: the [=viewport coordinate system=] of the [=furthest ancestral SVG viewport=].
  The stroke outline is calculated in the
  following manner: first, the shape's path is transformed into the host coordinate space.
  Stroke outline is calculated in the host coordinate space. The resulting outline is
  transformed back to the [=user coordinate system=].
  (Stroke outline is always filled with stroke paint in the current user coordinate system). The resulting visual effect of this
  modification is that stroke width is not dependent on the transformations of the element
  (including non-uniform scaling and shear transformations) and zoom level.</dd>
</dl>




<div class='ready-for-wider-review'>
<h3 id="Markers">Markers</h3>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Improve markers.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/27-svg-irc#T18-12-30">We will improve markers for SVG 2.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To solve the common problems authors have with SVG markers.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3286">ACTION-3286</a>)</td>
    </tr>
  </table>
</div>

<p>A marker is a graphical object that is painted at particular positions along
any [=shape=] element.

<p>The 'marker-start' and 'marker-end' properties
can be used to place markers at the first and last vertex of a
[=shape=], and the 'marker-mid' property can be used
to place markers at all other vertices (aside from the first and last).
The 'marker-start' and 'marker-end' can be used for example to
add arrowheads to paths.  Markers placed using these properties are known as
<dfn id="TermVertexMarker" data-dfn-type="dfn" data-export="">vertex markers</dfn>.

<p class='note'>In SVG 2, vertex markers are the only kind of markers
available.  Other specifications will add new types of markers.

<p>The graphics for a marker are defined by a <{marker}> element element.
The 'marker-start', 'marker-end' and 'marker-mid' properties,
together known as the <dfn id="TermMarkerProperties" data-dfn-type="dfn" data-export="">marker properties</dfn>, reference
<{marker}> element elements.

<p>Markers can be animated, and as with <{use}> elements, the animated
effects will show on all current uses of the markers within the document.

<p>Markers on a given element are painted in the following order, from
bottom to top:

<ul>
  <li>any marker specified by 'marker-start'</li>

  <li>the 'marker-mid' markers, in order of their position along the path</li>

  <li>any marker specified by 'marker-end'</li>
</ul>


<h4 id="MarkerElement">The <span class="element-name">marker</span> element</h4>

      <div class="element-summary">
        <div class="element-summary-name"><span class="element-name">‘<dfn data-dfn-type="element"
                 data-export=""
                 id="painting-elementdef-marker">marker</dfn>’</span></div>
        <dl>
          <dt>Categories:</dt>
          <dd>[=container element|Container element=], [=never-rendered element=]</dd>
          <dt>Content model:</dt>
          <dd>Any number of the following elements, in any order:<ul class="no-bullets">
              <li><a href="https://svgwg.org/specs/animations/#TermAnimationElement">animation elements</a><span
                      class="expanding"> — <span class="element-name">‘<a
                       href="https://svgwg.org/specs/animations/#AnimateElement"><span>animate</span></a>’</span>, <span
                        class="element-name">‘<a
                       href="https://svgwg.org/specs/animations/#AnimateMotionElement"><span>animateMotion</span></a>’</span>,
                  <span class="element-name">‘<a
                       href="https://svgwg.org/specs/animations/#AnimateTransformElement"><span>animateTransform</span></a>’</span>,
                  <span class="element-name">‘<a
                       href="https://svgwg.org/specs/animations/#SetElement"><span>set</span></a>’</span></span></li>
              <li>[=descriptive element|descriptive elements=]<span class="expanding"> — <span
                        class="element-name">‘<{desc}>’</span>, <span
                        class="element-name">‘<{title}>’</span>, <span
                        class="element-name">‘<{metadata}>’</span></span>
              </li>
              <li>[=paint server element|paint server elements=]<span class="expanding"> — <span
                        class="element-name">‘<{linearGradient}>’</span>, <span
                        class="element-name">‘<{radialGradient}>’</span>, <span
                        class="element-name">‘<{pattern}>’</span></span>
              </li>
              <li>[=shape elements=]<span class="expanding"> — <span
                        class="element-name">‘<{circle}>’</span>, <span
                        class="element-name">‘<{ellipse}>’</span>, <span
                        class="element-name">‘<{line}>’</span>, <span
                        class="element-name">‘<{path}>’</span>, <span
                        class="element-name">‘<{polygon}>’</span>, <span
                        class="element-name">‘<{polyline}>’</span>, <span
                        class="element-name">‘<{rect}>’</span></span></li>
              <li>[=structural element|structural elements=]<span class="expanding"> — <span
                        class="element-name">‘<{defs}>’</span>, <span
                        class="element-name">‘<{g}>’</span>, <span
                        class="element-name">‘<a href="#SVGElement"><span>svg</span></a>’</span>, <span
                        class="element-name">‘<{symbol}>’</span>, <span
                        class="element-name">‘<{use}>’</span></span></li>
            </ul><span class="element-name"><{a}></span>, <span
                  class="element-name"><a
                 href="https://drafts.fxtf.org/css-masking-1/#ClipPathElement"><span>clipPath</span></a></span>, <span
                  class="element-name"><a
                 href="https://drafts.fxtf.org/filter-effects/#FilterElement"><span>filter</span></a></span>, <span
                  class="element-name"><a href="#ForeignObjectElement"><span>foreignObject</span></a></span>,
            <span class="element-name"><{image}></span>, <span
                  class="element-name"><{marker}></span>, <span
                  class="element-name"><a
                 href="https://drafts.fxtf.org/css-masking-1/#MaskElement"><span>mask</span></a></span>, <span
                  class="element-name"><{script}></span>, <span
                  class="element-name"><{style}></span>, <span
                  class="element-name"><a href="#SwitchElement"><span>switch</span></a></span>, <span
                  class="element-name"><a href="#TextElement"><span>text</span></a></span>, <span
                  class="element-name"><a href="#ViewElement"><span>view</span></a></span></dd>
          <dt>Attributes:</dt>
          <dd>
            <ul class="no-bullets">
              <li>[=core attributes=]<span class="expanding"> — <span
                        class="attr-name">‘<span>id</span>’</span>, <span
                        class="attr-name">‘<span>tabindex</span>’</span>, <span
                        class="attr-name">‘<span>autofocus</span>’</span>, <span
                        class="attr-name">‘<span>lang</span>’</span>, <span
                        class="attr-name">‘<span>xml:space</span>’</span>, <span
                        class="attr-name">‘<span>class</span>’</span>, <span
                        class="attr-name">‘<span>style</span>’</span></span></li>
              <li><a href="https://html.spec.whatwg.org/multipage/webappapis.html#globaleventhandlers">global event
                  attributes</a><span class="expanding"> — <span class="attr-name">‘<span>oncancel</span>’</span>, <span class="attr-name">‘<span>oncanplay</span>’</span>, <span class="attr-name">‘<span>oncanplaythrough</span>’</span>, <span
                        class="attr-name">‘<span>onchange</span>’</span>, <span
                        class="attr-name">‘<span>onclick</span>’</span>, <span
                        class="attr-name">‘<span>onclose</span>’</span>, <span
                        class="attr-name">‘<span>oncopy</span>’</span>, <span
                        class="attr-name">‘<span>oncuechange</span>’</span>,
                  <span class="attr-name">‘<span>oncut</span>’</span>, <span
                        class="attr-name">‘<span>ondblclick</span>’</span>,
                  <span class="attr-name">‘<span>ondrag</span>’</span>, <span
                        class="attr-name">‘<span>ondragend</span>’</span>, <span
                        class="attr-name">‘<span>ondragenter</span>’</span>,
                  <span class="attr-name">‘<span>ondragexit</span>’</span>,
                  <span class="attr-name">‘<span>ondragleave</span>’</span>,
                  <span class="attr-name">‘<span>ondragover</span>’</span>,
                  <span class="attr-name">‘<span>ondragstart</span>’</span>,
                  <span class="attr-name">‘<span>ondrop</span>’</span>, <span
                        class="attr-name">‘<span>ondurationchange</span>’</span>, <span
                        class="attr-name">‘<span>onemptied</span>’</span>, <span
                        class="attr-name">‘<span>onended</span>’</span>, <span
                        class="attr-name">‘<span>onerror</span>’</span>, <span
                        class="attr-name">‘<span>onfocus</span>’</span>, <span
                        class="attr-name">‘<span>oninput</span>’</span>, <span
                        class="attr-name">‘<span>oninvalid</span>’</span>, <span
                        class="attr-name">‘<span>onkeydown</span>’</span>, <span
                        class="attr-name">‘<span>onkeypress</span>’</span>,
                  <span class="attr-name">‘<span>onkeyup</span>’</span>, <span
                        class="attr-name">‘<span>onload</span>’</span>, <span
                        class="attr-name">‘<span>onloadeddata</span>’</span>,
                  <span class="attr-name">‘<span>onloadedmetadata</span>’</span>, <span
                        class="attr-name">‘<span>onloadstart</span>’</span>,
                  <span class="attr-name">‘<span>onmousedown</span>’</span>,
                  <span class="attr-name">‘<span>onmouseenter</span>’</span>,
                  <span class="attr-name">‘<span>onmouseleave</span>’</span>,
                  <span class="attr-name">‘<span>onmousemove</span>’</span>,
                  <span class="attr-name">‘<span>onmouseout</span>’</span>,
                  <span class="attr-name">‘<span>onmouseover</span>’</span>,
                  <span class="attr-name">‘<span>onmouseup</span>’</span>, <span
                        class="attr-name">‘<span>onpaste</span>’</span>, <span
                        class="attr-name">‘<span>onpause</span>’</span>, <span
                        class="attr-name">‘<span>onplay</span>’</span>, <span
                        class="attr-name">‘<span>onplaying</span>’</span>, <span
                        class="attr-name">‘<span>onprogress</span>’</span>,
                  <span class="attr-name">‘<span>onratechange</span>’</span>,
                  <span class="attr-name">‘<span>onreset</span>’</span>, <span
                        class="attr-name">‘<span>onresize</span>’</span>, <span
                        class="attr-name">‘<span>onscroll</span>’</span>, <span
                        class="attr-name">‘<span>onseeked</span>’</span>, <span
                        class="attr-name">‘<span>onseeking</span>’</span>, <span
                        class="attr-name">‘<span>onselect</span>’</span>, <span
                        class="attr-name">‘<span>onshow</span>’</span>, <span
                        class="attr-name">‘<span>onstalled</span>’</span>, <span
                        class="attr-name">‘<span>onsubmit</span>’</span>, <span
                        class="attr-name">‘<span>onsuspend</span>’</span>, <span
                        class="attr-name">‘<span>ontimeupdate</span>’</span>,
                  <span class="attr-name">‘<span>ontoggle</span>’</span>, <span
                        class="attr-name">‘<span>onvolumechange</span>’</span>,
                  <span class="attr-name">‘<span>onwaiting</span>’</span>, <span
                        class="attr-name">‘<span>onwheel</span>’</span></span>
              </li>
              <li>[=presentation attributes=]<span class="expanding"> —
                </span></li>
              <li><span class="attr-name">‘<a href="#ViewBoxAttribute"><span>viewBox</span></a>’</span></li>
              <li><span class="attr-name">‘<a
                     href="#PreserveAspectRatioAttribute"><span>preserveAspectRatio</span></a>’</span></li>
              <li><span class="attr-name">‘<{marker/refX}>’</span>
              </li>
              <li><span class="attr-name">‘<{marker/refY}>’</span>
              </li>
              <li><span class="attr-name">‘<a href="#MarkerUnitsAttribute"><span>markerUnits</span></a>’</span>
              </li>
              <li><span class="attr-name">‘<a href="#MarkerWidthAttribute"><span>markerWidth</span></a>’</span>
              </li>
              <li><span class="attr-name">‘<a
                     href="#MarkerHeightAttribute"><span>markerHeight</span></a>’</span></li>
              <li><span class="attr-name">‘<a href="#OrientAttribute"><span>orient</span></a>’</span></li>
            </ul>
          </dd>
          <dt>DOM Interfaces:</dt>
          <dd>
            <ul class="no-bullets">
              <li>{{SVGMarkerElement}}</li>
            </ul>
          </dd>
        </dl>
      </div>

<p>The <{marker}> element element defines the graphics that are to
be used for drawing markers on a [=shape=].

<p id="MarkerAttributes"><em>Attribute definitions:</em>

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
    <td><dfn id="MarkerUnitsAttribute" data-dfn-type="element-attr" data-dfn-for="marker" data-export="">markerUnits</dfn></td>
    <td>strokeWidth | userSpaceOnUse</td>
    <td>strokeWidth</td>
    <td>yes</td>
  </tr>
</table>

</dt>
<dd>

<p>The {{markerUnits}} attribute defines the coordinate system for
attributes {{markerWidth}}, {{markerHeight}} and the
contents of the <{marker}> element.  Values have the
following meanings:

<dl>
  <dt><span class="attr-value">strokeWidth</span></dt>
  <dd>{{markerWidth}}, {{markerHeight}} and the contents
  of the <{marker}> element have values in a coordinate system
  which has a single unit equal to the size in user units of the
  painted stroke width of the element referencing the marker.</dd>

  <dt><span class="attr-value">userSpaceOnUse</span></dt>
  <dd>{{markerWidth}}, {{markerHeight}} and the contents
  of the <{marker}> element have values in the current
  user coordinate system in place for the element
  referencing the marker.</dd>
</dl>

</dd>
<dt>

Note: 
When {{markerUnits}} has the value <span class="attr-value">strokeWidth</span>,
the size of the marker is relative to the 'stroke-width' after it has
had any transforms applied that affect the width of the stroke in the
[=user coordinate system=] for the stroke. This means that, for example,
the 'vector-effect' attribute with a value of
<span class="attr-value">non-scaling-stroke</span> will result in the markers
also being non scaling.

<table class="attrdef def">
  <tr>
    <th>Name</th>
    <th>Value</th>
    <th>Initial value</th>
    <th>Animatable</th>
  </tr>
  <tr>
    <td><dfn id="MarkerWidthAttribute" data-dfn-type="element-attr" data-dfn-for="marker" data-export="">markerWidth</dfn>,
    <dfn id="MarkerHeightAttribute" data-dfn-type="element-attr" data-dfn-for="marker" data-export="">markerHeight</dfn></td>
    <td><<length-percentage>> | <<number>></td>
    <td>3</td>
    <td>yes</td>
  </tr>
</table>

</dt>
<dd>

<p>The {{markerWidth}} and {{markerHeight}} attributes
represent the size of the SVG viewport into which the marker is to
be fitted according to the [[#ViewBoxAttribute|viewBox]] and [[#PreserveAspectRatioAttribute|preserveAspectRatio]]
attributes.  A value of zero for either
attribute results in nothing being rendered for the marker.  A negative value
for either attribute is an error (see
<a href="conform.html#ErrorProcessing">Error processing</a>).

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
    <td><dfn id="MarkerElementRefXAttribute" data-dfn-type="element-attr" data-dfn-for="marker" data-export="">refX</dfn></td>
    <td><<length-percentage>> | <<number>> | left | center | right</td>
    <td>0</td>
    <td>yes</td>
  </tr>
  <tr>
    <td><dfn id="MarkerElementRefYAttribute" data-dfn-type="element-attr" data-dfn-for="marker" data-export="">refY</dfn></td>
    <td><<length-percentage>> | <<number>> | top | center | bottom</td>
    <td>0</td>
    <td>yes</td>
  </tr>
</table>

</dt>
<dd>

    Note: 
      New in SVG 2: geometric keywords (matches use in <{symbol}>).
    
    <p class="annotation">
      We will add top/center/bottom, left/center/right keywords to
      refX/refY on marker/symbol. Resolved at
      <a href="http://www.w3.org/2014/08/26-svg-minutes.html#item07">London
      F2F</a>. Values inspired by
      <a href="https://www.w3.org/TR/css3-background/#the-background-position">background-position</a>.
    

<p>The {{refX}} and {{refY}} attributes define the reference
point of the marker, which is to be placed exactly at the marker's
position on the [=shape=].  Lengths and numbers must be interpreted
as being in the coordinate system of the marker contents, after application of the
[[#ViewBoxAttribute|viewBox]] and [[#PreserveAspectRatioAttribute|preserveAspectRatio]] attributes. Percentage
values must be interpreted as being a percentage of the [[#ViewBoxAttribute|viewBox]]
width for {{refX}} or a percentage of the [[#ViewBoxAttribute|viewBox]] height for
{{refY}}.
<p>The keyword values must evaluate to the following percentages:
<table class="data compact">
<caption>Mapping of refX and refY keywords to percentages.</caption>
<thead>
<tr><th>keyword</th><th>percentage equivalent</th></tr>
</thead>
<tbody>
<tr><td>left</td><td>0%</td></tr>
<tr><td>center</td><td>50%</td></tr>
<tr><td>right</td><td>100%</td></tr>
<tr><td>top</td><td>0%</td></tr>
<tr><td>bottom</td><td>100%</td></tr>
</tbody>
</table>

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
    <td><dfn id="OrientAttribute" data-dfn-type="element-attr" data-dfn-for="marker" data-export="">orient</dfn></td>
    <td>auto | auto-start-reverse | <<angle>> | <<number>></td>
    <td>0</td>
    <td>yes&#160;(non-additive)</td>
  </tr>
</table>

</dt>
<dd>

<p>The {{orient}} attribute indicates how the marker
is rotated when it is placed at its position on the [=shape=].
Values have the following meanings:

<dl>
  <dt><span class="attr-value">auto</span></dt>
  <dd>
    <p>The marker is oriented such that its positive x-axis
    is pointing in a direction relative to the path
    at the position the marker is placed (See
    <a href="#RenderingMarkers">Rendering Markers</a>).
  </dd>
</dl>

<dl class="ready-for-wider-review">
  <dt><span class="attr-value">auto-start-reverse</span></dt>
  <dd>
    <p>If placed by 'marker-start', the marker is oriented
    180° different from the orientation that would be used if
    <span class="attr-value">auto</span> where specified.  For
    all other markers, <span class="attr-value">auto-start-reverse</span>
    means the same as <span class="attr-value">auto</span>.

    Note: This allows a single arrowhead marker to be defined
    that can be used for both the start and end of a path, i.e. which points
    outwards from both ends.
  </dd>
</dl>

<dl>
  <dt><span class="attr-value"><<angle>></span></dt>
  <dt><span class="attr-value"><<number>></span></dt>
  <dd>
    <p>The marker is oriented such that the specified angle is
    that measured between the [=shape=]'s positive x-axis
    and the marker's positive x-axis.  A <<number>> value
    specifies an angle in degrees.
    Note: For example, if a value of <span class="attr-value">45</span>
    is given, then the marker's positive x-axis would be pointing down and right
    in the [=shape=]'s coordinate system.
  </dd>
</dl>

</dd>

</dl>



<h4 id="VertexMarkerProperties">Vertex markers: the <span class="property">marker-start</span>, <span class="property">marker-mid</span> and <span class="property">marker-end</span> properties</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="MarkerStartProperty" data-dfn-type="property" data-export="">marker-start</dfn>,
        <dfn id="MarkerMidProperty" data-dfn-type="property" data-export="">marker-mid</dfn>,
        <dfn id="MarkerEndProperty" data-dfn-type="property" data-export="">marker-end</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>none | <a>&lt;marker-ref&gt;</a></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>none</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified, but with <a>&lt;url&gt;</a> values (that are part of
    a <a>&lt;marker-ref&gt;</a>) made absolute</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

<p>where:

<p class="definition prod"><dfn id="DataTypeMarkerRef"  data-dfn-type="type" data-export="">&lt;marker-ref&gt;</dfn> = <a>&lt;url&gt;</a>

<p>The 'marker-start' and 'marker-end' properties are used
to specify the marker that will be drawn at the first and last vertices
of the given [=shape=], respectively.  'marker-mid'
is used to specify the marker that will be drawn at all other vertices
(i.e., every vertex except the first and last).
Possible values for 'marker-start', 'marker-mid' and
'marker-end' are:

<dl>
  <dt><span class='prop-value'>none</span></dt>
  <dd>Indicates that no marker symbol will be drawn at the given
  vertex or vertices.</dd>

  <dt><span class='prop-value'>&lt;marker-ref&gt;</span></dt>
  <dd>Indicates that the <{marker}> element element referenced
  by the <a>&lt;marker-ref&gt;</a> value will be drawn at the given vertex or
  vertices.
  If the reference is not valid, then no marker will be drawn at the given
  vertex or vertices.</dd>
</dl>

<p>For all [=shapes=], the path that must be used when calculating
marker positions is the [=equivalent path=].

<div class='ready-for-wider-review'>
<p>For all [=shape=] elements, except <{polyline}> and <{path}>,
the last vertex is the same as the first
vertex. In this case, if the value of 'marker-start' and 'marker-end'
are both not <span class="prop-value">none</span>, then two markers
will be rendered on that final vertex.
For <{path}> elements, for each [=closed subpath=], the last vertex is
the same as the first vertex. 'marker-start' must only be rendered on
the first vertex of the [=path data=]. 'marker-end' must only be
rendered on the final vertex of the [=path data=].
'marker-mid' must be rendered on every vertex other than the first
vertex of the [=path data=] and the last vertex of the [=path data=].

<div class="example">
<pre class=include-raw>
path: images/painting/marker-doubled.svg
</pre>

  <div class="figure">
    <img no-autosize class="bordered" src="images/painting/marker-doubled.svg"
         alt="Image showing that for closed subpaths, two markers are painted at the start of each subpath.">
    <p class="caption">For [=path data=] containing [=closed subpaths=],
    two markers are drawn at the first/last vertex of each [=closed subpath=].
    For the leftmost [=closed subpath=], a 'marker-mid' is drawn over
    the 'marker-start'. For the middle [=closed subpath=], two
    'marker-mid' are drawn on top of one another. For the rightmost
    [=closed subpath=], 'marker-end' is drawn over 'marker-mid'.
    
  </div>
</div>
</div>

Note: Note that 'marker-start' and 'marker-end'
refer to the first and last vertex of the entire path, not each subpath.

<div class="ready-for-wider-review">
<div class="example">
  <p>The following example shows a triangular marker symbol used as a
  [=vertex marker=] to form an arrowhead at the end of two paths.

  <pre class=include-raw>
path: images/painting/marker.svg
</pre>

  <div class="figure">
    <img no-autosize class="bordered" src="images/painting/marker-rendering.svg"
         alt="Image showing the use of an automatically oriented marker.">
    <p class="caption">The triangle is placed at the end of the path and
    oriented automatically so that it points in the right direction.
    The use of <span class="prop-value">context-stroke</span> ensures
    the fill of the triangle matches the stroke of each <{path}>.
  </div>
</div>
</div>

<h4 id="MarkerShorthand">Marker shorthand: the <span class="property">marker</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="MarkerProperty" data-dfn-type="property" data-export="">marker</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>none | <a>&lt;marker-ref&gt;</a></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>not defined for shorthand properties</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>see individual properties</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

<p>The 'marker' property sets values for the
'marker-start', 'marker-mid' and 'marker-end'
properties.  The value of the 'marker' is used
directly for all three of the corresponding longhand properties.


<h4 id="RenderingMarkers">Rendering markers</h4>

<p>When orienting a marker automatically, due to specifying {{orient}}
as <code class='attr-value'>auto</code>, the following rules are used:

<ul>
  <li>If the vertex is the start or end of an [=open subpath=], then the marker is
  oriented in the <a href='paths.html#TermPathDirection'>path direction</a>.</li>

  <li>Otherwise, the marker is oriented in a direction half way between the
  <a href='paths.html#TermPathSegmentEndDirection'>direction at the end of the
  preceding segment</a> and the <a href='paths.html#TermPathSegmentStartDirection'>direction
  at the start of the following segment</a>.</li>
</ul>

<p>For each marker that is drawn, a temporary new user coordinate
system is established so that the marker will be positioned and sized
correctly, as follows:

<ul>
  <li>The axes of the temporary new user coordinate system are aligned
  according to the {{orient}} attribute on the
  <{marker}> element element.</li>

  <li>A temporary new coordinate system is established by attribute
  {{markerUnits}}. If {{markerUnits}} equals
  <span class="attr-value">strokeWidth</span>, then the temporary new
  user coordinate system is the result of scaling the current
  user coordinate system by the current value of property
  'stroke-width'. If {{markerUnits}} equals
  <span class="attr-value">userSpaceOnUse</span>, then no extra scale
  transformation is applied.</li>

  <li>An additional set of transformations might occur if the
  <{marker}> element element includes a [[#ViewBoxAttribute|viewBox]] attribute, in
  which case additional transformations are set up to produce the necessary
  result due to attributes [[#ViewBoxAttribute|viewBox]] and [[#PreserveAspectRatioAttribute|preserveAspectRatio]].</li>

  <li>If the [[#OverflowAndClipProperties|overflow]] property on the <{marker}> element element
  indicates that the marker needs to be clipped to its SVG viewport, then an
  implicit clipping path is established at the bounds of the SVG viewport.</li>
</ul>

<p class='note'>Note that the <a href="styling.html#UAStyleSheet">user agent style sheet</a> sets
the [[#OverflowAndClipProperties|overflow]] property for <{marker}> element elements to
<span class="prop-value">hidden</span>, which causes a rectangular clipping
path to be created at the bounds of marker's SVG viewport by default.

<p>Properties do not inherit from the element referencing the <{marker}> element
into the contents of the marker.  However, by using the
<span class="prop-value">context-stroke</span> value for the 'fill' or
'stroke' on elements in its definition, a single marker can be designed
to match the style of the element referencing the marker.

<p>Markers cannot be interacted with.  Events such as click or mouseover,
for example, are not dispatched to a <{marker}> element or its children when
the mouse is clicked or moved over a rendered marker.

<p>Markers are not rendered directly
and must be referenced by one of the [=marker properties=]
to be rendered.
The 'display' value for the <{marker}> element element
must always be set to <span class="prop-value">none</span>
by the [=user agent style sheet=],
and this declaration must have importance over any other CSS rule or presentation attribute.
  <!--
The 'display' property does not apply to the
<{marker}> element element; thus, <{marker}> element elements are not
directly rendered even if the 'display' property is
set to a value other than <span class="prop-value">none</span>, and
-->
<{marker}> element elements are available for referencing even when the
'display' property on the <{marker}> element element or any of its
ancestors is set to <span class="prop-value">none</span>.

<p>The rendering effect of a marker is as if the contents of the
referenced <{marker}> element element were deeply cloned
into a separate non-exposed DOM tree for each instance of the
marker. Because the cloned DOM tree is non-exposed, the SVG DOM
does not show the cloned instance of the marker.

<p>The conceptual deep cloning of the referenced
<{marker}> element element into a non-exposed DOM tree also
copies any property values resulting from
<a href="https://www.w3.org/TR/2011/REC-CSS2-20110607/cascade.html">the CSS cascade</a>
([[CSS2]], chapter 6) and
property inheritance on the referenced element and its contents. CSS
selectors can be applied to the original (i.e., referenced) elements
because they are part of the formal document structure. CSS selectors
cannot be applied to the (conceptually) cloned DOM tree because its
contents are not part of the formal document structure.

<div class='example'>
<p>For illustrative purposes, we'll repeat the marker example shown earlier:

<pre>
&lt;?xml version="1.0" standalone="no"?&gt;
&lt;svg width="4in" height="2in"
     viewBox="0 0 4000 2000"
     xmlns="http://www.w3.org/2000/svg"&gt;
  &lt;defs&gt;
    &lt;marker id="Triangle"
      viewBox="0 0 10 10" refX="0" refY="5"
      markerUnits="strokeWidth"
      markerWidth="4" markerHeight="3"
      orient="auto"&gt;
      &lt;path d="M 0 0 L 10 5 L 0 10 z" /&gt;
    &lt;/marker&gt;
  &lt;/defs&gt;
  &lt;rect x="10" y="10" width="3980" height="1980"
       fill="none" stroke="blue" stroke-width="10" /&gt;
  &lt;desc&gt;Placing an arrowhead at the end of a path.
  &lt;/desc&gt;
  &lt;path d="M 1000 750 L 2000 750 L 2500 1250"
        fill="none" stroke="black" stroke-width="100"
        marker-end="url(#Triangle)"  /&gt;
&lt;/svg&gt;
</pre>

<p>The rendering effect of the above file will be visually identical to
the following:

<pre>
&lt;?xml version="1.0" standalone="no"?&gt;
&lt;svg width="4in" height="2in"
     viewBox="0 0 4000 2000"
     xmlns="http://www.w3.org/2000/svg"&gt;
  &lt;desc&gt;File which produces the same effect
      as the marker example file, but without
      using markers.
  &lt;/desc&gt;
  &lt;rect x="10" y="10" width="3980" height="1980"
       fill="none" stroke="blue" stroke-width="10" /&gt;
  &lt;!-- The path draws as before, but without the marker properties --&gt;
  &lt;path d="M 1000 750 L 2000 750 L 2500 1250"
        fill="none" stroke="black" stroke-width="100"  /&gt;
  &lt;!-- The following logic simulates drawing a marker
       at final vertex of the path. --&gt;
  &lt;!-- First off, move the origin of the user coordinate system
       so that the origin is now aligned with the end point of the path. --&gt;
  <strong>&lt;g transform="translate(2500,1250)" &gt;</strong>
    &lt;!-- Rotate the coordinate system 45 degrees because
         the marker specified orient="auto" and the final segment
         of the path is going in the direction of 45 degrees. --&gt;
    <strong>&lt;g transform="rotate(45)" &gt;</strong>
      &lt;!-- Scale the coordinate system to match the coordinate system
           indicated by the 'markerUnits' attributes, which in this case has
           a value of 'strokeWidth'. Therefore, scale the coordinate system
           by the current value of the 'stroke-width' property, which is 100. --&gt;
      <strong>&lt;g transform="scale(100)" &gt;</strong>
        &lt;!-- Translate the coordinate system by
             (-refX*viewBoxToMarkerUnitsScaleX, -refY*viewBoxToMarkerUnitsScaleY)
             in order that (refX,refY) within the marker will align with the vertex.
             In this case, we use the default value for preserveAspectRatio
             ('xMidYMid meet'), which means find a uniform scale factor
             (i.e., viewBoxToMarkerUnitsScaleX=viewBoxToMarkerUnitsScaleY)
             such that the viewBox fits entirely within the SVG viewport ('meet') and
             is center-aligned ('xMidYMid'). In this case, the uniform scale factor
             is markerHeight/viewBoxHeight=3/10=.3. Therefore, translate by
             (-refX*.3,-refY*.3)=(0*.3,-5*.3)=(0,-1.5). --&gt;
        <strong>&lt;g transform="translate(0,-1.5)" &gt;</strong>
          &lt;!-- There is an implicit clipping path because the user agent style
               sheet says that the 'overflow' property for markers has the value
               'hidden'. To achieve this, create a clipping path at the bounds
               of the SVG viewport. Note that in this case the SVG viewport extends
               0.5 units to the left and right of the viewBox due to
               a uniform scale factor, different ratios for markerWidth/viewBoxWidth
               and markerHeight/viewBoxHeight, and 'xMidYMid' alignment --&gt;
          <strong>&lt;clipPath id="cp1" &gt;
            &lt;rect x="-0.5" y="0" width="4" height="3" /&gt;
          &lt;/clipPath&gt;</strong>
          <strong>&lt;g clip-path="url(#cp1)" &gt;</strong>
            &lt;!-- Scale the coordinate system by the uniform scale factor
                 markerHeight/viewBoxHeight=3/10=.3 to set the coordinate
                 system to viewBox units. --&gt;
            <strong>&lt;g transform="scale(.3)" &gt;</strong>
              &lt;!-- This 'g' element carries all property values that result from
                   cascading and inheritance of properties on the original 'marker' element.
                   In this example, neither fill nor stroke was specified on the 'marker'
                   element or any ancestors of the 'marker', so the initial values of
                   "black" and "none" are used, respectively. --&gt;
             <strong>&lt;g fill="black" stroke="none" &gt;</strong>
                &lt;!-- Expand out the contents of the 'marker' element. --&gt;
                <strong>&lt;path d="M 0 0 L 10 5 L 0 10 z" /&gt;</strong>
              <strong>&lt;/g&gt;</strong>
            <strong>&lt;/g&gt;</strong>
          <strong>&lt;/g&gt;</strong>
        <strong>&lt;/g&gt;</strong>
      <strong>&lt;/g&gt;</strong>
    <strong>&lt;/g&gt;</strong>
  <strong>&lt;/g&gt;</strong>
&lt;/svg&gt;
</pre>
<p class="view-as-svg"><a href="images/painting/marker-simulated.svg">View this example as SVG (SVG-enabled browsers only)</a>
</div>

</div>



<div class="ready-for-wider-review">
<h3 id="PaintOrder">Controlling paint operation order: the <span class="property">paint-order</span> property</h3>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Support control of the order of filling, stroke and painting markers on shapes.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2012/05/07-svg-minutes#item03">SVG 2 will adopt the <span class="property">paint-order</span>
 property proposal, though possibly with a different name.</a>
      The property name is now resolved, see <a href="http://www.w3.org/2013/11/15-svg-minutes.html#item12">15 Nov 2013 minutes</a>.</td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To address the common desire to paint strokes below fills without having to duplicate an element.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3285">ACTION-3285</a>)</td>
    </tr>
  </table>
</div>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn data-dfn-type="property" data-export="">paint-order</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>normal | [ fill || stroke || markers ]</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>normal</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=] and [=text content elements=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

Note: New in SVG 2.  Added primarily to allow painting the stroke
of text below its fill without needing to duplicate the <{text}> element.

<p>The 'paint-order' property controls the order that the three
paint operations that [=shapes=] and text are rendered with:
their fill, their stroke and any markers they might have.

<p>When the value of this property is <span class="prop-value">normal</span>,
the element is painted with the standard order of painting operations:
the fill is painted first, then its stroke and finally its markers.

<p>When any of the other keywords are used, the order of the paint
operations for painting the element is as given, from left to right.  If any of
the three keywords are omitted, they are painted last, in the order they
would be painted with <span class="prop-value">paint-order: normal</span>.

Note: This means that, for example,
<span class="prop-value">paint-order: stroke</span>
has the same rendering behavior as
<span class="prop-value">paint-order: stroke fill markers</span>.

<div class="example">
  <p>The following example shows how the 'paint-order' property can
  be used to render stroked text in a more aesthetically pleasing manner.

  <xmp>
<svg xmlns="http://www.w3.org/2000/svg"
     width="600" height="150" viewBox="0 0 600 150">

  <style>
    text {
      font: 80px bold sans-serif; stroke-linejoin: round;
      text-anchor: middle; fill: peachpuff; stroke: crimson;
    }
  </style>

  <text x="150" y="100" style="stroke-width: 6px;">pizazz</text>
  <text x="450" y="100" style="stroke-width: 12px; paint-order: stroke;">pizazz</text>
</svg>
</xmp>

  <div class="figure">
    <img no-autosize class="bordered" src="images/painting/paintorder.svg"
         alt="Image showing the effect of paint-order.">
    <p class="caption">Text painted with its stroke below the fill.
  </div>
</div>
</div>

<div class="ready-for-wider-review">
<h3 id="ColorInterpolation">Color space for interpolation: the <span class="property">color-interpolation</span> property</h3>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="ColorInterpolationProperty" data-dfn-type="property" data-export="">color-interpolation</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>auto | sRGB | linearRGB</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>sRGB</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=container elements=], [=graphics elements=],
    [=gradient elements=], <{use}> and <{animate}></td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

<p>The SVG user agent performs color interpolations and compositing
at various points as it processes SVG content.  The 'color-interpolation'
property controls which color space is used for the following graphics operations:

<ul>
  <li>interpolating between <a href="pservers.html#Gradients">gradient</a> stops,</li>

  <li>interpolating color when performing color animations with
  <{animate}>,</li>
  <li>and <a href="render.html#PaintersModel">compositing and blending</a> of
  [=graphics elements=] into the current background.</li>
</ul>

Note: For [[filter-effects-1|Filter Effects Module Level 1]], the
'color-interpolation-filters' property controls which color space is used.
[<a href="refs.html#ref-filter-effects-1">filter-effects-1</a>]
</div>

<div class='ready-for-wider-review'>
<p>The 'color-interpolation' property chooses between color operations
occurring in the sRGB color space or in a (light energy linear) linearized RGB
color space. Having chosen the appropriate color space, component-wise linear
interpolation is used.  Values for 'color-interpolation' have the
following meanings:

<dl>
  <dt><span class='prop-value'>auto</span></dt>
  <dd>Indicates that the user agent can choose either the
  <span class='prop-value'>sRGB</span> or
  <span class='prop-value'>linearRGB</span> spaces for color interpolation.
  This option indicates that the author doesn't require that color
  interpolation occur in a particular color space.</dd>

  <dt><span class='prop-value'>sRGB</span></dt>
  <dd>Indicates that color interpolation occurs in the sRGB
  color space.</dd>

  <dt><span class='prop-value'>linearRGB</span></dt>
  <dd>Indicates that color interpolation occurs in the
  linearized RGB color space as described below.</dd>
</dl>

<p id="sRGBlinearRGBConversionFormulas">The conversion formulas between the
sRGB color space (i.e., nonlinear with 2.2 gamma curve) and the linearized RGB
color space (i.e., color values expressed as sRGB tristimulus values without a
gamma curve) can be found in <a href="https://webstore.iec.ch/publication/6168">the sRGB specification</a>
[<a href="refs.html#ref-srgb">SRGB</a>].
For illustrative purposes, the following formula shows the conversion from
sRGB to linearized RGB, where <var ignore="">C<sub>srgb</sub></var> is one of the
three sRGB color components, <var ignore="">C<sub>linear</sub></var> is the corresponding
linearized RGB color component, and all color values are between 0 and 1:

<div role="math" aria-describedby="math-linearRGB">
  <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
    <mrow>
      <msub>
        <mi>C</mi>
        <mi>linear</mi>
      </msub>
      <mo>=</mo>
      <mo>{</mo>
      <mtable columnalign="left">
        <mtr>
          <mtd>
            <mfrac>
              <msub>
                <mi>C</mi>
                <mi>srgb</mi>
              </msub>
              <mn>12.92</mn>
            </mfrac>
          </mtd>
          <mtd>
            <mtext>if&#160;</mtext>
            <msub>
              <mi>C</mi>
              <mi>srgb</mi>
            </msub>
            <mo>≤</mo>
            <mn>0.04045</mn>
          </mtd>
        </mtr>
        <mtr>
          <mtd>
            <msup>
              <mfenced>
                <mfrac>
                  <mrow>
                    <msub>
                      <mi>C</mi>
                      <mi>srgb</mi>
                    </msub>
                    <mo>+</mo>
                    <mn>0.055</mn>
                  </mrow>
                  <mn>1.055</mn>
                </mfrac>
              </mfenced>
              <mn>2.4</mn>
            </msup>
          </mtd>
          <mtd>
            <mtext>if&#160;</mtext>
            <msub>
              <mi>C</mi>
              <mi>srgb</mi>
            </msub>
            <mo>></mo>
            <mn>0.04045</mn>
          </mtd>
        </mtr>
      </mtable>
    </mrow>
  </math>
  <pre id="math-linearRGB">
if C_srgb &lt;= 0.04045
  C_linear = C_srgb / 12.92
else if c_srgb &gt; 0.04045
  C_linear = ((C_srgb + 0.055) / 1.055) ^ 2.4
</pre>
</div>

<p>Out-of-range color values, if supported by the user agent, also are
converted using the above formulas.

<p>When a child element is blended into a background, the value of the
'color-interpolation' property on the child determines the type of
blending, not the value of the 'color-interpolation' on the parent.
For <a href="pservers.html#Gradients">gradients</a> which make use of the
<span class='attr-name'>href</span> attribute to reference another
gradient, the gradient uses the 'color-interpolation' property value
from the gradient element which is directly referenced by the 'fill' or
'stroke' property. When animating colors, color interpolation is
performed according to the value of the 'color-interpolation' property
on the element being animated.


<h3 id="RenderingHints">Rendering hints</h3>

<h4 id="ShapeRendering">The <span class="property">shape-rendering</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="ShapeRenderingProperty" data-dfn-type="property" data-export="">shape-rendering</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>auto | optimizeSpeed | crispEdges | geometricPrecision</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>auto</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>[=shapes=]</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

<p>The 'shape-rendering' property provides a hint to the
implementation about what tradeoffs to make as it renders vector graphics
elements such as <{path}> elements and <a href="shapes.html">basic shapes</a>
such as circles and rectangles.  Values have the following meanings:

<dl>
  <dt><span class='prop-value'>auto</span></dt>
  <dd>Indicates that the user agent shall make appropriate
  tradeoffs to balance speed, crisp edges and geometric
  precision, but with geometric precision given more importance
  than speed and crisp edges.</dd>

  <dt><span class='prop-value'>optimizeSpeed</span></dt>
  <dd>Indicates that the user agent shall emphasize rendering
  speed over geometric precision and crisp edges. This option
  will sometimes cause the user agent to turn off shape
  anti-aliasing.</dd>

  <dt><span class='prop-value'>crispEdges</span></dt>
  <dd>Indicates that the user agent shall attempt to emphasize
  the contrast between clean edges of artwork over rendering
  speed and geometric precision. To achieve crisp edges, the
  user agent might turn off anti-aliasing for all lines and
  curves or possibly just for straight lines which are close to
  vertical or horizontal. Also, the user agent might adjust
  line positions and line widths to align edges with device
  pixels.</dd>

  <dt><span class='prop-value'>geometricPrecision</span></dt>
  <dd>Indicates that the user agent shall emphasize geometric
  precision over speed and crisp edges.</dd>
</dl>

<h4 id="TextRendering">The <span class="property">text-rendering</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="TextRenderingProperty" data-dfn-type="property" data-export="">text-rendering</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>auto | optimizeSpeed | optimizeLegibility | geometricPrecision</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>auto</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td><{text}></td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

<p>The 'text-rendering' property provides a hint to the implementation
about what tradeoffs to make as it renders text.  Values have the
following meanings:

<dl>
  <dt><span class='prop-value'>auto</span></dt>
  <dd>Indicates that the user agent shall make appropriate
  tradeoffs to balance speed, legibility and geometric
  precision, but with legibility given more importance than
  speed and geometric precision.</dd>

  <dt><span class='prop-value'>optimizeSpeed</span></dt>
  <dd>Indicates that the user agent shall emphasize rendering
  speed over legibility and geometric precision. This option
  will sometimes cause the user agent to turn off text
  anti-aliasing.</dd>

  <dt><span class='prop-value'>optimizeLegibility</span></dt>
  <dd>Indicates that the user agent shall emphasize legibility
  over rendering speed and geometric precision. The user agent
  will often choose whether to apply anti-aliasing techniques,
  built-in font hinting or both to produce the most legible
  text.</dd>

  <dt><span class='prop-value'>geometricPrecision</span></dt>
  <dd>Indicates that the user agent shall emphasize geometric
  precision over legibility and rendering speed. This option
  will usually cause the user agent to suspend the use of
  hinting so that glyph outlines are drawn with comparable
  geometric precision to the rendering of path data.</dd>
</dl>

<h4 id="ImageRendering">The <span class="property">image-rendering</span> property</h4>

<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="ImageRenderingProperty" data-dfn-type="property" data-export="">image-rendering</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td>auto | optimizeQuality | optimizeSpeed</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>auto</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>images</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>yes</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>N/A</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>as specified</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>discrete</td>
  </tr>
</table>

Note: The <a href="http://dev.w3.org/csswg/css-images/#the-image-rendering">CSS Image Values and Replacement Content Module Level 4</a> may in the future redefine this property. In particular it should allow the choice between smoothing and keeping a pixelated look when upscaling.

<p>The [[SVG2#ImageRendering|image-rendering]] property provides a hint to the implementation
about how to make speed vs. quality tradeoffs as it performs
image processing.  Values have the following meanings:

<dl>
  <dt><span class='prop-value'>auto</span></dt>
  <dd>Indicates that the user agent shall make appropriate
  tradeoffs to balance speed and quality, but quality shall be
  given more importance than speed. The user agent shall employ
  a resampling algorithm at least as good as nearest neighbor
  resampling, but bilinear resampling is strongly preferred.
  For <a>Conforming
  High-Quality SVG Viewers</a>, the user agent shall employ a
  resampling algorithm at least as good as bilinear
  resampling.</dd>

  <dt><span class='prop-value'>optimizeQuality</span></dt>
  <dd>Indicates that the user agent shall emphasize quality
  over rendering speed. The user agent shall employ a
  resampling algorithm at least as good as bilinear
  resampling.</dd>

  <dt><span class='prop-value'>optimizeSpeed</span></dt>
  <dd>Indicates that the user agent shall emphasize rendering
  speed over quality. The user agent should use a resampling
  algorithm which achieves the goal of fast rendering, with the
  requirement that the resampling algorithm shall be at least
  as good as nearest neighbor resampling. If performance goals
  can be achieved with higher quality algorithms, then the user
  agent should use the higher quality algorithms instead of
  nearest neighbor resampling.</dd>
</dl>

<p>In all cases, resampling must be done in a truecolor (e.g.,
24-bit) color space even if the original data and/or the target
device is indexed color.  High quality SVG viewers should perform
image resampling using a linear color space.


<h3 id="WillChange">The effect of the <span class="property">will-change</span> property</h3>

Note: See the CSS Will Change Module Level 1 specification for the
definition of 'will-change'.

<p>The 'will-change' property is used to provide a hint to the user
agent as to the types of changes that will be made to content, giving
the user agent a better chance at performing rendering optimizations
for a given element.

<p>The 'will-change' property applies to all SVG [=graphics elements=],
however since SVG elements do not support scrolling, the
<span class='prop-value'>scroll-position</span> value will have no effect
on them.

<div class='example'>
  <p>The following example demonstrates how 'will-change' can be used
  to forewarn the user agent that an element will have its [[#TransformProperty|transform]]
  property changed, with the potential result of the user agent rendering the
  element into its own GPU layer so that the scripted [[#TransformProperty|transform]]
  changes appear smooth.

<pre class=include-raw>
path: images/painting/will-change.svg
</pre>

  <div class="figure">
    <img class="bordered" src="images/painting/will-change-image.svg"
         width="200" height="150"
         alt='A blue star with the text "Drag the star!" above.'>
    <p class="caption">In a user agent that supports 'will-change'
    on SVG elements, the star might be rendered into a layer so that
    it can be composited quickly when it is dragged around the canvas.
    <a href="images/painting/will-change.svg">View interactive SVG document.</a>
  </div>
</div>

Note: The 'will-change' property replaces the
<span class="property">buffered-rendering</span> property defined in
SVG Tiny 1.2.
</div>


<div class='ready-for-wider-review'>
<h3 id="painting-dom">DOM interfaces</h3>

<h4 id="InterfaceSVGMarkerElement">Interface SVGMarkerElement</h4>



<p>An [[#InterfaceSVGMarkerElement|SVGMarkerElement]] object represents a <{marker}> element
element in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGMarkerElement</b> : <a>SVGElement</a> {

  // Marker Unit Types
  const unsigned short <a href="painting.html#__svg__SVGMarkerElement__SVG_MARKERUNITS_UNKNOWN">SVG_MARKERUNITS_UNKNOWN</a> = 0;
  const unsigned short <a href="painting.html#__svg__SVGMarkerElement__SVG_MARKERUNITS_USERSPACEONUSE">SVG_MARKERUNITS_USERSPACEONUSE</a> = 1;
  const unsigned short <a href="painting.html#__svg__SVGMarkerElement__SVG_MARKERUNITS_STROKEWIDTH">SVG_MARKERUNITS_STROKEWIDTH</a> = 2;

  // Marker Orientation Types
  const unsigned short <a href="painting.html#__svg__SVGMarkerElement__SVG_MARKER_ORIENT_UNKNOWN">SVG_MARKER_ORIENT_UNKNOWN</a> = 0;
  const unsigned short <a href="painting.html#__svg__SVGMarkerElement__SVG_MARKER_ORIENT_AUTO">SVG_MARKER_ORIENT_AUTO</a> = 1;
  const unsigned short <a href="painting.html#__svg__SVGMarkerElement__SVG_MARKER_ORIENT_ANGLE">SVG_MARKER_ORIENT_ANGLE</a> = 2;
  const unsigned short <a href="painting.html#__svg__SVGMarkerElement__SVG_MARKER_ORIENT_AUTO_START_REVERSE">SVG_MARKER_ORIENT_AUTO_START_REVERSE</a> = 3;

  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="painting.html#__svg__SVGMarkerElement__refX">refX</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="painting.html#__svg__SVGMarkerElement__refY">refY</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedEnumeration</a> <a href="painting.html#__svg__SVGMarkerElement__markerUnits">markerUnits</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="painting.html#__svg__SVGMarkerElement__markerWidth">markerWidth</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="painting.html#__svg__SVGMarkerElement__markerHeight">markerHeight</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedEnumeration</a> <a href="painting.html#__svg__SVGMarkerElement__orientType">orientType</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedAngle</a> <a href="painting.html#__svg__SVGMarkerElement__orientAngle">orientAngle</a>;
  attribute DOMString <a href="painting.html#__svg__SVGMarkerElement__orient">orient</a>;

  undefined <a href="painting.html#__svg__SVGMarkerElement__setOrientToAuto">setOrientToAuto</a>();
  undefined <a href="painting.html#__svg__SVGMarkerElement__setOrientToAngle">setOrientToAngle</a>(<a>SVGAngle</a> angle);
};

<a>SVGMarkerElement</a> includes <a>SVGFitToViewBox</a>;
</pre>

<p>The numeric marker unit type constants defined on [[#InterfaceSVGMarkerElement|SVGMarkerElement]]
are used to represent the keyword values that the {{markerUnits}}
attribute can take.  Their meanings are as follows:

<table class='vert'>
  <tr><th>Constant</th><th>Meaning</th></tr>
  <tr><td><b id="__svg__SVGMarkerElement__SVG_MARKERUNITS_USERSPACEONUSE">SVG_MARKERUNITS_USERSPACEONUSE</b></td><td>The <span class="attr-value">userSpaceOnUse</span> keyword.</td></tr>
  <tr><td><b id="__svg__SVGMarkerElement__SVG_MARKERUNITS_STROKEWIDTH">SVG_MARKERUNITS_STROKEWIDTH</b></td><td>The <span class="attr-value">strokeWidth</span> keyword.</td></tr>
  <tr><td><b id="__svg__SVGMarkerElement__SVG_MARKERUNITS_UNKNOWN">SVG_MARKERUNITS_UNKNOWN</b></td><td>Some other value.</td></tr>
</table>

<p>The numeric marker orientation type constants defined on [[#InterfaceSVGMarkerElement|SVGMarkerElement]]
are used to represent the types of values that the {{orient}}
attribute can take.  Their meanings are as follows:

<table class='vert'>
  <tr><th>Constant</th><th>Meaning</th></tr>
  <tr><td><b id="__svg__SVGMarkerElement__SVG_MARKER_ORIENT_AUTO">SVG_MARKER_ORIENT_AUTO</b></td><td>The <span class="attr-value">auto</span> keyword.</td></tr>
  <tr><td><b id="__svg__SVGMarkerElement__SVG_MARKER_ORIENT_AUTO_START_REVERSE">SVG_MARKER_ORIENT_AUTO_START_REVERSE</b></td><td>The <span class="attr-value">auto-start-reverse</span> keyword.</td></tr>
  <tr><td><b id="__svg__SVGMarkerElement__SVG_MARKER_ORIENT_ANGLE">SVG_MARKER_ORIENT_ANGLE</b></td><td>An <<angle>> or <<number>> value indicating the orientation angle.</td></tr>
  <tr><td><b id="__svg__SVGMarkerElement__SVG_MARKER_ORIENT_UNKNOWN">SVG_MARKER_ORIENT_UNKNOWN</b></td><td>Some other value.</td></tr>
</table>

<p>The <b id="__svg__SVGMarkerElement__markerUnits">markerUnits</b> IDL attribute
[=reflects=] the {{markerUnits}} content attribute.  The
[=numeric type values=] for {{markerUnits}} are as
described above in the numeric marker unit type constant table.

<p>The <b id="__svg__SVGMarkerElement__orientType">orientType</b>,
<b id="__svg__SVGMarkerElement__orientAngle">orientAngle</b> and
<b id="__svg__SVGMarkerElement__orient">orient</b> IDL attributes
all reflect the {{orient}} content attribute.
The [=numeric type values=] for {{orient}} are as follows:

<table class="vert">
  <tr><th>Value</th><th>Numeric type value</th></tr>
  <tr>
    <td><span class='attr-value'>auto</span></td>
    <td><a href='painting.html#__svg__SVGMarkerElement__SVG_MARKER_ORIENT_AUTO'>SVG_MARKER_ORIENT_AUTO</a></td>
  </tr>
  <tr>
    <td><span class='attr-value'>auto-start-reverse</span></td>
    <td><a href='painting.html#__svg__SVGMarkerElement__SVG_MARKER_ORIENT_AUTO_START_REVERSE'>SVG_MARKER_ORIENT_AUTO_START_REVERSE</a></td>
  </tr>
  <tr>
    <td><<angle>> | <<number>></td>
    <td><a href='painting.html#__svg__SVGMarkerElement__SVG_MARKER_ORIENT_ANGLE'>SVG_MARKER_ORIENT_ANGLE</a></td>
  </tr>
</table>

<p>The <b id="__svg__SVGMarkerElement__refX">refX</b>,
<b id="__svg__SVGMarkerElement__refY">refY</b>,
<b id="__svg__SVGMarkerElement__markerWidth">markerWidth</b> and
<b id="__svg__SVGMarkerElement__markerHeight">markerHeight</b> IDL attributes
reflect the {{refX}}, {{refY}}, {{markerWidth}}
and {{markerHeight}} content attributes, respectively.

<p>The <b id="__svg__SVGMarkerElement__setOrientToAuto">setOrientToAuto</b>
method is used to set the value of the {{orient}} attribute
to <code class='attr-value'>auto</code>.  When setOrientToAuto() is
called, the {{orient}} attribute is simply set to <code class='attr-value'>auto</code>.

<p>The <b id="__svg__SVGMarkerElement__setOrientToAngle">setOrientToAngle</b>
method is used to set the value of the {{orient}} attribute
to a specific angle value.  When setOrientToAngle(<var>angle</var>) is
called, the {{orient}} attribute is [=reserialized=] using
<var>angle</var> as the value.


</div>
