<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:template match="/">

    <fits xmlns="http://hul.harvard.edu/ois/xml/ns/fits/fits_output"
    	  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://hul.harvard.edu/ois/xml/ns/fits/fits_output xml/fits_output.xsd">
		<identification>
			<identity>
				<xsl:attribute name="format">
					<xsl:value-of select="string('OpenDocument Text')"/>
				</xsl:attribute>
				<xsl:attribute name="mimetype">
					<xsl:value-of select="string('application/vnd.oasis.opendocument.text')"/>
				</xsl:attribute>
			</identity>		
		</identification>
		
 		<fileinfo>
			<created>
				<xsl:value-of select="//CREATION-DATE/DATE"/>
			</created>

			<creatingApplicationName>
				<xsl:value-of select="//GENERATOR"/>
			</creatingApplicationName>
						
		</fileinfo>
		
		<metadata>	
		<document>
		
			<pages>
				<xsl:value-of select="//PAGE-COUNT"/>
			</pages>

			<wordCount>
				<xsl:value-of select="//WORD-COUNT"/>
			</wordCount>
			
			<characterCount>
				<xsl:value-of select="//CHARACTER-COUNT"/>
			</characterCount>	
			
			<tableCount>
				<xsl:value-of select="//TABLE-COUNT"/>
			</tableCount>	
			
			<imageCount>
				<xsl:value-of select="//IMAGE-COUNT"/>
			</imageCount>	
										
			<title>
				<xsl:value-of select="//TITLE"/>
			</title>
			
			<author>
				<xsl:value-of select="//INITIAL-CREATOR"/>
			</author>			
			
			<language>
				<xsl:value-of select="//LANGUAGE"/>
			</language>		

		</document>	
		</metadata>
	</fits>	

</xsl:template>


</xsl:stylesheet>