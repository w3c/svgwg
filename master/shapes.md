<h2>Basic Shapes</h2>

<h3 id="Introduction">Introduction and definitions</h3>

<dl class="definitions">
  <dt id="TermBasicShapeElement"><dfn id="basic-shape" data-dfn-type="dfn" data-export="">basic shape</dfn></dt>
  <dt>shape</dt>
  <dt><dfn>shape elements</dfn></dt><!--keep that for Bikeshed! -->
  <dd>A graphics element that is defined by some combination of
  straight lines and curves. Specifically:
  @@elementcategory shape@@.</dd>
</dl>

<p>SVG contains the following set of basic shape elements:

<ul>
  <li>rectangles (including optional rounded corners), created with the <{rect}> element,</li>
  <li>circles, created with the {{circle}} element,</li>
  <li>ellipses, created with the {{ellipse}} element,</li>
  <li>straight lines, created with the {{line}} element,</li>
  <li>polylines, created with the {{polyline}} element, and</li>
  <li>polygons, created with the {{polygon}} element</li>
</ul>

<p>Mathematically, these shape elements are equivalent to a
{{path}} element that would construct the same shape. The basic
shapes may be stroked, filled and used as clip paths. All of the
properties available for {{path}} elements also apply to the basic
shapes.

<p>The [=equivalent path=] and algorithm to compute the stroke for each shape
  are defined in the shape sections below.

<h3 id="RectElement">The <span class="element-name">rect</span> element</h3>


<p>The <{rect}> element defines a rectangle which is axis-aligned
with the current [=user coordinate system=]. Rounded rectangles can be achieved by setting
non-zero values for the {{rx}} and {{ry}} geometric properties.

@@elementsummary rect@@

<p>The {{x}} and {{y}} coordinates refer to the left and top edges of the rectangle,
in the current user coordinate system.

<p>The {{width}} and {{height}} properties define the overall width and height of the rectangle.
A negative value for either property is [=invalid=] and must be [=ignored=].
A computed value of zero for either dimension disables rendering of the element.

<p>For rounded rectangles,
the computed values of the {{rx}} and {{ry}} properties define
the x- and y-axis radii of elliptical arcs used to round off the corners of the rectangle.
The arc are always symmetrical along both horizontal and vertical axis; to create a rectangle with uneven corner rounding, define the shape explicitly with a {{path}}.
A negative value for either property is [=invalid=] and must be [=ignored=].
A computed value of zero for either dimension,
or a computed value of <code>auto</code> for <em>both</em> dimensions,
results in a rectangle without corner rounding.


<p>The used values for the x- and y-axis rounded corner radii
may be determined implicitly from the other dimension (using the <code>auto</code> value),
and are also subject to clamping so that the lengths of
the straight segments of the rectangle are never negative.
The used values for {{rx}} and {{ry}} are determined
from the computed values by following these steps in order:

<ol>
  <li>If both {{rx}} and {{ry}} have a computed value of <code>auto</code>
  (since <code>auto</code> is the initial value for both properties, this will also occur if neither are specified by the author or if all author-supplied values are invalid),
  then the used value of both {{rx}} and {{ry}} is 0.  (This will result in square corners.)</li>
 <li>Otherwise, convert specified values to absolute values as follows:
   <ol>
  <li>If {{rx}} is set to a length value or a percentage,
  but {{ry}} is <code>auto</code>,
  calculate an absolute length equivalent for {{rx}}, resolving percentages against the used {{width}} of the rectangle;
  the absolute value for {{ry}} is the same.</li>

  <li>If {{ry}} is set to a length value or a percentage,
  but {{rx}} is <code>auto</code>,
  calculate the absolute length equivalent for {{ry}}, resolving percentages against the used {{height}} of the rectangle;
  the absolute value for {{rx}} is the same.</li>

  <li>If both {{rx}} and {{ry}} were set to lengths or percentages,
  absolute values are generated individually,
  resolving {{rx}} percentages against the used {{width}},
  and resolving {{ry}} percentages against the used {{height}}.</li>
 </ol></li>
 <li>Finally, apply clamping to generate the used values:
   <ol>
  <li>If the absolute {{rx}} (after the above steps)
  is greater than half of the used {{width}},
  then the used value of {{rx}} is half of the used {{width}}.</li>

  <li>If the absolute {{ry}} (after the above steps)
  is greater than half of the used {{height}},
  then the used value of {{ry}} is half of the used {{height}}.</li>

  <li>Otherwise, the used values of {{rx}} and {{ry}} are the absolute values computed previously.</li>
 </ol></li>
</ol>

<p>Mathematically, a <{rect}> element is mapped to an
equivalent {{path}} element as follows,
after generating absolute used values
<var>x</var>, <var>y</var>, <var>width</var>, <var>height</var>,
<var>rx</var>, and <var>rx</var>
in user units for the user coordinate system,
for each of the equivalent geometric properties
following the rules specified above and in <a href="coords.html#Units">Units</a>: 

<ol class='algorithm ready-for-wider-review'>
  <li>perform an absolute <a
  href="paths.html#PathDataMovetoCommands">moveto</a> operation to
  location (<var>x+rx</var>,<var>y</var>);</li>

  <li>perform an absolute horizontal <a href="paths.html#PathDataLinetoCommands">lineto</a>
  with parameter <var>x+width-rx</var>;</li>

  <li><em>if</em> both <var>rx</var> and <var>ry</var> are greater than zero,
  perform an absolute <a href="paths.html#PathDataEllipticalArcCommands">elliptical arc</a>
  operation to coordinate (<var>x+width</var>,<var>y+ry</var>),
  where <var>rx</var> and <var>ry</var> are used as the equivalent parameters to
  the <a href="paths.html#PathDataEllipticalArcCommands">elliptical arc</a> command,
  the <var>x-axis-rotation</var> and <var>large-arc-flag</var> are set to zero,
  the <var>sweep-flag</var> is set to one;</li>

  <li>perform an absolute vertical <a href="paths.html#PathDataLinetoCommands">lineto</a>
  parameter <var>y+height-ry</var>;</li>

  <li><em>if</em> both <var>rx</var> and <var>ry</var> are greater than zero,
  perform an absolute <a href="paths.html#PathDataEllipticalArcCommands">elliptical arc</a>
  operation to coordinate (<var>x+width-rx</var>,<var>y+height</var>),
  using the same parameters as previously;</li>

  <li>perform an absolute horizontal <a href="paths.html#PathDataLinetoCommands">lineto</a>
  parameter <var>x+rx</var>;</li>

  <li><em>if</em> both <var>rx</var> and <var>ry</var> are greater than zero,
  perform an absolute <a href="paths.html#PathDataEllipticalArcCommands">elliptical arc</a>
  operation to coordinate (<var>x</var>,<var>y+height-ry</var>),
  using the same parameters as previously;</li>

  <li>perform an absolute vertical <a href="paths.html#PathDataLinetoCommands">lineto</a>
  parameter <var>y+ry</var></li>

  <li><em>if</em> both <var>rx</var> and <var>ry</var> are greater than zero,
  perform an absolute <a href="paths.html#PathDataEllipticalArcCommands">elliptical arc</a>
  operation with a [=segment-completing close path=] operation,
  using the same parameters as previously.</li>
</ol>

<p class="annotation">
  Path decomposition resolved during teleconference on
  <a href="http://www.w3.org/2013/06/03-svg-minutes.html#item03">June
  3rd, 2013</a>.


<p id="ExampleRect01"><span class="example-ref">Example rect01</span> shows a
rectangle with sharp corners. The <{rect}> element is filled with yellow
and stroked with navy.

<pre class=include-raw>
path: images/shapes/rect01.svg
</pre>
<!--
@@fix
<pre class=include>
path: images/shapes/rect01.svg
</pre>
-->

<p id="ExampleRect02"><span class="example-ref">Example rect02</span> shows
two rounded rectangles. The {{rx}} specifies how to round the corners of
the rectangles. Note that since no value has been specified for the {{ry}}
attribute, the used value will be derived from the {{rx}} attribute.

<pre class=include-raw>
path: images/shapes/rect02.svg
</pre>
<!--
@@fix
<pre class=include>
path: images/shapes/rect02.svg
</pre>
-->

<h3 id="CircleElement">The <span class="element-name">circle</span> element</h3>


<p>The {{circle}} element defines a circle based on a center point and a
radius.

@@elementsummary circle@@
<p>
  The {{cx}} and {{cy}} attributes define the coordinates of the center of the circle.


<p>
  The {{r}} attribute defines the radius of the circle.
  A negative value is [=invalid=] and must be [=ignored=].
  A computed value of zero disables rendering of the element.


<p>
  Mathematically, a {{circle}} element is mapped to an
  equivalent {{path}} element that consists of four
  <a href="paths.html#PathDataEllipticalArcCommands">elliptical
  arc</a> segments, each covering a quarter of the circle. The path
  begins at the "3 o'clock" point on the radius and proceeds in a
  clock-wise direction (before any transformations).
  The <var>rx</var> and <var>ry</var> parameters to the arc commands
  are both equal to the used value of the {{r}} property, after conversion to local user units,
  while the <var>x-axis-rotation</var>
  and the <var>large-arc-flag</var> are set to zero,
  and the <var>sweep-flag</var> is set to one.
  The coordinates are computed as follows,
  where <var>cx</var>, <var>cy</var>, and <var>r</var> are the used values of the equivalent properties, converted to user units:

<ol>
  <li>A move-to command to the point
  <var>cx+r</var>,<var>cy</var>;</li>
  <li>arc to <var>cx</var>,<var>cy+r</var>;</li>
  <li>arc to <var>cx-r</var>,<var>cy</var>;</li>
  <li>arc to <var>cx</var>,<var>cy-r</var>;</li>
  <li>arc with a [=segment-completing close path=] operation.</li>
</ol>

<p class="annotation">
  Path decomposition resolved during teleconference on
  <a href="http://www.w3.org/2013/06/03-svg-minutes.html#item03">June
  3rd, 2013</a>.


<p id="ExampleCircle01"><span class="example-ref">Example
circle01</span> consists of a {{circle}} element that is filled
with red and stroked with blue.

<pre class=include-raw>
path: images/shapes/circle01.svg
</pre>
<!--
@@fix
<pre class=include>
path: images/shapes/circle01.svg
</pre>
-->

<h3 id="EllipseElement">The <span class="element-name">ellipse</span> element</h3>


<p>The {{ellipse}} element defines an ellipse which is axis-aligned
with the current [=user coordinate system=] based on a center point and two radii.

@@elementsummary ellipse@@
<p>
  The {{cx}} and {{cy}} coordinates define the center of the ellipse.


<p>
  The {{rx}} and {{ry}} properties define the x- and y-axis radii of the
  ellipse.
  A negative value for either property is [=invalid=] and must be [=ignored=].
  A computed value of zero for either dimension,
  or a computed value of <code>auto</code> for <em>both</em> dimensions,
  disables rendering of the element.


<p>
  An <code>auto</code> value for <em>either</em> {{rx}} or {{ry}}
  is converted to a used value, following the rules given above for rectangles
  (but without any clamping based on {{width}} or {{height}}).
  Effectively, an <code>auto</code> value creates a circular shape
  whose radius is defined by a value expressed solely in one dimension;
  this allows for creating a circle with a radius defined in terms of one of the following:

<ul>
  <li>a percentage of the coordinate system <b>width</b>; that is, a percentage value for <a><b>rx</b></a> and an <code>auto</code> value for {{ry}}.</li>
  <li>a percentage of the coordinate system <b>height</b>; that is, an <code>auto</code> value for {{rx}} and a percentage value for <a><b>ry</b></a>.</li>
</ul>

Note: 
  New in SVG 2.
  The <code>auto</code> value for {{rx}} and {{ry}} was added to allow consistent
  parsing of these properties for both ellipses and rectangles.
  Previously, if either {{rx}} or {{ry}} was unspecified,
  the ellipse would not render.


<p>
  Mathematically, an {{ellipse}} element is mapped to an
  equivalent {{path}} element that consists of four
  <a href="paths.html#PathDataEllipticalArcCommands">elliptical
  arc</a> segments, each covering a quarter of the ellipse. The path
  begins at the "3 o'clock" point on the radius and proceeds in a
  clock-wise direction (before any transformation).
  The <var>rx</var> and <var>ry</var> parameters to the arc commands
  are the used values of the equivalent properties after conversion to local user units,
  while the <var>x-axis-rotation</var>
  and the <var>large-arc-flag</var> are set to zero,
  and the <var>sweep-flag</var> is set to one.
  The coordinates are computed as follows,
  where <var>cx</var>, <var>cy</var>, <var>rx</var>, and <var>ry</var>
  are the used values of the equivalent properties, converted to user units:

<ol>
  <li>A move-to command to the point
  <var>cx+rx</var>,<var>cy</var>;</li>
  <li>arc to <var>cx</var>,<var>cy+ry</var>;</li>
  <li>arc to <var>cx-rx</var>,<var>cy</var>;</li>
  <li>arc to <var>cx</var>,<var>cy-ry</var>;</li>
  <li>arc with a [=segment-completing close path=] operation.</li>
</ol>

<p class="annotation">
  Path decomposition resolved during teleconference on
  <a href="http://www.w3.org/2013/06/03-svg-minutes.html#item03">June
  3rd, 2013</a>.


<p><span class="example-ref">Example ellipse01</span> below specifies
the coordinates of the two ellipses in the user coordinate system
established by the [[#ViewBoxAttribute|viewBox]] attribute on the <{svg}>
element and the [[#TransformProperty|transform]] property on the <{g}> and
{{ellipse}} elements. Both ellipses use the default values of
zero for the {{cx}} and {{cy}} attributes (the center of the
ellipse). The second ellipse is rotated.

<pre class=include-raw>
path: images/shapes/ellipse01.svg
</pre>
<!-- 
@@fix 
<pre class=include>
path: images/shapes/ellipse01.svg
</pre>
-->

<h3 id="LineElement">The <span class="element-name">line</span> element</h3>


<p>The {{line}} element defines a line segment that starts at one point
and ends at another.

@@elementsummary line@@

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
        <td><dfn id="LineElementX1Attribute" data-dfn-type="element-attr" data-dfn-for="line" data-export="">x1</dfn>, <dfn id="LineElementY1Attribute" data-dfn-type="element-attr" data-dfn-for="line" data-export="">y1</dfn></td>
        <td><<length-percentage>> | <<number>></td>
        <td>0</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    The x- and y-axis coordinates of the start of the line.
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
        <td><dfn id="LineElementX2Attribute" data-dfn-type="element-attr" data-dfn-for="line" data-export="">x2</dfn>, <dfn id="LineElementY2Attribute" data-dfn-type="element-attr" data-dfn-for="line" data-export="">y2</dfn></td>
        <td><<length-percentage>> | <<number>></td>
        <td>0</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    The x- and y-axis coordinates of the end of the line.
  </dd>
</dl>

Note: 
  A future specification may convert the {{x1}}, {{y1}}, {{x2}}, and {{y2}} attributes to geometric properties.
  Currently, they can only be specified via element attributes, and not CSS.


<p>Mathematically, a {{line}} element can be mapped to an
equivalent {{path}} element as follows,
after converting coordinates into user coordinate system user units according
to <a href="coords.html#Units">Units</a>
to generate values <var>x1</var>, <var>y1</var>, <var>x2</var>, and <var>y2</var>:

<ul>
  <li>perform an absolute <a href="paths.html#PathDataMovetoCommands">moveto</a>
  operation to absolute location (<var>x1</var>,<var>y1</var>)</li>

  <li>perform an absolute <a href="paths.html#PathDataLinetoCommands">lineto</a>
  operation to absolute location (<var>x2</var>,<var>y2</var>)</li>
</ul>

<p>Because {{line}} elements are single lines and thus are geometrically
one-dimensional, they have no interior; thus, {{line}} elements are never
filled (see the {{fill}} property).

<p id="ExampleLine01"><span class="example-ref">Example line01</span> below
specifies the coordinates of the five lines in the user coordinate system
established by the [[#ViewBoxAttribute|viewBox]] attribute on the <{svg}> element. The
lines have different thicknesses.

<pre class=include-raw>
path: images/shapes/line01.svg
</pre>
<!-- 
@@fix 
<pre class=include>
path: images/shapes/line01.svg
</pre>
-->

<h3 id="PolylineElement">The <span class="element-name">polyline</span> element</h3>


<p>The {{polyline}} element defines a set of connected straight
line segments. Typically, {{polyline}} elements define open
shapes.

@@elementsummary polyline@@

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
        <td><dfn id="PolylineElementPointsAttribute" data-dfn-type="element-attr" data-dfn-for="polyline" data-export="">points</dfn></td>
	<td><a>&lt;points&gt;</a></td>
        <td>(none)</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>where:
    <div class="definition prod">
      <dfn id="DataTypePoints" data-dfn-type="type" data-export="">&lt;points&gt;</dfn> =
      <div style="margin-left: 4em">[ <<number>>+ ]#</div>
    </div>
    <p>The points that make up the polyline. All coordinate
    values are in the user coordinate system.
    <p>If an odd number of coordinates is provided, then the element is in
    error, with the same user agent behavior as occurs with an incorrectly
    specified {{path}} element. In such error cases the user agent will drop
    the last, odd coordinate and otherwise render the shape.
    <p class="ready-for-wider-review">The initial value, (none), indicates that the polyline element
    is valid but does not render.
  </dd>
</dl>

Note: 
  A future specification may convert the {{points}} attribute to a geometric property.
  Currently, it can only be specified via an element attribute, and not CSS.


<p>Mathematically, a {{polyline}} element can be mapped to an
equivalent {{path}} element as follows:

<ul>
  <li>perform an absolute <a href="paths.html#PathDataMovetoCommands">moveto</a>
  operation to the first coordinate pair in the list of points</li>

  <li>for each subsequent coordinate pair, perform an absolute
  <a href="paths.html#PathDataLinetoCommands">lineto</a> operation to that
  coordinate pair.</li>
</ul>

<p id="ExamplePolyline01"><span class="example-ref">Example polyline01</span>
below specifies a polyline in the user coordinate system established by the
[[#ViewBoxAttribute|viewBox]] attribute on the <{svg}> element.

<pre class=include-raw>
path: images/shapes/polyline01.svg
</pre>
<!--
@@fix 
<pre class=include>
path: images/shapes/polyline01.svg
</pre>
-->


<h3 id="PolygonElement">The <span class="element-name">polygon</span> element</h3>


<p>The {{polygon}} element defines a closed shape consisting of a
set of connected straight line segments.

@@elementsummary polygon@@

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
        <td><dfn id="PolygonElementPointsAttribute" data-dfn-type="element-attr" data-dfn-for="polygon" data-export="">points</dfn></td>
	<td><a>&lt;points&gt;</a></td>
        <td>(none)</td>
        <td>yes</td>
      </tr>
    </table>
  </dt>
  <dd>
    <p>The points that make up the polygon. All coordinate
    values are in the user coordinate system.
    <p>If an odd number of coordinates is provided, then the element is in
    error, with the same user agent behavior as occurs with an incorrectly
    specified {{path}} element.
    <p class="ready-for-wider-review">The initial value, (none), indicates that the polygon element
    is valid, but does not render.
  </dd>
</dl>

Note: 
  A future specification may convert the {{points}} attribute to a geometric property.
  Currently, it can only be specified via an element attribute, and not CSS.


<p>Mathematically, a {{polygon}} element can be mapped to an
equivalent {{path}} element as follows:

<ul>
  <li>perform an absolute <a href="paths.html#PathDataMovetoCommands">moveto</a>
  operation to the first coordinate pair in the list of points</li>

  <li>for each subsequent coordinate pair, perform an absolute
  <a href="paths.html#PathDataLinetoCommands">lineto</a> operation to that
  coordinate pair</li>

  <li>perform a <a href="paths.html#PathDataClosePathCommand">closepath</a>
  command</li>
</ul>

<p id="ExamplePolygon01"><span class="example-ref">Example
polygon01</span> below specifies two polygons (a star and a hexagon) in
the user coordinate system established by the [[#ViewBoxAttribute|viewBox]] attribute
on the <{svg}> element.

<pre class=include-raw>
path: images/shapes/polygon01.svg
</pre>
<!--
@@fix 
<pre class=include>
path: images/shapes/polygon01.svg
</pre>
-->


<div class='ready-for-wider-review'>
<h3 id="DOMInterfaces">DOM interfaces</h3>

<h4 id="InterfaceSVGRectElement">Interface SVGRectElement</h4>


<p>An [[#InterfaceSVGRectElement|SVGRectElement]] object represents a <{rect}> element in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGRectElement</b> : <a>SVGGeometryElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGRectElement__x">x</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGRectElement__y">y</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGRectElement__width">width</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGRectElement__height">height</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGRectElement__rx">rx</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGRectElement__ry">ry</a>;
};
</pre>

<p>The
<b id="__svg__SVGRectElement__x">x</b>,
<b id="__svg__SVGRectElement__y">y</b>,
<b id="__svg__SVGRectElement__width">width</b>,
<b id="__svg__SVGRectElement__height">height</b>,
<b id="__svg__SVGRectElement__rx">rx</b> and
<b id="__svg__SVGRectElement__ry">ry</b> IDL attributes
[=reflect=] the computed values of the {{x}}, {{y}},
{{width}}, {{height}}, {{rx}} and {{ry}}
properties and their corresponding presentation attributes,
respectively.



<h4 id="InterfaceSVGCircleElement">Interface SVGCircleElement</h4>


<p>An [[#InterfaceSVGCircleElement|SVGCircleElement]] object represents a {{circle}} element in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGCircleElement</b> : <a>SVGGeometryElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGCircleElement__cx">cx</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGCircleElement__cy">cy</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGCircleElement__r">r</a>;
};
</pre>

<p>The
<b id="__svg__SVGCircleElement__cx">cx</b>,
<b id="__svg__SVGCircleElement__cy">cy</b> and
<b id="__svg__SVGCircleElement__r">r</b> IDL attributes
[=reflect=] the computed values of the {{cx}}, {{cy}}
and {{y}} properties and their corresponding presentation attributes,
respectively.



<h4 id="InterfaceSVGEllipseElement">Interface SVGEllipseElement</h4>


<p>An [[#InterfaceSVGEllipseElement|SVGEllipseElement]] object represents a {{ellipse}} element in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGEllipseElement</b> : <a>SVGGeometryElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGEllipseElement__cx">cx</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGEllipseElement__cy">cy</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGEllipseElement__rx">rx</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGEllipseElement__ry">ry</a>;
};
</pre>

<p>The
<b id="__svg__SVGEllipseElement__cx">cx</b>,
<b id="__svg__SVGEllipseElement__cy">cy</b>,
<b id="__svg__SVGEllipseElement__rx">rx</b> and
<b id="__svg__SVGEllipseElement__ry">ry</b>
IDL attributes [=reflect=] the computed values of the
{{cx}}, {{cy}}, {{rx}} and {{ry}} properties
and their corresponding presentation attributes,
respectively.


<h4 id="InterfaceSVGLineElement">Interface SVGLineElement</h4>


The [[#InterfaceSVGLineElement|SVGLineElement]] interface corresponds to the {{line}}
element.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGLineElement</b> : <a>SVGGeometryElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGLineElement__x1">x1</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGLineElement__y1">y1</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGLineElement__x2">x2</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedLength</a> <a href="shapes.html#__svg__SVGLineElement__y2">y2</a>;
};
</pre>

<p>The
<b id="__svg__SVGLineElement__x1">x1</b>,
<b id="__svg__SVGLineElement__y1">y1</b>,
<b id="__svg__SVGLineElement__x2">x2</b> and
<b id="__svg__SVGLineElement__y2">y2</b> IDL attributes
[=reflect=] the {{x1}}, {{y1}}, {{x2}} and {{y2}}
content attributes, respectively


<h4 id="InterfaceSVGAnimatedPoints" data-dfn-type="interface" data-lt="SVGAnimatedPoints">Mixin SVGAnimatedPoints</h4>

<p>The [[#InterfaceSVGAnimatedPoints|SVGAnimatedPoints]] interface is used to [=reflect=]
a <{polygon/points}> attribute on a {{polygon}} or {{polyline}}
element.  It is mixed in to the [[#InterfaceSVGPolygonElement|SVGPolygonElement]] and [[#InterfaceSVGPolylineElement|SVGPolylineElement]]
interfaces.

<pre class="idl">
interface mixin <b>SVGAnimatedPoints</b> {
  [<a>SameObject</a>] readonly attribute <a>SVGPointList</a> <a href="shapes.html#__svg__SVGAnimatedPoints__points">points</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGPointList</a> <a href="shapes.html#__svg__SVGAnimatedPoints__animatedPoints">animatedPoints</a>;
};
</pre>


<p class='ready-for-wider-review'>The <b id="__svg__SVGAnimatedPoints__points">points</b> IDL attribute
represents the current non-animated value of the reflected attribute.
On getting <a href="#__svg__SVGAnimatedPoints__points">points</a>,
an [[#InterfaceSVGPointList|SVGPointList]] object is returned that reflects the base
value of the reflected attribute.

<p>The <b id="__svg__SVGAnimatedPoints__animatedPoints">animatedPoints</b> IDL attribute
represents the current non-animated value of the reflected attribute.
On getting <a href="#__svg__SVGAnimatedPoints__animatedPoints">animatedPoints</a>,
an [[#InterfaceSVGPointList|SVGPointList]] object is returned that reflects the animated
value of the reflected attribute.

<p>The objects returned from <a href="#__svg__SVGAnimatedPoints__points">points</a>
and <a href="#__svg__SVGAnimatedPoints__animatedPoints">animatedPoints</a> must be distinct, even
if there is no animation currently affecting the attribute.

<h4 id="InterfaceSVGPointList">Interface SVGPointList</h4>

<p>The [[#InterfaceSVGPointList|SVGPointList]] interface is a [=list interface=] whose
elements are {{DOMPoint}} objects.  An [[#InterfaceSVGPointList|SVGPointList]]
object represents a list of points.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGPointList</b> {

  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__length">length</a>;
  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__numberOfItems">numberOfItems</a>;

  undefined <a href="types.html#__svg__SVGNameList__clear">clear</a>();
  <a>DOMPoint</a> <a href="types.html#__svg__SVGNameList__initialize">initialize</a>(<a>DOMPoint</a> newItem);
  getter <a>DOMPoint</a> <a href="types.html#__svg__SVGNameList__getItem">getItem</a>(unsigned long index);
  <a>DOMPoint</a> <a href="types.html#__svg__SVGNameList__insertItemBefore">insertItemBefore</a>(<a>DOMPoint</a> newItem, unsigned long index);
  <a>DOMPoint</a> <a href="types.html#__svg__SVGNameList__replaceItem">replaceItem</a>(<a>DOMPoint</a> newItem, unsigned long index);
  <a>DOMPoint</a> <a href="types.html#__svg__SVGNameList__removeItem">removeItem</a>(unsigned long index);
  <a>DOMPoint</a> <a href="types.html#__svg__SVGNameList__appendItem">appendItem</a>(<a>DOMPoint</a> newItem);
  <a href="types.html#__svg__SVGNameList__setter">setter</a> undefined (unsigned long index, <a>DOMPoint</a> newItem);
};
</pre>

<p>The behavior of all of the interface members of [[#InterfaceSVGPointList|SVGPointList]] are
defined in <a href="types.html#ListInterfaces">List interfaces</a>.

<p>This specification imposes additional requirements on the behaviour of {{DOMPoint}}
objects beyond those described in the
<a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/">Geometry Interfaces</a>
specification, so that they can be used to reflect <{polygon/points}> attributes.

<p id="PointMode">Every {{DOMPoint}} object operates in one of four modes. It
can:

<div class='ready-for-wg-review'>
<ol>
  <li><em>reflect an element of the base value</em> of a [=reflected=] animatable
  attribute (being exposed through the methods on the
  <a href="#__svg__SVGAnimatedPoints__points">points</a> member of
  an [[#InterfaceSVGAnimatedPoints|SVGAnimatedPoints]]),</li>
  <li><em>reflect an element of the animated value</em> of a [=reflected=] animatable
  attribute (being exposed through the methods on the
  <a href="#__svg__SVGAnimatedPoints__animatedPoints">animatedPoints</a> member of
  an [[#InterfaceSVGAnimatedPoints|SVGAnimatedPoints]]),</li>
  <li><em>represent the current translation</em> of a given <{svg}> element
  (being exposed through the
  <a href="struct.html#__svg__SVGSVGElement__currentTranslate">currentTranslate</a>
  member on [[#InterfaceSVGSVGElement|SVGSVGElement]]), or</li>
  <li><em>be detached</em>, which is the case for {{DOMPoint}} objects created
  using their constructor or with
  <a href='struct.html#__svg__SVGSVGElement__createSVGPoint'>createSVGPoint</a>.</li>
</ol>
</div>

<p id="PointAssociatedElement">A {{DOMPoint}} object can be <em>associated</em>
with a particular element.  The associated element is used to
determine which element's content attribute to update if the object [=reflects=]
an attribute.  Unless otherwise described, a {{DOMPoint}} object is not
associated with any element.

<p id="ReadOnlyPoint">A {{DOMPoint}} object can be designated as <em>read only</em>,
which means that attempts to modify the object will result in an exception
being thrown.  When assigning to a read only {{DOMPoint}}'s
<a href='https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-dompointreadonly-dompoint-x'>x</a>,
<a href='https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-dompointreadonly-dompoint-y'>y</a>,
<a href='https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-dompointreadonly-dompoint-w'>w</a> or
<a href='https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-dompointreadonly-dompoint-z'>z</a>
IDL attribute, a [=NoModificationAllowedError=] must be
[=thrown=] instead of updating the internal coordinate value.

<p class='note'>Note that this applies only to the read-write {{DOMPoint}}
interface; the [=DOMPointReadOnly=] interface, which is not used for reflecting
the <{polygon/points}> attribute, will already throw an exception if
an attempt is made to modify it.

<p id="AssignToDOMPoint">When assigning to a writable {{DOMPoint}}'s
<a href='https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-dompointreadonly-dompoint-x'>x</a>,
<a href='https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-dompointreadonly-dompoint-y'>y</a>,
<a href='https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-dompointreadonly-dompoint-w'>w</a> or
<a href='https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-dompointreadonly-dompoint-z'>z</a>
IDL attribute, the following steps are run after updating
the internal coordinate value:

<ol class='algorithm'>
  <li>If the {{DOMPoint}} <a href='#PointMode'>reflects an element of the
  base value</a> of a [=reflected=] attribute, then [=reserialize=]
  the reflected attribute using the [[#InterfaceSVGPointList|SVGPointList]] that reflects
  the attribute's base value.
  </li>
  <li>Otherwise, if the {{DOMPoint}} <a href='#PointMode'>represents
  the current translation</a> of an <{svg}> element and that
  element is the [=outermost svg element=], then:
    <ol>
      <li>Let [<var>a</var> <var>b</var> <var>c</var> <var>d</var> <var>e</var> <var>f</var>]
      be the 2x3 matrix that represents the document's magnification and panning
      transform.</li>
      <li>Let <var>x</var> and <var>y</var> be the x and y coordinates of the
      {{DOMPoint}} object, respectively.</li>
      <li>Set the document's magnification and panning transform to
      [<var>a</var> 0 0 <var>d</var> <var>x</var> <var>y</var>].</li>
    </ol>
  </li>
</ol>


<h4 id="InterfaceSVGPolylineElement">Interface SVGPolylineElement</h4>


<p>An [[#InterfaceSVGPolylineElement|SVGPolylineElement]] object represents a {{polyline}} element in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGPolylineElement</b> : <a>SVGGeometryElement</a> {
};

<a>SVGPolylineElement</a> includes <a>SVGAnimatedPoints</a>;
</pre>



<h4 id="InterfaceSVGPolygonElement">Interface SVGPolygonElement</h4>


<p>An [[#InterfaceSVGPolygonElement|SVGPolygonElement]] object represents a {{polygon}} element in the DOM.

<pre class="idl">
[<a>Exposed</a>=Window]
interface <b>SVGPolygonElement</b> : <a>SVGGeometryElement</a> {
};

<a>SVGPolygonElement</a> includes <a>SVGAnimatedPoints</a>;
</pre>

</div>
