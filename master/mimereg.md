<h2 id="mimereg">Appendix J: Media Type Registration for image/svg+xml</h2>

<p class="normativity"><strong>This appendix is normative.</strong>

<h3 id="mime-intro">Introduction</h3>

<p>
This appendix registers a new MIME media type, "image/svg+xml" in conformance with <a href="http://www.ietf.org/rfc/rfc4288.txt">BCP 13</a> and <a href="http://www.w3.org/2002/06/registering-mediatype.html">W3CRegMedia</a>.


<h3 id="mime-registration">Registration of media type image/svg+xml</h3>

<dl>
<dt>
Type name:</dt>
<dd>
<p>
image


</dd>
<dt>
Subtype name:</dt>
<dd>
<p>
svg+xml


</dd>
<dt>
Required parameters:</dt>
<dd>
<p>
None.


</dd>
<dt>
Optional parameters:</dt>
<dd>
<p>
charset


<p>
Same as application/xml media type, as specified in [<a href="refs.html#ref-rfc7303">rfc7303</a>] or its successors.


</dd>
<dt>
Encoding considerations:</dt>
<dd>
<p>
Same as for application/xml. See [<a href="refs.html#ref-rfc7303">rfc7303</a>], section 3.2 or its successors.


</dd>

<dt>
Security considerations:</dt>
<dd>
Note: 
The results of the SVG working group's
<a href="https://www.w3.org/TR/security-privacy-questionnaire/">self assessment of security and privacy</a>
concerns is at <a href="https://github.com/w3c/svgwg/wiki/SVG-2-Security-%26-Privacy-Review">https://github.com/w3c/svgwg/wiki/SVG-2-Security-&amp;-Privacy-Review</a>.
<p>
As with other XML types and as noted in [<a href="refs.html#ref-rfc7303">rfc7303</a>] section 10, repeated expansion of maliciously constructed XML entities can be used to consume large amounts of memory, which may cause XML processors in constrained environments to fail.



<p>
Several SVG elements may cause arbitrary URIs to be referenced. In this case, the security issues of [<a href="refs.html#ref-rfc3986">rfc3986</a>], section 7, should be considered.


<p>
In common with HTML, SVG documents may reference external media such as images, style sheets, and scripting languages. Scripting languages are executable content. In this case, the security considerations in the Media Type registrations for those formats shall apply.


<p>
In addition, because of the extensibility features for SVG and of XML in general, it is possible that "image/svg+xml" may describe content that has security implications beyond those described here. However, if the processor follows only the normative semantics of the published specification, this content will be outside the SVG namespace and shall be ignored. Only in the case where the processor recognizes and processes the additional content, or where further processing of that content is dispatched to other processors, would security issues potentially arise. And in that case, they would fall outside the domain of this registration document.


</dd>

<dt class='ready-for-wider-review'>
Privacy considerations:</dt>
<dd>
Note: 
The results of the SVG working group's
<a href="https://www.w3.org/TR/security-privacy-questionnaire/">self assessment of security and privacy</a>
concerns is at <a href="https://github.com/w3c/svgwg/wiki/SVG-2-Security-%26-Privacy-Review">https://github.com/w3c/svgwg/wiki/SVG-2-Security-&amp;-Privacy-Review</a>.
<p class='ready-for-wider-review'>SVG's {{requiredExtensions}} and {{systemLanguage}} attributes may
provide some opportunity for examining the configuration of a user agent's host
environment. {{requiredExtensions}} by determining whether custom
extensions are supported by the user agent. {{systemLanguage}} by
determining the preference of one language relative to another.

</dd>

<dt>
Interoperability considerations:</dt>
<dd>
<p>
The published specification describes processing semantics that dictate behavior that must be followed when dealing with, among other things, unrecognized elements and attributes, both in the SVG namespace and in other namespaces.


<p>
Because SVG is extensible, conformant "image/svg+xml" processors must expect that content received is well-formed XML, but it cannot be guaranteed that the content is valid to a particular DTD or Schema or that the processor will recognize all of the elements and attributes in the document.


<p>
SVG has a published Test Suite and associated implementation report showing which implementations passed which tests at the time of the report. This information is periodically updated as new tests are added or as implementations improve.


</dd>
<dt>
Published specification:</dt>
<dd>
<p>
This media type registration is extracted from Appendix P of the <a href="https://www.w3.org/TR/SVG11/">SVG 1.1 specification</a>.


</dd>

<dt>
Applications that use this media type:</dt>
<dd>
<p>
SVG is used by Web browsers, often in conjunction with HTML; by mobile phones and digital cameras, as a format for interchange of graphical assets in desktop publishing, for industrial process visualization, display signage, and many other applications which require scalable static or interactive graphical capability.


</dd>

<dt>
Additional information:</dt>
<dd><dl>
    <dt>Magic number(s):</dt>
    <dd></dd>
    <dt>File extension(s):</dt>
     <dd>svg
     <p>Note that the extension <span class="attr-value">svgz</span> is used as an alias for 'svg.gz'
       <cite>[[rfc1952]]</cite>,
		<em>i.e.</em> octet streams of type image/svg+xml, subsequently
        compressed with gzip.</dd>
     <dt>Macintosh file type code(s):</dt>
     <dd>"svg "  (all lowercase, with a space character as the
     fourth letter).
     <p>Note that the Macintosh file type code <span class="attr-value">svgz</span> (all lowercase) is used as an alias for GZIP
        <cite>[[rfc1952]]</cite> compressed "svg ", <em>i.e.</em>
         octet streams of type image/svg+xml, subsequently compressed with gzip.</dd>
 <dt>Macintosh Universal Type Identifier code:  </dt>
 <dd><code>org.w3c.svg</code> conforms to <code>public.image</code>   and to <code>public.xml</code></dd>
 <dt>Windows Clipboard Name:</dt>
 <dd>"SVG Image"</dd>
</dl>
<dl class="ready-for-wider-review">
 <dt>Fragment Identifiers</dt>
 <dd>For documents labeled as application/svg+xml, the fragment identifier
  notation is either Shorthand Pointers (formerly called barenames),
  the SVG-specific <a href="linking.html#LinksIntoSVG">SVG Views</a> syntax or a Media Fragment Identifier;
  all described in the <a href="linking.html#SVGFragmentIdentifiers">fragment
  identifiers section of the SVG specification</a>.</dd>
</dl>
</dd>

<dt>
Person &amp; email address to contact for further information:</dt>
<dd>
<p>
Chris Lilley (www-svg@w3.org) or raise an issue on GitHub:
<a href="https://github.com/w3c/svgwg/issues/685">https://github.com/w3c/svgwg/issues/685</a>


</dd>
<dt>
Intended usage:</dt>
<dd>
<p>
COMMON


</dd>

<dt>
Restrictions on usage:</dt>
<dd>
<p>
None


</dd>
<dt>
Author:</dt>
<dd>
<p>
The SVG specification is a work product of the World Wide Web Consortium's SVG Working Group.


</dd>
<dt>
Change controller:</dt>
<dd>
<p>
The W3C has change control over this specification.

</dd>

</dl>
