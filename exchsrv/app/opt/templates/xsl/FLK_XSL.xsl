<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
                <p><xsl:value-of select="FLK_P/FNAME"/></p>
                <p><xsl:value-of select="FLK_P/FNAME_I"/></p>
				<table class="table table-bordered">
                    <thead class="thead">
					<tr>
						<th>OSHIB</th>
						<th>IM_POL</th>
						<th>ZN_POL</th>
						<th>NSCHET</th>
						<th>BAS_EL</th>
						<th>N_ZAP</th>
						<th>ID_PAC</th>
						<th>IDCASE</th>
						<th>SL_ID</th>
						<th>COMMENT</th>
					</tr>
                    </thead>
                    <tbody>
					<xsl:for-each select="FLK_P/PR">
						<tr>
							<td>
								<xsl:value-of select="OSHIB"/>
							</td>
							<td>
								<xsl:value-of select="IM_POL"/>
							</td>
							<td>
								<xsl:value-of select="ZN_POL"/>
							</td>
							<td>
								<xsl:value-of select="NSCHET"/>
							</td>
							<td>
								<xsl:value-of select="BAS_EL"/>
							</td>
							<td>
								<xsl:value-of select="N_ZAP"/>
							</td>
							<td>
								<xsl:value-of select="ID_PAC"/>
							</td>
							<td>
								<xsl:value-of select="IDCASE"/>
							</td>
							<td>
								<xsl:value-of select="SL_ID"/>
							</td>
							<td>
								<xsl:value-of select="COMMENT"/>
							</td>
						</tr>
					</xsl:for-each>
                    </tbody>
				</table>
	</xsl:template>
</xsl:stylesheet>