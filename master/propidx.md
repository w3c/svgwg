<h2>Property Index</h2>

<p class="normativity"><em>This appendix is informative, not normative.</em>

<!-- It would be great if this table were automatically generated, too. -->

    <table class='proptable'>
      <thead>
        <tr>
          <th>Name</th>
          <th>Values</th>
          <th>Initial value</th>
          <th>Applies to</th>
          <th title='Inherited'>Inh.</th>
          <th>Percentages</th>
          <th>Media</th>
          <th>[=Animation type=]</th>
          <th>Computed value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>{{color-interpolation}}</th>
          <td>auto | sRGB | linearRGB </td>
          <td>sRGB</td>
          <td>[=container elements=], [=graphics elements=], [=gradient elements=], <{use}> and <{animate}></td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{cx}}</th>
          <td><<length-percentage>></td>
          <td>0</td>
          <td>{{circle}} and {{ellipse}} elements</td>
          <td>no</td>
          <td>refer to the width of the current SVG viewport (see
              <a href="coords.html#Units">Units</a>)</td>
          <td>by computed value</td>
          <td>an absolute length or percentage</td>
        </tr>
        <tr>
          <th>{{cy}}</th>
          <td><<length-percentage>></td>
          <td>0</td>
          <td>{{circle}} and {{ellipse}} elements</td>
          <td>no</td>
          <td>refer to the height of the current SVG viewport (see
              <a href="coords.html#Units">Units</a>)</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>an absolute length or percentage</td>
        </tr>
        <tr>
          <th>{{fill}}</th>
          <td>&lt;paint&gt; (See <a href="painting.html#SpecifyingPaint">Specifying
          paint</a>)</td>
          <td>black</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>as specified, but with [=&lt;color>=] values computed and [=&lt;url>=] values made absolute</td>
        </tr>
        <tr>
          <th>'fill-opacity'</th>
          <td>&lt;‘{{opacity}}’&gt;</td>
          <td>1</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>the specified value converted to a number, clamped to the range [0,1]</td>
        </tr>
        <tr>
          <th>'fill-rule'</th>
          <td>nonzero | evenodd </td>
          <td>nonzero</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>[[SVG2#ImageRendering|image-rendering]]</th>
          <td>auto | optimizeSpeed | optimizeQuality </td>
          <td>auto</td>
          <td>images</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{marker property}}</th>
          <td>see individual properties</td>
          <td>see individual properties</td>
          <td>[=shapes=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>see individual properties</td>
        </tr>
        <tr>
          <th>{{marker-end}}<br />
           {{marker-mid}}<br />
           {{marker-start}}</th>
          <td>none | <a>&lt;url&gt;</a></td>
          <td>none</td>
          <td>[=shapes=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified, but with [=&lt;url>=] values (that are part of a [=&lt;marker-ref>=]) made absolute</td>
        </tr>
        <tr class="ready-for-wider-review">
          <th>[=paint-order=]</th>
          <td>normal | [ fill || stroke || markers ] </td>
          <td>normal</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{pointer-events}}</th>
          <td>auto | bounding-box | visiblePainted | visibleFill | visibleStroke |
          visible |<br />
           painted | fill | stroke | all | none </td>
          <td>auto</td>
          <td>[=container elements=], [=graphics elements=] and <{use}></td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{r}}</th>
          <td><<length-percentage>></td>
          <td>0</td>
          <td>{{circle}} element</td>
          <td>no</td>
          <td>refer to the normalized diagonal of the current SVG viewport (see
              <a href="coords.html#Units">Units</a>)</td>
          <td>by computed value</td>
          <td>an absolute length or percentage</td>
        </tr>
        <tr>
          <th>{{rx}}</th>
          <td><<length-percentage>> | auto</td>
          <td>auto</td>
          <td>{{ellipse}}, <{rect}> elements</td>
          <td>no</td>
          <td>refer to the width of the current SVG viewport (see
              <a href="coords.html#Units">Units</a>)</td>
          <td>by computed value</td>
          <td>an absolute length or percentage</td>
        </tr>
        <tr>
          <th>{{ry}}</th>
          <td><<length-percentage>> | auto</td>
          <td>auto</td>
          <td>{{ellipse}}, <{rect}> elements</td>
          <td>no</td>
          <td>refer to the height of the current SVG viewport (see
              <a href="coords.html#Units">Units</a>)</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>an absolute length or percentage</td>
        </tr>
        <tr>
          <th>{{shape-rendering}}</th>
          <td>auto | optimizeSpeed | crispEdges |<br />
           geometricPrecision </td>
          <td>auto</td>
          <td>[=shapes=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{stop-color}}</th>
          <td>&lt;‘{{color}}’&gt;</td>
          <td>black</td>
          <td>{{stop}} elements</td>
          <td>no</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td></td>
        </tr>
        <tr>
          <th>'stop-opacity'</th>
          <td>&lt;‘{{opacity}}’&gt;</td>
          <td>1</td>
          <td>{{stop}} elements</td>
          <td>no</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>the specified value converted to a number, clamped to the range [0,1]</td>
        </tr>
        <tr>
          <th>{{stroke}}</th>
          <td>&lt;paint&gt; (See <a href="painting.html#SpecifyingPaint">Specifying
          paint</a>)</td>
          <td>none</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>as specified, but with [=&lt;color>=] values computed and [=&lt;url>=] values made absolute</td>
        </tr>
        <tr>
          <th>{{stroke-dasharray}}</th>
          <td>none | &lt;dasharray&gt; </td>
          <td>none</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>refer to the normalized diagonal of the current SVG viewport</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>See prose</td>
          <td>as comma separated list of absolute lengths or percentages, numbers converted to absolute lengths first, or keyword specified</td>
        </tr>
        <tr>
          <th>{{stroke-dashoffset}}</th>
          <td><<length-percentage>> | <<number>></td>
          <td>0</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>refer to the normalized diagonal of the current SVG viewport</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>as absolute length or percentage; numbers converted to absolute length first</td>
        </tr>
        <tr>
          <th>{{stroke-linecap}}</th>
          <td>butt | round | square </td>
          <td>butt</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{stroke-linejoin}}</th>
          <td>miter | round | bevel </td>
          <td>miter</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{stroke-miterlimit}}</th>
          <td><<number>> (non-negative)</td>
          <td>4</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>'stroke-opacity'</th>
          <td>&lt;‘{{opacity}}’&gt;</td>
          <td>1</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>the specified value converted to a number, clamped to the range [0,1]</td>
        </tr>
        <tr>
          <th>{{stroke-width}}</th>
          <td><<length-percentage>> | <<number>></td>
          <td>1px</td>
          <td>[=shapes=] and [=text content elements=]</td>
          <td>yes</td>
          <td>refer to the normalized diagonal of the current SVG viewport</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>as absolute length or percentage; numbers converted to absolute length first</td>
        </tr>
        <tr>
          <th>{{text-anchor}}</th>
          <td>start | middle | end </td>
          <td>start</td>
          <td>[=text content elements=]</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{text-rendering}}</th>
          <td>auto | optimizeSpeed | optimizeLegibility |<br />
           geometricPrecision </td>
          <td>auto</td>
          <td>{{text}} elements</td>
          <td>yes</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{vector-effect}}</th>
          <td>non-scaling-stroke | none</td>
          <td>none</td>
          <td>[=graphics elements=] and <{use}></td>
          <td>no</td>
          <td>N/A</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>discrete</td>
          <td>as specified</td>
        </tr>
        <tr>
          <th>{{x}}</th>
          <td><<length-percentage>></td>
          <td>0</td>
          <td><{svg}>, <{rect}>,
            {{image}}, <{foreignObject}> elements</td>
          <td>no</td>
          <td>refer to the width of the current SVG viewport (see
              <a href="coords.html#Units">Units</a>)</td>
          <td>by computed value</td>
          <td>an absolute length or percentage</td>
        </tr>
        <tr>
          <th>{{y}}</th>
          <td><<length-percentage>></td>
          <td>0</td>
          <td><{svg}>, <{rect}>,
            {{image}}, <{foreignObject}> elements</td>
          <td>no</td>
          <td>refer to the height of the current SVG viewport (see
              <a href="coords.html#Units">Units</a>)</td>
          <td><a href="https://www.w3.org/TR/2008/REC-CSS2-20080411/media.html#visual-media-group">visual</a></td>
          <td>by computed value</td>
          <td>an absolute length or percentage</td>
        </tr>
      </tbody>
    </table>

<ol class='notes'>
  <li id="note1"><sup>[1]</sup> The {{font property}}, {{font-size-adjust}} and {{stroke-dasharray}}
  properties are animatable but do not support additive animation.</li>
</ol>
