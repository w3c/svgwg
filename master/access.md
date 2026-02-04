<h2 id="accessibility">Appendix C: Accessibility Support</h2>

<p class="normativity"><em>This appendix is informative, not normative.</em>

<h3 id="AccessibilityAndSVG">SVG Accessibility Features</h3>

<p>This appendix highlights the accessibility features of SVG and accessibility related specifications used to support SVG and the associated <a href="https://www.w3.org/TR/WCAG21/"><cite>W3C Web Content Accessibility Guidelines (WCAG) 2.0 &bs[;WCAG2]</cite></a> requirements they are designed to support.
<dl>
 <dt><span class="gl"><a href="https://www.w3.org/TR/WCAG21/#content-structure-separation">&bs[;WCAG2] Create content that can be presented in different ways (for example simpler layout) without losing information or structure: Information and Relationships.</a></span></dt>
  <dd>
    <ul>
      <li>Support for <a href="https://www.w3.org/TR/wai-aria-1.1/#aria-labelledby">aria-labelledby</a> for label relationships.</li>
      <li>Support for <a href="https://www.w3.org/TR/wai-aria-1.1/#aria-describedby">aria-describedby</a> for description relationships.</li>
      <li>Support for <a href="https://www.w3.org/TR/wai-aria-1.1/#aria-owns">aria-owns</a> for structural relationships. </li>
      <li>Support for <a href="https://www.w3.org/TR/wai-aria-1.1/#aria-controls">aria-controls</a> for control relationships where an element controls the content and or behavior of another element. </li>
      <li>The <{g}> for defined groupings.</li>
      <li>Support for the WAI-ARIA <a href="https://www.w3.org/TR/wai-aria-1.1/#group">group</a> and <a href="https://www.w3.org/TR/wai-aria-1.1/#radiogroup">radiogroup</a> roles.</li>
    </ul>
  </dd>
</dl>
<dl>
 <dt><span class="gl"><a href="https://www.w3.org/TR/WCAG21/#keyboard-operation">&bs[;WCAG2] Keyboard Accessible: Make all functionality available from the keyboard.</a></span></dt>
  <dd>
    <ul>
      <li><a href="interact.html#Focus">Focus support</a> and the <a element-attr for="core-attributes">tabindex</a> attribute for sequential focus navigation aligned with HTML </li>

      <li><a href="interact.html#EventAttributes">Keyboard Event attribute support along with Mouse Event support</a>
 for script authors
      </li>
      <li><a href="interact.html#SVGEvents">Keyboard Events</a> for script authors
      </li>
      <li>Script support for setting focus on each <a href="types.html#InterfaceSVGElement">SVG Element</a> in the DOM</li>
      <li>Script support for acquiring the <a element-attr for="core-attributes">tabindex</a> attribute
on each <a href="types.html#InterfaceSVGElement">SVG Element</a> in the DOM</li>
      <li>Script support for the HTML activeElement property in the <a href="struct.html#InterfaceDocumentExtensions">Document interface</a></li>
    </ul>
  </dd>
</dl>
<dl>
 <dt><span class="gl"><a href="https://www.w3.org/TR/WCAG21/#navigation-mechanisms">&bs[;WCAG2] Navigable: Provide ways to help users navigate, find content, and determine where they are. </a></span></dt>
  <dd>
    <ul>
      <li>To enable bypassing of blocks of content SVG supports the: WAI-ARIA <a href="https://www.w3.org/TR/wai-aria-1.1/#landmark_roles">landmark</a> roles.</li>
      <li>Supports <{title}> to provide page titles.</li>
      <li>Supports <a element-attr for="core-attributes">tabindex</a> to provide a sequential focus navigation order.</li>
      <li>Supports the <a element spec="svg2">a</a> element, enabling authors to supply the link purpose both from its content.</li>
      <li>Supports headings and labels through the use of the <a href="https://www.w3.org/TR/wai-aria-1.1/#heading">heading</a> role with <a href="https://www.w3.org/TR/wai-aria-1.1/#aria-level">aria-level</a>, <a href="https://www.w3.org/TR/wai-aria-1.1/#aria-labelledby">aria-labelledby</a> and <a href="https://www.w3.org/TR/wai-aria-1.1/#aria-label">aria-label</a>.</li>
      <li>Support visible focus by rendering visible focus on focused elements in the tab order.</li>
    </ul>
  </dd>
</dl>
<dl>
 <dt><span class="gl"><a href="https://www.w3.org/TR/WCAG21/#meaning">&bs[;WCAG2] Readable: Make text content readable and understandable.</a></span></dt>
  <dd>
    <ul>
      <li>Supports the language of the page as well as its parts through the {{lang}} attribute.</li>
    </ul>
  </dd>
</dl>
<dl>
 <dt><span class="gl"><a href="https://www.w3.org/TR/WCAG21/#ensure-compat">&bs[;WCAG2] Compatible: Maximize compatibility with current and future user agents, including assistive technologies.
</a></span></dt>
  <dd>
    <ul>
      <li>Supports Name, Role, and Value through the use of <a href="struct.html#WAIARIAAttributes">WAI-ARIA attributes</a> and the <{title}> element.</li>
    </ul>
  </dd>
</dl>
<dl>
  <dt><span class="gl">WAI-ARIA Support and text alternatives</span></dt>
  <dd>
    <ul>
      <li><a href="struct.html#WAIARIAAttributes">WAI-ARIA attributes</a></li>
      <li><a href="struct.html#DescriptionAndTitleElements">Desc and Title text element alternatives</a></li>
    </ul>
  </dd>
</dl>

<h3 id="SVGRelatedAccessibilityDocuments">Supporting SVG Accessibility Specifications and Guidelines</h3>

<p>This section enumerates the SVG accessibility-related specifications and authoring guidelines.


<dl>
  <dt><span class="gl">Related SVG Accessibility Specifications for User Agents</span></dt>
  <dd>
    <ul>
      <li>The <a href="https://www.w3.org/TR/svg-aam-1.0/"><cite>SVG Accessibility API Mappings &bs[;SVG-AAM]</cite></a> specification.</li>
      <li>The <a href="https://www.w3.org/TR/core-aam-1.1/"><cite>Core Accessibility API Mappings 1.1 &bs[;SVG-AAM]</cite></a>specification.</li>
      <li>The <a href="https://www.w3.org/TR/accname-aam-1.1/"><cite>Accessible Name and Description: Computation and API Mappings 1.1 &bs[;ACCNAME-AAM]</cite></a> specification.
      </li>
    </ul>
  </dd>

  <dt><span class="gl">Related Specifications for Content Authors</span></dt>
  <dd>
    <ul>
      <li><a href="https://www.w3.org/TR/wai-aria-1.1/"><cite>WAI-ARIA 1.1 &bs[;WAI-ARIA]</cite></a></li>
      <li><a href="https://www.w3.org/TR/WCAG21/"><cite>W3C Web Content Accessibility Guidelines (WCAG) 2.0 &bs[;WCAG2]</cite></a></li>
    </ul>
  </dd>

</dl>
