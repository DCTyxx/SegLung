import pymysql



cnx = pymysql.connect(
    user="Shimmer",
    password="88888888",
    host="covid-19.mysql.database.azure.com",
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)
