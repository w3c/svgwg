<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:idl='http://mcc.id.au/ns/idl'
                xmlns:x='http://mcc.id.au/ns/local'
                version='2.0'>

  <xsl:output method='text'/>

  <xsl:template match="/">
    <xsl:for-each select="//(idl:interface | idl:exception)">
      <xsl:variable name='interface' select='.'/>
      <xsl:variable name='module' select='ancestor::idl:module[1]/@scopedname'/>
      <xsl:variable name='module-part' select='replace(substring-after($module, "::"), "::", ".")'/>
      <xsl:variable name='package' select='concat("org.w3c.", if ($module-part = "dom") then "" else "dom.", $module-part)'/>
      <xsl:if test='$module-part = ("svg", "smil")'>
        <xsl:result-document href='org/w3c/dom/{$module-part}/{@name}.java'>
          <xsl:text>/*
 * Copyright (c) 2010 World Wide Web Consortium,
 *
 * (Massachusetts Institute of Technology, European Research Consortium for
 * Informatics and Mathematics, Keio University). All Rights Reserved. This
 * work is distributed under the W3C(r) Software License [1] in the hope that
 * it will be useful, but WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * [1] http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231
 */

</xsl:text>
          <xsl:text>package </xsl:text><xsl:value-of select='$package'/><xsl:text>;&#10;&#10;</xsl:text>
          <xsl:variable name='importrefs' select='distinct-values(.//@ref/string())[id(x:deref(., $interface), $interface)/ancestor::idl:module[1]/@scopedname != $module]'/>
          <xsl:if test='count($importrefs)'>
            <xsl:for-each select='$importrefs'>
              <xsl:sort select='id(x:deref(., $interface), $interface)/@scopedname' case-order='upper-first'/>
              <xsl:text>import </xsl:text><xsl:value-of select='x:name(id(x:deref(., $interface), $interface), $package)'/><xsl:text>;&#10;</xsl:text>
            </xsl:for-each>
            <xsl:text>&#10;</xsl:text>
          </xsl:if>
          <xsl:choose>
            <xsl:when test="self::idl:interface">public interface <xsl:value-of select='@name'/></xsl:when>
            <xsl:when test="self::idl:exception">public class <xsl:value-of select='@name'/> extends RuntimeException</xsl:when>
          </xsl:choose>
          <xsl:if test='idl:extends'>
            <xsl:text> extends </xsl:text>
            <xsl:for-each select='idl:extends'>
              <xsl:if test='position() != 1'>, </xsl:if>
              <xsl:value-of select='id(x:deref(@ref, .))/@name'/>
            </xsl:for-each>
          </xsl:if>
          <xsl:text> {&#10;</xsl:text>
          <xsl:if test='self::idl:exception'>
            <xsl:value-of select='concat("&#10;    public ", @name, "(")'/>
            <xsl:for-each select='idl:member'>
              <xsl:value-of select='concat(x:type(.), " ", @name, ", ")'/>
            </xsl:for-each>
            <xsl:text>String message) {&#10;        super(message);&#10;</xsl:text>
            <xsl:for-each select='idl:member'>
              <xsl:value-of select='concat("        this.", @name, " = ", @name, ";&#10;")'/>
            </xsl:for-each>
            <xsl:text>    }&#10;</xsl:text>
          </xsl:if>
          <xsl:for-each select='idl:member'>
            <xsl:value-of select='concat("    public ", x:type(.), " ", @name, ";&#10;")'/>
          </xsl:for-each>
          <xsl:for-each select='idl:attribute'>
            <xsl:variable name="fixedname" select="replace(@name, 'xml', 'XML')"/>
            <xsl:value-of select='concat("    ", x:type(.), " get", upper-case(substring($fixedname, 1, 1)), substring($fixedname, 2), "();&#10;")'/>
	 	  	    <xsl:if test='not(@readonly="true")'>
	            <xsl:value-of select='concat("    void set", upper-case(substring($fixedname, 1, 1)), substring($fixedname, 2), "(", x:type(.), " ", $fixedname, ");&#10;")'/>
	          </xsl:if>
          </xsl:for-each>
          <xsl:for-each select='idl:operation'>
            <xsl:value-of select='concat("    ", x:type(.), " ", @name, "(")'/>
            <xsl:for-each select='idl:argument'>
              <xsl:if test='position() != 1'>, </xsl:if>
              <xsl:value-of select='concat(x:type(.), " ", @name)'/>
            </xsl:for-each>
            <xsl:text>);&#10;</xsl:text>
          </xsl:for-each>
          <xsl:if test='self::idl:exception'>
            <xsl:for-each select='//idl:const[@associatedexception=current()/@scopedname]'>
              <xsl:value-of select='concat("    public static final ", x:type(.), " ", @name, " = ", @value, ";&#10;")'/>
            </xsl:for-each>
          </xsl:if>
          <xsl:for-each select='idl:const'>
            <xsl:value-of select='concat("    final ", x:type(.), " ", @name, " = ", @value, ";&#10;")'/>
          </xsl:for-each>
          <xsl:text>}&#10;</xsl:text>
        </xsl:result-document>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:function name='x:name'>
    <xsl:param name='type'/>
    <xsl:param name='thispackage'/>
    <xsl:variable name='module-part' select='replace(substring-after($type/ancestor::idl:module[1]/@scopedname, "::"), "::", ".")'/>
    <xsl:variable name='package' select='concat("org.w3c.", if ($module-part = "dom") then "" else "dom.", $module-part)'/>
    <xsl:value-of select='if ($thispackage = $package) then $type/@name else concat($package, ".", $type/@name)'/>
  </xsl:function>

  <xsl:function name='x:type'>
    <xsl:param name='n'/>
    <xsl:choose>
      <xsl:when test='$n/idl:type/idl:scopedname'>
        <xsl:variable name='s' select='$n/idl:type/idl:scopedname/@name'/>
        <xsl:value-of select='reverse(tokenize($s, "::"))[1]'/>
      </xsl:when>
      <xsl:when test='$n/@type = "DOMString"'>String</xsl:when>
      <xsl:when test='$n/@type = "unsigned long"'>long</xsl:when>
      <xsl:when test='$n/@type = "unsigned short"'>short</xsl:when>
      <xsl:when test='$n/@type = "octet"'>byte</xsl:when>
      <xsl:otherwise><xsl:value-of select='$n/@type'/></xsl:otherwise>
    </xsl:choose>
  </xsl:function>

  <xsl:function name='x:deref'>
    <xsl:param name='s'/>
    <xsl:param name='ctx' as='node()'/>
    <xsl:variable name='n' select='id($s, $ctx)'/>
    <xsl:choose>
      <xsl:when test='$n/self::idl:typedef/idl:type/idl:scopedname'>
        <xsl:copy-of select='x:deref($n/idl:type/idl:scopedname/@ref, $ctx)'/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select='$s'/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:function>
</xsl:stylesheet>

