#-*- coding: utf-8 -*-
#!/usr/bin/python
import urllib
import json
import datetime
import MySQLdb

#api kye : 667a516e716a696e39354773566678
url = 'http://openAPI.seoul.go.kr:8088/667a516e716a696e39354773566678/json/ListSnowRemoveBox/1/1/'
u = urllib.urlopen(url)
data = u.read()

j = json.loads(data)
roopNum = j["ListSnowRemoveBox"]["list_total_count"]
#print j

# Open database connection
db = MySQLdb.connect("ec2-52-79-164-115.ap-northeast-2.compute.amazonaws.com","dev","dev1234","SNOWRMTOOL", charset='utf8')

# prepare a cursor object using cursor() method
cursor = db.cursor()

table = 'SRMBOX_TB'
for i in range((roopNum / 1000) + 1):
    if i == (roopNum / 1000):
        url = 'http://openAPI.seoul.go.kr:8088/667a516e716a696e39354773566678/json/ListSnowRemoveBox/%d/%d/' %(i*1000 +1, (i+1)*1000)
        u = urllib.urlopen(url)
        data = u.read()
        j = json.loads(data)

        for idx in range(roopNum - (roopNum / 1000)*1000):
            G2_ID = int(j["ListSnowRemoveBox"]["row"][idx]["G2_ID"])
            SBOX_NUM = j["ListSnowRemoveBox"]["row"][idx]["SBOX_NUM"]
            MGC_NM = j["ListSnowRemoveBox"]["row"][idx]["MGC_NM"]
            DETL_CN = j["ListSnowRemoveBox"]["row"][idx]["DETL_CN"]
            G2_XMIN = float(j["ListSnowRemoveBox"]["row"][idx]["G2_XMIN"])
            G2_YMIN = float(j["ListSnowRemoveBox"]["row"][idx]["G2_YMIN"])
            G2_XMAX = float(j["ListSnowRemoveBox"]["row"][idx]["G2_XMAX"])
            G2_YMAX = float(j["ListSnowRemoveBox"]["row"][idx]["G2_YMAX"])

            query = "INSERT INTO %s (G2_ID, SBOX_NUM, MGC_NM, DETL_CN, G2_XMIN, G2_YMIN, G2_XMAX, G2_YMAX) values (\'%d\', \'%s\', \'%s\', \'%s\', \'%.1f\', \'%.1f\', \'%.1f\', \'%.1f\')" % (table, G2_ID, SBOX_NUM, MGC_NM, DETL_CN, G2_XMIN, G2_YMIN, G2_XMAX, G2_YMAX)
            #print query
            #print "\n"
            cursor.execute(query)
        break
    url = 'http://openAPI.seoul.go.kr:8088/667a516e716a696e39354773566678/json/ListSnowRemoveBox/%d/%d/' %(i*1000 +1, (i+1)*1000)
    u = urllib.urlopen(url)
    data = u.read()
    j = json.loads(data)

    for idx in range(1000):
        G2_ID = int(j["ListSnowRemoveBox"]["row"][idx]["G2_ID"])
        SBOX_NUM = j["ListSnowRemoveBox"]["row"][idx]["SBOX_NUM"]
        MGC_NM = j["ListSnowRemoveBox"]["row"][idx]["MGC_NM"]
        DETL_CN = j["ListSnowRemoveBox"]["row"][idx]["DETL_CN"]
        G2_XMIN = float(j["ListSnowRemoveBox"]["row"][idx]["G2_XMIN"])
        G2_YMIN = float(j["ListSnowRemoveBox"]["row"][idx]["G2_YMIN"])
        G2_XMAX = float(j["ListSnowRemoveBox"]["row"][idx]["G2_XMAX"])
        G2_YMAX = float(j["ListSnowRemoveBox"]["row"][idx]["G2_YMAX"])

        query = "INSERT INTO %s (G2_ID, SBOX_NUM, MGC_NM, DETL_CN, G2_XMIN, G2_YMIN, G2_XMAX, G2_YMAX) values (\'%d\', \'%s\', \'%s\', \'%s\', \'%.1f\', \'%.1f\', \'%.1f\', \'%.1f\')" % (table, G2_ID, SBOX_NUM, MGC_NM, DETL_CN, G2_XMIN, G2_YMIN, G2_XMAX, G2_YMAX)
        #print query
        #print "\n"
        cursor.execute(query)
    #print i*1000






# execute SQL query using execute() method.

###
db.commit()
# disconnect from server
db.close()
