<h2 id="conformance">
Conformance Criteria</h2>

<h3 id="conformance-overview">
Overview</h3>

    Graphics defined with SVG have many different applications.
    As a result, not all software that uses SVG will have the same 
    features. Conformance to the SVG specification is therefore not a 
    binary matter; software may be conforming within a restricted 
    feature set.

    Furthermore, SVG is designed to be integrated into other types of 
    documents; depending on the type of integration, only a limited 
    feature-set may be appropriate. There are various ways that an SVG 
    document fragment can be referenced by or included in other 
    documents and thereby be processed by a user agent.  SVG documents 
    can also be viewed directly, as the primary document. Each 
    different method by which an SVG document fragment can be used 
    implies a certain set of requirements on how the SVG document
    fragment must be processed.

    This chapter therefore defines a number of [=processing modes=]
    that encompass the different combinations of features which may be 
    enabled or disabled in the document. In addition, it specifies 
    normative requirements for which processing mode must be used when 
    SVG documents reference or embed other SVG documents. The same set 
    of processing modes may be used by reference in other 
    specifications to describe how SVG documents should be processed.

    Note: This document does not place normative requirements on other 
    specifications that can reference or include SVG documents, such 
    as HTML and various CSS specifications.  The intention is for 
    these other specifications to normatively point to the appropriate 
    processing mode from this document.

    This chapter also outlines specific conformance requirements
    for <a href="#DocumentConformanceClasses">different types of SVG 
    content</a>, and <a href="#SoftwareConformanceClasses">different 
    classes of software</a> that use or create SVG.

<h3 id="processing-modes-section">
Processing modes</h3>

    This section defines a standard set of <dfn>processing modes</dfn> 
    for SVG documents.  Each processing mode specifies whether certain 
    high level SVG features are enabled.

<h4 id="features">
Features</h4>

    The features that can be enabled or disabled depending
    on the processing mode are as follows:

    <dl>
        <dt><dfn>declarative animation</dfn>
        <dd>
            Declarative animation includes both the animation elements 
            in SVG – <{animate}>, <{animateMotion}>, 
            <{animateTransform}> and <{set}> – and CSS Transitions and 
            Animations (see the [[#animation]] for details).
            When declarative animations are disabled in an SVG 
            document, any animation elements or CSS Transitions or 
            Animations must not be applied or run.

            Note: This is not the same as pausing the document's 
            animated state at <code>0s</code> document time; if an 
            animation is defined to begin at <code>0s</code>, it still 
            will not be applied.

        <dt><dfn dfn export>references to external resources</dfn>
        <dd>
            References to [=external file reference|external resources=] are URLs references
            or network access requests made by markup, style 
            properties, script or other Web platform features used in 
            the document, except for:
        
            <ul>
                <li>
                    [=same-document URL references=], as defined in 
                    [[#linking]].

                <li>
                    [=data URL=] references, as defined by
                    [[rfc2397#section-2|the "data" URL scheme]],
                    [[rfc2397]]
            </ul>

            When external references are disabled in an SVG document, 
            any attempt to fetch a document through an external 
            reference must instead be treated as if a network error 
            occurred and no data was received.
            
            When external references are enabled, user agents that 
            support external file requests from the Internet must 
            adhere to the restrictions on cross-origin resource 
            fetching, as outlined in [[#processingURL-fetch]].

        <dt><dfn>script execution</dfn>
        <dd>
            Script execution is the execution of any SVG [[SVG2#ScriptElement|&lt;script>]]
            elements, script found in [=event attributes=] (such as 
            [=event attribute|onclick=] on SVG elements), or any other 
            script defined 
            by other Web platform features used in the document, such 
            as any HTML <{script}> elements. When script execution is 
            disabled in an SVG document, no script in the document 
            must be run.


        <dt><dfn>interaction</dfn>
        <dd>
            Interaction refers to the delivery of DOM Events or the 
            invocation of any user agent specific UI behaviors such as 
            text selection, focus changing, link traversal, or 
            animation or transition triggering that is done in 
            response to user input such as mouse or keyboard activity.
            When interaction is disabled in an SVG document, any user 
            input events that would be targetted at the document or 
            any elements within the document must have no effect.

<h4 id="dynamic-interactive-mode">
Dynamic interactive mode</h4>

    This [=processing mode=] imposes no restrictions on any
    feature of the SVG language.

    <table class="features">
    <caption>Dynamic Interactive Features</caption>
    <tbody>
        <tr>
            <th>script execution</th>
            <td>yes</td>
        </tr>
        <tr>
            <th>external references</th>
            <td>yes</td>
        </tr>
        <tr>
            <th>declarative animation</th>
            <td>yes</td>
        </tr>
        <tr>
            <th>interactivity</th>
            <td>yes</td>
        </tr>
        </tbody>
    </table>

<h4 id="animated-mode">
Animated mode</h4>

    This [=processing mode=] is intended for circumstances where an 
    SVG document is to be used as an animated image that is allowed to 
    resolve external references, but which is not intended to be used
    as an interactive document.

    <table class="features">
    <caption>Animated Features</caption>
    <tbody>
        <tr>
        <th>script execution</th>
        <td>no</td>
        </tr>
        <tr>
        <th>external references</th>
        <td>yes</td>
        </tr>
        <tr>
        <th>declarative animation</th>
        <td>yes</td>
        </tr>
        <tr>
        <th>interactivity</th>
        <td>no</td>
        </tr>
    </tbody>
    </table>

<h4 id="secure-animated-mode">
Secure animated mode</h4>

    This [=processing mode=] is intended for circumstances where an 
    SVG document is to be used as an animated image that is not 
    allowed to resolve external references, and which is not intended 
    to be used as an interactive document.  This mode might be used 
    where image support has traditionally been limited to raster 
    images (such as JPEG, PNG and GIF).

    <table class="features">
        <caption>Secure Animated Features</caption>
        <tbody>
        <tr>
            <th>script execution</th>
            <td>no</td>
        </tr>
        <tr>
            <th>external references</th>
            <td>no</td>
        </tr>
        <tr>
            <th>declarative animation</th>
            <td>yes</td>
        </tr>
        <tr>
            <th>interactivity</th>
            <td>no</td>
        </tr>
        </tbody>
    </table>

<h4 id="static-mode">
Static mode</h4>

    This [=processing mode=] is intended for circumstances where an 
    SVG document is to be used as a non-animated image that is allowed
    to resolve external references, but which is not intended to be 
    used as an interactive document. For example, an SVG viewer that 
    processes graphics for inclusion in print documents would likely 
    use static mode.


<table class="features">
  <caption>Static Features</caption>
  <tbody>
    <tr>
      <th>script execution</th>
      <td>no</td>
    </tr>
    <tr>
      <th>external references</th>
      <td>yes</td>
    </tr>
    <tr>
      <th>declarative animation</th>
      <td>no</td>
    </tr>
    <tr>
      <th>interactivity</th>
      <td>no</td>
    </tr>
  </tbody>
</table>


<h4 id="secure-static-mode">
Secure static mode</h4>

    This [=processing mode=] is intended for circumstances where
    an SVG document is to be used as a non-animated image that is not 
    allowed to resolve external references, and which is not intended 
    to be used as an interactive document.  This mode might be used 
    where image support has traditionally been limited to non-animated 
    raster images (such as JPEG and PNG.)

    <table class="features">
    <caption>Secure Static Features</caption>
    <tbody>
        <tr>
        <th>script execution</th>
        <td>no</td>
        </tr>
        <tr>
        <th>external references</th>
        <td>no</td>
        </tr>
        <tr>
        <th>declarative animation</th>
        <td>no</td>
        </tr>
        <tr>
        <th>interactivity</th>
        <td>no</td>
        </tr>
    </tbody>
    </table>


<h3 id="referencing-modes">
Processing modes for SVG sub-resource documents</h3>

  
    When an SVG document is viewed directly, it is expected to be 
    displayed using the most comprehensive [=processing mode=] 
    supported by the user agent. However, when an SVG is processed
    as a sub-resource or embedded document, the following restrictions 
    must apply:
  

    <dl>
        <dt id="image-document-mode"><{image}> references
        <dd>
            An SVG embedded within an <{image}> element must be 
            processed in [[#secure-animated-mode]] if the embedding 
            document supports [=declarative animation=],
            or in [[#secure-static-mode]] otherwise.
        

            Note: The same processing modes are expected to be used
            for other cases where SVG is used in place of a raster
            image, such as an HTML <{img}> element or in any CSS
            property that takes an <<image>> data type. This is
            consistent with [[HTML#the-img-element|HTML's
            requirement]] that image sources must reference <q>a
            non-interactive, optionally animated, image resource that
            is neither paged nor scripted</q> [[!HTML]]


        <dt id="template-document-mode"><{use}> element and other <{a/href}> references
        <dd>
            When SVG documents are loaded through <{use}> element 
            references or [=paint server element=] cross-references
            they must be processed in [[#secure-static-mode]].
            

            Note: Animations do not run while processing the 
            sub-resource document, for both performance reasons and 
            because there is currently no context defined for resource 
            documents to reference their timeline against. However, 
            when elements from a sub-resource document are cloned into 
            the current document because of a <{use}> element 
            reference or paint-server cross-reference, the cloned 
            [=element instances=] may be animated in the current 
            document's timeline, as described in [[#UseAnimations]],
            and may trigger the loading of additional sub-resource 
            files.

        <dt id="resource-document-mode">Graphical effects references</dt>
        <dd>
            When SVG documents are loaded through any style property 
            references that target specific elements in the document
            (as opposed to SVG as an image format), they must be 
            processed in [[#secure-static-mode]].

            Note: animations do not run in sub-resource documents, for 
            both performance reasons and because there is currently no 
            context defined for resource documents to reference their 
            timeline against.

            Some style properties may reference either specific 
            elements or entire image files; the processing mode is 
            more restrictive in the first case. For example, a 
            reference to an SVG <{mask}> element will not be 
            animated, but an entire SVG file used as an image mask can 
            be.

        <dt id="font-document-mode">SVG in fonts</dt>
        <dd>
            When SVG files are processed as part of a font reference,
            they must use the [[#secure-animated-mode]] if animated 
            glyphs are supported, or [[#secure-static-mode]] otherwise.

            Note: These restrictions are included in the OpenType 
            specification for processing documents from the "SVG"
            table. OpenType also applies additional restrictions, in 
            the form of a user agent style sheet ([[#UAStyleSheet]]) 
            that prevents rendering of text and foreign objects 
            [[OPENTYPE]].
    </dl>


    SVG document fragments that are included inline in a host document
    must use a [=processing mode=] that matches that of the host 
    document. SVG document fragments included as children of an SVG 
    <{foreignObject}> element must use the [=processing mode=] of the 
    surrounding SVG document; non-SVG foreign content must be 
    processed with equivalent restrictions.

    Note: For example, if an SVG document is being used in 
    [[#secure-animated-mode]] due to being referenced by an HTML 
    <{img}> or SVG <{image}> element, then any content within a 
    <{foreignObject}> element must have scripts, interactivity, and 
    [=external file references=] disabled, but should have declarative 
    animation enabled.

<h4 id="examples">
    Examples</h4>

    <div class="example">
        Below are various methods of embedding SVG in an HTML page by
        reference, along with the expected processing mode and allowed 
        features for each.


        Each cell in the "Live Example" row should display a yellow
        smiley face. In each example below, clicking on the eyes tests
        link traversal, and clicking on the face tests declarative 
        interactivity and script execution. The link should replace 
        the image with a blue square (clicking it will revert it to 
        the original image). The declarative interactivity uses the 
        <{set}> element to change the face from shades of yellow to 
        shades of green, and uses CSS pseudoclasses to add a stroke to 
        the interactive elements. The script should fill in the smile.
        Time-based (as opposed to interactivity-based) declarative 
        animation is supported if the left eye is winking (using the 
        <{animate}> element) and if the eyes are dark blue with 
        regular flashes of light blue (using CSS keyframe animation).


        Note: The expected processing modes and features outlined here
        are subject to any future changes in the corresponding HTML or 
        CSS specification.

        <style>
        .embedcontext, table.ref_modes td {
            width: 120px;
            height: 120px;
        }
        table.ref_modes, table.ref_modes td, table.ref_modes th {
            border-collapse: collapse;
            border: gainsboro 1px solid;
        }
        td, th {padding: .5em;}
        td {
            text-align: center;
        }
        .bg {
            background-image: url(./smiley.svg);
            width: 120px;
            height: 120px;
        }
        </style>

        <table class="ref_modes">
        <tbody>
            <tr>
            <th scope="row">Embedding method</th>
            <th>object without sandboxing</th>
            <th>iframe</th>
            <th>img</th>
            <th>CSS background</th>
            </tr>
            <tr>
            <th scope="row">Expected processing mode</th>
            <td>dynamic interactive</td>
            <td>dynamic interactive, with restrictions</td>
            <td>secure animated</td>
            <td>secure animated</td>
            </tr>
            <tr>
            <th scope="row">Declarative, time-based animation<br/> (winking left eye, color-change in both eyes)</th>
            <td>allowed</td>
            <td>allowed</td>
            <td>allowed</td>
            <td>allowed</td>
            </tr>
            <tr>
            <th scope="row">Declarative, interactive animation and style changes<br/> (face color changes when clicked, face/eyes outlined when hovered or focused)</th>
            <td>allowed</td>
            <td>allowed</td>
            <td>disabled</td>
            <td>disabled</td>
            </tr>
            <tr>
            <th scope="row">Link navigation within the same browsing context, to the same domain<br/> (image changes when clicking eyes)</th>
            <td>allowed</td>
            <td>allowed</td>
            <td>disabled</td>
            <td>disabled</td>
            </tr>
            <tr>
            <th scope="row">Scripted interaction<br/> (smile widens when clicking face)</th>
            <td>allowed</td>
            <td>disabled (because of sandboxing)</td>
            <td>disabled</td>
            <td>disabled</td>
            </tr>
            <tr>
            <th scope="row">Live example</th>
            <td>
                <object class="embedcontext" type="image/svg+xml" data="images/conform/smiley.svg" aria-label="smiley face, as an object">This browser does not support embedded SVG images.</object>
            </td>
            <td>
                <iframe sandbox="" class="embedcontext" src="images/conform/smiley.svg" style="border: 0"  aria-label="smiley face, as an iframe">This browser does not support embedded SVG images.</iframe>
            </td>
            <td>
                <img no-autosize id="js-embed-img" class="embedcontext" alt="smiley face, as an image" src="images/conform/smiley.svg">
            </td>
            <td>
                <div class="embedcontext" style="background-image: url(images/conform/smiley.svg);"  aria-label="smiley face, as a background image">&#xA0;</div>
            </td>
            </tr>
        </tbody>
        </table>
    </div>

<h3 id="DocumentConformanceClasses">
Document Conformance Classes </h3>

    SVG is defined in terms of a document object model (DOM), rather
    than a particular file format or document type. For SVG content,
    therefore, conformance with this specification is defined by
    whether the content is or can generate a conforming DOM.
    Additional conformance classes depend on whether the content is
    also valid and well-formed XML [[!xml]].


<h4 id="ConformingSVGDOMSubtrees">
Conforming SVG DOM Subtrees</h4>

    A DOM node tree or subtree rooted at a given element is a
    <dfn>conforming SVG DOM subtree</dfn> if it forms a <a>SVG
    document fragment</a> that adheres to the specification described
    in this document ([[SVG2]]). Specifically, it:

    <ul>
        <li>
            is rooted by an <{svg}> element in the [=SVG namespace=],

        <li>
            conforms to the content model and attributes rules for the
            elements defined in this document ([[SVG2]]), and

        <li>
            conforms to the content model and attributes rules defined
            by other specifications for any elements in the [=SVG
            namespace=] defined by those specifications (including:
            [[filter-effects-1]], [[css-masking-1]],
            [[svg-animations]]).
    </ul>


    SVG document fragments can be included within parent XML documents
    using the XML namespace facilities described in Namespaces in XML
    [[!xml-names]]. Note, however, that since a conforming SVG DOM
    subtree must have an <{svg}> element as its root, the use of an
    individual non-<{svg}> element from the SVG namespace is
    disallowed.  Thus, the SVG part of the following document is
    <em>not</em> conforming:

    <pre highlight="xml">
        &lt;?xml version="1.0" standalone="no"?&gt;
        &lt;!DOCTYPE SomeParentXMLGrammar PUBLIC "-//SomeParent" "http://SomeParentXMLGrammar.dtd"&gt;
        &lt;ParentXML&gt;
        &lt;!-- Elements from ParentXML go here --&gt;
        &lt;!-- The following is <strong>not</strong> conforming --&gt;
        &lt;z:rect xmlns:z="http://www.w3.org/2000/svg"
                x="0" y="0" width="10" height="10" /&gt;
        &lt;!-- More elements from ParentXML go here --&gt;
        &lt;/ParentXML&gt;
    </pre>

    Instead, for the SVG part to become a [=conforming SVG DOM
    subtree=], the file could be modified as follows:

    <pre highlight="xml">
        &lt;?xml version="1.0" standalone="no"?&gt;
        &lt;!DOCTYPE SomeParentXMLGrammar PUBLIC "-//SomeParent" "http://SomeParentXMLGrammar.dtd"&gt;
        &lt;ParentXML&gt;
        &lt;!-- Elements from ParentXML go here --&gt;
        &lt;!-- The following is conforming --&gt;
        &lt;z:svg xmlns:z="http://www.w3.org/2000/svg"
                width="100px" height="100px"&gt;
            &lt;z:rect x="0" y="0" width="10" height="10"/&gt;
        &lt;/z:svg&gt;
        &lt;!-- More elements from ParentXML go here --&gt;
        &lt;/ParentXML&gt;
    </pre>

    The SVG language and these conformance criteria provide no
    designated size limits on any aspect of SVG content. There are no
    maximum values on the number of elements, the amount of character
    data, or the number of characters in attribute values.


<h4 id="ConformingSVGFragments">
Conforming SVG Markup Fragments</h4>

    A document or part of a document is a <dfn dfn export>conforming
    SVG markup fragment</dfn> if it can be parsed without error (other
    than network errors) by the appropriate parser for the document
    MIME type to form a [=conforming SVG DOM subtree=], and in
    addition if:

    <ul>
        <li>
            any CSS stylesheets included in the document conform to
            the core grammar of Cascading Style Sheets, level 2
            revision 1 [[CSS2]].
    </ul>

<h4 id="ConformingSVGXMLFragments">
Conforming XML-Compatible SVG Markup Fragments</h4>

    A [=conforming SVG markup fragment=] is also a
    <dfn>conforming XML-compatible SVG markup fragment</dfn>
    if it:

    <ul>
        <li>
            meets all [[xml#sec-well-formed|XML
            well-formedness constraints]] ([[!xml]]),

        <li>
            conforms to the <cite>Namespaces in XML</cite>
            specification [[!xml-names]],

        <li>
            all <a element-attr for="core-attributes" 
            spec="svg2">id</a> attributes are 
            [[xml#sec-attribute-types|valid XML IDs]] ([[!xml]], 
            section 3.3.1), and

        <li>
            any <code>&lt;?xml-stylesheet?&gt;</code> processing
            instruction conforms to <cite>Associating stylesheets with
            XML documents</cite> [[xml-stylesheet]].
    </ul>

<h4 id="ConformingSVGXMLDOMSubtrees">
Conforming XML-Compatible SVG DOM Subtrees</h4>

    A DOM node tree or subtree rooted at a given element is an
    <dfn dfn export>conforming XML-compatible SVG DOM subtree</dfn> if, once
    serialized to XML, it could form a [=conforming XML-compatible SVG
    markup fragment=].


    If the DOM subtree cannot be serialized to conforming XML without
    altering it, such as when an [[SVG2#Core.attrib|id]] value is
    not a valid XML name, or when a {{Comment}} node's data contains
    the substring "--", then the subtree is not a conforming
    XML-compatible SVG DOM subtree.

<h4 id="ConformingSVGStandAloneFiles">
Conforming SVG Stand-Alone Files</h4>

    A document is a <dfn>conforming SVG stand-alone file</dfn> if:

    <ul>
        <li>
            it is a well-formed XML document,

        <li>
            its root element is an <{svg}> element,

        <li>
            the SVG document fragment rooted at the document element
            is a [=conforming XML-Compatible SVG markup fragment=],
            and</li>

        <li>
            any other [=SVG document fragments=] within the document
            (such as those within a <{foreignObject}>) form a
            [=conforming XML-Compatible SVG markup fragment=].
    </ul>


<h4 id="ErrorProcessing">
Error processing</h4>

    There are various scenarios where an SVG document fragment
    is technically <em>in error</em>:

    <ul>
        <li>
            The document or DOM subtree is not-conforming for its
            document type, as described in the previous sections.


        <li>
            Other situations that are described as being <em>in
            error</em> in this specification, such as incorrect
            attribute values.
    </ul>

    A dynamic document can go in and out of error over time. For
    example, document changes from the [[#SVGDOMOverview|SVG DOM]] or
    from [[svg-animations]] can cause a document to become <em>in
    error</em> and a further change can cause the document to become
    correct again.

    User agents must use the following error processing rules whenever
    a document is in error, unless other sections of this
    specification define more specific rules for handling the
    particular error type:

    <ul>
        <li>
            The document rendering shall continue after encountering
            element which has an error. The element or its part that
            is in error won't be rendered.

        <li>
            If the user agent has access to an error reporting
            capability such as status bar or console, it is
            recommended that the user agent provide whatever
            additional detail it can to enable the user or developer
            to quickly find the source of the error. For example, the
            user agent might provide an error message along with a
            line number and character number at which the error was
            encountered.
    </ul>

    Because of situations where a block of scripting changes might
    cause a given SVG document fragment to go into and out of error,
    the user agent should only apply error processing at times when
    document presentation (e.g., rendering to the display device) is
    updated.

<h3 id="SoftwareConformanceClasses">
Software Conformance Classes</h3>

    For software, the requirements for conformance depend on the
    category of program:

    <dl>
        <dt><dfn>SVG generators</dfn>
        <dd>
            Any software that creates or makes available SVG content,
            either as markup or as a DOM (as is the case with
            client-side JavaScript libraries).

        <dt><dfn>SVG authoring tools</dfn>
        <dd>
            Any software that provides an interface for human content
            creators to manipulate graphics or code that will be used
            to generate SVG. SVG authoring tools are implicitly also
            [=SVG generators=].

        <dt><dfn dfn export>SVG servers</dfn>
        <dd>
            Any network or file server that makes available SVG
            content in response to requests from other software. SVG
            servers are implicitly also [=SVG generators=].

        <dt><dfn>SVG interpreters</dfn></dt>
        <dd>
            Any software that parses or processes SVG documents or
            markup fragments. An SVG interpreter is an [=SVG user
            agent=] for the purpose of any sections of this
            specification that relate to the parsing or processing
            steps undertaken by the interpreter.

        <dt><dfn>SVG viewers</dfn>
        <dd>
            Any software that creates a rendered graphical
            representation after parsing or processing an SVG document
            or SVG markup fragment. SVG viewers are implicitly also
            [=SVG interpreters=]. An SVG viewer is always an [=SVG
            user agent=] for the purpose of this specification.

        <dt><dfn>SVG user agent</dfn>
        <dd>
            An SVG user agent is a [=user agent=] that is able to
            retrieve and render SVG content.

        <dt><dfn>user agent</dfn>
        <dd>
            The general definition of a user agent is an application
            that retrieves and renders Web content, including text,
            graphics, sounds, video, images, and other content types.
            A user agent may require additional user agents that
            handle some types of content. For instance, a browser may
            run a separate program or plug-in to render sound or
            video. User agents include graphical desktop browsers,
            multimedia players, text browsers, voice browsers, and
            assistive technologies such as screen readers, screen
            magnifiers, speech synthesizers, onscreen keyboards, and
            voice input software.

            In general terms, a "user agent" may or may not have the
            ability to retrieve and render SVG content; however,
            unless the context requires an alternative interpretation,
            all references to a "user agent" in this specification are
            assumed to be references to an [=SVG user agent=] that
            retrieves and renders SVG content.
        </dd>
    </dl>

    Many programs will fall under multiple software classes. For
    example, a graphical editor that can import and display SVG files,
    allow the user to modify them, and then export the modified
    graphic to file, is an SVG interpreter, an SVG viewer, an SVG
    authoring tool, and an SVG generator.


<h4 id="ConformingSVGGenerators">
Conforming SVG Generators</h4>

    A <dfn>conforming SVG generator</dfn> is a
    [=SVG generator=] that:

    <ul>
        <li>
            always creates a [=conforming SVG DOM subtree=], a
            [=conforming SVG markup fragment=], or a [=conforming SVG
            stand-alone file=];

        <li>
            does not create documents containing non-conforming SVG
            document fragments;

        <li>
            meets all normative requirements in this specification for
            SVG authors, as well as specific normative requirements
            for SVG generators.
    </ul>

    SVG generators are strongly encouraged to use a Unicode character
    encoding by default, and to follow the other guidelines of the
    Character Model for the World Wide Web [[UNICODE]] [[charmod]].


    Note: SVG generators handling high-precision data are encouraged
    to follow the guidelines in the section
    [[#NumericPrecisionImplementationNotes]].


<h4 id="ConformingSVGAuthoringTools">
Conforming SVG Authoring Tools</h4>


    An [[ATAG20#def-Authoring-Tool|authoring tool]], as defined in
    [[ATAG20]], is a <dfn dfn export>conforming SVG authoring tool</dfn>
    if it is a [=conforming SVG generator=] and it also conforms to
    all relevant Level A requirements from that document [[ATAG20]].
    Level AA and Level AAA requirements are encouraged but not
    required for conformance.

<h4 id="ConformingSVGServers">
Conforming SVG Servers</h4>

    A <dfn dfn export>conforming SVG server</dfn> must meet all the requirements
    of a [=conforming SVG generator=]. In addition, conforming SVG
    servers using HTTP or other protocols that use Internet Media
    types must serve SVG stand-alone files with the media type
    <code>"image/svg+xml"</code>.

    Also, if the SVG file is compressed with gzip or deflate,
    conforming SVG Servers must indicate this with the appropriate
    header, according to what the protocol supports.  Specifically,
    for content compressed by the server immediately prior to
    transfer, the server must use the
    "<code>Transfer-Encoding:&nbsp;gzip</code>" or
    "<code>Transfer-Encoding:&nbsp;deflate</code>" headers as
    appropriate. For content stored in a compressed format on the
    server (e.g. with the file extension <i>.svgz</i>), the server
    must use the "<code>Content-Encoding:&nbsp;gzip</code>" or
    "<code>Content-Encoding:&nbsp;deflate</code>" headers as
    appropriate.

    Note: In HTTP, compression of stored <em>content</em> (the "entity")
    is distinct from automatic compression of the <em>message
    body</em>, as defined in HTTP/1.1 [[rfc9110#field.te|TE]]/
    [[rfc9112#field.transfer-encoding|Transfer Encoding]]
    ([[rfc9112]] sections 6.1 and [[rfc9110]] section 10.1.4.). If
    this is poorly configured, and the compression specified in
    the HTTP headers does not match the used values, SVG user
    agents are required to treat the document as being in error.

    Note: Configuring a server to handle both SVG and SVGZ files means
    that it must be able to assign the same media type to both
    types of files, but with different compression headers. Some
    commonly used servers do not support this configuration in an
    easy or efficient way, because compression behavior is
    configured based on media type.

    Note: With most modern web servers, it is often easier to upload
    uncompressed SVG files instead of SVGZ files. Then, rely on
    the server to compress the file for transmission, and cache it
    for future request, using the same server instructions as for
    other text-based file formats such as HTML. This also allows
    the server to use newer compression methods, when they are
    supported by the user agent requesting the file.

    Note: Alternatively, the web server may be able to correctly process
    pre-compressed SVGZ files if they are first renamed to use the
    <i>.svg.gz</i> compound file extension. The server would still
    need to be configured to support static gzip-compressed files.

<h4 id="ConformingSVGInterpreters">
Conforming SVG Interpreters</h4>

    Note: An [=SVG interpreter=] is a program which can parse and
    process SVG document fragments. Examples of SVG interpreters are
    server-side transcoding tools or optimizers (e.g., a tool which
    converts SVG content into modified SVG content) or analysis tools
    (e.g., a tool which extracts the text content from SVG content, or
    a validity checker). A transcoder from SVG into another graphics
    representation, such as an SVG-to-raster transcoder, represents a
    viewer, and thus viewer conformance criteria also apply.


    A <dfn>conforming SVG interpreter</dfn> must be able to parse and
    process all XML constructs defined in [[xml|XML 1.0]] [[!xml]] and
    [[xml-names|<cite>Namespaces in XML</cite>]] [[!xml-names]].

    A [=conforming SVG interpreter=] must parse any [=conforming
    XML-Compatible SVG markup fragment=] in a manner that correctly
    respects the DOM structure (elements, attributes, text content,
    comments, etc.) of the content. The interpreter is not required to
    interpret the semantics of all features correctly.

    If the SVG interpreter supports non-XML syntaxes (such as HTML),
    it must correctly parse any [=conforming SVG markup fragment=] in
    that syntax.


    If the SVG interpreter runs scripts or fetches external resource
    files as a consequence of processing the SVG content, it must
    follow the restrictions described for [=user agent|user agents=]
    in [[#referencing-modes|Processing modes for SVG sub-resource
    documents]] and in the [[#linking|linking section]].


<h4 id="ConformingSVGViewers">
Conforming SVG Viewers</h4>

    <div class="annotation">
        <table>
            <tr>
            <th>Action:</th>
            <td><a href="http://www.w3.org/2013/11/14-svg-minutes.html#action01">Look at the performance class requirements and decide whether to remove points or move them into general requirements.</a> (heycam)
            <br/>
            <a href="http://www.w3.org/2014/10/31-svg-minutes.html#action02">Spec that calculation of CTMs should use double precision.</a> (stakagi)</td>
            </tr>
            <tr>
            <th>Resolution:</th>
            <td><a href="http://www.w3.org/2013/11/14-svg-minutes.html#item01">Remove performance class requirements from SVG 2.</a> ( <a href="conform.html#ConformingHighQualitySVGViewers">ConformingHighQualitySVGViewers</a> )</td>
            </tr>
            <tr>
            <th>Purpose:</th>
            <td>To modulate the tradeoff of a numerical precision in use cases of the technical drawing and mapping, and the performance of user agent.</td>
            </tr>
            <tr>
            <th>Owner:</th>
            <td>heycam, stakagi</td>
            </tr>
        </table>
    </div>

    Note: An [=SVG viewer=] is a program which can parse and process
    an SVG document fragment and render the contents of the document
    onto some sort of graphical output medium such as a display,
    printer, or engraver. Thus, an [=SVG viewer=] is also an [=SVG
    interpreter=] (in that it can parse and process SVG document
    fragments), but with the additional requirement of correct
    rendering.

    A <dfn>conforming SVG viewer</dfn>
    must be a [=conforming SVG interpreter=], and must be able to
    support rendering output in at least one of the processing modes
    defined in this chapter:

    <ul>
        <li>
            [[#dynamic-interactive-mode]]
        <li>
            [[#animated-mode]]
        <li>
            [[#secure-animated-mode]]
        <li>
            [[#static-mode]]
        <li>
            [[#secure-static-mode]]
    </ul>

    A conforming SVG viewer must meet all normative requirements
    indicated in this specification for [=user agent|user agents=],
    for all features supported by its processing mode(s).


    Specific criteria that must apply to all [=conforming SVG
    viewers=]:

    <ul>
    
        <li>
            The viewer must be able to parse all CSS syntax features
            defined in [[CSS2|<cite>Cascading Style Sheets, level 2
            revision 1</cite>]] [[CSS2]], and must support CSS styling
            of SVG content including all
            [[SVG2#RequiredProperties|required properties]] and
            [[SVG2#RequiredCSSFeatures|required features]] listed in
            [[#styling]]. The viewer may support other CSS language
            features, and any other properties that are defined by the
            corresponding specification to apply to SVG elements. The
            supported features from CSS 2.1 must be implemented in
            accordance with the [[css2/conform#conformance|conformance
            definitions]] from the [[CSS2]].
    
        <li>
            The viewer must be able to apply styling properties to SVG
            content using [=presentation attributes=].
    
        <li>
            Areas of an image of SVG content may have opacity less
            than 100%. The viewer must at least support Simple Alpha
            Compositing of the image of the SVG content onto the
            target canvas, as described in the Compositing and
            Blending Specification [[compositing-1]].

        <li>
            The viewer must support [=data URL=] references containing
            base64-encoded or URL-encoded content, in conformance with
            [[rfc2397#section-2|the "data" URL scheme]] [[rfc2397]],
            wherever a URI reference to another document is permitted
            within SVG content. When the encoded document is of MIME
            type <code>image/svg+xml</code>, it must be a well-formed,
            complete SVG document in order to be processed.

        <li>
            The viewer must support JPEG and PNG image formats
            [[JPEG]] [[PNG]].

            Note: Even if the viewer only supports secure processing
            modes, it is still required to support these image
            formats, in order to process [=data URL=] references.

        <li>
            Resampling of image data must be consistent with the
            specification of property
            [[SVG2#ImageRendering|image-rendering]].</li>
    
        <li>
            Whenever possible in the parent environment, the viewer
            must use information about physical device resolution and
            expected viewing conditions in order to accurately
            determine the initial scale in conformance with
            [[css2/syndata#length-units|the rules described in CSS 2.1]]
            ([[CSS2]], section 4.3.2). In situations where this
            information is impossible to determine, the viewer or the
            parent environment must make a reasonable approximation
            for common target devices.</li>
    
        <li>
            All visual rendering must be accurate to within one device
            pixel or point of the mathematically correct result at the
            initial 1:1 zoom ratio. It is suggested that viewers
            attempt to keep a high degree of accuracy when zooming.
            
            Note: On lower-resolution display devices, support for
            anti-aliasing or other smoothing methods is highly
            recommended. It is a requirement for [=conforming
            high-quality SVG viewers=].

        <li>
            If printing devices are supported, SVG content must be
            printable at printer resolutions with the same graphics
            features available as required for display (e.g., the
            specified colors must be rendered on color printers).
    
        <li>
            On systems which support accurate sRGB [[SRGB]] color, all
            sRGB color computations and all resulting color values
            must be accurate to within one sRGB color component value,
            where sRGB color component values range from 0 to 255.
    
        <li id="user-agent-compression-requirements">
            SVG implementations must correctly support
            [[rfc1952|gzip-encoded]] [[rfc1952]] and
            [[rfc1951|deflate-encoded]] [[rfc1951]] data streams, for
            any content type (including SVG, script files, images).
            SVG implementations that support HTTP must support these
            encodings according to the [[rfc9110|HTTP 1.1]]
            specification [[rfc9110]]; in particular, the client must
            specify with an
            "<code>[[rfc9110#field.accept-encoding|Accept-Encoding:]]</code>"
            request header those encodings that it accepts, including
            at minimum gzip and deflate, and then decompress any
            [[rfc1952|gzip-encoded]] and [[rfc1951|deflate-encoded]]
            data streams that are downloaded from the server. When an
            SVG viewer retrieves compressed content (e.g., an
            <i>.svgz</i> file) over HTTP, if the "Content-Encoding"
            and "Transfer-Encoding" response headers are missing or
            specify a value that does not match the compression method
            that has been applied to the content, then the SVG viewer
            must not render the content and must treat the document as
            being <a href="#ErrorProcessing">in error</a>.

        <li>
            The viewer must use at least single-precision floating
            point for intermediate calculations on any numerical
            operations for conversion of coordinates. However, in
            order to prevent the rounding error on coordinate
            transformation, at least double-precision floating point
            computation must be used on 
            <a spec="css-transforms-1">current transformation matrix</a> 
            (CTM) generation processing. Such minimum typical 
            computation way is expressed with following formulas.
            
            <div role="math"
                 aria-describedby="ctm-matrix">
                <math display="block">
                    <mo stretchy="false">(</mo>
                    <mi>single</mi>
                    <mo stretchy="false">)</mo>
                    <mrow class="MJX-TeXAtom-ORD">
                        <mstyle mathsize="1.2em">
                            <mi mathvariant="normal">CTM</mi>
                        </mstyle>
                    </mrow>
                    <mo>=</mo>
                    <mo stretchy="false">(</mo>
                    <mi>single</mi>
                    <mo stretchy="false">)</mo>
                    <mrow>
                        <mo>(</mo>
                        <mo stretchy="false">(</mo>
                        <mi>double</mi>
                        <mo stretchy="false">)</mo>
                        <mrow>
                            <mo>[</mo>
                            <mtable rowspacing="4pt"
                                    columnspacing="1em">
                                <mtr>
                                    <mtd>
                                        <msub>
                                            <mi>a</mi>
                                            <mn>1</mn>
                                        </msub>
                                    </mtd>
                                    <mtd>
                                        <msub>
                                            <mi>c</mi>
                                            <mn>1</mn>
                                        </msub>
                                    </mtd>
                                    <mtd>
                                        <msub>
                                            <mi>e</mi>
                                            <mn>1</mn>
                                        </msub>
                                    </mtd>
                                </mtr>
                                <mtr>
                                    <mtd>
                                        <msub>
                                            <mi>b</mi>
                                            <mn>1</mn>
                                        </msub>
                                    </mtd>
                                    <mtd>
                                        <msub>
                                            <mi>d</mi>
                                            <mn>1</mn>
                                        </msub>
                                    </mtd>
                                    <mtd>
                                        <msub>
                                            <mi>f</mi>
                                            <mn>1</mn>
                                        </msub>
                                    </mtd>
                                </mtr>
                                <mtr>
                                    <mtd>
                                        <mn>0</mn>
                                    </mtd>
                                    <mtd>
                                        <mn>0</mn>
                                    </mtd>
                                    <mtd>
                                        <mn>1</mn>
                                    </mtd>
                                </mtr>
                            </mtable>
                            <mo>]</mo>
                        </mrow>
                        <mo>&#x22C5;<!-- ⋅ --></mo>
                        <mo stretchy="false">(</mo>
                        <mi>double</mi>
                        <mo stretchy="false">)</mo>
                        <mrow>
                            <mo>[</mo>
                            <mtable rowspacing="4pt"
                                    columnspacing="1em">
                                <mtr>
                                    <mtd>
                                        <msub>
                                            <mi>a</mi>
                                            <mn>2</mn>
                                        </msub>
                                    </mtd>
                                    <mtd>
                                        <msub>
                                            <mi>c</mi>
                                            <mn>2</mn>
                                        </msub>
                                    </mtd>
                                    <mtd>
                                        <msub>
                                            <mi>e</mi>
                                            <mn>2</mn>
                                        </msub>
                                    </mtd>
                                </mtr>
                                <mtr>
                                    <mtd>
                                        <msub>
                                            <mi>b</mi>
                                            <mn>2</mn>
                                        </msub>
                                    </mtd>
                                    <mtd>
                                        <msub>
                                            <mi>d</mi>
                                            <mn>2</mn>
                                        </msub>
                                    </mtd>
                                    <mtd>
                                        <msub>
                                            <mi>f</mi>
                                            <mn>2</mn>
                                        </msub>
                                    </mtd>
                                </mtr>
                                <mtr>
                                    <mtd>
                                        <mn>0</mn>
                                    </mtd>
                                    <mtd>
                                        <mn>0</mn>
                                    </mtd>
                                    <mtd>
                                        <mn>1</mn>
                                    </mtd>
                                </mtr>
                            </mtable>
                            <mo>]</mo>
                        </mrow>
                        <mo>)</mo>
                    </mrow>
                </math>
            </div>
    
            <div role="math"
                 aria-describedby="ctm-matrix2">
                <math display="block">
                    <mo stretchy="false">(</mo>
                    <mi>single</mi>
                    <mo stretchy="false">)</mo>
                    <mrow>
                        <mo>[</mo>
                        <mtable rowspacing="4pt"
                                columnspacing="1em">
                            <mtr>
                                <mtd>
                                    <msub>
                                        <mi>x</mi>
                                        <mrow class="MJX-TeXAtom-ORD">
                                            <mi mathvariant="normal">viewport</mi>
                                        </mrow>
                                    </msub>
                                </mtd>
                            </mtr>
                            <mtr>
                                <mtd>
                                    <msub>
                                        <mi>y</mi>
                                        <mrow class="MJX-TeXAtom-ORD">
                                            <mi mathvariant="normal">viewport</mi>
                                        </mrow>
                                    </msub>
                                </mtd>
                            </mtr>
                            <mtr>
                                <mtd>
                                    <mn>1</mn>
                                </mtd>
                            </mtr>
                        </mtable>
                        <mo>]</mo>
                    </mrow>
                    <mo>=</mo>
                    <mrow class="MJX-TeXAtom-ORD">
                        <mstyle mathsize="1.2em">
                            <mi mathvariant="normal">CTM</mi>
                        </mstyle>
                    </mrow>
                    <mo>&#x22C5;<!-- ⋅ --></mo>
                    <mo stretchy="false">(</mo>
                    <mi>single</mi>
                    <mo stretchy="false">)</mo>
                    <mrow>
                        <mo>[</mo>
                        <mtable rowspacing="4pt"
                                columnspacing="1em">
                            <mtr>
                                <mtd>
                                    <msub>
                                        <mi>x</mi>
                                        <mrow class="MJX-TeXAtom-ORD">
                                            <mi mathvariant="normal">userspace</mi>
                                        </mrow>
                                    </msub>
                                </mtd>
                            </mtr>
                            <mtr>
                                <mtd>
                                    <msub>
                                        <mi>y</mi>
                                        <mrow class="MJX-TeXAtom-ORD">
                                            <mi mathvariant="normal">userspace</mi>
                                        </mrow>
                                    </msub>
                                </mtd>
                            </mtr>
                            <mtr>
                                <mtd>
                                    <mn>1</mn>
                                </mtd>
                            </mtr>
                        </mtable>
                        <mo>]</mo>
                    </mrow>
                </math>
    
            </div>
    
            Furthermore, when it has nested viewport coordinate
            systems, the {{getScreenCTM}} which is a transformation
            matrix produced by nested CTM for transforming user
            coordinates into the coordinates of an output device also
            must be generated by double-precision floating point
            computation.
    </ul>

    A [=conforming SVG viewer=] that supports [=processing modes=]
    that include [=interaction=] must support the following additional
    features:

    <ul>

        <li>
            For interactive user environments, facilities must exist
            for zooming and panning of stand-alone SVG documents or
            SVG document fragments embedded within parent XML
            documents.

        <li>
            In environments that have appropriate user interaction
            facilities, the viewer must support the ability to
            activate hyperlinks.

        <li>
            In Web browser environments, the viewer must have the
            ability to search and select text strings within SVG
            content.

        <li>
            If display devices are supported, the viewer must have the
            ability to select and copy text from SVG content to the
            system clipboard.

        <li>
            The viewer must meet all applicable Level A requirements
            of the [[UAAG20|<cite>User Agent Accessibility Guidelines
            2.0</cite>]] [[UAAG20]]. Level AA and level AAA features
            are encouraged, but not required.
    </ul>

    A [=conforming SVG viewer=] that supports [=processing modes=]
    that include [=script execution=] must support the following
    additional features:

    <ul>
        <li>
            The viewer must be a @@fix <a
            href="https://webidl.spec.whatwg.org/#dfn-conforming-javascript-implementation">conforming
            JavaScript implementation</a> of all the IDL fragments in
            this specification. [[WebIDL]]
    </ul>

    If the user agent includes an HTML or XHTML viewing capability, or
    can apply CSS styling properties to XML documents, then a
    [=conforming SVG viewer=] must support resources of MIME type
    "image/svg+xml" wherever raster image external resources can be
    used, such as in the HTML or XHTML <{img}> element and in CSS
    properties that can refer to raster image resources (e.g.,
    'background-image').

<h5 id="PrintingImplementationNotes">
Printing implementation notes</h5>

    For user agents which support both zooming on display devices and
    printing, it is recommended that the default printing option
    produce printed output that reflects the display device's current
    view of the current SVG document fragment (assuming there is no
    media-specific styling), taking into account any zooming and
    panning done by the user, the current state of animation, and any
    document changes due to DOM and scripting.

    Thus, if the user zooms into a particular area of a map on the
    display device and then requests a hardcopy, the hardcopy should
    show the same view of the map as appears on the display device. If
    a user pauses an animation and prints, the hardcopy should show
    the same graphics as the currently paused picture on the display
    device. If scripting has added or removed elements from the
    document, then the hardcopy should reflect the same changes that
    would be reflected on the display.

    When an SVG document is rendered on a static-only device such as a
    printer which does not support SVG's animation and scripting and
    facilities, then the user agent shall ignore any animation and
    scripting elements in the document and render the remaining
    graphics elements according to the rules in this specification.

<h4 id="ConformingHighQualitySVGViewers">
Conforming High-Quality SVG Viewer</h4>

@@fix to remove? cf issue above.

    In order for a [=conforming SVG viewer=] to be considered a
    <dfn>conforming high-quality SVG viewer</dfn>, it must support the
    following additional features:

    <ul>
        <li>
            Professional-quality results with good processing and
            rendering performance and smooth, flicker-free animations.

        <li>
            On low-resolution devices such as display devices at
            150dpi or less, support for smooth edges on lines, curves
            and text. (Smoothing is often accomplished using
            anti-aliasing techniques.)

        <li>
            Color management via ICC profile support [[ICC]] (i.e.,
            the ability to support colors defined using ICC profiles)
            [[css-color-4]]

        <li>
            Resampling of image data must conform to the requirements
            for conforming high-quality SVG viewers as specified in
            the description of property
            [[SVG2#ImageRendering|image-rendering]].

        <li>
            At least double-precision floating point computation on
            coordinate system transformation numerical calculations.
    </ul>

    A [=conforming high-quality SVG viewer=] that supports
    [=processing modes=] that include [=script execution=],
    [=declarative animation=], or [=interaction=] must support the
    following additional features:

        <ul>
            <li>
                Progressive rendering and animation effects (i.e., the
                start of the document will start appearing and
                animations will start running in parallel with
                downloading the rest of the document).

            <li>
                Restricted screen updates (i.e., only required areas
                of the display are updated in response to redraw
                events).
        </ul>

    A [=conforming high-quality SVG viewer=] that supports
    [=processing modes=] that include [=interaction=] must support the
    following additional features:

        <ul>
            <li>
                Background downloading of images and fonts retrieved
                from a Web server, with updating of the display once
                the downloads are complete.
        </ul>
