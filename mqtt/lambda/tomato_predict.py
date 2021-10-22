import connect
import pymysql
import datetime


rds_host = connect.host
name = connect.name
db = connect.db
password = connect.password

def lambda_handler(event, context):
    farm = str(event["farm_id"])
    key = str(event["key"])
    predict = str(event["predict"])
    time = str(event["measure_time"])
    key = connect.image_url + key
    db_connection = pymysql.connect(
        host=rds_host,
        user=name,
        port=3306,
        db=db,
        password=password
    )
    try:
        with db_connection.cursor() as cursor:
            check = "SELECT farm_id FROM screen WHERE measure_time='"+time+"' AND farm_id="+farm
            cursor.execute(check)
            result = cursor.fetchall()
            if len(result) == 0:
                insert = "VALUES("+farm+",'"+predict+"','"+key+"','"+time+"');"
                insert_sql = "INSERT INTO screen(farm_id,crop_condition,image_url,measure_time) "+ insert
                print(insert_sql)
                cursor.execute(insert_sql)
            else:
                update = "crop_condition="+predict+",image_url='"+key+"',measure_time='"+time+"'"
                update_sql = "UPDATE screen SET "+ update + "WHERE measure_time='"+time+"' AND farm_id="+farm
                print(update_sql)
                cursor.execute(update_sql)
        db_connection.commit()
    
    finally:
        db_connection.close()