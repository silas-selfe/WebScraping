import urllib
import requests
from bs4 import BeautifulSoup

markup = '''<html><body><table class="dgrid-row-table" role="presentation"><tr><td class="dgrid-cell dgrid-cell-padding dgrid-column-selectionHandle field-selectionHandle selection-handle-column" role="gridcell"></td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field0 field-OBJECTID field0" role="gridcell">3</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field1 field-PIDN field1" role="gridcell">001-00-00-001.00</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field2 field-ADDRESS field2" role="gridcell">1096 RIVER RD</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field3 field-ACREAGE field3" role="gridcell">1.740</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field4 field-MAIL_ADD1 field4" role="gridcell">1096 RIVER RD</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field5 field-MAIL_CITY field5" role="gridcell">VILLA HILLS</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field6 field-MAIL_STATE field6" role="gridcell">KY</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field7 field-MAIL_ZIP field7" role="gridcell">41017-4429</td></tr></table></div></body></html>'''
soup = BeautifulSoup(markup, 'html.parser')

div = soup.find('div', id='dgrid_2-row-3')
print(div.string)




#<table class="dgrid-row-table" role="presentation"><tr><td class="dgrid-cell dgrid-cell-padding dgrid-column-selectionHandle field-selectionHandle selection-handle-column" role="gridcell"></td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field0 field-OBJECTID field0" role="gridcell">3</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field1 field-PIDN field1" role="gridcell">001-00-00-001.00</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field2 field-ADDRESS field2" role="gridcell">1096 RIVER RD</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field3 field-ACREAGE field3" role="gridcell">1.740</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field4 field-MAIL_ADD1 field4" role="gridcell">1096 RIVER RD</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field5 field-MAIL_CITY field5" role="gridcell">VILLA HILLS</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field6 field-MAIL_STATE field6" role="gridcell">KY</td><td class="dgrid-cell dgrid-cell-padding dgrid-column-field7 field-MAIL_ZIP field7" role="gridcell">41017-4429</td></tr></table>



url = "https://linkgis.org/mapviewer_development"
url_contents = urllib.request.urlopen(url).read()

soup = BeautifulSoup(url_contents, "html")
div = soup.find("div", {"class": "dgrid-content ui-widget-content"})

content = str(div)



div = soup.find(id="dgrid_2-row-3")
table = soup.find('div', attrs={"class": "dgrid-content ui-widget-content"})
spans
print(type[1].find('strong').strong)



content = url.read()




## didnt work -- got some of the data on excel though
