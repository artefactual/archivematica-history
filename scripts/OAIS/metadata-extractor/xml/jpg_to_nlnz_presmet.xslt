<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:nz_govt_natlib_xsl_XSLTFunctions="nz.govt.natlib.xsl.XSLTFunctions">
  <xsl:strip-space elements="doc chapter section"/>
  <xsl:output omit-xml-declaration="yes" indent="yes" encoding="iso-8859-1" version="1.0"/>
  <xsl:template match="/">
    <File>
      <FileIdentifier>
        <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:determineFileIdentifier(string(JPG/METADATA/PID),string(JPG/METADATA/OID),string(JPG/METADATA/FILENAME),string(JPG/METADATA/FID))"/>
      </FileIdentifier>
      <xsl:for-each select="JPG/METADATA/PATH">
        <Path>
          <xsl:value-of select="."/>
        </Path>
      </xsl:for-each>
      <Filename>
        <xsl:for-each select="JPG/METADATA/FILENAME">
          <Name>
            <xsl:value-of select="."/>
          </Name>
        </xsl:for-each>
        <xsl:for-each select="JPG/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </Filename>
      <xsl:for-each select="JPG/METADATA/FILELENGTH">
        <Size>
          <xsl:value-of select="."/>
        </Size>
      </xsl:for-each>
      <FileDateTime>
        <xsl:for-each select="JPG/METADATA/DATE">
          <Date format="yyyyMMdd">
            <xsl:value-of select="."/>
          </Date>
        </xsl:for-each>
        <xsl:for-each select="JPG/METADATA/TIME">
          <Time format="HHmmssSSS">
            <xsl:value-of select="."/>
          </Time>
        </xsl:for-each>
      </FileDateTime>
      <xsl:for-each select="JPG/METADATA/TYPE">
        <Mimetype>
          <xsl:value-of select="."/>
        </Mimetype>
      </xsl:for-each>
      <FileFormat>
        <Format>
          <xsl:value-of select="string('JPEG')"/>
        </Format>
      </FileFormat>
      <Image>
        <ImageResolution>
          <!-- Choose the EXIF vaues instead of the JFIF if present -->
          <xsl:variable name="exif" select="JPG/EXIF"/>
          <xsl:choose>
            <!-- JFIFTag is the default value -->
            <xsl:when test="string-length($exif)=0">
              <xsl:variable name="units" select="JPG/JFIF/DENSITYUNITS"/>
              <SamplingFrequencyUnit>
                <xsl:choose>
                  <xsl:when test="$units=0">
                    <xsl:value-of select="1"/>
                  </xsl:when>
                  <xsl:when test="$units=1">
                    <xsl:value-of select="2"/>
                  </xsl:when>
                  <xsl:when test="$units=2">
                    <xsl:value-of select="3"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="string('')"/>
                  </xsl:otherwise>
                </xsl:choose>
              </SamplingFrequencyUnit>
              <XSamplingFrequency>
                <xsl:variable name="xdens" select="JPG/JFIF/XDENSITY"/>
                <xsl:choose>
                  <xsl:when test="$units=0">
                    <xsl:value-of select="$xdens"/>
                  </xsl:when>
                  <xsl:when test="$units=1">
                    <xsl:value-of select="$xdens"/>
                  </xsl:when>
                  <xsl:when test="$units=2">
                    <xsl:value-of select="$xdens"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="string('')"/>
                  </xsl:otherwise>
                </xsl:choose>
              </XSamplingFrequency>
              <YSamplingFrequency>
                <xsl:variable name="ydens" select="JPG/JFIF/YDENSITY"/>
                <xsl:choose>
                  <xsl:when test="$units=0">
                    <xsl:value-of select="$ydens"/>
                  </xsl:when>
                  <xsl:when test="$units=1">
                    <xsl:value-of select="$ydens"/>
                  </xsl:when>
                  <xsl:when test="$units=2">
                    <xsl:value-of select="$ydens"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="string('')"/>
                  </xsl:otherwise>
                </xsl:choose>
              </YSamplingFrequency>
            </xsl:when>
            <xsl:otherwise>
              <SamplingFrequencyUnit>
                <xsl:value-of select="JPG/EXIF/RESOLUTIONUNIT/VALUE"/>
              </SamplingFrequencyUnit>
              <XSamplingFrequency>
                <xsl:value-of select="JPG/EXIF/XRESOLUTION/VALUE"/>
              </XSamplingFrequency>
              <YSamplingFrequency>
                <xsl:value-of select="JPG/EXIF/YRESOLUTION/VALUE"/>
              </YSamplingFrequency>
            </xsl:otherwise>
          </xsl:choose>
        </ImageResolution>
        <ImageDimension>
          <xsl:for-each select="JPG/IMAGE/IMAGEWIDTH">
            <Width>
              <xsl:value-of select="."/>
            </Width>
          </xsl:for-each>
          <xsl:for-each select="JPG/IMAGE/IMAGEHEIGHT">
            <Length>
              <xsl:value-of select="."/>
            </Length>
          </xsl:for-each>
        </ImageDimension>
        <xsl:for-each select="JPG/IMAGE/PRECISION">
          <BitsPerSample>
            <xsl:value-of select="."/>
          </BitsPerSample>
        </xsl:for-each>
        <PhotometricInterpretation>
          <xsl:variable name="cspace" select="JPG/IMAGE/COMPONENTS"/>
          <xsl:choose>
            <xsl:when test="$cspace=1">
              <xsl:value-of select="string('WhiteIsZero')"/>
            </xsl:when>
            <xsl:when test="$cspace=3">
              <xsl:value-of select="string('YCbCr')"/>
            </xsl:when>
            <xsl:when test="$cspace=4">
              <xsl:value-of select="string('CMYK')"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="string('Unknown')"/>
            </xsl:otherwise>
          </xsl:choose>
        </PhotometricInterpretation>
        <ICCProfileName>
          <xsl:value-of select="string('')"/>
        </ICCProfileName>
        <ColorMap>
          <xsl:value-of select="string('')"/>
        </ColorMap>
        <Orientation>
          <!-- All JFIFs are 0 degrees -->
          <xsl:value-of select="string('0degrees')"/>
        </Orientation>
        <Compression>
          <Scheme>
            <!-- JPEG = 6 -->
            <xsl:value-of select="6"/>
          </Scheme>
          <Level>
            <xsl:value-of select="string('')"/>
          </Level>
        </Compression>
      </Image>
    </File>
  </xsl:template>


</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2002 eXcelon Corp.
<metaInformation>
<scenarios ><scenario default="yes" name="Test" userelativepaths="yes" externalpreview="no" url="..\..\..\..\Temp\harvested\native\Picture 038.jpg.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/><scenario default="no" name="JFIF" userelativepaths="yes" externalpreview="no" url="..\..\..\..\Temp\harvested\native\0,,2731487,00.jpg.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="jpg.dtd" srcSchemaRoot="JPG" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="nlnz_file.xsd" destSchemaRoot="File" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->