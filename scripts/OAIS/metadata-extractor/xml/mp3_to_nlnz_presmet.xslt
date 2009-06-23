<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:nz_govt_natlib_xsl_XSLTFunctions="nz.govt.natlib.xsl.XSLTFunctions">
  <xsl:strip-space elements="doc chapter section"/>
  <xsl:output omit-xml-declaration="yes" indent="yes" encoding="iso-8859-1" version="1.0"/>
  <xsl:template match="/">
    <File>
      <FileIdentifier>
        <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:determineFileIdentifier(string(MP3/METADATA/PID),string(MP3/METADATA/OID),string(MP3/METADATA/FILENAME),string(MP3/METADATA/FID))"/>
      </FileIdentifier>
      <xsl:for-each select="MP3/METADATA/PATH">
        <Path>
          <xsl:value-of select="."/>
        </Path>
      </xsl:for-each>
      <Filename>
        <xsl:for-each select="MP3/METADATA/FILENAME">
          <Name>
            <xsl:value-of select="."/>
          </Name>
        </xsl:for-each>
        <xsl:for-each select="MP3/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </Filename>
      <xsl:for-each select="MP3/METADATA/FILELENGTH">
        <Size>
          <xsl:value-of select="."/>
        </Size>
      </xsl:for-each>
      <FileDateTime>
        <xsl:for-each select="MP3/METADATA/DATE">
          <Date format="yyyyMMdd">
            <xsl:value-of select="."/>
          </Date>
        </xsl:for-each>
        <xsl:for-each select="MP3/METADATA/TIME">
          <Time format="HHmmssSSS">
            <xsl:value-of select="."/>
          </Time>
        </xsl:for-each>
      </FileDateTime>
      <xsl:for-each select="MP3/METADATA/TYPE">
        <Mimetype>
          <xsl:value-of select="."/>
        </Mimetype>
      </xsl:for-each>
      <FileFormat>
        <Format>
          <xsl:value-of select="string('MPEG Audio')"/>
        </Format>
        <Version>
          <xsl:value-of select="concat(string(MP3/MPEG/VERSION),string(', '),string(MP3/MPEG/LAYER-NAME))"/>
        </Version>
      </FileFormat>
      <Audio>
          <Resolution>
            <xsl:value-of select="string('16')"/>
          </Resolution>
        <Duration>
          <Time>
            <xsl:attribute name="format">
              <xsl:value-of select="string('ms')"/>
            </xsl:attribute>
            <xsl:value-of select="MP3/MPEG/DURATION/TOTAL-MILLISECONDS"/>
          </Time>
        </Duration>
        <xsl:for-each select="MP3/MPEG/SAMPLE-RATE">
          <BitRate>
            <xsl:value-of select="."/>
          </BitRate>
        </xsl:for-each>
          <Compression>
            <xsl:value-of select="string('MPEG Audio')"/>
          </Compression>
        <xsl:for-each select="MP3/MPEG/CHANNELS">
          <Channels>
            <xsl:value-of select="."/>
          </Channels>
        </xsl:for-each>
        <xsl:for-each select="MP3/MPEG/VERSION-NAME">
          <EncapsulationName>
            <xsl:value-of select="."/>
          </EncapsulationName>
        </xsl:for-each>
        <xsl:for-each select="MP3/MPEG/LAYER-NAME">
          <EncapsulationVersion>
            <xsl:value-of select="."/>
          </EncapsulationVersion>
        </xsl:for-each>
      </Audio>
    </File>
  </xsl:template>
</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2002 eXcelon Corp.
<metaInformation>
<scenarios ><scenario default="yes" name="Test1" userelativepaths="yes" externalpreview="no" url="..\..\harvested\new native\02&#x2D;AudioTrack 02.wav.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="wav.dtd" srcSchemaRoot="MP3" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="nlnz_file.xsd" destSchemaRoot="File" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->