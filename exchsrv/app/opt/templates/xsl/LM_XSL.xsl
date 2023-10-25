<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
            <xsl:for-each select="PERS_LIST/ZGLV">
                <div class="card" style="margin-top: 20px;">
                <div class="card-body">
                <h5 style="margin-bottom: 20px;">Секция ZGLV</h5>
                    <div class="input-group mb-3">
                        <span class="input-group-text">VERSION</span>
                        <input type="text" name="ZGLV###VERSION" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VERSION" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">DATA</span>
                        <input type="text" name="ZGLV###DATA" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DATA" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">FILENAME</span>
                        <input type="text" name="ZGLV###FILENAME" class="form-control"><xsl:attribute name="value"><xsl:value-of select="FILENAME" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">FILENAME1</span>
                        <input type="text" name="ZGLV###FILENAME1" class="form-control"><xsl:attribute name="value"><xsl:value-of select="FILENAME1" /></xsl:attribute></input>
                    </div>
                </div>
                </div>
            </xsl:for-each>
            <xsl:for-each select="PERS_LIST/PERS">
                <div class="card" style="margin-top: 20px;">
                <div class="card-body">
                <h5 style="margin-bottom: 20px;">Секция PERS</h5>
                    <div class="input-group mb-3">
                        <span class="input-group-text">ID_PAC</span>
                        <input type="text" name="PERS###ID_PAC" class="form-control"><xsl:attribute name="value"><xsl:value-of select="ID_PAC" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">FAM</span>
                        <input type="text" name="PERS###FAM" class="form-control"><xsl:attribute name="value"><xsl:value-of select="FAM" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">IM</span>
                        <input type="text" name="PERS###IM" class="form-control"><xsl:attribute name="value"><xsl:value-of select="IM" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">OT</span>
                        <input type="text" name="PERS###OT" class="form-control"><xsl:attribute name="value"><xsl:value-of select="OT" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">W</span>
                        <input type="text" name="PERS###W" class="form-control"><xsl:attribute name="value"><xsl:value-of select="W" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">DR</span>
                        <input type="text" name="PERS###DR" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DR" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">DOCTYPE</span>
                        <input type="text" name="PERS###DOCTYPE" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DOCTYPE" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">DOCSER</span>
                        <input type="text" name="PERS###DOCSER" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DOCSER" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">DOCNUM</span>
                        <input type="text" name="PERS###DOCNUM" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DOCNUM" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">DOCDATE</span>
                        <input type="text" name="PERS###DOCDATE" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DOCDATE" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">DOCORG</span>
                        <input type="text" name="PERS###DOCORG" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DOCORG" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">SNILS</span>
                        <input type="text" name="PERS###SNILS" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SNILS" /></xsl:attribute></input>
                    </div>
                </div>
                </div>
            </xsl:for-each>
	</xsl:template>
</xsl:stylesheet>