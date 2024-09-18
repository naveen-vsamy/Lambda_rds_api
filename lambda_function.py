import json
import boto3
from botocore.exceptions import ClientError
import mysql.connector

file = open("credentials.json")
credentials = json.load(file)
secret_name = credentials["secret_name"]
region_name = "ap-south-1"

def lambda_handler(event, context):
    
    mydb = mysql.connector.connect(
        host = credentials["db_host"],
        database = credentials['db_name'],
        user =secret["username"],
        password = secret['password']
        )
    cursor = mydb.cursor()

    directory = path(event)["context"]["resource-path"]
    data = path(event)["body-json"]

    def path(data):
        bucket = {}
        for i in data:
            bucket[i] = data[i]
        #info = bucket["context"]["resource-path"]
        #directory = bucket["body-json"]
        return(bucket)

    # Create a Secrets Manager client
    def secret(secret_name):
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            return (eval(get_secret_value_response['SecretString']))
        except ClientError as e:
            raise e
            return e
    
    secret = secret(secret_name)

    def register():
        name = data['name']
        phone = data['phone']
        sql = "INSERT INTO client_registry VALUES (last_insert_id(), %s, %s)"
        value = (name, phone)
        cursor.execute(sql,value)
        mydb.commit()
        return({"Message":"Registered"})

    def admin_pass():
        if credentials["admin_password"] == path(event)["body-json"]["admin_password"]:
            return True
        else:
            return False        

    def admin_job():
        if admin_pass() == False:
            return {"Error" : "Invalid password"}
        else:
            if "fetch" in data and data["fetch"] == "all":
                    sql = "SELECT * FROM client_registry"
                    cursor.execute(sql)
                    results =cursor.fetchall()
                    message = []
                    for x in results:
                        message.append(x)
                    return ({"message" : message})
                        
            elif "name" in data:
                name = data["name"]
                sql = "SELECT * FROM client_registry WHERE `name` = "+"'" + str(name)+ "'"
                cursor.execute(sql)
                results =cursor.fetchall()
                message = []
                for x in results:
                    message.append(x)
                    
                return({"message" : message})
            
            elif "phone" in data:
                phone = data["phone"]
                sql = "SELECT * FROM client_registry WHERE `phone` = "+"'" + str(phone)+ "'"
                cursor.execute(sql)
                results =cursor.fetchall()
                message = []
                for x in results:
                    message.append(x)
                return ({"message" : message})
                
            elif "reg_no" in data:
                phone = data["reg_no"]
                sql = "SELECT * FROM client_registry WHERE `reg_no` = "+"'" + str(phone)+ "'"
                cursor.execute(sql)
                results =cursor.fetchall()
                for x in results:
                    message = x
                return ({"message" : message})
            
            else:
                return({"Error": "Invalid data"})

    if directory == "/register":
        return register()
    elif directory == "/admin":
        return admin_job()
    
                

        
