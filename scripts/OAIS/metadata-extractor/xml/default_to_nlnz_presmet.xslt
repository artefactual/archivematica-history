<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:nz_govt_natlib_xsl_XSLTFunctions="nz.govt.natlib.xsl.XSLTFunctions">
  <xsl:strip-space elements="doc chapter section"/>
  <xsl:output omit-xml-declaration="yes" indent="yes" encoding="iso-8859-1" version="1.0"/>
  <xsl:template match="/">
    <File>
      <FileIdentifier>
        <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:determineFileIdentifier(string(DEFAULT/METADATA/PID),string(DEFAULT/METADATA/OID),string(DEFAULT/METADATA/FILENAME),string(DEFAULT/METADATA/FID))"/>
      </FileIdentifier>
      <Filename>
        <xsl:for-each select="DEFAULT/METADATA/FILENAME">
          <Name>
            <xsl:value-of select="."/>
          </Name>
        </xsl:for-each>
        <xsl:for-each select="DEFAULT/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </Filename>
      <FormerFilename>
        <Name>
          <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:getPreviousFileName(string('c:\temp\props1.props'),string(DEFAULT/METADATA/PATH))"/>
        </Name>
        <xsl:for-each select="DEFAULT/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </FormerFilename>
      <xsl:for-each select="DEFAULT/METADATA/FILELENGTH">
        <Size>
          <xsl:value-of select="."/>
        </Size>
      </xsl:for-each>
      <FileDateTime>
        <xsl:for-each select="DEFAULT/METADATA/DATE">
          <Date format="yyyyMMdd">
            <xsl:value-of select="."/>
          </Date>
        </xsl:for-each>
        <xsl:for-each select="DEFAULT/METADATA/TIME">
          <Time format="HHmmssSSS">
            <xsl:value-of select="."/>
          </Time>
        </xsl:for-each>
      </FileDateTime>
      <xsl:for-each select="DEFAULT/METADATA/TYPE">
        <Mimetype>
          <xsl:value-of select="."/>
        </Mimetype>
      </xsl:for-each>
    </File>
  </xsl:template>
</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2002 eXcelon Corp.
<metaInformation>
<scenarios ><scenario default="yes" name="Test" userelativepaths="yes" externalpreview="no" url="..\..\harvested\new native\bowen hosp.gif.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="default.dtd" srcSchemaRoot="DEFAULT" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="nlnz_file.xsd" destSchemaRoot="File" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->