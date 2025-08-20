<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="3.0">
   
        
        <xsl:import href="docbook/fo/docbook.xsl"/>
        
        <xsl:template name="insertBodyOddHeader">
            <fo:static-content flow-name="xsl-region-before">
                <fo:block text-align="end" font-size="8pt" font-family="sans-serif">
                    <xsl:value-of select="normalize-space(current-date())"/>
                    <xsl:text> | </xsl:text>
                    <fo:page-number/>
                </fo:block>
            </fo:static-content>
        </xsl:template>
        
        <xsl:template name="insertBodyEvenFooter">
            <fo:static-content flow-name="xsl-region-after">
                <fo:block text-align="start" font-size="8pt" font-family="sans-serif">
                    My Company Confidential
                </fo:block>
            </fo:static-content>
        </xsl:template>
        
        <xsl:template name="generate.chapter.title.in.header">
        </xsl:template>
        
    </xsl:stylesheet>
</xsl:stylesheet>