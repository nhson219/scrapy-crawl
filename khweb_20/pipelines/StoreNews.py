# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import mysql.connector
from mysql.connector import errorcode

logger = logging.getLogger(__name__)


class StoreNewsPipeline(object):
    table = 'news'

    conf = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'khweb_20',
        'raise_on_warnings': True
    }

    def __init__(self, **kwargs):
        self.cnx = self.mysql_connect()

    def open_spider(self, spider):
        print("spider open")

    def process_item(self, item, spider):
        print("Saving item into db ...")
        self.save(dict(item))
        return item

    def mysql_connect(self):
        try:
            return mysql.connector.connect(**self.conf)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def save(self, row):
        cursor = self.cnx.cursor()
        create_query = ("INSERT INTO " + self.table +
                        "(title, description, url_img, identify_sign, content) "
                        "VALUES (%(title)s, %(description)s, %(url_img)s, %(identify_sign)s, %(content)s)")

        # Insert new row
        cursor.execute(create_query, row)
        lastRecordId = cursor.lastrowid

        # Make sure data is committed to the database
        self.cnx.commit()
        cursor.close()
        print("Item saved with ID: {}" . format(lastRecordId))

    def mysql_close(self):
        self.cnx.close()

    def close_spider(self, spider):
        print("Closing spider")
        self.mysql_close()
