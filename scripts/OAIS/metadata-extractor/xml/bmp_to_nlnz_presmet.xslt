<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:nz_govt_natlib_xsl_XSLTFunctions="nz.govt.natlib.xsl.XSLTFunctions">
  <xsl:strip-space elements="doc chapter section"/>
  <xsl:output omit-xml-declaration="yes" indent="yes" encoding="iso-8859-1" version="1.0"/>
  <xsl:template match="/">
    <File>
      <FileIdentifier>
        <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:determineFileIdentifier(string(BMP/METADATA/PID),string(BMP/METADATA/OID),string(BMP/METADATA/FILENAME),string(BMP/METADATA/FID))"/>
      </FileIdentifier>
      <xsl:for-each select="BMP/METADATA/PATH">
        <Path>
          <xsl:value-of select="."/>
        </Path>
      </xsl:for-each>
      <Filename>
        <xsl:for-each select="BMP/METADATA/FILENAME">
          <Name>
            <xsl:value-of select="."/>
          </Name>
        </xsl:for-each>
        <xsl:for-each select="BMP/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </Filename>
      <xsl:for-each select="BMP/METADATA/FILELENGTH">
        <Size>
          <xsl:value-of select="."/>
        </Size>
      </xsl:for-each>
      <FileDateTime>
        <xsl:for-each select="BMP/METADATA/DATE">
          <Date format="yyyyMMdd">
            <xsl:value-of select="."/>
          </Date>
        </xsl:for-each>
        <xsl:for-each select="BMP/METADATA/TIME">
          <Time format="HHmmssSSS">
            <xsl:value-of select="."/>
          </Time>
        </xsl:for-each>
      </FileDateTime>
      <xsl:for-each select="BMP/METADATA/TYPE">
        <Mimetype>
          <xsl:value-of select="."/>
        </Mimetype>
      </xsl:for-each>
      <FileFormat>
        <Format>
          <xsl:value-of select="string('MS Bitmap')"/>
        </Format>
      </FileFormat>
      <Image>
        <ImageResolution>
          <xsl:for-each select="BMP/BITMAPINFO/RESOLUTIONUNIT">
            <SamplingFrequencyUnit>
              <xsl:value-of select="."/>
            </SamplingFrequencyUnit>
          </xsl:for-each>
          <xsl:for-each select="BMP/BITMAPINFO/XRESOLUTION">
            <XSamplingFrequency>
              <xsl:value-of select="."/>
            </XSamplingFrequency>
          </xsl:for-each>
          <xsl:for-each select="BMP/BITMAPINFO/YRESOLUTION">
            <YSamplingFrequency>
              <xsl:value-of select="."/>
            </YSamplingFrequency>
          </xsl:for-each>
          <xsl:for-each select="BMP/INFORMATION/XRESOLUTION">
            <XSamplingFrequency>
              <xsl:value-of select="."/>
            </XSamplingFrequency>
          </xsl:for-each>
          <xsl:for-each select="BMP/INFORMATION/YRESOLUTION">
            <YSamplingFrequency>
              <xsl:value-of select="."/>
            </YSamplingFrequency>
          </xsl:for-each>
        </ImageResolution>
        <ImageDimension>
          <xsl:for-each select="BMP/BITMAPINFO/WIDTH">
            <Width>
              <xsl:value-of select="."/>
            </Width>
          </xsl:for-each>
          <xsl:for-each select="BMP/BITMAPINFO/HEIGHT">
            <Length>
              <xsl:value-of select="."/>
            </Length>
          </xsl:for-each>
          <xsl:for-each select="BMP/INFORMATION/WIDTH">
            <Width>
              <xsl:value-of select="."/>
            </Width>
          </xsl:for-each>
          <xsl:for-each select="BMP/INFORMATION/HEIGHT">
            <Length>
              <xsl:value-of select="."/>
            </Length>
          </xsl:for-each>
        </ImageDimension>
        <xsl:for-each select="BMP/BITMAPINFO/BITCOUNT">
          <BitsPerSample>
            <xsl:value-of select="."/>
          </BitsPerSample>
        </xsl:for-each>
        <xsl:for-each select="BMP/INFORMATION/BITCOUNT">
          <BitsPerSample>
            <xsl:value-of select="."/>
          </BitsPerSample>
        </xsl:for-each>
        <ColorMap>
          <xsl:value-of select="string('')"/>
        </ColorMap>
        <Orientation>
          <xsl:value-of select="string('')"/>
        </Orientation>
        <Compression>
          <xsl:for-each select="BMP/BITMAPINFO/COMPRESSIONNAME">
            <Scheme>
              <xsl:value-of select="."/>
            </Scheme>
          </xsl:for-each>
          <xsl:for-each select="BMP/BITMAPINFO/COMPRESSION">
            <Level>
              <xsl:value-of select="."/>
            </Level>
          </xsl:for-each>
          <xsl:for-each select="BMP/INFORMATION/COMPRESSION">
            <Scheme>
              <xsl:value-of select="."/>
            </Scheme>
          </xsl:for-each>
        </Compression>
      </Image>
    </File>
  </xsl:template>
</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2002 eXcelon Corp.
<metaInformation>
<scenarios ><scenario default="yes" name="Test" userelativepaths="yes" externalpreview="no" url="..\..\harvested\new native\Blue Lace 16.bmp.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="bmp.dtd" srcSchemaRoot="BMP" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="nlnz_file.xsd" destSchemaRoot="File" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->