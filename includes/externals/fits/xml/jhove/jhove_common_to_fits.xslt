<?xml version="1.0" ?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:fits_XsltFunctions="edu.harvard.hul.ois.fits.tools.utils.XsltFunctions"
	xmlns:mix="http://www.loc.gov/mix/"
	xmlns="http://hul.harvard.edu/ois/xml/ns/fits/fits_output">
	<xsl:output method="xml" indent="yes" />
	<xsl:strip-space elements="*"/>

	<xsl:template match="/">

	<xsl:variable name="mime" select="repInfo/mimeType"/>
	<identification>
		<identity>
			<xsl:attribute name="mimetype">
				<xsl:choose>
					<xsl:when test="$mime='text/plain; charset=US-ASCII'">
						<xsl:value-of select="string('text/plain')"/>
					</xsl:when>
					<xsl:when test="$mime='text/plain; charset=UTF-8'">
						<xsl:value-of select="string('text/plain')"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="$mime"/>
					</xsl:otherwise>
				</xsl:choose>
 			</xsl:attribute> 
			<!-- profile and format format attributes-->
			<xsl:attribute name="format">
				<xsl:variable name="format">
				<xsl:choose>
			  		<xsl:when test='string(repInfo/profiles/profile)'>
			  			<xsl:value-of select="concat(repInfo/format, ' ', repInfo/profiles/profile)"/>
			  		</xsl:when>		  		
			  		<xsl:otherwise>
			  			<xsl:value-of select="repInfo/format"/>
					</xsl:otherwise>
				</xsl:choose>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="$format='JPEG JFIF'">
						<xsl:value-of select="string('JPEG File Interchange Format')"/>
					</xsl:when>
					<xsl:when test="$format='GIF GIF 87a'">
						<xsl:value-of select="string('Graphics Interchange Format')"/>
					</xsl:when>		
					<xsl:when test="$format='GIF GIF 89a'">
						<xsl:value-of select="string('Graphics Interchange Format')"/>
					</xsl:when>	
					<xsl:when test="$format='TIFF'">
						<xsl:value-of select="string('Tagged Image File Format')"/>
					</xsl:when>
					<xsl:when test="$format='TIFF Baseline RGB (Class R)'">
						<xsl:value-of select="string('Tagged Image File Format')"/>						
					</xsl:when>
					<xsl:when test="$format='TIFF TIFF/IT-BP/P2 (ISO 12639:1998)'">
						<xsl:value-of select="string('Tagged Image File Format')"/>						
					</xsl:when>
					<xsl:when test="$format='XML'">
						<xsl:value-of select="string('Extensible Markup Language')"/>		
					</xsl:when>
					<xsl:when test="$format='HTML'">
						<xsl:value-of select="string('Hypertext Markup Language')"/>		
					</xsl:when>
					<xsl:when test="$format='WAVE PCMWAVEFORMAT'">
						<xsl:value-of select="string('Waveform Audio')"/>	
					</xsl:when>
					<xsl:when test="$format='WAVE WAVEFORMATEX'">
						<xsl:value-of select="string('Waveform Audio')"/>
					</xsl:when>
					<xsl:when test="starts-with($format,'JPEG 2000')">
						<xsl:value-of select="string('JPEG 2000')"/>
					</xsl:when>		
					<xsl:when test="starts-with($format,'TIFF DNG')">
						<xsl:value-of select="string('Digital Negative')"/>
					</xsl:when>
					<xsl:when test="starts-with($format,'PDF')">
						<xsl:value-of select="string('Portable Document Format')"/>
					</xsl:when>												
					<xsl:when test="$format='AIFF AIFF'">
						<xsl:value-of select="string('Audio Interchange File Format')"/>		
					</xsl:when>			
					<xsl:when test="$format='ASCII'">
						<xsl:value-of select="string('Plain text')"/>		
					</xsl:when>
					<xsl:when test="$format='UTF-8'">
						<xsl:value-of select="string('Plain text')"/>		
					</xsl:when>		
					<xsl:when test="$format='bytestream'">
						<xsl:value-of select="string('Unknown Binary')"/>		
					</xsl:when>				
					<xsl:otherwise>
						<xsl:value-of select="$format"/>
					</xsl:otherwise>			
				</xsl:choose>
			</xsl:attribute>
				
			<!-- version -->
			<xsl:if test='repInfo/version'>
				<version>
					<xsl:value-of select="repInfo/version" />
				</version>
			</xsl:if>
		</identity>
	</identification>
	
	<fileinfo>
		<size>
			<xsl:value-of select="repInfo/size" />
		</size>
		<!-- 
		<fslastmodified>
			<xsl:value-of select="repInfo/lastModified" />
		</fslastmodified>
		 -->
		<creatingApplicationName>
			<xsl:choose>
				<xsl:when test="$mime='image/tiff'">
					<xsl:value-of select="//mix:ScanningSoftware"/>					
				</xsl:when>
				<xsl:when test="$mime='image/jpeg'">
					<xsl:choose>
						<xsl:when test="//mix:ScannerModelName">
							<xsl:value-of select="//mix:ScannerModelName"/>	
						</xsl:when>
						<xsl:when test="//property[name='Comments']/values/value">						
						    <xsl:for-each select="//property[name='Comments']/values/value">
						    	<xsl:choose>
						    		<xsl:when test="position()=last()">
						    			<xsl:value-of select="//property[name='Comments']/values/value"/>
						    		</xsl:when>
						    		<xsl:otherwise>
						    			<xsl:value-of select="concat(//property[name='Comments']/values/value,', ')"/>
						    		</xsl:otherwise>
						    	</xsl:choose>
    						</xsl:for-each>
						</xsl:when>
					</xsl:choose>
				</xsl:when>
				<xsl:when test="$mime='image/jp2'">
					<xsl:if test="//property[name='Comments']/values/value">							
						<xsl:value-of select="//property[name='Comments']/values/value"/>			
					</xsl:if>	
				</xsl:when>	
				<xsl:when test="$mime='application/pdf'">
					<xsl:if test="//property[name='Producer']/values/value and //property[name='Creator']/values/value">
						<xsl:value-of select="concat(//property[name='Producer']/values/value,'/',//property[name='Creator']/values/value)"/>
					</xsl:if>
				</xsl:when>			
			</xsl:choose>
		</creatingApplicationName>	
		 
	</fileinfo>
	
	<filestatus>
			<xsl:choose>
			  <xsl:when test='contains(repInfo/status,"Not well-formed")'>
				  <well-formed>false</well-formed>
				  <valid>false</valid>
			  </xsl:when>
			  <xsl:otherwise>
			  	<well-formed>true</well-formed>
				<xsl:choose>
					<xsl:when test='contains(repInfo/status,"not valid")'>
						<valid>false</valid>
					</xsl:when>
				  	<xsl:otherwise>
				  		<valid>true</valid>
				  	</xsl:otherwise>
				  	</xsl:choose>
			  </xsl:otherwise>
			</xsl:choose>
		
		
		<xsl:for-each select="repInfo/messages/message">
			<message>
				<xsl:variable name="messageText" select="."/>
				<xsl:variable name="subMessage" select="@subMessage"/>
				<xsl:variable name="severity" select="@severijty"/>
				<xsl:variable name="offset" select="@offset"/>
				<xsl:value-of select="fits_XsltFunctions:getMessageString($messageText,$subMessage,$severity,$offset)"/>				
			</message>
		</xsl:for-each>
	</filestatus>
	
	</xsl:template>
</xsl:stylesheet>