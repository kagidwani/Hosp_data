import pandas as pd
import folium
import branca


## import all the data files
df = pd.read_csv('/Projects/4DG/APRDRG_HOSP_latlong_ethnicity.csv')
# hosp_ID = pd.read_csv('/Users/kgidwani/Documents/Purdue/Current/BIOL_597/Projects/4DG/HOSPITAL_ID_2019.csv')
# df_hosptlatlong = pd.read_csv('/Users/kgidwani/Documents/Purdue/Current/BIOL_597/Projects/4DG/HospLatlong.csv')


# drop all the columns with data we do not need
df.drop(columns=["PAYOR1", "SEVERITY", "PATS", "PWC", "TD", "TC", "XC", "XD", "Hosptial_name_city"], index = 1, inplace=True)

# manipulating the data frames to get what we want
ordered_diag = df.groupby(["HOSPITAL_ID", "APRDRG_DESCRIPTION", "Hospital_Name", "Lat", "Long", "Percentage, People Who Are White Alone", 
                            "Percentage, Black Or African American Alone", "Percentage, People Who Are American Indian And Alaska Native Alone", 
                            "Percentage, People Who Are Asian Alone", "Percentage, People Who Are Native Hawaiian And Other Pacific Islander Alone", 
                            "Percentage, People Who Are Some Other Race Alone"])["APRDRG"].count().to_frame(name='count').reset_index()
ordered_diag2 = ordered_diag.sort_values(["HOSPITAL_ID", "count"], ascending = (True, False))
topfive_diag2 = ordered_diag2.groupby('HOSPITAL_ID').head(5)
topfive_diag2.to_csv("top5_diag2.csv", index=False, encoding='utf-8-sig')


concat_ordered_diag2 = pd.read_csv('/Projects/4DG/top5_diag2.csv')
concat_ordered_diag2['Combo'] = concat_ordered_diag2.agg('{0[APRDRG_DESCRIPTION]} : {0[count]}'.format, axis=1)
concat_ordered_diag2.drop(columns=["APRDRG_DESCRIPTION", "count"], index = 1, inplace=True)
array_agg = lambda x: ' , '.join(x.astype(str))
concated_ordered_diag2 = concat_ordered_diag2.groupby(['HOSPITAL_ID', 'Hospital_Name', 'Lat', 'Long', "Percentage, People Who Are White Alone", 
                            "Percentage, Black Or African American Alone", "Percentage, People Who Are American Indian And Alaska Native Alone", 
                            "Percentage, People Who Are Asian Alone", "Percentage, People Who Are Native Hawaiian And Other Pacific Islander Alone", 
                            "Percentage, People Who Are Some Other Race Alone"], as_index=False).agg({'Combo': array_agg})


## now lets create an HTML table that we can input into the Folium Popup
def data_html(row):
    i = row
    Percent_white = concated_ordered_diag2['Percentage, People Who Are White Alone'].iloc[i]
    Percent_black = concated_ordered_diag2['Percentage, Black Or African American Alone'].iloc[i]
    Percent_AIAN = concated_ordered_diag2['Percentage, People Who Are American Indian And Alaska Native Alone'].iloc[i]
    Percent_asian = concated_ordered_diag2['Percentage, People Who Are Asian Alone'].iloc[i]
    Percent_nhpi = concated_ordered_diag2['Percentage, People Who Are Native Hawaiian And Other Pacific Islander Alone'].iloc[i]
    Percent_other = concated_ordered_diag2['Percentage, People Who Are Some Other Race Alone'].iloc[i]
    name = concated_ordered_diag2.iloc[i]['Hospital_Name']
    top5aprdrg = concated_ordered_diag2.iloc[i]['Combo']

    left_col_colour = "#2A799C"
    right_col_colour = "#C5DCE7"

    html = """<!DOCTYPE html>
<html>

<head>
<h4 style="margin-bottom:0"; width="300px">{}</h4>""".format(name) + """

</head>
    <table style="height: 126px; width: 300px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Top 5 most common APRDRG Descriptors</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(top5aprdrg) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Percentage, People Who Are White Alone</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Percent_white) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Percentage, Black Or African American Alone</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Percent_black) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Percentage, People Who Are American Indian And Alaska Native Alone</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Percent_AIAN) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Percentage, People Who Are Asian Alone</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Percent_asian) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Percentage, People Who Are Native Hawaiian And Other Pacific Islander Alone</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Percent_nhpi) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Percentage, People Who Are Some Other Race Alone</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Percent_other) + """
</tr>
</tbody>
</table>
</html>
"""
    return html



map_indiana = folium.Map(location=[39.790341,-86.163356])
map_indiana

for i in range(0, len(concated_ordered_diag2)):
    html = data_html(i)
    popup_table = branca.element.IFrame(html=html, width=400, height=300)
    popup = folium.Popup(popup_table, parse_html=True)
    folium.Marker(
        location=[concated_ordered_diag2.iloc[i]['Lat'], 
        concated_ordered_diag2.iloc[i]['Long']],
        popup=popup,
        tooltip = concated_ordered_diag2.iloc[i]['Hospital_Name']
    ).add_to(map_indiana)

map_indiana.save(HealthTrendsIN.html)