<h2>Geometry Properties</h2>

<p>Beside SVG's styling properties, SVG also defines
<dfn id='geometry-properties' data-dfn-type="dfn" data-export="">geometry properties</dfn>. Geometry properties
describe the position and dimension of the [=graphics element=]s {{circle}},
{{ellipse}}, <{rect}>, {{image}}, <{foreignObject}> and the
<{svg}> element.

<h3 id='CX'>Horizontal center coordinate: The <span class="property">cx</span> property</h3>
<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="CxProperty" data-dfn-type="property" data-export="">cx</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>0</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>{{circle}} and {{ellipse}} elements
    </td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>no</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the width of the current SVG viewport (see
    <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The {{cx}} property describes the horizontal center coordinate
of the position of the element.

<h3 id='CY'>Vertical center coordinate: The <span class="property">cy</span> property</h3>
<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="CyProperty" data-dfn-type="property" data-export="">cy</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>0</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>{{circle}} and {{ellipse}} elements
    </td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>no</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the height of the current SVG viewport (see
    <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The {{cy}} property describes the vertical center coordinate
of the position of the element. 

<h3 id='R'>Radius: The <span class="property">r</span> property</h3>
<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="RProperty" data-dfn-type="property" data-export="">r</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>0</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>{{circle}} element</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>no</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the normalized diagonal of the current SVG viewport (see
    <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The {{r}} property describes the radius of the {{circle}}
element.

<p>A negative value for {{r}} is [=invalid=] and must be [=ignored=].

<h3 id='RX'>Horizontal radius: The <span class="property">rx</span> property</h3>
<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="RxProperty" data-dfn-type="property" data-export="">rx</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>> | auto</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>auto</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>{{ellipse}}, <{rect}> elements</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>no</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the width of the current SVG viewport (see
    <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The {{rx}} property describes the horizontal radius of the
{{ellipse}} element and the curve radius of the <{rect}>
element.
    When the computed value of <span class="property">rx</span>
 is <span class="prop-value">auto</span>, the used radius is equal to the absolute length used for {{ry}}, creating a circular arc.
    If both <span class="property">rx</span>
 and <span class="property">ry</span>
 have a computed value of <span class="prop-value">auto</span>, the used value is 0.

<p> Regardless of how the value is calculated, the used value of <span class="property">rx</span>
 for a <{rect}> is never more than 50% of the used value of {{width}} for the same shape.


Note: 
    The <span class="prop-value">auto</span> behavior is new in SVG 2 for {{ellipse}},
    matching the behavior for <{rect}> elements when {{rx}} was not specified.


<p>A negative value for {{rx}} is [=invalid=] and must be [=ignored=].

<h3 id='RY'>Vertical radius: The <span class="property">ry</span> property</h3>
<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="RyProperty" data-dfn-type="property" data-export="">ry</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>> | auto</td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>auto</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td>{{ellipse}}, <{rect}></td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>no</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the height of the current SVG viewport (see
    <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage</td>
  </tr>
  <tr>
    <th>Animatable type:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The {{ry}} property describes the vertical radius of the
{{ellipse}} element and the vertical curve radius of the <{rect}>
    element.
    When the computed value of <span class="property">ry</span>
 is <span class="prop-value">auto</span>, the used radius is equal to the absolute length used for {{rx}}, creating a circular arc.
    If both <span class="property">rx</span>
 and <span class="property">ry</span>
 have a computed value of <span class="prop-value">auto</span>, the used value is 0.

<p> Regardless of how the value is calculated, the used value of <span class="property">ry</span>
 for a <{rect}> is never more than 50% of the used value of {{height}} for the same shape.


Note: 
    The <span class="prop-value">auto</span> behavior is new in SVG 2 for {{ellipse}},
    matching the behavior for <{rect}> elements when {{ry}} was not specified.


<p>A negative value for {{ry}} is [=invalid=] and must be [=ignored=].

<h3 id='X'>Horizontal coordinate: The <span class="property">x</span> property</h3>
<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="XProperty" data-dfn-type="property" data-export="">x</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>0</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td><{svg}>, <{rect}>,
    {{image}}, <{foreignObject}> elements</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>no</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the width of the current SVG viewport (see
    <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The {{x}} property describes the horizontal coordinate of
the position of the element.

<h3 id='Y'>Vertical coordinate: The <span class="property">y</span> property</h3>
<table class="propdef def">
  <tr>
    <th>Name:</th>
    <td><dfn id="YProperty" data-dfn-type="property" data-export="">y</dfn></td>
  </tr>
  <tr>
    <th>Value:</th>
    <td><<length-percentage>></td>
  </tr>
  <tr>
    <th>Initial:</th>
    <td>0</td>
  </tr>
  <tr>
    <th>Applies to:</th>
    <td><{svg}>, <{rect}>,
    {{image}}, <{foreignObject}> elements</td>
  </tr>
  <tr>
    <th>Inherited:</th>
    <td>no</td>
  </tr>
  <tr>
    <th>Percentages:</th>
    <td>refer to the height of the current SVG viewport (see
    <a href="coords.html#Units">Units</a>)</td>
  </tr>
  <tr>
    <th>Media:</th>
    <td>visual</td>
  </tr>
  <tr>
    <th>Computed value:</th>
    <td>an absolute length or percentage</td>
  </tr>
  <tr>
    <th>[=Animation type=]:</th>
    <td>by computed value</td>
  </tr>
</table>

<p>The {{y}} property describes the vertical coordinate of
the position of the element.

<h3 id="Sizing">Sizing properties: the effect of the <span class="property">width</span> and <span class="property">height</span> properties</h3>

<p class='note'>See the CSS 2.1 specification for the definitions of
<a href="https://www.w3.org/TR/CSS21/visudet.html#propdef-width"><span class="prop-name">width</span></a> and
<a href="https://www.w3.org/TR/CSS21/visudet.html#propdef-height"><span class="prop-name">height</span></a>.

<p>The CSS {{width}} and {{height}} properties are used for
sizing some SVG elements.  Specifically, they are used to size
<{rect}>, <{svg}>, {{image}} and
<{foreignObject}>.  All of these elements have <span class="attr-name">width</span>
and <span class="attr-name">height</span> presentation attributes.
The properties are also used for laying out embedded elements from the HTML namespace.


<p>The used value of {{width}}
may be constrained by the value of the
<a href="https://www.w3.org/TR/CSS21/visudet.html#propdef-max-width"><span class="prop-name">max-width</span></a> and
<a href="https://www.w3.org/TR/CSS21/visudet.html#propdef-max-width"><span class="prop-name">min-width</span></a> properties.
The used value of {{height}}
may be constrained by the value of the
<a href="https://www.w3.org/TR/CSS21/visudet.html#propdef-max-height"><span class="prop-name">max-height</span></a> and
<a href="https://www.w3.org/TR/CSS21/visudet.html#propdef-max-height"><span class="prop-name">min-height</span></a> properties.


<p>The value <span class='prop-value'>auto</span> for {{width}}
and {{height}} on the <{svg}> element is treated as 100%.

<p>The value <span class='prop-value'>auto</span> for {{width}}
and {{height}} on the {{image}} element is calculated from the referenced image's intrinsic dimensions and aspect ratio, according to the CSS [=Default Sizing Algorithm=].

<p>Content dependent units used in 'width' and 'height' for inner SVG elements resolve to SVG's definition of <a><span class='prop-value'>auto</span></a>. These content dependent units include 
<a href="https://drafts.csswg.org/css-sizing-3/#valdef-width-min-content">min-content</a>, <a href="https://drafts.csswg.org/css-sizing-3/#valdef-width-max-content">max-content</a>, 
<a href="https://drafts.csswg.org/css-sizing-3/#funcdef-width-fit-content">fit-content()</a> and <a href="https://drafts.csswg.org/css-sizing-3/#funcdef-width-calc-size">calc-size()</a>.

Note: 
    New in SVG 2.  Images embedded in SVG can now be auto-sized to the intrinsic size, or scaled to a fixed height or width according to the intrinsic aspect ratio.  This matches the behavior of embedded images in HTML.


<p>The value <span class='prop-value'>auto</span> for {{width}}
and {{height}} on other elements is treated as 0.

<p class='note'>This means that, for example, a <{foreignObject}>
object element will not shrink-wrap to its contents if
<span class='prop-value'>auto</span> is used.
