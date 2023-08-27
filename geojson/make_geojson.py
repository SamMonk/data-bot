import sqlite3
import json
import sys
#input
all_properties = json.load(open('/home/shawnmonk/monk/qgis/volusia-addresses/parcel.geojson'))
shell = json.load(open('/home/shawnmonk/monk/data-bot/geojson/shell.geojson'))
# sqlite query get all records
# 
# select * from VCPA_CAMA_OWNER vco join VCPA_CAMA_PARCEL vcp on vco.PARID  = vcp.PARID where vcp.TAXDIST = '012'
conn = sqlite3.connect('/home/shawnmonk/monk/scripts/property-data/database.db')
cursor = conn.cursor()

# Execute a SELECT query
query = "select * from VCPA_CAMA_OWNER vco join VCPA_CAMA_PARCEL vcp on vco.PARID  = vcp.PARID where vcp.TAXDIST = '012' and vcp.LUC_DESC != 'Single Family'"
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    for v in all_properties['features']:
        # print(v['properties']['ALTKEY'])
        # break
        # print(v['properties']['ALTKEY'])
        # sys.exit()
        if(str(v['properties']['ALTKEY']) == row[0].split('.')[0]):
            #print('made it here')
            v['properties']['name'] = row[4]
            v['properties']['address'] = row[7]
            v['properties']['type'] = row[25]
            shell['features'].append(v)

# Close the connection
conn.close()


# for v in all_properties['features']:
#     # print(v['properties']['ALTKEY'])
#     # break
#     if(str(v['properties']['ALTKEY']) in parcel_ids):
#         shell['features'].append(v)

#output
results = open('/home/shawnmonk/monk/data-bot/geojson/default.geojson', 'w')
json.dump(shell, results)
