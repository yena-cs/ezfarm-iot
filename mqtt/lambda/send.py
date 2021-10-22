import connect
import pymysql


rds_host = connect.host
name = connect.name
db = connect.db
password = connect.password

def lambda_handler(event, context):
    farm_id = str(event["farm_id"])
    tmp = str(event["tmp"])
    co2 = str(event["co2"])
    humidity = str(event["humidity"])
    illuminance = str(event["illuminance"])
    mos = str(event["mos"])
    ph = str(event["ph"])
    measure_date = str(event["measure_date"])
    
    db_connection = pymysql.connect(
        host=rds_host,
        user=name,
        port=3306,
        db=db,
        password=password
    )
    try:
        with db_connection.cursor() as cursor:
            value = "VALUES("+farm_id+","+tmp+","+co2+","+humidity+","+illuminance+","+mos+","+ph+",'"+measure_date+"');"
            sql = "INSERT INTO facility(farm_id,tmp,co2,humidity,illuminance,mos,ph,measure_date)"+value
            print(sql)
            cursor.execute(sql)
        db_connection.commit()
    
    finally:
        db_connection.close()