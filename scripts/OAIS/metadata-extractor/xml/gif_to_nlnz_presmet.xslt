<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:nz_govt_natlib_xsl_XSLTFunctions="nz.govt.natlib.xsl.XSLTFunctions">
  <xsl:strip-space elements="doc chapter section"/>
  <xsl:output omit-xml-declaration="yes" indent="yes" encoding="iso-8859-1" version="1.0"/>
  <xsl:template match="/">
    <File>
      <FileIdentifier>
        <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:determineFileIdentifier(string(GIF/METADATA/PID),string(GIF/METADATA/OID),string(GIF/METADATA/FILENAME),string(GIF/METADATA/FID))"/>
      </FileIdentifier>
      <xsl:for-each select="GIF/METADATA/PATH">
        <Path>
          <xsl:value-of select="."/>
        </Path>
      </xsl:for-each>
      <Filename>
        <xsl:for-each select="GIF/METADATA/FILENAME">
          <Name>
            <xsl:value-of select="."/>
          </Name>
        </xsl:for-each>
        <xsl:for-each select="GIF/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </Filename>
      <xsl:for-each select="GIF/METADATA/FILELENGTH">
        <Size>
          <xsl:value-of select="."/>
        </Size>
      </xsl:for-each>
      <FileDateTime>
        <xsl:for-each select="GIF/METADATA/DATE">
          <Date format="yyyyMMdd">
            <xsl:value-of select="."/>
          </Date>
        </xsl:for-each>
        <xsl:for-each select="GIF/METADATA/TIME">
          <Time format="HHmmssSSS">
            <xsl:value-of select="."/>
          </Time>
        </xsl:for-each>
      </FileDateTime>
      <xsl:for-each select="GIF/METADATA/TYPE">
        <Mimetype>
          <xsl:value-of select="."/>
        </Mimetype>
      </xsl:for-each>
      <FileFormat>
        <Format>
          <xsl:value-of select="string('GIF')"/>
        </Format>
        <xsl:for-each select="GIF/VERSION">
        <Version>
          <xsl:value-of select="."/>
        </Version>
        </xsl:for-each>
      </FileFormat>
      <Image>
        <ImageDimension>
          <xsl:for-each select="GIF/SCREEN-WIDTH">
            <Width>
              <xsl:value-of select="."/>
            </Width>
          </xsl:for-each>
          <xsl:for-each select="GIF/SCREEN-HEIGHT">
            <Length>
              <xsl:value-of select="."/>
            </Length>
          </xsl:for-each>
        </ImageDimension>
        <xsl:for-each select="GIF/BITS-PER-PIXEL">
          <BitsPerSample>
            <xsl:value-of select="."/>
          </BitsPerSample>
        </xsl:for-each>
        <ColorMap>
          <xsl:value-of select="string('RGB')"/>
        </ColorMap>
        <Orientation>
          <xsl:value-of select="string('n/a')"/>
        </Orientation>
        <Compression>
            <Scheme>
              <xsl:value-of select="string('n/a')"/>
            </Scheme>
            <Level>
              <xsl:value-of select="string('n/a')"/>
            </Level>
            <Scheme>
              <xsl:value-of select="string('n/a')"/>
            </Scheme>
        </Compression>
      </Image>
    </File>
  </xsl:template>
</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2002 eXcelon Corp.
<metaInformation>
<scenarios ><scenario default="yes" name="Test" userelativepaths="yes" externalpreview="no" url="..\..\harvested\new native\Blue Lace 16.bmp.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="bmp.dtd" srcSchemaRoot="GIF" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="nlnz_file.xsd" destSchemaRoot="File" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->