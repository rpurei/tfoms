<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
            <xsl:for-each select="ZL_LIST/ZGLV">
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
                        <span class="input-group-text">SD_Z</span>
                        <input type="text" name="ZGLV###SD_Z" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SD_Z" /></xsl:attribute></input>
                    </div>
                </div>
                </div>
            </xsl:for-each>
            <xsl:for-each select="ZL_LIST/SCHET">
                <div class="card" style="margin-top: 20px;">
                <div class="card-body">
                <h5 style="margin-bottom: 20px;">Секция SCHET</h5>
                    <div class="input-group mb-3">
                        <span class="input-group-text">CODE</span>
                        <input type="text" name="SCHET###CODE" class="form-control"><xsl:attribute name="value"><xsl:value-of select="CODE" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">CODE_MO</span>
                        <input type="text" name="SCHET###CODE_MO" class="form-control"><xsl:attribute name="value"><xsl:value-of select="CODE_MO" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">YEAR</span>
                        <input type="text" name="SCHET###YEAR" class="form-control"><xsl:attribute name="value"><xsl:value-of select="YEAR" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">MONTH</span>
                        <input type="text" name="SCHET###MONTH" class="form-control"><xsl:attribute name="value"><xsl:value-of select="MONTH" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">NSCHET</span>
                        <input type="text" name="SCHET###NSCHET" class="form-control"><xsl:attribute name="value"><xsl:value-of select="NSCHET" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">DSCHET</span>
                        <input type="text" name="SCHET###DSCHET" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DSCHET" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">PLAT</span>
                        <input type="text" name="SCHET###PLAT" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PLAT" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">SUMMAV</span>
                        <input type="text" name="SCHET###SUMMAV" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SUMMAV" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">COMENTS</span>
                        <input type="text" name="SCHET###COMENTS" class="form-control"><xsl:attribute name="value"><xsl:value-of select="COMENTS" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">SUMMAP</span>
                        <input type="text" name="SCHET###SUMMAP" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SUMMAP" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">SANK_MEK</span>
                        <input type="text" name="SCHET###SANK_MEK" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SANK_MEK" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">SANK_MEE</span>
                        <input type="text" name="SCHET###SANK_MEE" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SANK_MEE" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">SANK_EKMP</span>
                        <input type="text" name="SCHET###SANK_EKMP" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SANK_EKMP" /></xsl:attribute></input>
                    </div>
                </div>
                </div>
            </xsl:for-each>
            <xsl:for-each select="ZL_LIST/ZAP">
                <div class="card" style="margin-top: 20px;">
                <div class="card-body">
                <h5 style="margin-bottom: 20px;">Секция ZAP</h5>
                <xsl:variable name="idzap" select="N_ZAP" />
                    <div class="input-group mb-3">
                        <span class="input-group-text">N_ZAP</span>
                        <input type="text" name="ZAP%%%{$idzap}###N_ZAP" class="form-control"><xsl:attribute name="value"><xsl:value-of select="N_ZAP" /></xsl:attribute></input>
                    </div>
                    <div class="input-group mb-3">
                        <span class="input-group-text">PR_NOV</span>
                        <input type="text" name="ZAP%%%{$idzap}###PR_NOV" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PR_NOV" /></xsl:attribute></input>
                    </div>
                <xsl:for-each select="PACIENT">
                    <div class="card" style="margin-top: 20px;">
                    <div class="card-body">
                    <h5 style="margin-bottom: 20px;">Секция PACIENT</h5>
                        <div class="input-group mb-3">
                            <span class="input-group-text">ID_PAC</span>
                            <input type="text" name="PACIENT%%%{$idzap}###ID_PAC" class="form-control"><xsl:attribute name="value"><xsl:value-of select="ID_PAC" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">VPOLIS</span>
                            <input type="text" name="PACIENT%%%{$idzap}###VPOLIS" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VPOLIS" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">SPOLIS</span>
                            <input type="text" name="PACIENT%%%{$idzap}###SPOLIS" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SPOLIS" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">NPOLIS</span>
                            <input type="text" name="PACIENT%%%{$idzap}###NPOLIS" class="form-control"><xsl:attribute name="value"><xsl:value-of select="NPOLIS" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">ENP</span>
                            <input type="text" name="PACIENT%%%{$idzap}###ENP" class="form-control"><xsl:attribute name="value"><xsl:value-of select="ENP" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">ST_OKATO</span>
                            <input type="text" name="PACIENT%%%{$idzap}###ST_OKATO" class="form-control"><xsl:attribute name="value"><xsl:value-of select="ST_OKATO" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">SMO</span>
                            <input type="text" name="PACIENT%%%{$idzap}###SMO" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SMO" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">SMO_OGRN</span>
                            <input type="text" name="PACIENT%%%{$idzap}###SMO_OGRN" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SMO_OGRN" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">SMO_NAM</span>
                            <input type="text" name="PACIENT%%%{$idzap}###SMO_NAM" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SMO_NAM" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">INV</span>
                            <input type="text" name="PACIENT%%%{$idzap}###INV" class="form-control"><xsl:attribute name="value"><xsl:value-of select="INV" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">MSE</span>
                            <input type="text" name="PACIENT%%%{$idzap}###MSE" class="form-control"><xsl:attribute name="value"><xsl:value-of select="MSE" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">SMO_OK</span>
                            <input type="text" name="PACIENT%%%{$idzap}###SMO_OK" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SMO_OK" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">NOVOR</span>
                            <input type="text" name="PACIENT%%%{$idzap}###NOVOR" class="form-control"><xsl:attribute name="value"><xsl:value-of select="NOVOR" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">VNOV_D</span>
                            <input type="text" name="PACIENT%%%{$idzap}###VNOV_D" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VNOV_D" /></xsl:attribute></input>
                        </div>
                    </div>
                    </div>
                </xsl:for-each>
                <xsl:for-each select="Z_SL">
                    <div class="card" style="margin-top: 20px;">
                    <div class="card-body">
                    <h5 style="margin-bottom: 20px;">Секция Z_SL</h5>
                        <div class="input-group mb-3">
                            <span class="input-group-text">IDCASE</span>
                            <input type="text" name="Z_SL%%%{$idzap}###IDCASE" class="form-control"><xsl:attribute name="value"><xsl:value-of select="IDCASE" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">USL_OK</span>
                            <input type="text" name="Z_SL%%%{$idzap}###USL_OK" class="form-control"><xsl:attribute name="value"><xsl:value-of select="USL_OK" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">VIDPOM</span>
                            <input type="text" name="Z_SL%%%{$idzap}###VIDPOM" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VIDPOM" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">FOR_POM</span>
                            <input type="text" name="Z_SL%%%{$idzap}###FOR_POM" class="form-control"><xsl:attribute name="value"><xsl:value-of select="FOR_POM" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">NPR_MO</span>
                            <input type="text" name="Z_SL%%%{$idzap}###NPR_MO" class="form-control"><xsl:attribute name="value"><xsl:value-of select="NPR_MO" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">NPR_DATE</span>
                            <input type="text" name="Z_SL%%%{$idzap}###NPR_DATE" class="form-control"><xsl:attribute name="value"><xsl:value-of select="NPR_DATE" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">LPU</span>
                            <input type="text" name="Z_SL%%%{$idzap}###LPU" class="form-control"><xsl:attribute name="value"><xsl:value-of select="LPU" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">DATE_Z_1</span>
                            <input type="text" name="Z_SL%%%{$idzap}###DATE_Z_1" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DATE_Z_1" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">DATE_Z_2</span>
                            <input type="text" name="Z_SL%%%{$idzap}###DATE_Z_2" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DATE_Z_2" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">KD_Z</span>
                            <input type="text" name="Z_SL%%%{$idzap}###KD_Z" class="form-control"><xsl:attribute name="value"><xsl:value-of select="KD_Z" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">VNOV_M</span>
                            <input type="text" name="Z_SL%%%{$idzap}###VNOV_M" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VNOV_M" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">RSLT</span>
                            <input type="text" name="Z_SL%%%{$idzap}###RSLT" class="form-control"><xsl:attribute name="value"><xsl:value-of select="RSLT" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">ISHOD</span>
                            <input type="text" name="Z_SL%%%{$idzap}###ISHOD" class="form-control"><xsl:attribute name="value"><xsl:value-of select="ISHOD" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">OS_SLUCH</span>
                            <input type="text" name="Z_SL%%%{$idzap}###OS_SLUCH" class="form-control"><xsl:attribute name="value"><xsl:value-of select="OS_SLUCH" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">VB_P</span>
                            <input type="text" name="Z_SL%%%{$idzap}###VB_P" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VB_P" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">IDSP</span>
                            <input type="text" name="Z_SL%%%{$idzap}###IDSP" class="form-control"><xsl:attribute name="value"><xsl:value-of select="IDSP" /></xsl:attribute></input>
                        </div>
                        <div class="input-group mb-3">
                            <span class="input-group-text">SUMV</span>
                            <input type="text" name="Z_SL%%%{$idzap}###SUMV" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SUMV" /></xsl:attribute></input>
                        </div>
                    <xsl:for-each select="SL">
                        <div class="card" style="margin-top: 20px;">
                        <div class="card-body">
                        <h5 style="margin-bottom: 20px;">Секция SL</h5>
                            <div class="input-group mb-3">
                                <span class="input-group-text">SL_ID</span>
                                <input type="text" name="SL%%%{$idzap}###SL_ID" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SL_ID" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">LPU_1</span>
                                <input type="text" name="SL%%%{$idzap}###LPU_1" class="form-control"><xsl:attribute name="value"><xsl:value-of select="LPU_1" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">PODR</span>
                                <input type="text" name="SL%%%{$idzap}###PODR" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PODR" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">PROFIL</span>
                                <input type="text" name="SL%%%{$idzap}###PROFIL" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PROFIL" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">PROFIL_K</span>
                                <input type="text" name="SL%%%{$idzap}###PROFIL_K" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PROFIL_K" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">DET</span>
                                <input type="text" name="SL%%%{$idzap}###DET" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DET" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">P_CEL</span>
                                <input type="text" name="SL%%%{$idzap}###P_CEL" class="form-control"><xsl:attribute name="value"><xsl:value-of select="P_CEL" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">NHISTORY</span>
                                <input type="text" name="SL%%%{$idzap}###NHISTORY" class="form-control"><xsl:attribute name="value"><xsl:value-of select="NHISTORY" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">P_PER</span>
                                <input type="text" name="SL%%%{$idzap}###P_PER" class="form-control"><xsl:attribute name="value"><xsl:value-of select="P_PER" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">DATE_1</span>
                                <input type="text" name="SL%%%{$idzap}###DATE_1" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DATE_1" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">DATE_2</span>
                                <input type="text" name="SL%%%{$idzap}###DATE_2" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DATE_2" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">KD</span>
                                <input type="text" name="SL%%%{$idzap}###KD" class="form-control"><xsl:attribute name="value"><xsl:value-of select="KD" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">WEI</span>
                                <input type="text" name="SL%%%{$idzap}###WEI" class="form-control"><xsl:attribute name="value"><xsl:value-of select="WEI" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">DS0</span>
                                <input type="text" name="SL%%%{$idzap}###DS0" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DS0" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">DS1</span>
                                <input type="text" name="SL%%%{$idzap}###DS1" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DS1" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">DS2</span>
                                <input type="text" name="SL%%%{$idzap}###DS2" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DS2" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">DS3</span>
                                <input type="text" name="SL%%%{$idzap}###DS3" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DS3" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">C_ZAB</span>
                                <input type="text" name="SL%%%{$idzap}###C_ZAB" class="form-control"><xsl:attribute name="value"><xsl:value-of select="C_ZAB" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">DN</span>
                                <input type="text" name="SL%%%{$idzap}###DN" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DN" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">CODE_MES1</span>
                                <input type="text" name="SL%%%{$idzap}###CODE_MES1" class="form-control"><xsl:attribute name="value"><xsl:value-of select="CODE_MES1" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">CODE_MES2</span>
                                <input type="text" name="SL%%%{$idzap}###CODE_MES1" class="form-control"><xsl:attribute name="value"><xsl:value-of select="CODE_MES2" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">REAB</span>
                                <input type="text" name="SL%%%{$idzap}###REAB" class="form-control"><xsl:attribute name="value"><xsl:value-of select="REAB" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">PRVS</span>
                                <input type="text" name="SL%%%{$idzap}###PRVS" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PRVS" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">VERS_SPEC</span>
                                <input type="text" name="SL%%%{$idzap}###VERS_SPEC" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VERS_SPEC" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">IDDOKT</span>
                                <input type="text" name="SL%%%{$idzap}###IDDOKT" class="form-control"><xsl:attribute name="value"><xsl:value-of select="IDDOKT" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">ED_COL</span>
                                <input type="text" name="SL%%%{$idzap}###ED_COL" class="form-control"><xsl:attribute name="value"><xsl:value-of select="ED_COL" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">TARIF</span>
                                <input type="text" name="SL%%%{$idzap}###TARIF" class="form-control"><xsl:attribute name="value"><xsl:value-of select="TARIF" /></xsl:attribute></input>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text">SUM_M</span>
                                <input type="text" name="SL%%%{$idzap}###SUM_M" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SUM_M" /></xsl:attribute></input>
                            </div>
                        <xsl:for-each select="KSG_KPG">
                            <div class="card" style="margin-top: 20px;">
                            <div class="card-body">
                            <h5 style="margin-bottom: 20px;">Секция KSG_KPG</h5>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">N_KSG</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###N_KSG" class="form-control"><xsl:attribute name="value"><xsl:value-of select="N_KSG" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">VER_KSG</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###VER_KSG" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VER_KSG" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">KSG_PG</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###KSG_PG" class="form-control"><xsl:attribute name="value"><xsl:value-of select="KSG_PG" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">KOEF_Z</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###KOEF_Z" class="form-control"><xsl:attribute name="value"><xsl:value-of select="KOEF_Z" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">KOEF_UP</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###KOEF_UP" class="form-control"><xsl:attribute name="value"><xsl:value-of select="KOEF_UP" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">BZTSZ</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###BZTSZ" class="form-control"><xsl:attribute name="value"><xsl:value-of select="BZTSZ" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">KOEF_D</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###KOEF_D" class="form-control"><xsl:attribute name="value"><xsl:value-of select="KOEF_D" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">KOEF_U</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###KOEF_U" class="form-control"><xsl:attribute name="value"><xsl:value-of select="KOEF_U" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">CRIT</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###CRIT" class="form-control"><xsl:attribute name="value"><xsl:value-of select="CRIT" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">SL_K</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###SL_K" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SL_K" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">IT_SL</span>
                                    <input type="text" name="KSG_KPG%%%{$idzap}###IT_SL" class="form-control"><xsl:attribute name="value"><xsl:value-of select="IT_SL" /></xsl:attribute></input>
                                </div>
                            </div>
                            </div>
                        </xsl:for-each>
                        <xsl:for-each select="USL">
                            <div class="card" style="margin-top: 20px;">
                            <div class="card-body">
                            <h5 style="margin-bottom: 20px;">Секция USL</h5>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">IDSERV</span>
                                    <input type="text" name="USL%%%{$idzap}###IDSERV" class="form-control"><xsl:attribute name="value"><xsl:value-of select="IDSERV" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">LPU</span>
                                    <input type="text" name="USL%%%{$idzap}###LPU" class="form-control"><xsl:attribute name="value"><xsl:value-of select="LPU" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">LPU_1</span>
                                    <input type="text" name="USL%%%{$idzap}###LPU_1" class="form-control"><xsl:attribute name="value"><xsl:value-of select="LPU_1" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">PODR</span>
                                    <input type="text" name="USL%%%{$idzap}###PODR" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PODR" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">PROFIL</span>
                                    <input type="text" name="USL%%%{$idzap}###PROFIL" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PROFIL" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">VID_VME</span>
                                    <input type="text" name="USL%%%{$idzap}###VID_VME" class="form-control"><xsl:attribute name="value"><xsl:value-of select="VID_VME" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">DET</span>
                                    <input type="text" name="USL%%%{$idzap}###DET" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DET" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">DATE_IN</span>
                                    <input type="text" name="USL%%%{$idzap}###DATE_IN" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DATE_IN" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">DATE_OUT</span>
                                    <input type="text" name="USL%%%{$idzap}###DATE_OUT" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DATE_OUT" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">DS</span>
                                    <input type="text" name="USL%%%{$idzap}###DS" class="form-control"><xsl:attribute name="value"><xsl:value-of select="DS" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">CODE_USL</span>
                                    <input type="text" name="USL%%%{$idzap}###CODE_USL" class="form-control"><xsl:attribute name="value"><xsl:value-of select="CODE_USL" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">KOL_USL</span>
                                    <input type="text" name="USL%%%{$idzap}###KOL_USL" class="form-control"><xsl:attribute name="value"><xsl:value-of select="KOL_USL" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">TARIF</span>
                                    <input type="text" name="USL%%%{$idzap}###TARIF" class="form-control"><xsl:attribute name="value"><xsl:value-of select="TARIF" /></xsl:attribute></input>
                                </div>
                                <div class="input-group mb-3">
                                    <span class="input-group-text">SUMV_USL</span>
                                    <input type="text" name="USL%%%{$idzap}###SUMV_USL" class="form-control"><xsl:attribute name="value"><xsl:value-of select="SUMV_USL" /></xsl:attribute></input>
                                </div>
                                <xsl:for-each select="MR_USL_N">
                                    <div class="card" style="margin-top: 20px;">
                                    <div class="card-body">
                                    <h5 style="margin-bottom: 20px;">Секция MR_USL_N</h5>
                                        <div class="input-group mb-3">
                                            <span class="input-group-text">MR_N</span>
                                            <input type="text" name="MR_USL_N%%%{$idzap}###MR_N" class="form-control"><xsl:attribute name="value"><xsl:value-of select="MR_N" /></xsl:attribute></input>
                                        </div>
                                        <div class="input-group mb-3">
                                            <span class="input-group-text">PRVS</span>
                                            <input type="text" name="MR_USL_N%%%{$idzap}###PRVS" class="form-control"><xsl:attribute name="value"><xsl:value-of select="PRVS" /></xsl:attribute></input>
                                        </div>
                                        <div class="input-group mb-3">
                                            <span class="input-group-text">CODE_MD</span>
                                            <input type="text" name="MR_USL_N%%%{$idzap}###CODE_MD" class="form-control"><xsl:attribute name="value"><xsl:value-of select="CODE_MD" /></xsl:attribute></input>
                                        </div>
                                    </div>
                                    </div>
                                </xsl:for-each>
                            </div>
                            </div>
                        </xsl:for-each>
                        </div>
                        </div>
                    </xsl:for-each>
                    </div>
                    </div>
                </xsl:for-each>
                </div>
                </div>
            </xsl:for-each>
	</xsl:template>
</xsl:stylesheet>