<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:droid="http://www.nationalarchives.gov.uk/pronom/FileCollection">

  <xsl:template match="/">
    <fits xmlns="http://hul.harvard.edu/ois/xml/ns/fits/fits_output">
		<identification>
		<xsl:for-each select="droid:FileCollection/droid:IdentificationFile/droid:FileFormatHit">
			<identity>
				<!-- format and mimetype -->
				<xsl:attribute name="format">
					<xsl:variable name="format" select="droid:Name" />
					<xsl:choose>
						<xsl:when test="starts-with($format,'Microsoft Word')">
							<xsl:value-of select="string('Microsoft Word')"/>
						</xsl:when>			
						<xsl:when test="not($format) or $format=''">
							<xsl:value-of select="string('Unknown Binary')"/>
						</xsl:when>	
						<xsl:otherwise>
							<xsl:value-of select="$format"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute> 
				<xsl:attribute name="mimetype">		
					<xsl:variable name="mime" select="droid:MimeType" />
					<xsl:choose>
						<xsl:when test="$mime='txt/xml'">
							<xsl:value-of select="string('text/xml')"/>
						</xsl:when>
						<xsl:when test="not($mime) or $mime=''">
							<xsl:value-of select="string('application/octet-stream')"/>
						</xsl:when>	
						<xsl:otherwise>
							<xsl:value-of select="$mime"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute> 
			  
			  <!-- version -->	
			  <xsl:if test="droid:Version">		  
			  	<xsl:variable name="version" select="droid:Version"/>
					<xsl:choose>
						<xsl:when test="$version='1987a'">
							<version>
								<xsl:value-of select="string('87a')"/>
							</version>
						</xsl:when>
						<xsl:otherwise>
							<version>
								<xsl:value-of select="$version"/>
							</version>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:if>

			  <!-- external PUID Identifier -->
			  <xsl:for-each select="droid:PUID">
				<externalIdentifier type="puid">
					<xsl:value-of select="."/>
				</externalIdentifier>
			  </xsl:for-each>
	
			</identity>
			</xsl:for-each>
	   </identification>
    </fits>
  </xsl:template>
</xsl:stylesheet>