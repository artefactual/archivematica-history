<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:nz_govt_natlib_xsl_XSLTFunctions="nz.govt.natlib.xsl.XSLTFunctions">
  <xsl:strip-space elements="doc chapter section"/>
  <xsl:output omit-xml-declaration="yes" indent="yes" encoding="iso-8859-1" version="1.0"/>
  <xsl:template match="/">
    <File>
      <FileIdentifier>
        <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:determineFileIdentifier(string(OPENOFFICE/METADATA/PID),string(OPENOFFICE/METADATA/OID),string(OPENOFFICE/METADATA/FILENAME),string(OPENOFFICE/METADATA/FID))"/>
      </FileIdentifier>
      <xsl:for-each select="OPENOFFICE/METADATA/PATH">
        <Path>
          <xsl:value-of select="."/>
        </Path>
      </xsl:for-each>
      <Filename>
        <xsl:for-each select="OPENOFFICE/METADATA/FILENAME">
          <Name>
            <xsl:value-of select="."/>
          </Name>
        </xsl:for-each>
        <xsl:for-each select="OPENOFFICE/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </Filename>
      <xsl:for-each select="OPENOFFICE/METADATA/FILELENGTH">
        <Size>
          <xsl:value-of select="."/>
        </Size>
      </xsl:for-each>
      <FileDateTime>
        <xsl:for-each select="OPENOFFICE/METADATA/DATE">
          <Date format="yyyyMMdd">
            <xsl:value-of select="."/>
          </Date>
        </xsl:for-each>
        <xsl:for-each select="OPENOFFICE/METADATA/TIME">
          <Time format="HHmmssSSS">
            <xsl:value-of select="."/>
          </Time>
        </xsl:for-each>
      </FileDateTime>
      <xsl:for-each select="OPENOFFICE/METADATA/TYPE">
        <Mimetype>
          <xsl:value-of select="."/>
        </Mimetype>
      </xsl:for-each>
      <FileFormat>
        <Format>
          <xsl:value-of select="concat(string('Open Office'),string(', '),string(OPENOFFICE/CONTENT/CLASS))"/>
        </Format>
        <Version>
          <xsl:value-of select="string(OPENOFFICE/CONTENT/VERSION)"/>
        </Version>
      </FileFormat>
      <Text>
        <CharacterSet>
          <xsl:value-of select="string('ISO-8859-1')"/>
        </CharacterSet>
        <MarkupLanguage>
          <xsl:value-of select="string(OPENOFFICE/PROPERTIES/LANGUAGE)"/>
        </MarkupLanguage>
      </Text>
    </File>
  </xsl:template>
</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2002 eXcelon Corp.
<metaInformation>
<scenarios ><scenario default="yes" name="test1" userelativepaths="yes" externalpreview="no" url="..\..\harvested\nlnz_dd\A PSALM OF LIFE wordv97&#x2D;v2000.doc.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="word_ole.dtd" srcSchemaRoot="OPENOFFICE" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="nlnz_file.xsd" destSchemaRoot="File" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->