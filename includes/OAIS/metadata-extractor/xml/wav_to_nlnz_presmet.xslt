<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:nz_govt_natlib_xsl_XSLTFunctions="nz.govt.natlib.xsl.XSLTFunctions">
  <xsl:strip-space elements="doc chapter section"/>
  <xsl:output omit-xml-declaration="yes" indent="yes" encoding="iso-8859-1" version="1.0"/>
  <xsl:template match="/">
    <File>
      <FileIdentifier>
        <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:determineFileIdentifier(string(WAV/METADATA/PID),string(WAV/METADATA/OID),string(WAV/METADATA/FILENAME),string(WAV/METADATA/FID))"/>
      </FileIdentifier>
      <xsl:for-each select="WAV/METADATA/PATH">
        <Path>
          <xsl:value-of select="."/>
        </Path>
      </xsl:for-each>
      <Filename>
        <xsl:for-each select="WAV/METADATA/FILENAME">
          <Name>
            <xsl:value-of select="."/>
          </Name>
        </xsl:for-each>
        <xsl:for-each select="WAV/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </Filename>
      <xsl:for-each select="WAV/METADATA/FILELENGTH">
        <Size>
          <xsl:value-of select="."/>
        </Size>
      </xsl:for-each>
      <FileDateTime>
        <xsl:for-each select="WAV/METADATA/DATE">
          <Date format="yyyyMMdd">
            <xsl:value-of select="."/>
          </Date>
        </xsl:for-each>
        <xsl:for-each select="WAV/METADATA/TIME">
          <Time format="HHmmssSSS">
            <xsl:value-of select="."/>
          </Time>
        </xsl:for-each>
      </FileDateTime>
      <xsl:for-each select="WAV/METADATA/TYPE">
        <Mimetype>
          <xsl:value-of select="."/>
        </Mimetype>
      </xsl:for-each>
      <FileFormat>
        <Format>
          <xsl:value-of select="string('WAVE Audio')"/>
        </Format>
      </FileFormat>
      <Audio>
        <xsl:for-each select="WAV/WAVEHEADER/BITSPERSAMPLE">
          <Resolution>
            <xsl:value-of select="."/>
          </Resolution>
        </xsl:for-each>
        <xsl:for-each select="WAV/WAVE/BITSPERSAMPLE">
          <Resolution>
            <xsl:value-of select="."/>
          </Resolution>
        </xsl:for-each>
        <Duration>
          <Time>
            <xsl:attribute name="format">
              <xsl:value-of select="string('hh:mm:ss.sss')"/>
            </xsl:attribute>
            <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:getDuration(number(WAV/RIFF/LENGTH),number(WAV/WAVE/AVERAGEBYTESPERSEC))"/>
          </Time>
        </Duration>
        <xsl:for-each select="WAV/WAVEHEADER/SAMPLESPERSEC">
          <BitRate>
            <xsl:value-of select="."/>
          </BitRate>
        </xsl:for-each>
        <xsl:for-each select="WAV/WAVEHEADER/COMPRESSED">
          <Compression>
            <xsl:value-of select="."/>
          </Compression>
        </xsl:for-each>
        <xsl:for-each select="WAV/WAVEHEADER/CHANNELS">
          <Channels>
            <xsl:value-of select="."/>
          </Channels>
        </xsl:for-each>
        <xsl:for-each select="WAV/WAVE/SAMPLESPERSEC">
          <BitRate>
            <xsl:value-of select="."/>
          </BitRate>
        </xsl:for-each>
        <Compression>
          <xsl:value-of select="string('')"/>
        </Compression>
        <xsl:for-each select="WAV/WAVE/FORMAT">
          <EncapsulationName>
            <xsl:value-of select="."/>
          </EncapsulationName>
          <EncapsulationVersion/>
        </xsl:for-each>
        <xsl:for-each select="WAV/WAVE/CHANNELS">
          <Channels>
            <xsl:value-of select="."/>
          </Channels>
        </xsl:for-each>
      </Audio>
    </File>
  </xsl:template>
</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2002 eXcelon Corp.
<metaInformation>
<scenarios ><scenario default="yes" name="Test1" userelativepaths="yes" externalpreview="no" url="..\..\harvested\new native\02&#x2D;AudioTrack 02.wav.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="wav.dtd" srcSchemaRoot="WAV" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="nlnz_file.xsd" destSchemaRoot="File" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->