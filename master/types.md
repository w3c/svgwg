<h2>Basic Data Types and Interfaces</h2>

<h3 id="definitions">Definitions</h3>
<dl class="definitions">
  <dt><dfn id="TermInitialValue" data-dfn-type="dfn" data-export="">initial value</dfn></dt>
  <dd>
    <p>
      The initial value of an attribute or property is the value used when
      that attribute or property is not specified, or when it has an
      [=invalid value=].
      This value is to be used for the purposes of rendering, calculating
      <a href="https://svgwg.org/specs/animations/">animation values</a>,
      and when accessing the attribute or property via DOM interfaces.
    
  </dd>

  <dt><dfn id="TermInvalidValue" data-dfn-type="dfn" data-export="">invalid value</dfn></dt>
  <dd>An invalid value specified for a [=property=], either in a style sheet
  or a [=presentation attribute=], is one that is either not allowed according
  to the grammar defining the property's values, or is allowed by the grammar but
  subsequently disallowed in prose.  A CSS declaration with an invalid value is
  [=ignored=].</dd>

</dl>

<h3 id="syntax">Attribute syntax</h3>

<div class='ready-for-wider-review'>

<p>In this specification, attributes are defined with an attribute definition
table, which looks like this:

<table class="attrdef def">
  <tr>
    <th>Name</th>
    <th>Value</th>
    <th>Initial&nbsp;value</th>
    <th>Animatable</th>
  </tr>
  <tr>
    <td>@@exampleattr@@ (there was a dfn element for demo.)</td>
    <td>@@fix <a>length</a> | none</td>
    <td>none</td>
    <td>yes</td>
  </tr>
</table>

<p>In the Value column is a description of the attribute's syntax.  There are
six methods for describing an attribute's syntax:

<ol>
  <li>Using the <a href="https://www.w3.org/TR/css-values/#value-defs">CSS Value
  Definition Syntax</a> [<a href="refs.html#ref-css-values-3">css-values</a>].
  This is the notation used to define the syntax for most attributes in this
  specification and is the default.</li>

  <li>By reference to an
  <a href="https://www.w3.org/TR/REC-xml/#sec-notation">EBNF symbol</a> defined
  in this or another specification [[!xml]].
  For external definitions, this is indicated by <span class="syntax">&bs[;EBNF]</span>
  appearing in the Value column.</li>

  <li>By reference to an
  <a href="http://tools.ietf.org/html/std68">ABNF symbol</a> defined
  in another specification [<a href="refs.html#ref-rfc5234">rfc5234</a>].  This is
  indicated by <span class="syntax">&bs[;ABNF]</span> appearing in the Value
  column.</li>

  <li>As a URL as defined by the <a href="https://url.spec.whatwg.org/">URL
  Standard</a> [<a href="refs.html#ref-URL">URL</a>].  This is indicated by
  <span class="syntax">&bs[;URL]</span> appearing in the Value column.</li>

  <li>As a type as defined by the <a href="https://html.spec.whatwg.org/">HTML
  Standard</a> [[!HTML]].  This is indicated by
  <span class="syntax">&bs[;HTML]</span> appearing in the Value column.</li>

  <li>In prose, below the attribute definition table.  This is indicated by the
  text "(see below)" appearing in the Value column.</li>
</ol>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Consider relaxing case sensitivity of presentation attribute values.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/28-svg-irc#T16-40-11">We will make property values case insensitivity.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To align presentation attribute syntax parsing with parsing of the corresponding CSS property.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3276">ACTION-3276</a>)</td>
    </tr>
    <tr>
      <th>Status:</th>
      <td>Done</td>
    </tr>
  </table>
</div>

<p id="presentation-attribute-css-value">When a [=presentation attribute=]
defined using the CSS Value Definition Syntax is parsed, this is done as
follows:

<ol>
  <li>Let <var>value</var> be the value of the attribute.</li>
  <li>Let <var>grammar</var> be the grammar given in the attribute definition
  table's Value column.</li>
  <li>Replace all instances of <a>&lt;length&gt;</a> in <var>grammar</var> with
  [<a>&lt;length&gt;</a> | <a>&lt;number&gt;</a>].</li>
  <li>Replace all instances of <a>&lt;length-percentage&gt;</a> in <var>grammar</var> with
    [<a>&lt;length-percentage&gt;</a> | <a>&lt;number&gt;</a>].</li>
  <li>Replace all instances of <a>&lt;angle&gt;</a> in <var>grammar</var> with
  [<a>&lt;angle&gt;</a> | <a>&lt;number&gt;</a>].</li>
  <li>Return the result of
  <a href="http://dev.w3.org/csswg/css-syntax/#parse-grammar">parsing
  <var>value</var> with <var>grammar</var></a>.</li>
</ol>

Note: The insertion of the <a>&lt;number&gt;</a> symbols allows for
unitless length and angles to be used in presentation attribute while
disallowing them in corresponding property values.

Note: Note that all [=presentation attributes=], since they are
defined by reference to their corresponding CSS properties, are defined using
the CSS Value Definition Syntax.

<p id="attribute-css-value">When any other attribute defined using the CSS Value
Definition Syntax is parsed, this is done by
<a href="http://dev.w3.org/csswg/css-syntax/#parse-grammar">parsing the
attribute's value according to the grammar given in attribute definition
table</a>.

Note: Note that this allows CSS comments and escapes to be used
in such attributes.  For example, a value of <span class='attr-value'>'10\px/**/'</span>
would successfully parse as <span class='attr-value'>'10px'</span> in
the <span class="attr-name">x</span> presentation attribute of the {{rect}} element.

<p id="attribute-url">When an attribute defined as a URL is parsed, this is
done by invoking the
<a href="https://url.spec.whatwg.org/#concept-url-parser">URL parser</a> with
the attribute's value as <var>input</var> and the document's URL as
<var>base</var> [<a href="refs.html#ref-URL">URL</a>].

<p>The Initial value column gives the [=initial value=] for the attribute.
When an attribute fails to parse according to the specified CSS Value Definition Syntax,
ABNF or EBNF grammar, or if parsing according to the URL Standard
or by the prose describing how to parse the attribute indicates failure,
the attribute is assumed to have been specified as the given [=initial value=].

<div class="note">
  <p>The initial value of a [=presentation attribute=] is its
  corresponding property's initial value.  Since the use of an [=invalid value=]
  in a [=presentation attribute=] will be treated as if the initial value
  was specified, this value can override values that come from lower priority
  style sheet rules, such as those from the user agent style sheet.
  <p>For example, although the user agent style sheet sets the value of the
  {{overflow}} property to <span class="prop-value">hidden</span>
  for <{svg}> elements, specifying an invalid presentation attribute such
  as <span class='attr-value'>overflow="invalid"</span> will result
  in a rule setting {{overflow}} to <span class="prop-value">visible</span>,
  overriding the user agent style sheet value.
</div>

<p>The Animatable column indicates whether the attribute can be animated using
[=animation elements=] as defined in the <a
  href="https://svgwg.org/specs/animations/">SVG Animation</a> module.

</div>

<h4 id="Precision">Real number precision</h4>

<p>Unless stated otherwise, numeric values in SVG attributes and in
properties that are defined to have an effect on SVG elements must
support at least all finite single-precision values supported by the host
architecture.


<p>It is recommended that higher precision floating point
storage and computation be performed on operations such as
coordinate system transformations to provide the best
possible precision and to prevent round-off errors.

<p class="ready-for-wider-review">[=Conforming SVG Viewers=]
are required to perform numerical computation in accordance with their
conformance class, as described in <a href="conform.html">Conformance Criteria</a>.

<h4 id="RangeClamping">Clamping values which are restricted to a particular range</h4>

<p>Some numeric attribute and property values have restricted ranges.
Other values will be restricted by the capabilities of the device.
If not otherwise specified,
the user agent shall defer any out-of-range error checking until
as late as possible in the rendering process.
This is particularly important for device limitations,
as compound operations
might produce intermediate values which are out-of-range but
final values which are within range.

<h3 id="SVGDOMOverview">SVG DOM overview</h3>

<p>Conforming [=SVG viewers=] or [=SVG interpreters=]
that support [=script execution=]
must implement SVG DOM interfaces as defined throughout this specification,
with the specific requirements and dependencies listed in this section.


<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Improve the DOM.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/27-svg-irc#T18-35-49">We will generally improve the SVG DOM for SVG 2.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>Help authors use the SVG DOM by making it less Java-oriented.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3273">ACTION-3273</a>)</td>
    </tr>
    <tr>
      <th>Note:</th>
      <td>See <a href="http://www.w3.org/Graphics/SVG/WG/wiki/SVG_2_DOM">SVG 2 DOM</a> Wiki page.</td>
    </tr>
  </table>
</div>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Improve the SVG path DOM APIs.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/10/27-svg-irc#T18-23-23">We will improve the SVG path DOM APIs in SVG 2.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>Clean up SVGPathSegList interface, and possibly share an API with Canvas.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Cameron (no action)</td>
    </tr>
  </table>
</div>


<h4 id="SVGDOMDependencies">Dependencies for SVG DOM support</h4>

<p class="ready-for-wider-review">The SVG DOM is defined in terms of <a href="https://heycam.github.io/webidl/">Web IDL</a>
interfaces. All IDL fragments in this specification must be interpreted as
required for <a href="https://heycam.github.io/webidl/#dfn-conforming-set-of-idl-fragments">conforming IDL fragments</a>,
as described in the Web IDL specification. [<a href="refs.html#ref-webidl">WebIDL</a>]

<p>The SVG DOM builds upon a number of DOM specifications.  In particular:

<ul>
  <li>The SVG DOM requires full support for the DOM,
  as defined by the most recent <a href="https://dom.spec.whatwg.org/review-drafts/">Review Draft</a>
  of the DOM living standard at the time this specification was published,
  except for any features that have been removed or deprecated since.
  SVG software with DOM support should implement
  the <a href="https://dom.spec.whatwg.org/">latest DOM standard</a>
  wherever possible
  [<a href="refs.html#ref-dom">DOM</a>]</li>

  <li>The SVG DOM requires support for relevant aspects of
  <a href="https://www.w3.org/TR/uievents/">UI Events</a> and
  <a href="https://www.w3.org/TR/clipboard-apis/">Clipboard API and events</a>
  ([<a href="refs.html#ref-uievents">uievents</a>], [<a href="refs.html#ref-clipboard-apis">clipboard-apis</a>]).
  (For the specific features that are required, see
  <a href="interact.html#RelationshipWithUIEVENTS">Relationship with UI Events</a>.)</li>

  <li>The SVG DOM requires, at a minimum, complete
  support for all interfaces from
  <a href="https://www.w3.org/TR/DOM-Level-2-Style/">DOM Level 2 Style</a>
  ([<a href="refs.html#ref-dom-level-2-style">dom-level-2-style</a>])
  that have not been dropped in the
  <a href="https://drafts.csswg.org/cssom/">CSS Object Model (CSSOM)</a> specification.
  SVG software should implement the latest version of
  <a href="https://drafts.csswg.org/cssom/">CSS Object Model (CSSOM)</a>
  wherever possible
  ([<a href="refs.html#ref-cssom-1">cssom-1</a>])
  </li>

  <li>The SVG DOM requires complete support for
  <a href="http://www.w3.org/TR/2014/CR-geometry-1-20141125/">Geometry Interfaces Module Level 1</a>
  ([<a href="refs.html#ref-geometry-1">geometry-1</a>]).
  </li>
</ul>

<h4 id="SVGDOMNamingConventions">Naming conventions</h4>

<p>The SVG DOM follows similar naming conventions to HTML and DOM standards
([[!HTML]], [<a href="refs.html#ref-dom">DOM</a>]).

<p>All names are defined as one or more English words
concatenated together to form a single string. Property or
method names start with the initial keyword in lowercase, and
each subsequent word starts with a capital letter. For example,
a property that returns document meta information such as the
date the file was created might be named "fileDateCreated".

<p>Interface names defined in this specification nearly all start with "SVG".
Interfaces that represent the DOM [=Element=] object
for an SVG-namespaced element follow the format
<code>SVG<i>ElementName</i>Element</code>, where <code><i>ElementName</i></code>
is the element's tag name with the initial letter capitalized.
So [=SVGRadialGradientElement=] is the interface for an {{radialGradient}} element.


Note: 
An exception to this casing convention is [=SVGSVGElement=],
in which the entire tag name is capitalized.


<h4 id="ElementsInTheSVGDOM">Elements in the SVG DOM</h4>

<p>Any SVG software that is required to support the SVG DOM
must enhance the DOM elements created for [=SVG document fragments=]
as follows:


<ul>
<li>
<p>Every [=Element=] object that corresponds to a supported SVG element (that is,
an element with namespace URI "http://www.w3.org/2000/svg" and a
local name that is one of the elements defined in this specification
or another specification implemented by the software)
must also implement the DOM interface identified in the element definition.

</li>
<li>
  <p>
  Elements in the SVG namespace whose local name does not match an element
  defined in any specification supported by the software
  must nonetheless implement the [=SVGElement=] interface.
  
  </li>
</ul>


<p class="example">
In the {{rect}} @@to review@@ element,
the [=SVGRectElement=] interface is identified.  This means that every
[=Element=] object whose namespace URI is "http://www.w3.org/2000/svg"
and whose local name is "rect" must also implement [=SVGRectElement=].


<h4 id="ReflectingAttributes">Reflecting content attributes in the DOM</h4>

<p>Many SVG DOM properties (IDL attributes)
<dfn id="TermReflect" data-dfn-type="dfn">reflect</dfn> a content attribute or property
on the corresponding element,
meaning that content and IDL attributes represent the same underlying data.
For example,
the [=SVGAnimatedLength=] [=SVGRectElement::ry=] in an
[=SVGRectElement=]
reflects the {{ry}} presentation attribute on the associated {{rect}} element.


<p>The way this reflection is done depends on the type of the IDL attribute:
    <ul>
      <li>If the type of the reflecting IDL attribute is a
      <a href="http://heycam.github.io/webidl/#dfn-primitive-type">primitive type</a> (such as
      <b>long</b>, as used by <a href="https://html.spec.whatwg.org/multipage/interaction.html#dom-tabindex">tabIndex</a>
       on [=SVGElement=]) or <b>DOMString</b> (as used by
      <a href="styling.html#__svg__SVGStyleElement__title">title</a> on [=SVGStyleElement=]),
      then the rules for
      <a href="https://html.spec.whatwg.org/multipage/common-dom-interfaces.html#reflect">reflecting
      content attributes in IDL attributes</a> in HTML are used.</li>

      <li>If the type of the reflecting IDL attribute is an [=SVGAnimatedBoolean=],
      [=SVGAnimatedString=], [=SVGAnimatedEnumeration=], [=SVGAnimatedNumber=],
      [=SVGAnimatedNumberList=], [=SVGAnimatedLength=], [=SVGAnimatedLengthList=],
      [=SVGAnimatedAngle=], [=SVGAnimatedRect=] or [=SVGAnimatedPreserveAspectRatio=],
      then the rules in the corresponding
      section defining the reflecting interface are used.

      Note: At a high level, the object's
      <code>baseVal</code> is used to reflect the value of the content attribute.
      For objects that reflect a CSS property, the <code>baseVal</code> is used
      to reflect the presentation attribute.
      
      </li>
    </ul>

<p>
This relationship is live, and values must be synchronized
(following the rules in <a href="#SynchronizingReflectedValues">Synchronizing reflected values</a>)
when either the attribute or its reflected property is modified.


<p>
If the attribute hasn't been specified explicitly in the document markup,
the reflected object is nonetheless initialized upon access,
to the attribute's initial value.
If the attribute's initial value is <span class="attr-value">(none)</span>,
the object is initialized as defined in
<a href="#SVGObjectInitialization">Reflecting an empty initial value</a>.
This newly constructed object does not generate an attribute on the element until
it is modified for the first time. Modifications made to the corresponding
attribute are immediately reflected in the object.

<p class="example">If <code>lineElement.x1.baseVal</code> is accessed
(where <code>lineElement</code> is an instance of [=SVGLineElement=])
and the {{line/x1}} attribute was not specified in the document, the
returned [=SVGLength=] object would represent the value <span class="attr-value">0 user units</span>,
because the initial value for the attribute is <span class="attr-value">0</span>.

<h4 id="SynchronizingReflectedValues">Synchronizing reflected values</h4>

<p>Whenever a reflected content attribute's base value changes,
then the reflecting object must be <dfn id="TermSynchronize" data-dfn-type="dfn" data-export="">synchronized</dfn>,
immediately after the value changed, by running the following steps:

<ol class='algorithm'>
  <li>If the reflecting object is a [=list interface=] object,
  then run the steps for {{TermSynchronizeList/synchronizing
  a list interface object}}.</li>
  <li>Otherwise, update the object's value to be the base value of the reflected
  content attribute (using the attribute's [=initial value=] if it is not
  present or invalid).
  <p class='note'>This will, for example, update the {{LengthValue/value}}
  of an [=SVGLength=] object.</li>
</ol>

<p>When a [=reflected=] content attribute is to be
<dfn id="TermReserialize" data-dfn-type="dfn" data-export="">reserialized</dfn>, optionally using a
specific value, the following steps must be performed:

<ol class="algorithm">
  <li>Let <var>value</var> be the specific value given, or
  the value of the content attribute's reflecting IDL attribute
  if a specific value was not provided.</li>

  <li>Depending on <var>value</var>'s type:
    <dl class="switch">
      <dt>[=SVGAnimatedBoolean=]</dt>
      <dt>[=SVGAnimatedNumber=]</dt>
      <dt>[=SVGAnimatedLength=]</dt>
      <dt>[=SVGAnimatedAngle=]</dt>
      <dt>[=SVGAnimatedRect=]</dt>
      <dt>[=SVGAnimatedString=]</dt>
      <dt>[=SVGAnimatedNumberList=]</dt>
      <dt>[=SVGAnimatedLengthList=]</dt>
      <dt>[=SVGAnimatedTransformList=]</dt>
      <dd><a href="#TermReserialize">Reserialize</a> the content attribute using
      <var>value</var>'s baseVal member.</dd>

      <dt>[=SVGAnimatedEnumeration=]</dt>
      <dd>
        <ol>
          <li>Let <var>number</var> be the value of <var>value</var>'s
          baseVal member.</li>
          <li>Let <var>keyword</var> be the content attribute's keyword
          value corresponding to <var>number</var>, or the empty string
          if <var>number</var> is 0.
          Note: This means that if the enumeration value is
          somehow set to the "unknown" value, the content attribute will be
          set to the empty string.
          However, this unknown value can never be set directly on the <code>SVGAnimatedEnumeration</code> object;
          it represents an unknown attribute value set in the markup.
          </li>
          <li>Set the content attribute to <var>keyword</var>.</li>
        </ol>
      </dd>

      <dt>boolean</dt>
      <dd>Set the content attribute to "true" if <var>value</var> is true,
      and "false" otherwise.</dd>

      <dt>float</dt>
      <dt>double</dt>
      <dd>Set the content attribute to an implementation specific string
      that, if parsed as a <a>&lt;number&gt;</a> using CSS syntax,
      would return the number value closest to <var>value</var>, given
      the implementation's supported <a href="#Precision">real number precision</a>.</dd>

      <dt>[=SVGLength=]</dt>
      <dd>Set the content attribute to the value that would be returned
      from getting <var>value</var>'s <a href="#__svg__SVGLength__valueAsString">valueAsString</a>
      member.</dd>

      <dt>[=SVGAngle=]</dt>
      <dd>Set the content attribute to the value that would be returned
      from getting <var>value</var>'s <a href="#__svg__SVGAngle__valueAsString">valueAsString</a>
      member.</dd>

      <dt>[=DOMRect=]</dt>
      <dd>
        <ol>
          <li>Let <var>components</var> be a list of four values, being the values of the
          <a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-domrectreadonly-domrect-x">x</a>,
          <a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-domrectreadonly-domrect-y">y</a>,
          <a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-domrectreadonly-domrect-width">width</a> and
          <a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#dom-domrectreadonly-domrect-height">height</a>
          members of <var>value</var>.</li>

          <li>Let <var>serialized components</var> be a list of four strings,
          where each is an implementation specific string that, if parsed
          as a <a>&lt;number&gt;</a> using CSS syntax, would return the number
          value closest to the corresponding value in <var>components</var>, given
          the implementation's supported <a href="#Precision">real number precision</a>.</li>

          <li>Set the content attribute to a string consisting of the strings in
          <var>serialized components</var> joined and separated by single
          U+0020 SPACE characters.</li>
        </ol>
      </dd>

      <dt>DOMString</dt>
      <dd>Set the content attribute to <var>value</var>.</dd>

      <dt>[=SVGNumberList=]</dt>
      <dt>[=SVGLengthList=]</dt>
      <dt>[=SVGPointList=]</dt>
      <dt>[=SVGTransformList=]</dt>
      <dt>[=SVGStringList=]</dt>
      <dd>
        <ol>
          <li>Let <var>elements</var> be the list of values in <var>value</var>.
            Note: The values will be [=SVGNumber=], [=SVGLength=],
            [=DOMPoint=] or [=SVGTransform=] objects, or <b>DOMString</b> values,
            depending on <var>value</var>'s type.
          </li>

          <li>Let <var>serialized elements</var> be a list of strings, where each
          string is formed based on the corresponding value in <var>elements</var>
          and its type:
            <dl class="switch">
              <dt>an [=SVGNumber=] object</dt>
              <dd>The string is an implementation specific string that, if parsed
              as a <a>&lt;number&gt;</a> using CSS syntax, would return the number
              value closest to the [=SVGNumber=] object's
              <a href="#__svg__SVGNumber__value">value</a> member, given
              the implementation's supported <a href="#Precision">real number precision</a>.</dd>
              <dt>an [=SVGLength=] object</dt>
              <dd>The string is the value that would be returned
              from getting the value's <a href="#__svg__SVGLength__valueAsString">valueAsString</a>
              member.</dd>
              <dt>a [=DOMPoint=] object</dt>
              <dd>The string value is computed as follows:
                <ol>
                  <li>Let <var>string</var> be an empty string.</li>
                  <li>Let <var>x</var> and <var>y</var> be the values of the
                  [=DOMPoint=] object's x and y coordinates, respectively.</li>
                  <li>Append to <var>string</var> an implementation specific string
                  that, if parsed as <a>&lt;number&gt;</a> using CSS syntax, would return the number
                  value closest to <var>x</var>, given
                  the implementation's supported <a href="#Precision">real number precision</a>.</li>
                  <li>Append a single U+002C COMMA character to <var>string</var>.</li>
                  <li>Append to <var>string</var> an implementation specific string
                  that, if parsed as <a>&lt;number&gt;</a> using CSS syntax, would return the number
                  value closest to <var>y</var>, given
                  the implementation's supported <a href="#Precision">real number precision</a>.</li>
                  <li>The string is <var>string</var>.</li>
                </ol>
              </dd>
              <dt>a [=SVGTransform=] object</dt>
              <dd>The string is the <a href="https://drafts.csswg.org/css-transforms-1/#serialization-of-transform-functions">serialization</a>
              of the [=SVGTransform=] object's <a href="coords.html#TransformMatrixObject">matrix object</a>.</dd>
              <dt>a <b>DOMString</b></dt>
              <dd>The string is the <b>DOMString</b>'s value itself.</dd>
            </dl>
          </li>

          <li>Set the content attribute to a string consisting of the strings in
          <var>serialized elements</var> joined and separated by single
          U+0020 SPACE characters.</li>
        </ol>
      </dd>
    </dl>
  </li>
</ol>


<h4 id="SVGObjectInitialization">Reflecting an empty initial value</h4>

<p>
When initializing an SVG DOM attribute that [=reflects=] a null or empty initial value,
then the property must be initialized according to its data type,
as defined in this section.
This occurs only if there is no explicit value for the reflected content attribute,
and the initial value in the attribute's definition table is <span class="attr-value">(none)</span>.


<p>
If an interface is not listed below that means
that the object initialization shall be done using the values for the
objects that the interface contains, e.g.,
an [=SVGAnimatedString=] consists of two <span class="DOMInterfaceName">DOMString</span> members,
while a [=DOMRect=] consists of many <span class="DOMInterfaceName">double</span>s.

<dl id="SVGObjectInitValues">
  <dt class="DOMInterfaceName">DOMString</dt>
  <dd>Initialized as the empty string (<span class="attr-value">""</span>).</dd>

  <dt class="DOMInterfaceName">float</dt>
  <dt class="DOMInterfaceName">long</dt>
  <dt class="DOMInterfaceName">short</dt>
  <dt>Any other <a href="https://heycam.github.io/webidl/#dfn-numeric-type">numeric type</a> defined in WebIDL</dt>
  <dd>Initialized as <span class="attr-value">0</span>.</dd>

  <dt class="DOMInterfaceName">boolean</dt>
  <dd>Initialized as <span class="attr-value">false</span>.</dd>

  <dt class="DOMInterfaceName">[=SVGLength=]</dt>
  <dd>Initialized as <span class="attr-value">0 user units</span>
  (<a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_NUMBER">SVG_LENGTHTYPE_NUMBER</a>).</dd>

  <dt class="DOMInterfaceName">[=SVGLengthList=]</dt>
  <dt class="DOMInterfaceName">[=SVGNumberList=]</dt>
  <dt class="DOMInterfaceName">[=SVGPointList=]</dt>
  <dt class="DOMInterfaceName">[=SVGStringList=]</dt>
  <dt class="DOMInterfaceName">[=SVGTransformList=]</dt>
  <dd>Initialized as the empty list.</dd>

  <dt class="DOMInterfaceName">[=SVGAngle=]</dt>
  <dd>Initialized as <span class="attr-value">0 in unspecified units</span>
  (<a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNSPECIFIED">SVG_ANGLETYPE_UNSPECIFIED</a>).</dd>

  <dt class="DOMInterfaceName">[=SVGPreserveAspectRatio=]</dt>
  <dd>Initialized as <span class="attr-value">'xMidYMid meet'</span>.</dd>
</dl>

<p class="example">If <code>textElement.dx.baseVal</code> is accessed
(where <code>textElement</code> is an instance of [=SVGTextElement=])
and the {{text/dx}} attribute was not specified in the document, the
returned [=SVGLengthList=] object would be empty.

<h4 id="InvalidValues">Invalid values</h4>

<p>If a script sets a [=reflected=] DOM attribute
to an [=invalid value=] for the content attribute (e.g.,
a negative number for an attribute that requires a non-negative
number), unless
this specification indicates otherwise, no exception shall be
raised on setting, but the given document fragment shall become
technically <em>in error</em> as described in
<a href="conform.html#ErrorProcessing">Error processing</a>.

Note: 
DOM attributes that reflect enumerated values using integer constants are an exception:
these throw a [=TypeError=] when set to an out-of-range integer,
or to the constant (0) that represents an unknown attribute value.
This is consistent with the
<a href="https://heycam.github.io/webidl/#es-enumeration">behavior of the WebIDL enumeration type</a>
[<a href="refs.html#ref-webidl">WebIDL</a>].




<h3 id="DOMInterfacesForSVGElements">DOM interfaces for SVG elements</h3>

<div class='ready-for-wider-review'>
<h4 id="InterfaceSVGElement">Interface SVGElement</h4>

<p>All of the SVG DOM interfaces that correspond directly to elements in the
SVG language (such as the [=SVGPathElement=] interface for the
{{path}} element) derive from the [=SVGElement=] interface.

Note: The CSSOM specification
<a href="http://dev.w3.org/csswg/cssom/#the-elementcssinlinestyle-interface">augments
SVGElement with a style IDL attribute</a>, so that the {{style attribute}}
attribute can be accessed in the same way as on HTML elements.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGElement</b> : <a>Element</a> {

  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedString</a> <a href="types.html#__svg__SVGElement__className">className</a>;

  readonly attribute <a>SVGSVGElement</a>? <a href="types.html#__svg__SVGElement__ownerSVGElement">ownerSVGElement</a>;
  readonly attribute <a>SVGElement</a>? <a href="types.html#__svg__SVGElement__viewportElement">viewportElement</a>;
};

<a>SVGElement</a> includes <a>GlobalEventHandlers</a>;
<a>SVGElement</a> includes <a>SVGElementInstance</a>;
<a>SVGElement</a> includes <a>HTMLOrSVGElement</a>;</pre>


<p>The <b id="__svg__SVGElement__className">className</b> IDL attribute
[=reflects=] the {{class}} attribute.

<div class="note"><p>This attribute is deprecated and may be removed in a
future version of this specification.  Authors are advised to use
Element.classList instead.
<p>
The <a href="types.html#__svg__SVGElement__className">className</a>
attribute on [=SVGElement=] overrides the correspond attribute on
[=Element=], following the WebIDL rules for
<a href="https://www.w3.org/TR/WebIDL/#dfn-inherit">inheritance</a>.
</div>

<p>The <b id="__svg__SVGElement__ownerSVGElement">ownerSVGElement</b> IDL attribute
represents the nearest ancestor <{svg}> element.  On getting
<a href="#__svg__SVGElement__ownerSVGElement">ownerSVGElement</a>,
the nearest ancestor <{svg}> element is returned; if the current
element is the [=outermost svg element=], then null is returned.

<p>The <b id="__svg__SVGElement__viewportElement">viewportElement</b> IDL attribute
represents the element that provides the SVG viewport for the current element.  On getting
<a href="#__svg__SVGElement__viewportElement">viewport</a>,
the nearest ancestor element that establishes an SVG viewport is returned; if the current
element is the [=outermost svg element=], then null is returned.

<h4 id="InterfaceSVGGraphicsElement">Interface SVGGraphicsElement</h4>

<div class="annotation svg2-requirement">
  <table>
    <tr><th>SVG 2 Requirement:</th>
    <td>Detect if a mouse event is on the fill or stroke of a shape.</td></tr>
    <tr><th>Resolution:</th>
    <td><a href="http://www.w3.org/2012/03/22-svg-irc#T20-20-03">SVG 2 will make it easier to detect if an mouse event is on the stroke or fill of an element.</a></td></tr>
    <tr><th>Purpose:</th>
    <td>To allow authors to discriminate between pointer events on the fill and stroke of an element without having to duplicate the element</td></tr>
    <tr><th>Owner:</th>
    <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3279">ACTION-3279</a>)</td></tr>
    <tr><th>Status:</th>
    <td>Done.</td></tr>
  </table>
</div>

<p>The [=SVGGraphicsElement=] interface represents SVG elements whose primary purpose
is to directly render graphics into a group.

<pre class="idl">dictionary <b id="SVGBoundingBoxOptions">SVGBoundingBoxOptions</b> {
  boolean fill = true;
  boolean stroke = false;
  boolean markers = false;
  boolean clipped = false;
};

[Exposed=Window]
interface <b>SVGGraphicsElement</b> : <a>SVGElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedTransformList</a> <a href="types.html#__svg__SVGGraphicsElement__transform">transform</a>;

  <a>DOMRect</a> <a href="types.html#__svg__SVGGraphicsElement__getBBox">getBBox</a>(optional <a>SVGBoundingBoxOptions</a> options = {});
  <a>DOMMatrix</a>? <a href="types.html#__svg__SVGGraphicsElement__getCTM">getCTM</a>();
  <a>DOMMatrix</a>? <a href="types.html#__svg__SVGGraphicsElement__getScreenCTM">getScreenCTM</a>();
};

<a>SVGGraphicsElement</a> includes <a>SVGTests</a>;</pre>

<p>The <b id="__svg__SVGGraphicsElement__transform">transform</b> IDL attribute
[=reflects=] the computed value of the {{transform}} property and its
corresponding <span class="attr-name">transform</span> presentation attribute.

<p>The <b id="__svg__SVGGraphicsElement__getBBox">getBBox</b> method is used
to compute the bounding box of the current element.  When the getBBox(<var>options</var>)
method is called, the <a href="coords.html#BoundingBoxes">bounding box algorithm</a>
is invoked for the current element,
with <var>fill</var>, <var>stroke</var>, <var>markers</var>
and <var>clipped</var> members of the <var>options</var> dictionary argument
used to control which parts of the element are included in the bounding box,
using the element's user coordinate system as the coordinate system to return the
bounding box in.  A newly created [=DOMRect=] object that defines the
computed bounding box is returned. If <a
href="types.html#__svg__SVGGraphicsElement__getBBox">getBBox</a> gets called on a <a>
non-rendered element</a>, and the UA is not able to compute the geometry of the element, then
throw an [=InvalidStateError=].

<p>The <b id="__svg__SVGGraphicsElement__getCTM">getCTM</b> method is used to
get the matrix that transforms the current element's coordinate system to
its SVG viewport's coordinate system.  When getCTM() is called, the following
steps are run:

<ol class='algorithm'>
  <li>If the current element is not in the document, then return null.</li>
  <li>If the current element is a [=non-rendered element=], and the UA
    is not able to resolve the style of the element, then return null.</li>
  <li>Let <var>ctm</var> be a matrix determined based on what the
  current element is:
    <dl class='switch'>
      <dt>the current element is the [=outermost svg element=]</dt>
      <dd><var>ctm</var> is a matrix that transforms the coordinate
      space of the {{svg}} (including its {{transform}} property)
      to the coordinate space of the document's viewport.  The matrix includes the
      transforms produced by the {{viewBox}} and {{preserveAspectRatio}}
      attributes, the {{transform}} property, and any transform
      due to <a href="struct.html#__svg__SVGSVGElement__currentScale">currentScale</a>
      and <a href="struct.html#__svg__SVGSVGElement__currentTranslate">currentTranslate</a>
      properties on the [=SVGSVGElement=].</dd>
      <dt>any other element</dt>
      <dd><var>ctm</var> is a matrix that transforms the coordinate
      space of the current element (including its {{transform}}
      property) to the coordinate space of its closest ancestor
      viewport-establishing element (also including its {{transform}}
      property).</dd>
    </dl>
  </li>
  <li>Return a newly created, <a href="coords.html#MatrixMode">detached</a>
  [=DOMMatrix=] object that represents the same matrix as <var>ctm</var>.</li>
</ol>

<p>The <b><dfn dfn export>getScreenCTM</dfn></b> method
is used to get the matrix that transforms the current element's coordinate
system to the coordinate system of the SVG viewport for the SVG document fragment.
When getScreenCTM() is called, the following steps are run:

<ol class='algorithm'>
  <li>If the current element is not in the document, then return null.</li>
  <li>If the current element is a [=non-rendered element=], and the UA
    is not able to resolve the style of the element, then return null.</li>
  <li>Let <var>ctm</var> be a matrix that transforms the coordinate
  space of the current element (including its {{transform}} property)
  to the coordinate space of the document's viewport.
    <div class='note'>
      <p>This will include:
      <ul>
        <li>all of the transforms from the current element up to the
        [=outermost svg element=]</li>
        <li>any transforms due to {{viewBox}}, {{preserveAspectRatio}},
        the {{transform}} property and any transform
        due to <a href="struct.html#__svg__SVGSVGElement__currentScale">currentScale</a>
        and <a href="struct.html#__svg__SVGSVGElement__currentTranslate">currentTranslate</a>
        properties on the [=SVGSVGElement=] for the [=outermost svg element=]</li>
        <li>any transforms from the SVG viewport's coordinate space
        to the document's viewport, i.e. taking into account the positions of
        all of the CSS boxes from the [=outermost svg element=]'s box
        to the initial containing block when the SVG document fragment
	is inline in an HTML document</li>
      </ul>
    </div>
  </li>
  <li>Return a newly created, <a href="coords.html#MatrixMode">detached</a>
  [=DOMMatrix=] object that represents the same matrix as <var>ctm</var>.</li>
</ol>

<p class='note'>This method would have been more aptly named as <code>getClientCTM</code>,
but the name <code>getScreenCTM</code> is kept for historical reasons.
</div>


<div class="ready-for-wider-review">

<h4 id="InterfaceSVGGeometryElement">Interface SVGGeometryElement</h4>

<p>Interface [=SVGGeometryElement=] represents SVG elements whose rendering
is defined by geometry with an [=equivalent path=],
and which can be filled and stroked.
This includes paths and the basic shapes.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGGeometryElement</b> : <a>SVGGraphicsElement</a> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedNumber</a> <a href="types.html#__svg__SVGGeometryElement__pathLength">pathLength</a>;

  boolean <a href="types.html#__svg__SVGGeometryElement__isPointInFill">isPointInFill</a>(optional <a>DOMPointInit</a> point = {});
  boolean <a href="types.html#__svg__SVGGeometryElement__isPointInStroke">isPointInStroke</a>(optional <a>DOMPointInit</a> point = {});
  float <a href="types.html#__svg__SVGGeometryElement__getTotalLength">getTotalLength</a>();
  <a>DOMPoint</a> <a href="types.html#__svg__SVGGeometryElement__getPointAtLength">getPointAtLength</a>(float distance);
};</pre>

<p>The <b id="__svg__SVGGeometryElement__isPointInFill">isPointInFill</b> method,
when invoked, must return true if the point given by <var>point</var> passed to the method,
in the coordinate space of an element, is inside the intended path as determined by the winding
rule indicated by the {{fill-rule}} property of an element; and must return false otherwise.
Open subpaths must be implicitly closed when computing the area inside the path, without affecting
the actual subpaths. Points on the path itself must be considered to be inside the path.
The returned value is independent of any visual CSS property but {{fill-rule}}
If either of the <var>x</var> or <var>y</var> properties on <var>point</var> are infinite or NaN,
then the method must return false. If current element is a <a>
non-rendered element</a>, and the UA is not able to compute the geometry of the element, then
throw an [=InvalidStateError=].


Note: [=isPointInFill=] takes the winding
rule indicated by the {{fill-rule}} property of an element even if the element is a child
of a {{clipPath}} element.

Note: [=isPointInFill=] is aligned
with the [=isPointInPath=] method on the [=CanvasDrawPath=] mixin as much as the SVG context
allows it to be.

<p>The <b id="__svg__SVGGeometryElement__isPointInStroke">isPointInStroke</b> method,
when invoked, must return true if the point given by <var>point</var> passed to the method,
in the coordinate space of an element, is in or on the outline path of an applied stroke on
an element; and must return false otherwise.
The outline path must take the stroke properties {{stroke-width}},
{{stroke-linecap}}, {{stroke-linejoin}}, {{stroke-miterlimit}}, {{stroke-dasharray}},
{{stroke-dashoffset}} and {{vector-effect}} of an element into account. See sections
<a href="https://svgwg.org/svg2-draft/painting.html#StrokeShape">Computing the shape of the stroke</a> and
<a href="https://svgwg.org/svg2-draft/painting.html#PaintingVectorEffects">Vector effects</a> for details.
The returned value is independent of any visual CSS property but the listed stroke properties.
If either of the <var>x</var> or <var>y</var> properties on <var>point</var> are infinite or NaN,
then the method must return false. If current element is a <a>
non-rendered element</a>, and the UA is not able to compute the geometry of the element, then
throw an [=InvalidStateError=].


Note: <a href="types.html#__svg__SVGGeometryElement__isPointInStroke">isPointInStroke</a> is aligned
with the [=isPointInStroke=] method on the [=CanvasDrawPath=] mixin as much as the SVG context
allows it to be.

<p>The <b id="__svg__SVGGeometryElement__pathLength">pathLength</b> IDL attribute
[=reflects=] the {{pathLength}} content attribute.

<p>The <b id="__svg__SVGGeometryElement__getTotalLength">getTotalLength</b> method
is used to compute the length of the path.  When getTotalLength()
is called, the user agent's computed value for the total length of the path,
in user units, is returned. If current element is a <a>
non-rendered element</a>, and the UA is not able to compute the total length of the path, then
throw an [=InvalidStateError=].

Note: The user agent's computed path length does not take the
{{pathLength}} attribute into account.

<p>The <b id="__svg__SVGGeometryElement__getPointAtLength">getPointAtLength</b> method
is used to return the point at a given distance along the path.  When
getPointAtLength(<var>distance</var>) is called, the following steps are run:

<ol class='algorithm'>
  <li>If current element is a [=non-rendered element=], and the UA is not able to
    compute the total length of the path, then throw an [=InvalidStateError=].</li>
  <li>Let <var>length</var> be the user agent's computed value for the total
  length of the path, in user units.
    Note: As with <a href="#__svg__SVGGeometryElement__getTotalLength">getTotalLength</a>,
    this does not take into account the {{pathLength}} attribute.
  </li>
  <li>Clamp <var>distance</var> to [0, <var>length</var>].</li>
  <li>Let (<var>x</var>, <var>y</var>) be the point on the path at distance
  <var>distance</var>.</li>
  <li>Return a newly created, <a href="shapes.html#PointMode">detached</a>
  [=DOMPoint=] object representing the point
  (<var>x</var>, <var>y</var>).</li>
</ol>

</div>


<h3 id="DOMInterfacesForBasicDataTypes">DOM interfaces for basic data types</h3>

<h4 id="InterfaceSVGNumber">Interface SVGNumber</h4>

<p>The [=SVGNumber=] interface is used primarily to represent a <a>&lt;number&gt;</a>
value that is a part of an [=SVGNumberList=].  Individual [=SVGNumber=]
objects can also be created by script.

<p id="ReadOnlyNumber" class='ready-for-wider-review'>An [=SVGNumber=] object can be designated as <em>read only</em>,
which means that attempts to modify the object will result in an exception
being thrown, as described below.
[=SVGNumber=] objects reflected through the animVal IDL attribute are always
<em>read only</em>.

<p id="NumberAssociatedElement">An [=SVGNumber=] object can be <em>associated</em>
with a particular element.  The associated element is used to
determine which element's content attribute to update if the object [=reflects=]
an attribute.  Unless otherwise described, an [=SVGNumber=] object is not
associated with any element.

<div class='ready-for-wider-review'>
<p id="NumberMode">Every [=SVGNumber=] object operates in one of two
modes.  It can:

<ol>
  <li><em>reflect an element of the base value</em> of a [=reflected=] animatable
  attribute (being exposed through the methods on the
  <a href="types.html#__svg__SVGAnimatedNumberList__baseVal">baseVal</a> member of
  an [=SVGAnimatedNumberList=]),</li>
  <li><em>be detached</em>, which is the case for [=SVGNumber=] objects created
  with <a href='struct.html#__svg__SVGSVGElement__createSVGNumber'>createSVGNumber</a>.</li>
</ol>
</div>

<p>An [=SVGNumber=] object maintains an internal number value,
which is called its <dfn id="NumberValue">value</dfn>.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGNumber</b> {
  attribute float <a href="types.html#__svg__SVGNumber__value">value</a>;
};</pre>

<p>The <b id="__svg__SVGNumber__value">value</b> IDL attribute
represents the number.  On getting <a href="#__svg__SVGNumber__value">value</a>,
the [=SVGNumber=]'s <a href='#NumberValue'>value</a> is returned.

<p>On setting <a href="#__svg__SVGNumber__value">value</a>, the following
steps are run:

<ol class='algorithm'>
  <li>If the [=SVGNumber=] is <a href="#ReadOnlyNumber">read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>Set the [=SVGNumber=]'s <a href='#NumberValue'>value</a> to the
  value being assigned to the <a href="#__svg__SVGNumber__value">value</a>
  member.</li>
  <li>If the [=SVGNumber=] <a href='#NumberMode'>reflects an element of the
  base value</a> of a [=reflected=] attribute, then [=reserialize=]
  the reflected attribute.
  </li>
</ol>


<h4 id="InterfaceSVGLength">Interface SVGLength</h4>

<p>The [=SVGLength=] interface is used to represent a value that
can be a <a>&lt;length&gt;</a>, <a>&lt;percentage&gt;</a> or
<a>&lt;number&gt;</a> value.

<p id="ReadOnlyLength" class='ready-for-wider-review'>An [=SVGLength=] object can be designated as <em>read only</em>,
which means that attempts to modify the object will result in an exception
being thrown, as described below.
[=SVGLength=] objects reflected through the animVal IDL attribute are always
<em>read only</em>.

<p id="LengthAssociatedElement">An [=SVGLength=] object can be <em>associated</em>
with a particular element, as well as being designated with a <em>directionality</em>:
horizontal, vertical or unspecified.  The associated element and the directionality of the
length are used to resolve percentage values to user units and is also used to
determine which element's content attribute to update if the object [=reflects=]
an attribute.  Unless otherwise
described, an [=SVGLength=] object is not associated with any element and
has unspecified directionality.

<div class='ready-for-wider-review'>
<p id='LengthMode'>Every [=SVGLength=] object operates in one of
four modes.  It can:

<ol>
  <li><em>reflect the base value</em> of a [=reflected=] animatable attribute
  (being exposed through the <a href="types.html#__svg__SVGAnimatedLength__baseVal">baseVal</a>
  member of an [=SVGAnimatedLength=]),</li>
  <li><em>reflect a presentation attribute value</em>
  (such as by <a href="shapes.html#__svg__SVGRectElement__width">SVGRectElement.width.baseVal</a>),</li>
  <li><em>reflect an element of the base value</em> of a [=reflected=] animatable
  attribute (being exposed through the methods on the
  <a href="types.html#__svg__SVGAnimatedLengthList__baseVal">baseVal</a> member of
  an [=SVGAnimatedLengthList=]), or</li>
  <li><em>be detached</em>, which is the case for [=SVGLength=] objects created
  with <a href='struct.html#__svg__SVGSVGElement__createSVGLength'>createSVGLength</a>.</li>
</ol>
</div>

<p>An [=SVGLength=] object maintains an internal <a>&lt;length&gt;</a> or
<a>&lt;percentage&gt;</a> or <a>&lt;number&gt;</a> value, which is called its
<dfn attribute for=LengthValue>value</dfn>.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGLength</b> {

  // Length Unit Types
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_UNKNOWN">SVG_LENGTHTYPE_UNKNOWN</a> = 0;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_NUMBER">SVG_LENGTHTYPE_NUMBER</a> = 1;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_PERCENTAGE">SVG_LENGTHTYPE_PERCENTAGE</a> = 2;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_EMS">SVG_LENGTHTYPE_EMS</a> = 3;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_EXS">SVG_LENGTHTYPE_EXS</a> = 4;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_PX">SVG_LENGTHTYPE_PX</a> = 5;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_CM">SVG_LENGTHTYPE_CM</a> = 6;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_MM">SVG_LENGTHTYPE_MM</a> = 7;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_IN">SVG_LENGTHTYPE_IN</a> = 8;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_PT">SVG_LENGTHTYPE_PT</a> = 9;
  const unsigned short <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_PC">SVG_LENGTHTYPE_PC</a> = 10;

  readonly attribute unsigned short <a href="types.html#__svg__SVGLength__unitType">unitType</a>;
           attribute float <a href="types.html#__svg__SVGLength__value">value</a>;
           attribute float <a href="types.html#__svg__SVGLength__valueInSpecifiedUnits">valueInSpecifiedUnits</a>;
           attribute DOMString <a href="types.html#__svg__SVGLength__valueAsString">valueAsString</a>;

  undefined <a href="types.html#__svg__SVGLength__newValueSpecifiedUnits">newValueSpecifiedUnits</a>(unsigned short unitType, float valueInSpecifiedUnits);
  undefined <a href="types.html#__svg__SVGLength__convertToSpecifiedUnits">convertToSpecifiedUnits</a>(unsigned short unitType);
};</pre>

<p>The numeric length unit type constants defined on [=SVGLength=] are used
to represent the type of an [=SVGLength=]'s {{LengthValue/value}}.
Their meanings are as follows:

<table class='vert'>
  <tr><th>Constant</th><th>Meaning</th></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_NUMBER">SVG_LENGTHTYPE_NUMBER</b></td><td>A unitless <a>&lt;number&gt;</a> interpreted as a value in <span class='prop-value'>px</span>.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_PERCENTAGE">SVG_LENGTHTYPE_PERCENTAGE</b></td><td>A <a>&lt;percentage&gt;</a>.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_EMS">SVG_LENGTHTYPE_EMS</b></td><td>A <a>&lt;length&gt;</a> with an <span class='prop-value'>em</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_EXS">SVG_LENGTHTYPE_EXS</b></td><td>A <a>&lt;length&gt;</a> with an <span class='prop-value'>ex</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_PX">SVG_LENGTHTYPE_PX</b></td><td>A <a>&lt;length&gt;</a> with a <span class='prop-value'>px</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_CM">SVG_LENGTHTYPE_CM</b></td><td>A <a>&lt;length&gt;</a> with a <span class='prop-value'>cm</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_MM">SVG_LENGTHTYPE_MM</b></td><td>A <a>&lt;length&gt;</a> with a <span class='prop-value'>mm</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_IN">SVG_LENGTHTYPE_IN</b></td><td>A <a>&lt;length&gt;</a> with an <span class='prop-value'>in</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_PT">SVG_LENGTHTYPE_PT</b></td><td>A <a>&lt;length&gt;</a> with a <span class='prop-value'>pt</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_PC">SVG_LENGTHTYPE_PC</b></td><td>A <a>&lt;length&gt;</a> with a <span class='prop-value'>pc</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGLength__SVG_LENGTHTYPE_UNKNOWN">SVG_LENGTHTYPE_UNKNOWN</b></td><td>Some other type of value.</td></tr>
</table>

Note: The use of numeric length unit type constants is an anti-pattern and
new constant values will not be introduced for any other units or length types supported by
[=SVGLength=].  If other types of lengths are supported and used, the [=SVGLength=]
uses the <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_UNKNOWN">SVG_LENGTHTYPE_UNKNOWN</a>
unit type.  See below for details on how the other properties of an [=SVGLength=]
operate with these types of lengths.

<p>The <b id="__svg__SVGLength__unitType">unitType</b> IDL attribute represents
the type of value that the [=SVGLength=]'s {{LengthValue/value}} is.
On getting <a href='#__svg__SVGLength__unitType'>unitType</a>, the following steps
are run:

<ol class='algorithm'>
  <li>If the [=SVGLength=]'s {{LengthValue/value}} is a unitless
  <a>&lt;number&gt;</a>, a <a>&lt;percentage&gt;</a>, or a <a>&lt;length&gt;</a>
  with an
  <span class='prop-value'>em</span>,
  <span class='prop-value'>ex</span>,
  <span class='prop-value'>px</span>,
  <span class='prop-value'>cm</span>,
  <span class='prop-value'>mm</span>,
  <span class='prop-value'>in</span>,
  <span class='prop-value'>pt</span> or
  <span class='prop-value'>pc</span> unit, then return the corresponding constant
  value from the length unit type table above.</li>
  <li>Otherwise, return <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_UNKNOWN">SVG_LENGTHTYPE_UNKNOWN</a>.
    <p class='note'>For example, for a <a>&lt;length&gt;</a> with a <span class='prop-value'>ch</span>
    unit or one that has a non-scalar value such as <span class='attr-value'>calc()</span>,
    <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_UNKNOWN">SVG_LENGTHTYPE_UNKNOWN</a>
    would be returned.
  </li>
</ol>

<p>The <b id="__svg__SVGLength__value">value</b> IDL attribute represents
the [=SVGLength=]'s {{LengthValue/value}} in user units.
On getting <a href='#__svg__SVGLength__value'>value</a>, the following steps
are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the [=SVGLength=]'s {{LengthValue/value}}.</li>
  <li>If <var>value</var> is a <a>&lt;number&gt;</a>, return that number.</li>
  <li>Let <var>viewport size</var> be a basis to resolve percentages against, based on the [=SVGLength=]'s
  <a href='#LengthAssociatedElement'>associated element</a> and
  <a href='#LengthAssociatedElement'>directionality</a>:
    <dl class='switch'>
      <dt>has no <a href='#LengthAssociatedElement'>associated element</a></dt>
      <dd><var>size</var> is 100</dd>
      <dt>has an <a href='#LengthAssociatedElement'>associated element</a> and horizontal <a href='#LengthAssociatedElement'>directionality</a></dt>
      <dd><var>size</var> is the width of the <a href='#LengthAssociatedElement'>associated element</a>'s SVG viewport</dd>
      <dt>has an <a href='#LengthAssociatedElement'>associated element</a> and vertical <a href='#LengthAssociatedElement'>directionality</a></dt>
      <dd><var>size</var> is the height of the <a href='#LengthAssociatedElement'>associated element</a>'s SVG viewport</dd>
      <dt>has an <a href='#LengthAssociatedElement'>associated element</a> and unspecified <a href='#LengthAssociatedElement'>directionality</a></dt>
      <dd><var>size</var> is the length of the <a href='#LengthAssociatedElement'>associated element</a>'s SVG viewport
      diagonal (see <a href='coords.html#Units'>Units</a>)</dd>
    </dl>
  </li>
  <li>Let <var>font size</var> be a basis to resolve font size values against,
  based on the [=SVGLength=]'s <a href='#LengthAssociatedElement'>associated element</a>:
    <dl class='switch'>
      <dt>has no <a href='#LengthAssociatedElement'>associated element</a></dt>
      <dd><var>font size</var> is the absolute length of the initial value of the {{font-size}} property</dd>
      <dt>has an <a href='#LengthAssociatedElement'>associated element</a></dt>
      <dd><var>size</var> is the computed value of the <a href='#LengthAssociatedElement'>associated element</a>'s {{font-size}} property</dd>
    </dl>
  </li>
  <li>Return the result of converting <var>value</var> to an absolute length,
  using <var>viewport size</var> and <var>font size</var> as percentage and font size
  bases.  If the conversion is not possible due to the lack of an
  <a href='#LengthAssociatedElement'>associated element</a>, return 0.</li>
</ol>

<p>On setting <a href='#__svg__SVGLength__value'>value</a>, the following steps
are run:

<ol class='algorithm'>
  <li>If the [=SVGLength=] object is <a href='#ReadOnlyLength'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>Let <var>value</var> be the value being assigned to
  <a href='#__svg__SVGLength__value'>value</a>.</li>
  <li>Set the [=SVGLength=]'s {{LengthValue/value}} to a
  <a>&lt;number&gt;</a> whose value is <var>value</var>.</li>
  <li>If the [=SVGLength=]
  <a href='#LengthMode'>reflects the base value</a> of a [=reflected=] attribute,
  <a href='#LengthMode'>reflects a presentation attribute</a>, or
  <a href='#LengthMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>

<p>The <b id="__svg__SVGLength__valueInSpecifiedUnits">valueInSpecifiedUnits</b> IDL attribute represents
the numeric factor of the [=SVGLength=]'s {{LengthValue/value}}.
On getting <a href='#__svg__SVGLength__valueInSpecifiedUnits'>valueInSpecifiedUnits</a>, the following steps
are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the [=SVGLength=]'s {{LengthValue/value}}.</li>
  <li>If <var>value</var> is a <a>&lt;number&gt;</a>, return that number.</li>
  <li>Otherwise, if <var>value</var> is a <a>&lt;percentage&gt;</a> or any scalar <a>&lt;length&gt;</a>
  value, return the numeric factor before its unit.</li>
  <li>Otherwise, return 0.
    <p class='note'>Thus <a href='#__svg__SVGLength__valueInSpecifiedUnits'>valueInSpecifiedUnits</a>
    would return 12 for both <span class='attr-value'>'12%'</span> and
    <span class='attr-value'>12em</span>, but
    0 would be returned for non-scalar values like
    <span class='attr-value'>calc(12px + 5%)</span>.
  </li>
</ol>

<p>On setting <a href='#__svg__SVGLength__valueInSpecifiedUnits'>valueInSpecifiedUnits</a>, the following steps
are run:

<ol class='algorithm'>
  <li>If the [=SVGLength=] object is <a href='#ReadOnlyLength'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>Let <var>value</var> be the value being assigned to
  <a href='#__svg__SVGLength__valueInSpecifiedUnits'>valueInSpecifiedUnits</a>.</li>
  <li>If the [=SVGLength=]'s {{LengthValue/value}} is a
  <a>&lt;number&gt;</a>, then update its value to <var>value</var>.</li>
  <li>Otherwise, if the [=SVGLength=]'s {{LengthValue/value}}
  is a <a>&lt;percentage&gt;</a> or a scalar-valued <a>&lt;length&gt;</a>,
  then update its numeric factor to <var>value</var>.</li>
  <li>Otherwise, the [=SVGLength=]'s {{LengthValue/value}}
  is of some other type.  Set it to a <a>&lt;number&gt;</a>
  whose value is <var>value</var>.</li>
  <li>If the [=SVGLength=]
  <a href='#LengthMode'>reflects the base value</a> of a [=reflected=] attribute or
  <a href='#LengthMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>

<p>The <b id="__svg__SVGLength__valueAsString">valueAsString</b> IDL attribute represents
the [=SVGLength=]'s {{LengthValue/value}} as a string.
On getting <a href='#__svg__SVGLength__valueAsString'>valueAsString</a>, the following steps
are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the [=SVGLength=]'s {{LengthValue/value}}.</li>
  <li>Let <var>string</var> be an empty string.</li>
  <li>If <var>value</var> is a <a>&lt;number&gt;</a>, <a>&lt;percentage&gt;</a>
  or scalar <a>&lt;length&gt;</a> value, then:
    <ol>
      <li>Let <var>factor</var> be <var>value</var>'s numeric factor,
      if it is a <a>&lt;percentage&gt;</a> or <a>&lt;length&gt;</a>,
      or <var>value</var> itself it is a <a>&lt;number&gt;</a>.</li>
      <li>Append to <var>string</var> an implementation
      specific string that, if parsed as a <a>&lt;number&gt;</a> using CSS syntax,
      would return the number value closest to <var>factor</var>, given the
      implementation's supported <a href="#Precision">real number precision</a>.</li>
      <li>If <var>value</var> is a <a>&lt;percentage&gt;</a> then append to
      <var>string</var> a single U+0025 PERCENT SIGN character.</li>
      <li>Otherwise, if <var>value</var> is a <a>&lt;length&gt;</a>,
      then append to <var>string</var> the canonical spelling of
      <var>value</var>'s unit.</li>
      <li>Return <var>string</var>.</li>
    </ol>
  </li>
  <li>Otherwise, return an implementation specific string that,
  if parsed as a <a>&lt;length&gt;</a>, would return the closest
  length value to <var>value</var>, given the
  implementation's supported <a href="#Precision">real number precision</a>.</li>
</ol>

<p>On setting <a href='#__svg__SVGLength__valueAsString'>valueAsString</a>, the following steps
are run:

<ol class='algorithm'>
  <li>If the [=SVGLength=] object is <a href='#ReadOnlyLength'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>Let <var>value</var> be the value being assigned to
  <a href='#__svg__SVGLength__valueAsString'>valueAsString</a>.</li>
  <li>Parse <var>value</var> using the CSS syntax
  [ <a>&lt;number&gt;</a> | <a>&lt;length&gt;</a> | <a>&lt;percentage&gt;</a> ].</li>
  <li>If parsing failed, then [=throw=] a [=SyntaxError=].</li>
  <li>Otherwise, parsing succeeded.  Set [=SVGLength=]'s {{LengthValue/value}}
  to the parsed value.</li>
  <li>If the [=SVGLength=]
  <a href='#LengthMode'>reflects the base value</a> of a [=reflected=] attribute or
  <a href='#LengthMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>

<p>The <b id="__svg__SVGLength__newValueSpecifiedUnits">newValueSpecifiedUnits</b>
method is used to set the [=SVGLength=]'s value in a typed manner.  When
newValueSpecifiedUnits(unitType, valueInSpecifiedUnits) is called, the following
steps are run:

<ol class='algorithm'>
  <li>If the [=SVGLength=] object is <a href='#ReadOnlyLength'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>If <var>unitType</var> is
  <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_UNKNOWN">SVG_LENGTHTYPE_UNKNOWN</a>
  or is a value that does not appear in the length unit type table above,
  then [=throw=] a [=NotSupportedError=].</li>
  <li>Set [=SVGLength=]'s {{LengthValue/value}} depending
  on the value of <var>unitType</var>:
    <dl class='switch'>
      <dt><a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_NUMBER">SVG_LENGTHTYPE_NUMBER</a></dt>
      <dd>a <a>&lt;number&gt;</a> whose value is <var>valueInSpecifiedUnits</var></dd>
      <dt><a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_PERCENTAGE">SVG_LENGTHTYPE_PERCENTAGE</a></dt>
      <dd>a <a>&lt;percentage&gt;</a> whose numeric factor is <var>valueInSpecifiedUnits</var></dd>
      <dt>anything else</dt>
      <dd>a <a>&lt;length&gt;</a> whose numeric factor is <var>valueInSpecifiedUnits</var>
      and whose unit is as indicated by the length unit type table above</dd>
    </dl>
  </li>
  <li>If the [=SVGLength=]
  <a href='#LengthMode'>reflects the base value</a> of a [=reflected=] attribute or
  <a href='#LengthMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>

<p>The <b id="__svg__SVGLength__convertToSpecifiedUnits">convertToSpecifiedUnits</b>
method is used to convert the [=SVGLength=]'s value to a specific type.
When convertToSpecifiedUnits(unitType) is called, the following steps are run:

<ol class='algorithm'>
  <li>If the [=SVGLength=] object is <a href='#ReadOnlyLength'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>If <var>unitType</var> is
  <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_UNKNOWN">SVG_LENGTHTYPE_UNKNOWN</a>
  or is a value that does not appear in the length unit type table above,
  then [=throw=] a [=NotSupportedError=].</li>
  <li>Let <var>absolute</var> be the value that would be returned from the
  <a href='#__svg__SVGLength__value'>value</a> member.</li>
  <li>If <var>unitType</var> is <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_NUMBER">SVG_LENGTHTYPE_NUMBER</a>, then:
    <ol>
      <li>Set the [=SVGLength=]'s {{LengthValue/value}} to a <a>&lt;number&gt;</a>
      whose value is <var>absolute</var>.</li>
    </ol>
  </li>
  <li>Otherwise, if <var>unitType</var> is <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_PERCENTAGE">SVG_LENGTHTYPE_PERCENTAGE</a>, then:
    <ol>
      <li>Let <var>viewport size</var> be a basis to resolve percentages against, based on the [=SVGLength=]'s
      <a href='#LengthAssociatedElement'>associated element</a> and
      <a href='#LengthAssociatedElement'>directionality</a>:
        <dl class='switch'>
          <dt>has no <a href='#LengthAssociatedElement'>associated element</a></dt>
          <dd><var>size</var> is 100</dd>
          <dt>has an <a href='#LengthAssociatedElement'>associated element</a> and horizontal <a href='#LengthAssociatedElement'>directionality</a></dt>
          <dd><var>size</var> is the width of the <a href='#LengthAssociatedElement'>associated element</a>'s SVG viewport</dd>
          <dt>has an <a href='#LengthAssociatedElement'>associated element</a> and vertical <a href='#LengthAssociatedElement'>directionality</a></dt>
          <dd><var>size</var> is the height of the <a href='#LengthAssociatedElement'>associated element</a>'s SVG viewport</dd>
          <dt>has an <a href='#LengthAssociatedElement'>associated element</a> and unspecified <a href='#LengthAssociatedElement'>directionality</a></dt>
          <dd><var>size</var> is the length of the <a href='#LengthAssociatedElement'>associated element</a>'s SVG viewport
          diagonal (see <a href='coords.html#Units'>Units</a>)</dd>
        </dl>
      </li>
      <li>Set the [=SVGLength=]'s {{LengthValue/value}} to the result of
      converting <var>absolute</var> to a <a>&lt;percentage&gt;</a>, using <var>viewport size</var>
      as the percentage basis.</li>
    </ol>
  </li>
  <li>Otherwise, if <var>unitType</var> is <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_EMS">SVG_LENGTHTYPE_EMS</a>
  or <a href="types.html#__svg__SVGLength__SVG_LENGTHTYPE_EXS">SVG_LENGTHTYPE_EXS</a>, then:
    <ol>
      <li>Let <var>font size</var> be a basis to resolve font size values against,
      based on the [=SVGLength=]'s <a href='#LengthAssociatedElement'>associated element</a>:
        <dl class='switch'>
          <dt>has no <a href='#LengthAssociatedElement'>associated element</a></dt>
          <dd><var>font size</var> is the absolute length of the initial value of the {{font-size}} property</dd>
          <dt>has an <a href='#LengthAssociatedElement'>associated element</a></dt>
          <dd><var>size</var> is the computed value of the <a href='#LengthAssociatedElement'>associated element</a>'s {{font-size}} property</dd>
        </dl>
      </li>
      <li>Set the [=SVGLength=]'s {{LengthValue/value}} to the result of
      converting <var>absolute</var> to a <a>&lt;length&gt;</a> with an <span class='prop-value'>em</span>
      or <span class='prop-value'>ex</span> unit (depending on <var>unitType</var>),
      using <var>font size</var> as the {{font-size}} basis.</li>
    </ol>
  </li>
  <li>Otherwise:
    <ol>
      <li>Set the [=SVGLength=]'s {{LengthValue/value}} to the result of
      converting <var>absolute</var> to a <a>&lt;length&gt;</a> with the unit
      found by looking up <var>unitType</var> in the length unit type table above.</li>
    </ol>
  </li>
  <li>If the [=SVGLength=]
  <a href='#LengthMode'>reflects the base value</a> of a [=reflected=] attribute or
  <a href='#LengthMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>


<h4 id="InterfaceSVGAngle">Interface SVGAngle</h4>

<p>The [=SVGAngle=] interface is used to represent a value that
can be an <a>&lt;angle&gt;</a> or <a>&lt;number&gt;</a> value.

<p id="ReadOnlyAngle" class='ready-for-wider-review'>An [=SVGAngle=] object can be designated as <em>read only</em>,
which means that attempts to modify the object will result in an exception
being thrown, as described below. An [=SVGAngle=] reflected through the
animVal attribute is always <em>read only</em>.

<p id="AngleAssociatedElement">An [=SVGAngle=] object can be <em>associated</em>
with a particular element.  The associated element is used to
determine which element's content attribute to update if the object [=reflects=]
an attribute.  Unless otherwise described, an [=SVGAngle=] object is not
associated with any element.

<div class='ready-for-wider-review'>
<p id='AngleMode'>Every [=SVGAngle=] object operates in one of
two modes.  It can:

<ol>
  <li><em>reflect the base value</em> of a [=reflected=] animatable attribute
  (being exposed through the <a href="types.html#__svg__SVGAnimatedAngle__baseVal">baseVal</a>
  member of an [=SVGAnimatedAngle=]),</li>
  <li><em>be detached</em>, which is the case for [=SVGAngle=] objects created
  with <a href='struct.html#__svg__SVGSVGElement__createSVGAngle'>createSVGAngle</a>.</li>
</ol>
</div>

<p>An [=SVGAngle=] object maintains an internal <a>&lt;angle&gt;</a> or
<a>&lt;number&gt;</a> value, which is called its <dfn attribute for=AngleValue>value</dfn>.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAngle</b> {

  // Angle Unit Types
  const unsigned short <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNKNOWN">SVG_ANGLETYPE_UNKNOWN</a> = 0;
  const unsigned short <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNSPECIFIED">SVG_ANGLETYPE_UNSPECIFIED</a> = 1;
  const unsigned short <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_DEG">SVG_ANGLETYPE_DEG</a> = 2;
  const unsigned short <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_RAD">SVG_ANGLETYPE_RAD</a> = 3;
  const unsigned short <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_GRAD">SVG_ANGLETYPE_GRAD</a> = 4;

  readonly attribute unsigned short <a href="types.html#__svg__SVGAngle__unitType">unitType</a>;
           attribute float <a href="types.html#__svg__SVGAngle__value">value</a>;
           attribute float <a href="types.html#__svg__SVGAngle__valueInSpecifiedUnits">valueInSpecifiedUnits</a>;
           attribute DOMString <a href="types.html#__svg__SVGAngle__valueAsString">valueAsString</a>;

  undefined <a href="types.html#__svg__SVGAngle__newValueSpecifiedUnits">newValueSpecifiedUnits</a>(unsigned short unitType, float valueInSpecifiedUnits);
  undefined <a href="types.html#__svg__SVGAngle__convertToSpecifiedUnits">convertToSpecifiedUnits</a>(unsigned short unitType);
};</pre>

<p>The numeric angle unit type constants defined on [=SVGAngle=] are used
to represent the type of an [=SVGAngle=]'s {{AngleValue/value}}.
Their meanings are as follows:

<table class='vert'>
  <tr><th>Constant</th><th>Meaning</th></tr>
  <tr><td><b id="__svg__SVGAngle__SVG_ANGLETYPE_UNSPECIFIED">SVG_ANGLETYPE_UNSPECIFIED</b></td><td>A unitless <a>&lt;number&gt;</a> interpreted as a value in degrees.</td></tr>
  <tr><td><b id="__svg__SVGAngle__SVG_ANGLETYPE_DEG">SVG_ANGLETYPE_DEG</b></td><td>An <a>&lt;angle&gt;</a> with a <span class='prop-value'>deg</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGAngle__SVG_ANGLETYPE_RAD">SVG_ANGLETYPE_RAD</b></td><td>An <a>&lt;angle&gt;</a> with a <span class='prop-value'>rad</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGAngle__SVG_ANGLETYPE_GRAD">SVG_ANGLETYPE_GRAD</b></td><td>An <a>&lt;angle&gt;</a> with a <span class='prop-value'>grad</span> unit.</td></tr>
  <tr><td><b id="__svg__SVGAngle__SVG_ANGLETYPE_UNKNOWN">SVG_ANGLETYPE_UNKNOWN</b></td><td>Some other type of value.</td></tr>
</table>

Note: The use of numeric angle unit type constants is an anti-pattern and
new constant values will not be introduced for any other units or angle types supported by
[=SVGAngle=].  If other types of angles are supported and used, the [=SVGAngle=]
uses the <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNKNOWN">SVG_ANGLETYPE_UNKNOWN</a>
unit type.  See below for details on how the other properties of an [=SVGAngle=]
operate with these types of angles.

<p>The <b id="__svg__SVGAngle__unitType">unitType</b> IDL attribute represents
the type of value that the [=SVGAngle=]'s {{AngleValue/value}} is.
On getting <a href='#__svg__SVGAngle__unitType'>unitType</a>, the following steps
are run:

<ol class='algorithm'>
  <li>If the [=SVGAngle=]'s {{AngleValue/value}} is a unitless
  <a>&lt;number&gt;</a> or a <a>&lt;length&gt;</a> with a
  <span class='prop-value'>deg</span>,
  <span class='prop-value'>rad</span> or
  <span class='prop-value'>grad</span> unit, then return the corresponding constant
  value from the angle unit type table above.</li>
  <li>Otherwise, return <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNKNOWN">SVG_ANGLETYPE_UNKNOWN</a>.
    <p class='note'>For example, for an <a>&lt;angle&gt;</a> with a <span class='prop-value'>turn</span>
    unit, <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNKNOWN">SVG_ANGLETYPE_UNKNOWN</a>
    would be returned.
  </li>
</ol>

<p>The <b id="__svg__SVGAngle__value">value</b> IDL attribute represents
the [=SVGAngle=]'s {{AngleValue/value}} in degrees.
On getting <a href='#__svg__SVGAngle__value'>value</a>, the following steps
are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the [=SVGAngle=]'s {{AngleValue/value}}.</li>
  <li>If <var>value</var> is a <a>&lt;number&gt;</a>, return that number.</li>
  <li>Return the result of converting <var>value</var> to an angle in degrees.</li>
</ol>

<p>On setting <a href='#__svg__SVGAngle__value'>value</a>, the following steps
are run:

<ol class='algorithm'>
  <li>If the [=SVGAngle=] object is <a href='#ReadOnlyAngle'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>Let <var>value</var> be the value being assigned to
  <a href='#__svg__SVGAngle__value'>value</a>.</li>
  <li>Set the [=SVGAngle=]'s {{AngleValue/value}} to a
  <a>&lt;number&gt;</a> whose value is <var>value</var>.</li>
  <li>If the [=SVGAngle=]
  <a href='#AngleMode'>reflects the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>

<p>The <b id="__svg__SVGAngle__valueInSpecifiedUnits">valueInSpecifiedUnits</b> IDL attribute represents
the numeric factor of the [=SVGAngle=]'s {{AngleValue/value}}.
On getting <a href='#__svg__SVGAngle__valueInSpecifiedUnits'>valueInSpecifiedUnits</a>, the following steps
are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the [=SVGAngle=]'s {{AngleValue/value}}.</li>
  <li>If <var>value</var> is a <a>&lt;number&gt;</a>, return that number.</li>
  <li>Otherwise, <var>value</var> is an <a>&lt;angle&gt;</a> value.  Return
  the numeric factor before its unit.</li>
</ol>

<p>On setting <a href='#__svg__SVGAngle__valueInSpecifiedUnits'>valueInSpecifiedUnits</a>, the following steps
are run:

<ol class='algorithm'>
  <li>If the [=SVGAngle=] object is <a href='#ReadOnlyAngle'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>Let <var>value</var> be the value being assigned to
  <a href='#__svg__SVGAngle__valueInSpecifiedUnits'>valueInSpecifiedUnits</a>.</li>
  <li>If the [=SVGAngle=]'s {{AngleValue/value}} is a
  <a>&lt;number&gt;</a>, then update its value to <var>value</var>.</li>
  <li>Otherwise, if the [=SVGAngle=]'s {{AngleValue/value}}
  is an <a>&lt;angle&gt;</a>,
  then update its numeric factor to <var>value</var>.</li>
  <li>If the [=SVGAngle=]
  <a href='#AngleMode'>reflects the base value</a> of a [=reflected=] attribute or
  <a href='#AngleMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>

<p>The <b id="__svg__SVGAngle__valueAsString">valueAsString</b> IDL attribute represents
the [=SVGAngle=]'s {{AngleValue/value}} as a string.
On getting <a href='#__svg__SVGAngle__valueAsString'>valueAsString</a>, the following steps
are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the [=SVGAngle=]'s {{AngleValue/value}}.</li>
  <li>Let <var>string</var> be an empty string.</li>
  <li>Let <var>factor</var> be <var>value</var>'s numeric factor,
  if it is an <a>&lt;angle&gt;</a>,
  or <var>value</var> itself it is a <a>&lt;number&gt;</a>.</li>
  <li>Append to <var>string</var> an implementation
  specific string that, if parsed as a <a>&lt;number&gt;</a> using CSS syntax,
  would return the number value closest to <var>factor</var>, given the
  implementation's supported <a href="#Precision">real number precision</a>.</li>
  <li>If <var>value</var> is an <a>&lt;angle&gt;</a>,
  then append to <var>string</var> the canonical spelling of
  <var>value</var>'s unit.</li>
  <li>Return <var>string</var>.</li>
</ol>

<p>On setting <a href='#__svg__SVGAngle__valueAsString'>valueAsString</a>, the following steps
are run:

<ol class='algorithm'>
  <li>If the [=SVGAngle=] object is <a href='#ReadOnlyAngle'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>Let <var>value</var> be the value being assigned to
  <a href='#__svg__SVGAngle__valueAsString'>valueAsString</a>.</li>
  <li>Parse <var>value</var> using the CSS syntax
  [ <a>&lt;number&gt;</a> | <a>&lt;angle&gt;</a> ].</li>
  <li>If parsing failed, then [=throw=] a [=SyntaxError=].</li>
  <li>Otherwise, parsing succeeded.  Set [=SVGAngle=]'s {{AngleValue/value}}
  to the parsed value.</li>
  <li>If the [=SVGAngle=]
  <a href='#AngleMode'>reflects the base value</a> of a [=reflected=] attribute or
  <a href='#AngleMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>

<p>The <b id="__svg__SVGAngle__newValueSpecifiedUnits">newValueSpecifiedUnits</b>
method is used to set the [=SVGAngle=]'s value in a typed manner.  When
newValueSpecifiedUnits(unitType, valueInSpecifiedUnits) is called, the following
steps are run:

<ol class='algorithm'>
  <li>If the [=SVGAngle=] object is <a href='#ReadOnlyAngle'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>If <var>unitType</var> is
  <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNKNOWN">SVG_ANGLETYPE_UNKNOWN</a>
  or is a value that does not appear in the angle unit type table above,
  then [=throw=] a [=NotSupportedError=].</li>
  <li>Set [=SVGAngle=]'s {{AngleValue/value}} depending
  on the value of <var>unitType</var>:
    <dl class='switch'>
      <dt><a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNSPECIFIED">SVG_ANGLETYPE_UNSPECIFIED</a></dt>
      <dd>a <a>&lt;number&gt;</a> whose value is <var>valueInSpecifiedUnits</var></dd>
      <dt>anything else</dt>
      <dd>an <a>&lt;angle&gt;</a> whose numeric factor is <var>valueInSpecifiedUnits</var>
      and whose unit is as indicated by the angle unit type table above</dd>
    </dl>
  </li>
  <li>If the [=SVGAngle=]
  <a href='#AngleMode'>reflects the base value</a> of a [=reflected=] attribute or
  <a href='#AngleMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>

<p>The <b id="__svg__SVGAngle__convertToSpecifiedUnits">convertToSpecifiedUnits</b>
method is used to convert the [=SVGAngle=]'s value to a specific type.
When convertToSpecifiedUnits(unitType) is called, the following steps are run:

<ol class='algorithm'>
  <li>If the [=SVGAngle=] object is <a href='#ReadOnlyAngle'>read only</a>, then
  [=throw=] a [=NoModificationAllowedError=].</li>
  <li>If <var>unitType</var> is
  <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNKNOWN">SVG_ANGLETYPE_UNKNOWN</a>
  or is a value that does not appear in the angle unit type table above,
  then [=throw=] a [=NotSupportedError=].</li>
  <li>Let <var>degrees</var> be the value that would be returned from the
  <a href='#__svg__SVGAngle__value'>value</a> member.</li>
  <li>If <var>unitType</var> is <a href="types.html#__svg__SVGAngle__SVG_ANGLETYPE_UNSPECIFIED">SVG_ANGLETYPE_UNSPECIFIED</a>, then:
    <ol>
      <li>Set the [=SVGAngle=]'s {{AngleValue/value}} to a <a>&lt;number&gt;</a>
      whose value is <var>degrees</var>.</li>
    </ol>
  </li>
  <li>Otherwise:
    <ol>
      <li>Set the [=SVGAngle=]'s {{AngleValue/value}} to the result of
      converting <var>degrees</var> to an <a>&lt;angle&gt;</a> with the unit
      found by looking up <var>unitType</var> in the angle unit type table above.</li>
    </ol>
  </li>
  <li>If the [=SVGAngle=]
  <a href='#AngleMode'>reflects the base value</a> of a [=reflected=] attribute or
  <a href='#AngleMode'>reflects an element of the base value</a> of a [=reflected=] attribute,
  then [=reserialize=] the reflected attribute.
  </li>
</ol>


<h4 id="ListInterfaces">List interfaces</h4>

<div class="annotation svg2-requirement">
  <table>
    <tr>
      <th>SVG 2 Requirement:</th>
      <td>Make the SVGList* interfaces a bit more like other lists/arrays.</td>
    </tr>
    <tr>
      <th>Resolution:</th>
      <td><a href="http://www.w3.org/2011/02/28-svg-minutes.html#item04">Add array style indexing and .length and .item to svg list types.</a></td>
    </tr>
    <tr>
      <th>Purpose:</th>
      <td>To align with other array types (e.g. NodeList).  Already implemented in Opera and Firefox.</td>
    </tr>
    <tr>
      <th>Owner:</th>
      <td>Erik (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/2975">ACTION-2975</a>)</td>
    </tr>
    <tr>
      <th>Status:</th>
      <td>Done</td>
    </tr>
  </table>
</div>

<p>Some SVG attributes contain lists of values, and to represent these values
there are a number of SVG DOM <dfn id="TermListInterface" data-dfn-type="dfn" data-export="">list interfaces</dfn>, one
for each required element type – [=SVGNumberList=], [=SVGLengthList=],
[=SVGPointList=], [=SVGTransformList=] and [=SVGStringList=].
The first four are used to represent the base and
animated components of [=SVGAnimatedNumberList=], [=SVGAnimatedLengthList=],
[=SVGAnimatedPoints=] and [=SVGTransformList=] objects,
while the fifth, [=SVGStringList=], is used to [=reflect=] a
few unanimated attributes that take a list of strings.

<p>Most [=list interfaces=] take the following form:

<pre class="example">interface <b>SVG<var>Name</var>List</b> {

  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__length">length</a>;
  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__numberOfItems">numberOfItems</a>;

  undefined <a href="types.html#__svg__SVGNameList__clear">clear</a>();
  <var>Type</var> <a href="types.html#__svg__SVGNameList__initialize">initialize</a>(<var>Type</var> newItem);
  getter <var>Type</var> <a href="types.html#__svg__SVGNameList__getItem">getItem</a>(unsigned long index);
  <var>Type</var> <a href="types.html#__svg__SVGNameList__insertItemBefore">insertItemBefore</a>(<var>Type</var> newItem, unsigned long index);
  <var>Type</var> <a href="types.html#__svg__SVGNameList__replaceItem">replaceItem</a>(<var>Type</var> newItem, unsigned long index);
  <var>Type</var> <a href="types.html#__svg__SVGNameList__removeItem">removeItem</a>(unsigned long index);
  <var>Type</var> <a href="types.html#__svg__SVGNameList__appendItem">appendItem</a>(<var>Type</var> newItem);
  <a href="#__svg__SVGNameList__setter">setter</a> undefined (unsigned long index, <var>Type</var> newItem);
};</pre>

<p>where <var>Name</var> is a descriptive name for the list element's
("Number", "Length", "Point", "Transform" or "String") and <var>Type</var> is the IDL type of the
list's elements ([=SVGNumber=], [=SVGLength=], [=DOMPoint=], [=SVGTransform=] or <b>DOMString</b>).

<p>The [=SVGTransformList=] interface takes the above form but has
two additional methods on it.

<p class='ready-for-wider-review'>All [=list interface=] objects apart from [=SVGTransformList=]
reflect the base value of a reflected content
attribute.  [=SVGTransformList=] objects reflect a presentation
attribute (<span class="attr-name">transform</span>,
{{linearGradient/gradientTransform}} or {{pattern/patternTransform}}).
All [=list interface=] objects are associated with a particular element.
Unlike [=SVGLength=] and similar objects, there are no "detached"
[=list interface=] objects.

<p>A [=list interface=] object maintains an internal list of elements,
which is referred to in the text below simply as "the list".
The IDL attributes and methods are used to inspect and manipulate elements
of the list.  The list can also be changed in response to
changes to the reflected content attribute and to animation of
the content attribute (or, for [=SVGTransformList=] objects,
in response to changes to the computed value of the {{transform}}
property).

<p id="ReadOnlyList" class='ready-for-wider-review'>A [=list interface=] object can be designated as
<em>read only</em>, which means that attempts to modify the object will result
in an exception being thrown, as described below. [=List interface=] objects
reflected through the animVal IDL attribute are always <em>read only</em>.

<p id="ListSynchronize">A [=list interface=] object
is <dfn attribute for=TermSynchronizeList>synchronized</dfn> by running
the following steps:

<ol class='algorithm'>
  <li class='ready-for-wider-review'>Let <var>value</var> be the base value of the
    reflected content attribute (using the attribute's [=initial value=]
    if it is not present or invalid).</li>
  <li>Let <var>length</var> be the number of items in the list.</li>
  <li>Let <var>new length</var> be the number of values in <var>value</var>.
  If <var>value</var> is the keyword <span class='prop-value'>none</span>
  (as supported by the {{transform}} property), <var>new length</var>
  is 0.</li>

  <li>If the list element type is [=SVGNumber=], [=SVGLength=], [=DOMPoint=] or [=SVGTransform=], then:
    <ol>
      <li>If <var>length</var> &gt; <var>new length</var>, then:
        <ol>
          <li>[=Detach=] each object in the list at an index
          greater than or equal to <var>new length</var>.</li>
          <li>Truncate the list to length <var>new length</var>.</li>
          <li>Set <var>length</var> to <var>new length</var>.</li>
        </ol>
      </li>
      <li>While <var>length</var> &lt; <var>new length</var>:
        <ol>
          <li>Let <var>item</var> be a newly created
          object of the list element type.</li>
          <li>[=Attach=] <var>item</var> to this [=list interface=]
          object.</li>
          <li>Append <var>item</var> to the list.</li>
          <li>Set <var>length</var> to <var>length</var> + 1.</li>
        </ol>
      </li>
      <li>Let <var>index</var> be 0.</li>
      <li>While <var>index</var> &lt; <var>length</var>:
        <ol>
          <li>Let <var>item</var> be the object in the list at index
          <var>index</var>.</li>
          <li>Let <var>v</var> be the value in <var>value</var> at index
          <var>index</var>.</li>
          <li>Set <var>item</var>'s value to <var>v</var>.</li>
          <li>If <var>item</var> is an [=SVGTransform=] object, then
          set the components of its <a href="coords.html#TransformMatrixObject">matrix object</a>
          to match the new transform function value.</li>
          <li>Set <var>index</var> to <var>index</var> + 1.</li>
        </ol>
      </li>
    </ol>
  </li>
  <li>Otherwise, the list element type is <b>DOMString</b>:
    <ol>
      <li>Replace the list with a new list consisting
      of the values in <var>value</var>.</li>
    </ol>
  </li>
</ol>

<p>Whenever a list element object is to be <dfn id="TermDetach" data-dfn-type="dfn" data-export="">detached</dfn>,
the following steps are run, depending on the list element type:

<dl class='switch'>
  <dt>[=SVGNumber=]</dt>
  <dd>
    Set the [=SVGNumber=] to no longer be
    <a href="#NumberAssociatedElement">associated</a> with any element.
    If the [=SVGNumber=] is <a href='#ReadOnlyNumber'>read only</a>,
    set it to be no longer read only.
  </dd>
  <dt>[=SVGLength=]</dt>
  <dd>
    Set the [=SVGLength=] to no longer be
    <a href="#LengthAssociatedElement">associated</a> with any element.
    If the [=SVGLength=] is <a href='#ReadOnlyLength'>read only</a>,
    set it to be no longer read only.  Set the [=SVGLength=] to have
    unspecified <a href="#LengthAssociatedElement">directionality</a>.
  </dd>
  <dt>[=DOMPoint=]</dt>
  <dd>
    Set the [=DOMPoint=] to no longer be
    <a href="shapes.html#PointAssociatedElement">associated</a> with any element.
    If the [=DOMPoint=] is <a href='shapes.html#ReadOnlyPoint'>read only</a>,
    set it to be no longer read only.
  </dd>
  <dt>[=SVGTransform=]</dt>
  <dd>
    Set the [=SVGTransform=] to no longer be
    <a href="coords.html#TransformAssociatedElement">associated</a> with any element.
    If the [=SVGTransform=] is <a href='coords.html#ReadOnlyTransform'>read only</a>,
    set it to be no longer read only.
  </dd>
  <dt><b>DOMString</b></dt>
  <dd>Nothing is done.</dd>
</dl>

<p>Whenever a list element object is to be <dfn id="TermAttach" data-dfn-type="dfn" data-export="">attached</dfn>,
the following steps are run, depending on the list element type:
<div class='ready-for-wider-review'>
<dl class='switch'>
  <dt>[=SVGNumber=]</dt>
  <dd>
    <a href="#NumberAssociatedElement">Associate</a> the
    [=SVGNumber=] with the element that the [=list interface=]
    object is associated with.  Additionally, depending on which IDL attribute
    the [=list interface=] object is reflected through:
      <dl class='switch'>
        <dt>baseVal</dt>
        <dd>Set the [=SVGNumber=] to <a href="#NumberMode">reflect an
        element of the base value</a>.</dd>
        <dt>animVal</dt>
        <dd>Set the [=SVGNumber=] to <a href="#NumberMode">reflect an
        element of the base value</a>.</dd>
      </dl>
  </dd>
  <dt>[=SVGLength=]</dt>
  <dd>
    <a href="#LengthAssociatedElement">Associate</a> the
    [=SVGLength=] with the element that the [=list interface=]
    object is associated with and set its
    <a href="#LengthAssociatedElement">directionality</a> to that
    specified by the attribute being reflected.
    Additionally, depending on which IDL attribute the [=list interface=]
    object is reflected through:
      <dl class='switch'>
        <dt>baseVal</dt>
        <dd>Set the [=SVGLength=] to <a href="#LengthMode">reflect an
        element of the base value</a>.</dd>
        <dt>animVal</dt>
        <dd>Set the [=SVGLength=] to <a href="#LengthMode">reflect an
        element of the base value</a>. Set the [=SVGLength=] to be
        <em>read only</em>.</dd>
      </dl>
  </dd>
  <dt>[=DOMPoint=]</dt>
  <dd>
    <a href="shapes.html#PointAssociatedElement">Associate</a> the
    [=DOMPoint=] with the element that the [=list interface=]
    object is associated with.
    Additionally, depending on which IDL attribute the [=list interface=]
    object is reflected through:
      <dl class='switch'>
        <dt>baseVal</dt>
        <dd>Set the [=DOMPoint=] to <a href="shapes.html#PointMode">reflect an
        element of the base value</a>.</dd>
        <dt>animVal</dt>
        <dd>Set the [=DOMPoint=] to <a href="shapes.html#PointMode">reflect an
        element of the base value</a>.</dd>
      </dl>
  </dd>
  <dt>[=SVGTransform=]</dt>
  <dd>
    <a href="coords.html#TransformAssociatedElement">Associate</a> the
    [=SVGTransform=] with the element that the [=list interface=]
    object is associated with.
    Set the [=SVGTransform=] to <a href="coords.html#TransformMode">reflect an
    element of a presentation attribute value</a>.
  </dd>
  <dt><b>DOMString</b></dt>
  <dd>Nothing is done.</dd>
</dl>
</div>

<p>The <a href="http://heycam.github.io/webidl/#dfn-supported-property-indices">supported property indices</a>
of a [=list interface=] object is the set of all non-negative integers
less than the length of the list.

<p>The <b id="__svg__SVGNameList__length">length</b> and
<b id="__svg__SVGNameList__numberOfItems">numberOfItems</b> IDL attributes
represents the length of the list, and on getting simply return
the length of the list.

<p>The <b id="__svg__SVGNameList__clear">clear</b> method is used to
remove all items in the list.  When clear() is called, the following steps are run:
<ol class="algorithm">
  <li>If the list is <a href="#ReadOnlyList">read only</a>, then [=throw=] a
  [=NoModificationAllowedError=].</li>
  <li>[=Detach=] and then remove all elements in the list.</li>
  <li>If the list [=reflects=] an attribute, or represents the
  base value of an object that [=reflects=] an attribute, then
  [=reserialize=] the reflected attribute.</li>
</ol>

<p>The <b id="__svg__SVGNameList__initialize">initialize</b> method
is used to clear the list and add a single, specified value to it.
When initialize(<var>newItem</var>) is called, the following steps are run:

<ol class="algorithm">
  <li>If the list is <a href="#ReadOnlyList">read only</a>, then [=throw=] a
  [=NoModificationAllowedError=].</li>
  <li>[=Detach=] and then remove all elements in the list.</li>
  <li>If <var>newItem</var> is an object type, and <var>newItem</var>
  is not a detached object,  then set <var>newItem</var> to be
  a newly created object of the same type as <var>newItem</var>
  and which has the same (number or length) value.</li>
  <li>[=Attach=] <var>newItem</var> to the [=list interface=] object.</li>
  <li>Append <var>newItem</var> to this list.</li>
  <li>If the list [=reflects=] an attribute, or represents the
  base value of an object that [=reflects=] an attribute, then
  [=reserialize=] the reflected attribute.</li>
  <li>Return <var>newItem</var>.</li>
</ol>

<p>The <b id="__svg__SVGNameList__getItem">getItem</b> method is used
to get an item from the list at the specified position.  When
getItem(<var>index</var>) is called, the following steps are run:

<ol class="algorithm">
  <li>If <var>index</var> is greater than or equal to the length
  of the list, then [=throw=] an [=IndexSizeError=].</li>
  <li>Return the element in the list at position <var>index</var>.
    Note: Note that if the list's element type is an object type,
    such as [=SVGLength=], then a reference to that object and not
    a copy of it is returned.</li>
</ol>

<p>The <b id="__svg__SVGNameList__insertItemBefore">insertItemBefore</b>
method is used to insert an element into the list at a specific position.
When insertItemBefore(<var>newItem</var>, <var>index</var>) is called,
the following steps are run:

<ol class="algorithm">
  <li>If the list is <a href="#ReadOnlyList">read only</a>, then [=throw=] a
  [=NoModificationAllowedError=].</li>
  <li>If <var>newItem</var> is an object type, and <var>newItem</var>
  is not a detached object,  then set <var>newItem</var> to be
  a newly created object of the same type as <var>newItem</var>
  and which has the same (number or length) value.</li>
  <li>If <var>index</var> is greater than the length of the list, then
  set <var>index</var> to be the list length.</li>
  <li>Insert <var>newItem</var> into the list at index <var>index</var>.</li>
  <li>Attach <var>newItem</var> to the [=list interface=] object.</li>
  <li>If the list [=reflects=] an attribute, or represents the
  base value of an object that [=reflects=] an attribute, then
  [=reserialize=] the reflected attribute.</li>
  <li>Return <var>newItem</var>.</li>
</ol>

<p>The <b id="__svg__SVGNameList__replaceItem">replaceItem</b> method
is used to replace an existing item in the list with a new item.
When replaceItem(<var>newItem</var>, <var>index</var>) is called, the
following steps are run:

<ol class="algorithm">
  <li>If the list is <a href="#ReadOnlyList">read only</a>, then [=throw=] a
  [=NoModificationAllowedError=].</li>
  <li>If <var>index</var> is greater than or equal to the length of
  the list, then [=throw=] an [=IndexSizeError=].</li>
  <li>If <var>newItem</var> is an object type, and <var>newItem</var>
  is not a detached object, then set <var>newItem</var> to be
  a newly created object of the same type as <var>newItem</var>
  and which has the same (number or length) value.</li>
  <li>[=Detach=] the element in the list at index <var>index</var>.</li>
  <li>Replace the element in the list at index <var>index</var>
  with <var>newItem</var>.</li>
  <li>[=Attach=] <var>newItem</var> to the [=list interface=] object.</li>
  <li>If the list [=reflects=] an attribute, or represents the
  base value of an object that [=reflects=] an attribute, then
  [=reserialize=] the reflected attribute.</li>
  <li>Return <var>newItem</var>.</li>
</ol>

<p>The <b id="__svg__SVGNameList__removeItem">removeItem</b> method
is used to remove an item from the list.  When removeItem(<var>index</var>)
is called, the following steps are run:

<ol class="algorithm">
  <li>If the list is <a href="#ReadOnlyList">read only</a>, then [=throw=] a
  [=NoModificationAllowedError=].</li>
  <li>If <var>index</var> is greater than or equal to the length of
  the list, then [=throw=] an [=IndexSizeError=] with code.</li>
  <li>Let <var>item</var> be the list element at index <var>index</var>.</li>
  <li>[=Detach=] <var>item</var>.</li>
  <li>Remove the list element at index <var>index</var>.</li>
  <li>Return <var>item</var>.</li>
</ol>

<p>The <b id="__svg__SVGNameList__appendItem">appendItem</b> method
is used to append an item to the end of the list.  When appendItem(<var>newItem</var>)
is called, the following steps are run:

<ol class="algorithm">
  <li>If the list is <a href="#ReadOnlyList">read only</a>, then [=throw=] a
  [=NoModificationAllowedError=].</li>
  <li>If <var>newItem</var> is an object type, and <var>newItem</var>
  is not a detached object, then set <var>newItem</var> to be
  a newly created object of the same type as <var>newItem</var>
  and which has the same (number or length) value.</li>
  <li>Let <var>index</var> be the length of the list.</li>
  <li>Append <var>newItem</var> to the end of the list.</li>
  <li>[=Attach=] <var>newItem</var> to the [=list interface=] object.</li>
  <li>If the list [=reflects=] an attribute, or represents the
  base value of an object that [=reflects=] an attribute, then
  [=reserialize=] the reflected attribute.</li>
  <li>Return <var>newItem</var>.</li>
</ol>

<p>The behavior of the <b id="__svg__SVGNameList__setter">indexed property setter</b>
is the same as that for the <a href="#__svg__SVGNameList__replaceItem">replaceItem</a>
method.

<h4 id="InterfaceSVGNumberList">Interface SVGNumberList</h4>

<p>The [=SVGNumberList=] interface is a [=list interface=] whose
elements are [=SVGNumber=] objects.  An [=SVGNumberList=] object
represents a list of numbers.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGNumberList</b> {

  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__length">length</a>;
  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__numberOfItems">numberOfItems</a>;

  undefined <a href="types.html#__svg__SVGNameList__clear">clear</a>();
  <a>SVGNumber</a> <a href="types.html#__svg__SVGNameList__initialize">initialize</a>(<a>SVGNumber</a> newItem);
  getter <a>SVGNumber</a> <a href="types.html#__svg__SVGNameList__getItem">getItem</a>(unsigned long index);
  <a>SVGNumber</a> <a href="types.html#__svg__SVGNameList__insertItemBefore">insertItemBefore</a>(<a>SVGNumber</a> newItem, unsigned long index);
  <a>SVGNumber</a> <a href="types.html#__svg__SVGNameList__replaceItem">replaceItem</a>(<a>SVGNumber</a> newItem, unsigned long index);
  <a>SVGNumber</a> <a href="types.html#__svg__SVGNameList__removeItem">removeItem</a>(unsigned long index);
  <a>SVGNumber</a> <a href="types.html#__svg__SVGNameList__appendItem">appendItem</a>(<a>SVGNumber</a> newItem);
  <a href="#__svg__SVGNameList__setter">setter</a> undefined (unsigned long index, <a>SVGNumber</a> newItem);
};</pre>

<p>The behavior of all of the interface members of [=SVGNumberList=] are
defined in the <a href="#ListInterfaces">List interfaces</a> section above.


<h4 id="InterfaceSVGLengthList">Interface SVGLengthList</h4>

<p>The [=SVGLengthList=] interface is a [=list interface=] whose
elements are [=SVGLength=] objects.  An [=SVGLengthList=] object
represents a list of lengths.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGLengthList</b> {

  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__length">length</a>;
  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__numberOfItems">numberOfItems</a>;

  undefined <a href="types.html#__svg__SVGNameList__clear">clear</a>();
  <a>SVGLength</a> <a href="types.html#__svg__SVGNameList__initialize">initialize</a>(<a>SVGLength</a> newItem);
  getter <a>SVGLength</a> <a href="types.html#__svg__SVGNameList__getItem">getItem</a>(unsigned long index);
  <a>SVGLength</a> <a href="types.html#__svg__SVGNameList__insertItemBefore">insertItemBefore</a>(<a>SVGLength</a> newItem, unsigned long index);
  <a>SVGLength</a> <a href="types.html#__svg__SVGNameList__replaceItem">replaceItem</a>(<a>SVGLength</a> newItem, unsigned long index);
  <a>SVGLength</a> <a href="types.html#__svg__SVGNameList__removeItem">removeItem</a>(unsigned long index);
  <a>SVGLength</a> <a href="types.html#__svg__SVGNameList__appendItem">appendItem</a>(<a>SVGLength</a> newItem);
  <a href="#__svg__SVGNameList__setter">setter</a> undefined (unsigned long index, <a>SVGLength</a> newItem);
};</pre>

<p>The behavior of all of the interface members of [=SVGLengthList=] are
defined in the <a href="#ListInterfaces">List interfaces</a> section above.


<h4 id="InterfaceSVGStringList">Interface SVGStringList</h4>

<p>The [=SVGStringList=] interface is a [=list interface=] whose
elements are <b>DOMString</b> values.  An [=SVGStringList=] object
represents a list of strings.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGStringList</b> {

  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__length">length</a>;
  readonly attribute unsigned long <a href="types.html#__svg__SVGNameList__numberOfItems">numberOfItems</a>;

  undefined <a href="types.html#__svg__SVGNameList__clear">clear</a>();
  DOMString <a href="types.html#__svg__SVGNameList__initialize">initialize</a>(DOMString newItem);
  getter DOMString <a href="types.html#__svg__SVGNameList__getItem">getItem</a>(unsigned long index);
  DOMString <a href="types.html#__svg__SVGNameList__insertItemBefore">insertItemBefore</a>(DOMString newItem, unsigned long index);
  DOMString <a href="types.html#__svg__SVGNameList__replaceItem">replaceItem</a>(DOMString newItem, unsigned long index);
  DOMString <a href="types.html#__svg__SVGNameList__removeItem">removeItem</a>(unsigned long index);
  DOMString <a href="types.html#__svg__SVGNameList__appendItem">appendItem</a>(DOMString newItem);
  <a href="#__svg__SVGNameList__setter">setter</a> undefined (unsigned long index, DOMString newItem);
};</pre>

<p>The behavior of all of the interface members of [=SVGStringList=] are
defined in the <a href="#ListInterfaces">List interfaces</a> section above.


<h3 id="DOMInterfacesForReflectingSVGAttributes">DOM interfaces for reflecting animatable SVG attributes</h3>

<p>
  The following interfaces are used to represent the reflected value
  of animatable content attributes.
  They each consist of two component objects, representing the same data:
  <code>baseVal</code> and <code>animVal</code>.
  The <code>baseVal</code> (base value) object is modifiable,
  to update the corresponding attribute value.


<p class='note'>
  In SVG 1.1, the <code>animVal</code> attribute of the SVG DOM interfaces represented the
  current animated value of the reflected attribute. In this version of SVG,
  <code>animVal</code> no longer represents the current animated value and is instead an
  alias of <code>baseVal</code>.



<h4 id="InterfaceSVGAnimatedBoolean">Interface SVGAnimatedBoolean</h4>

<p>An [=SVGAnimatedBoolean=] object is used to [=reflect=] an
animatable attribute that takes a boolean value.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedBoolean</b> {
           attribute boolean <a href="types.html#__svg__SVGAnimatedBoolean__baseVal">baseVal</a>;
  readonly attribute boolean <a href="types.html#__svg__SVGAnimatedBoolean__animVal">animVal</a>;
};</pre>

<p class="ready-for-wider-review">The <b id="__svg__SVGAnimatedBoolean__baseVal">baseVal</b> and
<b id="__svg__SVGAnimatedBoolean__animVal">animVal</b> IDL attributes
both represent the current non-animated value of the reflected attribute.
On getting <a href="types.html#__svg__SVGAnimatedBoolean__baseVal">baseVal</a>
or <a href="types.html#__svg__SVGAnimatedBoolean__animVal">animVal</a>,
the following steps are run:

<ol class="algorithm">
  <li>Let <var>value</var> be the value of the reflected attribute,
  or the empty string if it is not present.</li>
  <li>If <var>value</var> is not "true" or "false", then set <var>value</var>
  to the reflected attribute's [=initial value=].</li>
  <li>Return true if <var>value</var> is "true", and false otherwise.</li>
</ol>

<p>On setting <a href="types.html#__svg__SVGAnimatedBoolean__baseVal">baseVal</a>,
the reflected attribute is set to "true" if the value is true, and "false"
otherwise.

<h4 id="InterfaceSVGAnimatedEnumeration">Interface SVGAnimatedEnumeration</h4>

<p>An [=SVGAnimatedEnumeration=] object is used to [=reflect=]
an animatable attribute that takes a keyword value (such as
the {{textPath/method}} attribute on {{textPath}}) or to reflect
the type of value that an animatable attribute has (done
only by the <a href='painting.html#__svg__SVGMarkerElement__orientType'>orientType</a>
IDL attribute for the {{marker element}} element's
{{marker/orient}} attribute).

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedEnumeration</b> {
           attribute unsigned short <a href="types.html#__svg__SVGAnimatedEnumeration__baseVal">baseVal</a>;
  readonly attribute unsigned short <a href="types.html#__svg__SVGAnimatedEnumeration__animVal">animVal</a>;
};</pre>

<p class='ready-for-wider-review'>For [=SVGAnimatedEnumeration=] objects that [=reflect=] an
animatable attribute that takes only a keyword value, the
<b id="__svg__SVGAnimatedEnumeration__baseVal">baseVal</b> and
<b id="__svg__SVGAnimatedEnumeration__animVal">animVal</b> IDL attributes
represents the current non-animated value of the reflected attribute.
For <a href='painting.html#__svg__SVGMarkerElement__orientType'>orientType</a>,
they represent the type of the current non-animated value of the
reflected {{marker/orient}} attribute.  On getting
<a href='#__svg__SVGAnimatedEnumeration__baseVal'>baseVal</a> or
<a href='#__svg__SVGAnimatedEnumeration__animVal'>animVal</a>, the
following steps are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the value of the reflected attribute
  (using the attribute's [=initial value=] if it is not present
  or invalid).</li>
  <li>Return the <dfn id="TermNumericTypeValue" data-dfn-type="dfn" data-export="">numeric type value</dfn>
  for <var>value</var>, according to the reflecting IDL attribute's
  definition.</li>
</ol>

<p>On setting <a href="types.html#__svg__SVGAnimatedEnumeration__baseVal">baseVal</a>,
the following steps are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the value being assigned to
  <a href="types.html#__svg__SVGAnimatedEnumeration__baseVal">baseVal</a>.</li>
  <li>If <var>value</var> is 0 or is not the [=numeric type value=]
  for any value of the reflected attribute, then throw a [=TypeError=].</li>
  <li>Otherwise, if the reflecting IDL attribute is
  <a href='painting.html#__svg__SVGMarkerElement__orientType'>orientType</a>
  and <var>value</var> is <a href='painting.html#__svg__SVGMarkerElement__SVG_MARKER_ORIENT_ANGLE'>SVG_MARKER_ORIENT_ANGLE</a>,
  then set the reflected attribute to the string "0".</li>
  <li>Otherwise, <var>value</var> is the [=numeric type value=]
  for a specific, single keyword value for the reflected attribute.
  Set the reflected attribute to that value.</li>
</ol>

<h4 id="InterfaceSVGAnimatedInteger">Interface SVGAnimatedInteger</h4>

<p>An [=SVGAnimatedInteger=] object is used to [=reflect=] an
animatable attribute that takes an integer value (such as
{{feTurbulence/numOctaves}} on {{feTurbulence}}).  It is also
used to reflect one part of an animatable attribute that takes
an integer followed by an optional second integer (such as
{{feConvolveMatrix/order}} on {{feConvolveMatrix}}).

Note: This [=SVGAnimatedInteger=] interface
is not used in this specification, however the
<a href="https://www.w3.org/TR/filter-effects/">Filter Effects</a>
specification has a number of uses of it.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedInteger</b> {
           attribute long <a href="types.html#__svg__SVGAnimatedInteger__baseVal">baseVal</a>;
  readonly attribute long <a href="types.html#__svg__SVGAnimatedInteger__animVal">animVal</a>;
};</pre>

<p class='ready-for-wider-review'>For [=SVGAnimatedInteger=] objects that [=reflect=]
an animatable attribute that takes a single integer value, the
<b id="__svg__SVGAnimatedInteger__baseVal">baseVal</b> and
<b id="__svg__SVGAnimatedInteger__animVal">animVal</b> IDL attributes
represent the current non-animated value of the reflected attribute.
For those that reflect one integer of an attribute that takes an
integer followed by an optional second integer, they represent the
current non-animated value of one of the two integers.  On getting
<a href="#__svg__SVGAnimatedInteger__baseVal">baseVal</a> or
<a href="#__svg__SVGAnimatedInteger__animVal">animVal</a>, the
following steps are run:

<ol class="algorithm">
  <li>Let <var>value</var> be the value of the reflected attribute
  (using the attribute's [=initial value=] if it is not present
  or invalid).</li>
  <li>If the reflected attribute is defined to take an integer
  followed by an optional second integer, then:
    <ol>
      <li>If this [=SVGAnimatedInteger=] object reflects the
      first integer, then return the first value in <var>value</var>.</li>
      <li>Otherwise, this [=SVGAnimatedInteger=] object reflects the
      second integer.  Return the second value in <var>value</var> if it has been
      explicitly specified, and if not, return the implicit value
      as described in the definition of the attribute.
      <p class='note'>For example, the definition of {{feConvolveMatrix/order}}
      says that the implicit second integer is the same as the explicit
      first integer.</li>
    </ol>
  </li>
  <li>Otherwise, the reflected attribute is defined to take a single
  integer value.  Return <var>value</var>.</li>
</ol>

<p>On setting <a href="#__svg__SVGAnimatedInteger__baseVal">baseVal</a>,
the following steps are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the value being assigned to
  <a href="types.html#__svg__SVGAnimatedInteger__baseVal">baseVal</a>.</li>
  <li>Let <var>new</var> be a list of integers.</li>
  <li>If the reflected attribute is defined to take an integer
  followed by an optional second integer, then:
    <ol>
      <li>Let <var>current</var> be the value of the reflected attribute
      (using the attribute's [=initial value=] if it is not present
      or invalid).</li>
      <li>Let <var>first</var> be the first integer in <var>current</var>.</li>
      <li>Let <var>second</var> be the second integer in <var>current</var>
      if it has been explicitly specified, and if not, the implicit value
      as described in the definition of the attribute.</li>
      <li>If this [=SVGAnimatedInteger=] object reflects the
      first integer, then set <var>first</var> to <var>value</var>.
      Otherwise, set <var>second</var> to <var>value</var>.</li>
      <li>Append <var>first</var> to <var>new</var>.</li>
      <li>Append <var>second</var> to <var>new</var>.</li>
    </ol>
  </li>
  <li>Otherwise, the reflected attribute is defined to take a single
  integer value.  Append <var>value</var> to <var>new</var>.</li>
  <li>Set the content attribute to a string consisting of each integer
  in <var>new</var> serialized to an implementation specific string that,
  if parsed as an <a>&lt;number&gt;</a> using CSS syntax, would return that
  integer, joined and separated by a single U+0020 SPACE character.</li>
</ol>

<h4 id="InterfaceSVGAnimatedNumber">Interface SVGAnimatedNumber</h4>

<p>An [=SVGAnimatedNumber=] object is used to [=reflect=] an
animatable attribute that takes a number value (such as
{{path/pathLength}} on {{path}}).  It is also
used to reflect one part of an animatable attribute that takes
an number followed by an optional second number (such as
{{feDiffuseLighting/kernelUnitLength}} on {{feDiffuseLighting}}).

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedNumber</b> {
           attribute float <a href="types.html#__svg__SVGAnimatedNumber__baseVal">baseVal</a>;
  readonly attribute float <a href="types.html#__svg__SVGAnimatedNumber__animVal">animVal</a>;
};</pre>

<p class='ready-for-wider-review'>For [=SVGAnimatedNumber=] objects that [=reflect=]
an animatable attribute that takes a single number value, the
<b id="__svg__SVGAnimatedNumber__baseVal">baseVal</b> and
<b id="__svg__SVGAnimatedNumber__animVal">animVal</b> IDL attributes
represent the current non-animated value of the reflected attribute.
For those that reflect one number of an attribute that takes a
number followed by an optional second number, they represent the
current non-animated value of one of the two numbers.  On getting
<a href="#__svg__SVGAnimatedNumber__baseVal">baseVal</a> or
<a href="#__svg__SVGAnimatedNumber__animVal">animVal</a>, the
following steps are run:

<ol class="algorithm">
  <li>Let <var>value</var> be the value of the reflected attribute
  (using the attribute's [=initial value=] if it is not present
  or invalid).</li>
  <li>If the reflected attribute is defined to take an number
  followed by an optional second number, then:
    <ol>
      <li>If this [=SVGAnimatedNumber=] object reflects the
      first number, then return the first value in <var>value</var>.</li>
      <li>Otherwise, this [=SVGAnimatedNumber=] object reflects the
      second number.  Return the second value in <var>value</var> if it has been
      explicitly specified, and if not, return the implicit value
      as described in the definition of the attribute.
      <p class='note'>For example, the definition of {{feDiffuseLighting/kernelUnitLength}}
      says that the implicit second number is the same as the explicit
      first number.</li>
    </ol>
  </li>
  <li>Otherwise, the reflected attribute is defined to take a single
  number value.  Return <var>value</var>.</li>
</ol>

<p>On setting <a href="#__svg__SVGAnimatedNumber__baseVal">baseVal</a>,
the following steps are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the value being assigned to
  <a href="types.html#__svg__SVGAnimatedNumber__baseVal">baseVal</a>.</li>
  <li>Let <var>new</var> be a list of numbers.</li>
  <li>If the reflected attribute is defined to take an number
  followed by an optional second number, then:
    <ol>
      <li>Let <var>current</var> be the value of the reflected attribute
      (using the attribute's [=initial value=] if it is not present
      or invalid).</li>
      <li>Let <var>first</var> be the first number in <var>current</var>.</li>
      <li>Let <var>second</var> be the second number in <var>current</var>
      if it has been explicitly specified, and if not, the implicit value
      as described in the definition of the attribute.</li>
      <li>If this [=SVGAnimatedNumber=] object reflects the
      first number, then set <var>first</var> to <var>value</var>.
      Otherwise, set <var>second</var> to <var>value</var>.</li>
      <li>Append <var>first</var> to <var>new</var>.</li>
      <li>Append <var>second</var> to <var>new</var>.</li>
    </ol>
  </li>
  <li>Otherwise, the reflected attribute is defined to take a single
  number value.  Append <var>value</var> to <var>new</var>.</li>
  <li>Set the content attribute to a string consisting of each number
  in <var>new</var> serialized to an implementation specific string that,
  if parsed as an <a>&lt;number&gt;</a> using CSS syntax, would return the
  value closest to the number (given the implementation's supported
  <a href='#Precision'>Precision</a>real number precision),
  joined and separated by a single U+0020 SPACE character.</li>
</ol>

<h4 id="InterfaceSVGAnimatedLength">Interface SVGAnimatedLength</h4>

<!--
<div class="annotation svg2-requirement">
  <table>
    <tr><th>SVG 2 Requirement:</th>
    <td>Make it easier to read and write to attributes in the SVG DOM.</td></tr>
    <tr><th>Resolution:</th>
    <td><a href="http://www.w3.org/2011/10/27-svg-irc#T18-19-13">We will make it easier to read and write to attributes in the SVG DOM in SVG2.</a></td></tr>
    <tr><th>Purpose:</th>
    <td>To avoid the awkward access to the base values of [=SVGAnimatedLength=]s.</td></tr>
    <tr><th>Owner:</th>
    <td>Cameron (<a href="http://www.w3.org/Graphics/SVG/WG/track/actions/3414">ACTION-3414</a>)</td></tr>
  </table>
</div>
-->
<p class='ready-for-wider-review'>An [=SVGAnimatedLength=] object is used to [=reflect=] either
(a) an animatable attribute that takes a <a>&lt;length&gt;</a>,
<a>&lt;percentage&gt;</a> or <a>&lt;number&gt;</a> value, or (b) a
CSS property that takes one of these values and its corresponding
presentation attribute.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedLength</b> {
  [<a>SameObject</a>] readonly attribute <a>SVGLength</a> <a href="types.html#__svg__SVGAnimatedLength__baseVal">baseVal</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGLength</a> <a href="types.html#__svg__SVGAnimatedLength__animVal">animVal</a>;
};</pre>

<p class='ready-for-wider-review'>The <b id="__svg__SVGAnimatedLength__baseVal">baseVal</b> and
<b id="__svg__SVGAnimatedLength__animVal">animVal</b> IDL attributes
represent the current value of the reflected content attribute.
On getting <a href="#__svg__SVGAnimatedLength__baseVal">baseVal</a> or
<a href="#__svg__SVGAnimatedLength__animVal">animVal</a>,
an [=SVGLength=] object is returned that:

<ul>
  <li>either <a href='#LengthMode'>reflects the base value</a> of the
  reflected attribute or <a href='#LengthMode'>reflects the
  given presentation attribute</a>,</li>
  <li>is <a href='#LengthAssociatedElement'>associated with</a> the SVG element that
  the object with the reflecting IDL attribute of type [=SVGAnimatedLength=]
  was obtained from, and</li>
  <li>has a <a href='#LengthAssociatedElement'>directionality</a> as defined by the
  specific reflected attribute.</li>
</ul>

<h4 id="InterfaceSVGAnimatedAngle">Interface SVGAnimatedAngle</h4>

<p>An [=SVGAnimatedAngle=] object is used to [=reflect=]
the <a>&lt;angle&gt;</a> value of the animated {{marker/orient}}
attribute on {{marker element}}, through the
<a href='painting.html#__svg__SVGMarkerElement__orientAngle'>orientAngle</a>
IDL attribute.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedAngle</b> {
  [<a>SameObject</a>] readonly attribute <a>SVGAngle</a> <a href="types.html#__svg__SVGAnimatedAngle__baseVal">baseVal</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAngle</a> <a href="types.html#__svg__SVGAnimatedAngle__animVal">animVal</a>;
};</pre>


<p class='ready-for-wider-review'>The <b id="__svg__SVGAnimatedAngle__baseVal">baseVal</b> and
<b id="__svg__SVGAnimatedAngle__animVal">animVal</b> IDL attributes represent
the current non-animated <a>&lt;angle&gt;</a> value of the
reflected {{marker/orient}} attribute.  On getting
<a href="#__svg__SVGAnimatedAngle__baseVal">baseVal</a> or
<a href="#__svg__SVGAnimatedAngle__animVal">animVal</a>, an
[=SVGAngle=] object is returned that:

<ul>
  <li><a href='#AngleMode'>reflects the base value</a> of the
  reflected {{marker/orient}} attribute, and</li>
  <li>is <a href='#AngleAssociatedElement'>associated with</a> the SVG {{marker element}}
  element that the object with the reflecting IDL attribute of type
  [=SVGAnimatedAngle=] was obtained from.</li>
</ul>

<h4 id="InterfaceSVGAnimatedString">Interface SVGAnimatedString</h4>

<p>An [=SVGAnimatedString=] object is used to [=reflect=] an
animatable attribute that takes a string value.  It can optionally
be defined to additionally reflect a second, deprecated attribute.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedString</b> {
           attribute (DOMString or TrustedScriptURL) <a href="types.html#__svg__SVGAnimatedString__baseVal">baseVal</a>;
  readonly attribute DOMString <a href="types.html#__svg__SVGAnimatedString__animVal">animVal</a>;
};</pre>

<p class='ready-for-wider-review'>The <b id="__svg__SVGAnimatedString__baseVal">baseVal</b>
and <b id="__svg__SVGAnimatedString__animVal">animVal</b> IDL attributes
represent the current non-animated value of the reflected attribute.
On getting <a href="types.html#__svg__SVGAnimatedString__baseVal">baseVal</a>
or <a href="types.html#__svg__SVGAnimatedString__animVal">animVal</a>,
the following steps are run:

<ol class="algorithm">
  <li>If the reflected attribute is not present, then:
    <ol>
      <li>If the [=SVGAnimatedString=] object is defined to additionally
      reflect a second, deprecated attribute, and that attribute is present,
      then return its value.</li>
      <li>Otherwise, if the reflected attribute has an [=initial value=],
      then return it.</li>
      <li>Otherwise, return the empty string.</li>
    </ol>
  </li>
  <li>Otherwise, the reflected attribute is present.  Return its value.</li>
</ol>

<p class='note'>For the <a href='#__svg__SVGURIReference__href'>href</a>
member on the [=SVGURIReference=] interface, this will result in
the deprecated {{xlink:href}} attribute being returned if it is
present and the <span class="attr-name">href</span> attribute is not,
and in the <span class="attr-name">href</span> attribute being
returned in all other cases.

<p>On setting <a href="types.html#__svg__SVGAnimatedString__baseVal">baseVal</a>,
the following steps are run:

<ol class='algorithm'>
  <li>If the reflected attribute’s element is an [=SVGScriptElement=], let <var>value</var> be the result of
    executing the <a href="https://www.w3.org/TR/trusted-types/#get-trusted-type-compliant-string-algorithm">Get Trusted Type compliant string</a>
    algorithm, with <a href="https://www.w3.org/TR/trusted-types/#trustedscripturl">TrustedScriptURL</a>,
    reflected attribute’s Document's relevant global object, 'SVGScriptElement href', and 'script'.</li>
  <li>Otherwise, let value be the specified value.</li>
  <li>If the reflected attribute is not present,
  the [=SVGAnimatedString=] object is defined to additionally reflect
  a second, deprecated attribute, and that deprecated attribute is present,
  then set that deprecated attribute to value.</li>
  <li>Otherwise, set the reflected attribute to value.</li>
</ol>

<p class='note'> SVG does not have a complete script processing model <a href="https://github.com/w3c/svgwg/issues/196">yet</a>.
<a href="https://www.w3.org/TR/trusted-types/">Trusted Types</a> assumes that the attribute and
text body modification protections behave similarly to ones for HTML scripts.

<p class='note'>For the <a href='#__svg__SVGURIReference__href'>href</a>
member on the [=SVGURIReference=] interface, this will result in
the deprecated {{xlink:href}} attribute being set if it is
present and the <span class="attr-name">href</span> attribute is not,
and in the <span class="attr-name">href</span> attribute being
set in all other cases.

<h4 id="InterfaceSVGAnimatedRect">Interface SVGAnimatedRect</h4>

<p>An [=SVGAnimatedRect=] object is used to [=reflect=] an
animatable attribute that takes a rectangle value as specified
by an <var>x</var>, <var>y</var>, <var>width</var> and <var>height</var>.

Note: In this specification the only attribute to be
reflected as an [=SVGAnimatedRect=] is {{viewBox}}.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedRect</b> {
  [<a>SameObject</a>] readonly attribute <a>DOMRect</a> <a href="types.html#__svg__SVGAnimatedRect__baseVal">baseVal</a>;
  [<a>SameObject</a>] readonly attribute <a>DOMRectReadOnly</a> <a href="types.html#__svg__SVGAnimatedRect__animVal">animVal</a>;
};</pre>

<p class='ready-for-wider-review'>The <b id="__svg__SVGAnimatedRect__baseVal">baseVal</b>
and <b id="__svg__SVGAnimatedRect__animVal">animVal</b> IDL
attributes represent the current non-animated rectangle value of
the reflected attribute.  On getting <a href="#__svg__SVGAnimatedRect__baseVal">baseVal</a>
or <a href="#__svg__SVGAnimatedRect__animVal">animVal</a>,
a [=DOMRect=] object is returned.

<p class='ready-for-wider-review'>Upon creation of the <a href="#__svg__SVGAnimatedRect__baseVal">baseVal</a>
or <a href="#__svg__SVGAnimatedRect__animVal">animVal</a>
[=DOMRect=] objects, and afterwards whenever the reflected content attribute
is added, removed, or changed, the following steps are run:

<ol class='algorithm'>
  <li>Let <var>value</var> be the value of the reflected attribute
  (using the attribute's [=initial value=] if it is not present
  or invalid).</li>
  <li>Let <var>x</var>, <var>y</var>, <var>width</var> and <var>height</var>
  be those corresponding components of <var>value</var>.</li>
  <li>Set the [=DOMRect=] object's
  <a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#x-coordinate">x coordinate</a>,
  <a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#y-coordinate">y coordinate</a>,
  <a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#width">width</a> and
  <a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#height">height</a>
  to <var>x</var>, <var>y</var>, <var>width</var> and <var>height</var>,
  respectively.</li>
</ol>

<p class='ready-for-wider-review'>Whenever the
<a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#x-coordinate">x coordinate</a>,
<a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#y-coordinate">y coordinate</a>,
<a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#width">width</a> or
<a href="https://www.w3.org/TR/2014/WD-geometry-1-20140522/#height">height</a> property
of the <a href="#__svg__SVGAnimatedRect__baseVal">baseVal</a> or
<a href="#__svg__SVGAnimatedRect__animVal">animVal</a>
[=DOMRect=] object changes, except as part of the previous algorithm that
reflects the value of the content attribute into the [=DOMRect=], the reflected
content attribute must be [=reserialized=].

<h4 id="InterfaceSVGAnimatedNumberList">Interface SVGAnimatedNumberList</h4>

<p>An [=SVGAnimatedNumberList=] object is used to [=reflect=] an animatable
attribute that takes a list of <a>&lt;number&gt;</a> values.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedNumberList</b> {
  [<a>SameObject</a>] readonly attribute <a>SVGNumberList</a> <a href="types.html#__svg__SVGAnimatedNumberList__baseVal">baseVal</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGNumberList</a> <a href="types.html#__svg__SVGAnimatedNumberList__animVal">animVal</a>;
};</pre>

<p class='ready-for-wider-review'>The <b id="__svg__SVGAnimatedNumberList__baseVal">baseVal</b>
and <b id="__svg__SVGAnimatedNumberList__animVal">animVal</b> IDL attributes
represent the current non-animated value of the reflected attribute.
On getting <a href="#__svg__SVGAnimatedNumberList__baseVal">baseVal</a> or
<a href="#__svg__SVGAnimatedNumberList__animVal">animVal</a>,
an [=SVGNumberList=] object is returned that reflects the base value
of the reflected attribute.

<h4 id="InterfaceSVGAnimatedLengthList">Interface SVGAnimatedLengthList</h4>

<p>An [=SVGAnimatedLengthList=] object is used to [=reflect=] an animatable
attribute that takes a list of <a>&lt;length&gt;</a>, <a>&lt;percentage&gt;</a>
or <a>&lt;number&gt;</a> values.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGAnimatedLengthList</b> {
  [<a>SameObject</a>] readonly attribute <a>SVGLengthList</a> <a href="types.html#__svg__SVGAnimatedLengthList__baseVal">baseVal</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGLengthList</a> <a href="types.html#__svg__SVGAnimatedLengthList__animVal">animVal</a>;
};</pre>

<p class='ready-for-wider-review'>The <b id="__svg__SVGAnimatedLengthList__baseVal">baseVal</b>
or <b id="__svg__SVGAnimatedLengthList__animVal">animVal</b> IDL attributes
represent the current non-animated value of the reflected attribute.
On getting <a href="#__svg__SVGAnimatedLengthList__baseVal">baseVal</a> or
<a href="#__svg__SVGAnimatedLengthList__animVal">animVal</a>,
an [=SVGLengthList=] object is returned that reflects the base value
of the reflected attribute.


<h3 id="OtherDOMInterfaces">Other DOM interfaces</h3>


<h4 id="InterfaceSVGUnitTypes">Interface SVGUnitTypes</h4>

<p>The [=SVGUnitTypes=] interface defines a commonly used set of constants
used for reflecting {{linearGradient/gradientUnits}}, {{pattern/patternContentUnits}} and
other similar attributes.

<pre class="idl">[<a>Exposed</a>=Window]
interface <b>SVGUnitTypes</b> {
  // Unit Types
  const unsigned short <a href="types.html#__svg__SVGUnitTypes__SVG_UNIT_TYPE_UNKNOWN">SVG_UNIT_TYPE_UNKNOWN</a> = 0;
  const unsigned short <a href="types.html#__svg__SVGUnitTypes__SVG_UNIT_TYPE_USERSPACEONUSE">SVG_UNIT_TYPE_USERSPACEONUSE</a> = 1;
  const unsigned short <a href="types.html#__svg__SVGUnitTypes__SVG_UNIT_TYPE_OBJECTBOUNDINGBOX">SVG_UNIT_TYPE_OBJECTBOUNDINGBOX</a> = 2;
};</pre>

<p>The unit type constants defined on [=SVGUnitTypes=] have the following meanings:

<table class='vert'>
  <tr><th>Constant</th><th>Meaning</th></tr>
  <tr><td><b id="__svg__SVGUnitTypes__SVG_UNIT_TYPE_USERSPACEONUSE">SVG_UNIT_TYPE_USERSPACEONUSE</b></td><td>Corresponds to the <span class='attr-value'>'userSpaceOnUse'</span> attribute value.</td></tr>
  <tr><td><b id="__svg__SVGUnitTypes__SVG_UNIT_TYPE_OBJECTBOUNDINGBOX">SVG_UNIT_TYPE_OBJECTBOUNDINGBOX</b></td><td>Corresponds to the <span class='attr-value'>'objectBoundingBox'</span> attribute value.</td></tr>
  <tr><td><b id="__svg__SVGUnitTypes__SVG_UNIT_TYPE_UNKNOWN">SVG_UNIT_TYPE_UNKNOWN</b></td><td>Some other type of value.</td></tr>
</table>


<h3 id="InterfaceSVGTests" data-dfn-type="interface" data-lt="SVGTests">Mixin SVGTests</h3>

<p>The [=SVGTests=] interface is used to reflect
[=conditional processing attributes=], and is mixed in to other
interfaces for elements that support these attributes.

<pre class="idl">interface mixin <b>SVGTests</b> {
  [<a>SameObject</a>] readonly attribute <a>SVGStringList</a> <a href="types.html#__svg__SVGTests__requiredExtensions">requiredExtensions</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGStringList</a> <a href="types.html#__svg__SVGTests__systemLanguage">systemLanguage</a>;
};</pre>

<p>The <b id="__svg__SVGTests__requiredExtensions">requiredExtensions</b> IDL attribute
[=reflects=] the {{requiredExtensions}} content attribute.

<p>The <b id="__svg__SVGTests__systemLanguage">systemLanguage</b> IDL attribute
[=reflects=] the {{systemLanguage}} content attribute.


<h3 id="InterfaceSVGFitToViewBox" data-dfn-type="interface" data-lt="SVGFitToViewBox">Mixin SVGFitToViewBox</h3>

<p>The [=SVGFitToViewBox=] interface is used to reflect
the {{viewBox}} and {{preserveAspectRatio}} attributes,
and is mixed in to other interfaces for elements that support
these two attributes.

<pre class="idl">interface mixin <b>SVGFitToViewBox</b> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedRect</a> <a href="types.html#__svg__SVGFitToViewBox__viewBox">viewBox</a>;
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedPreserveAspectRatio</a> <a href="types.html#__svg__SVGFitToViewBox__preserveAspectRatio">preserveAspectRatio</a>;
};</pre>

<p>The <b id="__svg__SVGFitToViewBox__viewBox">viewBox</b> IDL attribute
[=reflects=] the {{viewBox}} content attribute.

<p>The <b id="__svg__SVGFitToViewBox__preserveAspectRatio">preserveAspectRatio</b> IDL attribute
[=reflects=] the {{preserveAspectRatio}} content attribute.


<h3 id="InterfaceSVGURIReference" data-dfn-type="interface" data-lt="SVGURIReference">Mixin SVGURIReference</h3>

<p>The [=SVGURIReference=] interface is used to reflect
the <span class="attr-name">href</span> attribute and the deprecated
{{xlink:href}} attribute.

<pre class="idl">interface mixin <b>SVGURIReference</b> {
  [<a>SameObject</a>] readonly attribute <a>SVGAnimatedString</a> <a href="types.html#__svg__SVGURIReference__href">href</a>;
};</pre>

<p>The <b id="__svg__SVGURIReference__href">href</b> IDL attribute
represents the value of the <span class="attr-name">href</span>
attribute, and, on elements that are defined to support it,
the deprecated {{xlink:href}} attribute.  On getting
<a href='#__svg__SVGURIReference__href'>href</a>, an
[=SVGAnimatedString=] object is returned that:

<ul>
  <li>reflects the <span class="attr-name">href</span> attribute, and</li>
  <li>if the element is defined to support the deprecated
  {{xlink:href}} attribute, additionally reflects that deprecated attribute.</li>
</ul>

<p class='note'>The [=SVGAnimatedString=] interface is defined
to reflect, through its <a href='#__svg__SVGAnimatedString__baseVal'>baseVal</a>
and <a href='#__svg__SVGAnimatedString__animVal'>animVal</a> members, the deprecated
{{xlink:href}} attribute, if that attribute is
present and the <span class="attr-name">href</span> is not, and to
reflect the <span class="attr-name">href</span> attribute in all
other circumstances. <a href="https://svgwg.org/specs/animations/">Animation elements</a>
treat <span class='attr-value'>attributeName='xlink:href'</span>
as being an alias for targeting the <span class="attr-name">href</span> attribute.