import requests
import mysql.connector
from mysql.connector import errorcode
import json

try:
    cnx = mysql.connector.connect(
        user='root', password='', host='127.0.0.1', database='khweb_20')

    add_player = ("INSERT INTO `statistics`"
                  "(`name`, `club`, `national`, `position`, `age`, `matches`, `starts`, `mins`, `goals`, `assists`, `passes_attempted`,"
                  " `perc_passes_completed`, `penalty_goals`, `penalty_attempted`, `yellow_cards`, `red_cards`, `rating`) "
                  " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    # cursor.execute(add_employee, data_employee)

    response = requests.get(
        "https://www.footballcritic.com/json/competition-player-stats.php?uid=41756")

    for item in response.json():
        for item2 in item:
            cursor = cnx.cursor()
            data_player = (item2["2"], item2["5"], item2["3"], item2["13"], item2["0"],
                           item2["25"], item2["20"], item2["17"], item2["20"], item2["21"], 0, 0, 0, 0, item2["18"], item2["19"], int(item2["1"]) if (item2["1"]) else 0)
            cursor.execute(add_player, data_player)
            cnx.commit()
            cursor.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username and password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("DB does not exist")
    else:
        print(err)
else:
    cnx.close()
