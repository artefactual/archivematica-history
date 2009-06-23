<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:nz_govt_natlib_xsl_XSLTFunctions="nz.govt.natlib.xsl.XSLTFunctions">
  <xsl:strip-space elements="doc chapter section"/>
  <xsl:output omit-xml-declaration="yes" indent="yes" encoding="iso-8859-1" version="1.0"/>
  <xsl:template match="/">
    <File>
      <FileIdentifier>
        <xsl:value-of select="nz_govt_natlib_xsl_XSLTFunctions:determineFileIdentifier(string(TIFF/METADATA/PID),string(TIFF/METADATA/OID),string(TIFF/METADATA/FILENAME),string(TIFF/METADATA/FID))"/>
      </FileIdentifier>
      <xsl:for-each select="TIFF/METADATA/PATH">
        <Path>
          <xsl:value-of select="."/>
        </Path>
      </xsl:for-each>
      <Filename>
        <xsl:for-each select="TIFF/METADATA/FILENAME">
          <Name>
            <xsl:value-of select="."/>
          </Name>
        </xsl:for-each>
        <xsl:for-each select="TIFF/METADATA/EXTENSION">
          <Extension>
            <xsl:value-of select="."/>
          </Extension>
        </xsl:for-each>
      </Filename>
      <xsl:for-each select="TIFF/METADATA/FILELENGTH">
        <Size>
          <xsl:value-of select="."/>
        </Size>
      </xsl:for-each>
      <FileDateTime>
        <xsl:for-each select="TIFF/METADATA/DATE">
          <Date format="yyyyMMdd">
            <xsl:value-of select="."/>
          </Date>
        </xsl:for-each>
        <xsl:for-each select="TIFF/METADATA/TIME">
          <Time format="HHmmssSSS">
            <xsl:value-of select="."/>
          </Time>
        </xsl:for-each>
      </FileDateTime>
      <xsl:for-each select="TIFF/METADATA/TYPE">
        <Mimetype>
          <xsl:value-of select="."/>
        </Mimetype>
      </xsl:for-each>
      <FileFormat>
        <Format>
          <xsl:value-of select="string('Tagged Information File Format')"/>
        </Format>
        <Version>
          <xsl:value-of select="string('6.0')"/>
        </Version>
      </FileFormat>
      <!-- now process the individual tags for this file format -->
      <xsl:apply-templates select="TIFF/IMAGEFILEDIRECTORY"/>
    </File>
  </xsl:template>
  <!-- process the image file directory -->
  <xsl:template match="IMAGEFILEDIRECTORY">
    <xsl:element name="Image">
      <!-- put all gathered variables into the proper format and stream... -->
      <!-- Resolution, Dimension, TonalResolution, ColourSpace, ColourManagement, ColourLookupTable, Orientation, Compression -->
      <xsl:element name="ImageResolution">
        <xsl:element name="SamplingFrequencyUnit">
          <xsl:variable name="resunit">
            <xsl:call-template name="get-element">
              <xsl:with-param name="in" select="//ELEMENT"/>
              <xsl:with-param name="find" select="'ResolutionUnit'"/>
            </xsl:call-template>
          </xsl:variable>
          <xsl:variable name="resunitstring">
            <!--
                    1 = No absolute unit of measurement. Used for images that may have a non-square
                    aspect ratio but no meaningful absolute dimensions.
                    2 = Inch.
                    3 = Centimeter.
                  -->
            <xsl:choose>
              <xsl:when test="$resunit=1">none</xsl:when>
              <xsl:when test="$resunit=2">dpi</xsl:when>
              <xsl:when test="$resunit=2">dpcm</xsl:when>
              <xsl:otherwise>dpi</xsl:otherwise>
            </xsl:choose>
          </xsl:variable>
          <xsl:value-of select="$resunitstring"/>
        </xsl:element>
        <xsl:element name="XSamplingFrequency">
          <xsl:call-template name="get-element">
            <xsl:with-param name="in" select="//ELEMENT"/>
            <xsl:with-param name="find" select="'XResolution'"/>
          </xsl:call-template>
        </xsl:element>
        <xsl:element name="YSamplingFrequency">
          <xsl:call-template name="get-element">
            <xsl:with-param name="in" select="//ELEMENT"/>
            <xsl:with-param name="find" select="'YResolution'"/>
          </xsl:call-template>
        </xsl:element>
      </xsl:element>
      <xsl:element name="ImageDimension">
        <xsl:element name="Width">
          <xsl:call-template name="get-element">
            <xsl:with-param name="in" select="//ELEMENT"/>
            <xsl:with-param name="find" select="'ImageWidth'"/>
          </xsl:call-template>
        </xsl:element>
        <xsl:element name="Length">
          <xsl:call-template name="get-element">
            <xsl:with-param name="in" select="//ELEMENT"/>
            <xsl:with-param name="find" select="'ImageLength'"/>
          </xsl:call-template>
        </xsl:element>
      </xsl:element>
      <xsl:element name="BitsPerSample">
        <xsl:call-template name="get-element">
          <xsl:with-param name="in" select="//ELEMENT"/>
          <xsl:with-param name="find" select="'BitsPerSample'"/>
        </xsl:call-template>
      </xsl:element>
      <xsl:element name="PhotometricInterpretation">
        <xsl:element name="ColourSpace">
          <xsl:variable name="cspace">
            <xsl:call-template name="get-element">
              <xsl:with-param name="in" select="//ELEMENT"/>
              <xsl:with-param name="find" select="'PhotometricInterpretation'"/>
            </xsl:call-template>
          </xsl:variable>
          <!--
                    WhiteIsZero 0
                    BlackIsZero 1
                    RGB 2
                    RGB Palette 3
                    Transparency mask 4
                    CMYK 5
                    YCbCr 6
                    CIELab 8
                  -->
          <xsl:choose>
            <xsl:when test="$cspace=0">WhiteIsZero</xsl:when>
            <xsl:when test="$cspace=1">BlackIsZero</xsl:when>
            <xsl:when test="$cspace=2">RGB</xsl:when>
            <xsl:when test="$cspace=3">RGB Palette</xsl:when>
            <xsl:when test="$cspace=4">Transparency mask</xsl:when>
            <xsl:when test="$cspace=5">CMYK</xsl:when>
            <xsl:when test="$cspace=6">YCbCr</xsl:when>
            <xsl:when test="$cspace=8">CIELab</xsl:when>
            <xsl:otherwise>unknown</xsl:otherwise>
          </xsl:choose>
        </xsl:element>
        <xsl:element name="ICCProfileName"/>
      </xsl:element>
      <xsl:element name="ColourMap"/>
      <xsl:element name="Orientation">
        <xsl:variable name="orient">
          <xsl:call-template name="get-element">
            <xsl:with-param name="in" select="//ELEMENT"/>
            <xsl:with-param name="find" select="'Orientation'"/>
          </xsl:call-template>
        </xsl:variable>
        <!--
                  1 = The 0th row represents the visual top of the image, and the 0th column represents
                  the visual left-hand side.
                  2 = The 0th row represents the visual top of the image, and the 0th column represents
                  the visual right-hand side.
                  3 = The 0th row represents the visual bottom of the image, and the 0th column represents
                  the visual right-hand side.
                  4 = The 0th row represents the visual bottom of the image, and the 0th column represents
                  the visual left-hand side.
                  5 = The 0th row represents the visual left-hand side of the image, and the 0th column
                  represents the visual top.
                  6 = The 0th row represents the visual right-hand side of the image, and the 0th column
                  represents the visual top.
                  7 = The 0th row represents the visual right-hand side of the image, and the 0th column
                  represents the visual bottom.
                  8 = The 0th row represents the visual left-hand side of the image, and the 0th column
                  represents the visual bottom.
                -->
        <xsl:choose>
          <xsl:when test="$orient=2">0degrees, mirror</xsl:when>
          <xsl:when test="$orient=3">180degrees</xsl:when>
          <xsl:when test="$orient=4">180degrees, mirror</xsl:when>
          <xsl:when test="$orient=5">90degrees, mirror</xsl:when>
          <xsl:when test="$orient=6">270degrees</xsl:when>
          <xsl:when test="$orient=7">270degrees, mirror</xsl:when>
          <xsl:when test="$orient=8">90degrees</xsl:when>
          <xsl:otherwise>0degrees</xsl:otherwise>
        </xsl:choose>
      </xsl:element>
      <xsl:element name="Compression">
        <xsl:element name="Scheme">
          <xsl:variable name="comp">
            <xsl:call-template name="get-element">
              <xsl:with-param name="in" select="//ELEMENT"/>
              <xsl:with-param name="find" select="'Compression'"/>
            </xsl:call-template>
          </xsl:variable>
          <!--
                    Uncompressed=1
                    CCITT 1D=2
                    Group 3 Fax=3
                    Group 4 Fax=4
                    LZW=5
                    JPEG=6
                    PackBits=32773
  				-->
          <xsl:choose>
            <xsl:when test="$comp=2">CCITT 1D</xsl:when>
            <xsl:when test="$comp=3">Group 3 Fax</xsl:when>
            <xsl:when test="$comp=4">Group 4 Fax</xsl:when>
            <xsl:when test="$comp=5">LZW</xsl:when>
            <xsl:when test="$comp=6">JPEG</xsl:when>
            <xsl:when test="$comp=32773">PackBits</xsl:when>
            <xsl:otherwise>Uncompressed</xsl:otherwise>
          </xsl:choose>
         </xsl:element>
         <xsl:element name="Level"/>
      </xsl:element>
    </xsl:element>
  </xsl:template>
  <xsl:template match="ELEMENT"/>
  <!-- helper method designed to get a node that has the valie "find" in it -->
  <xsl:template name="get-element">
    <xsl:param name="in"/>
    <xsl:param name="find"/>
    <xsl:for-each select="$in/NAME">
      <xsl:if test="normalize-space(.)=$find">
        <xsl:for-each select="../VALUE">
          <xsl:value-of select="normalize-space(.)"/>
          <xsl:if test="position()!=last()">
            <xsl:value-of select="', '"/>
          </xsl:if>
        </xsl:for-each>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2002 eXcelon Corp.
<metaInformation>
<scenarios ><scenario default="yes" name="Test" userelativepaths="yes" externalpreview="no" url="..\..\harvested\new native\003856.tif.xml" htmlbaseurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="tiff_6_0.dtd" srcSchemaRoot="TIFF" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="nlnz_file.xsd" destSchemaRoot="File" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->