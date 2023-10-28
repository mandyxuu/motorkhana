from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def base():
    return render_template("base.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/listcourses")
def listcourses():
    connection = getCursor()
    connection.execute("SELECT * FROM course;")
    courseList = connection.fetchall()
    return render_template("courselist.html", course_list = courseList) #course_list is from courselist.html

@app.route("/listdrivers")
def listdrivers():
    connection = getCursor()
    sql = """ SELECT driver.driver_id
            , CONCAT(driver.first_name,' ',driver.surname) AS driverName
            , car.model
            , car.drive_class
            , IF (driver.age <= 25,1,0) AS isJunior
            FROM driver
            JOIN car ON driver.car = car.car_num
            LEFT JOIN driver AS caregiver ON driver.caregiver= caregiver.driver_id
            ORDER BY driver.surname, driver.first_name
            ;"""
    # if clause marks junior driver who are 12-25 in the html.
    connection.execute(sql)
    driverList = connection.fetchall()
    print(driverList)
   
    return render_template("driverlist.html", driver_list = driverList)

@app.route("/listdrivers/filter", methods = ['GET','POST'])
def listdriversfilter():
    driver_id = request.form.get('driver') #post the driver_id from pulldown
    driverID = request.args.get('driverid') #get the driverid from driverlist
    connection = getCursor()
    sql1 = """SELECT driver.driver_id
        , CONCAT(driver.first_name,' ',driver.surname) AS driver_name
        , car.model
        , car.drive_class
        , course.name AS course_name
        , run.run_num 
        , run.seconds
        , IFNULL(run.cones,"") AS cones
        , IF(run.wd =1, "WD","") AS wd
        , IFNULL(ROUND((run.seconds + IFNULL(run.cones,0) *5 + run.wd * 10),2),'dnf')AS run_total
            FROM driver
            JOIN car ON driver.car = car.car_num
            LEFT JOIN run ON run.dr_id = driver.driver_id
            JOIN course ON course.course_id = run.crs_id
            """
    # note: don't not add';' here, consider below where clause.
    if request.method =='POST':
        sql2 = "WHERE driver.driver_id= %s"
        parameters = (driver_id,)
    elif request.method == "GET":
        sql2 = "WHERE driver.driver_id= %s"
        parameters = (driverID,)
    else:
        sql2 = ""
        parameters = ()
    sql3 = "order by driver.driver_id ;"
    sql= sql1 + " " +sql2+" " + sql3
    connection.execute(sql,parameters)
    runDetails = connection.fetchall()
    print(runDetails)

    connection = getCursor()
    sql = """ SELECT driver.driver_id
            , concat(driver.first_name,' ',driver.surname) AS driverName
            FROM driver
            LEFT JOIN driver as caregiver on driver.caregiver= caregiver.driver_id
        ;"""  
    connection.execute(sql)
    dropList = connection.fetchall()
    print(dropList)
    print(runDetails)
    return render_template("dropdriverlist.html", drop_list = dropList,run_details = runDetails,driver_id=driver_id,driverid = driverID)  
  
@app.route("/overall")
def overall():
    connection = getCursor()
    sql = """SELECT
            driver.driver_id,
            IF(driver.age IS NOT NULL, CONCAT(driver.first_name, ' ', driver.surname, ' (J)'), CONCAT(driver.surname, ' ', driver.first_name)) AS driver_name,
            MAX(car.model) AS model,
            CAST(MIN(CASE WHEN course.course_id = 'A' THEN course_time ELSE NULL END )AS DECIMAL(6,2)) AS courseA,
            CAST(MIN(CASE WHEN course.course_id = 'B' THEN course_time ELSE NULL END )AS DECIMAL(6,2)) AS courseB,
            CAST(MIN(CASE WHEN course.course_id = 'C' THEN course_time ELSE NULL END )AS DECIMAL(6,2)) AS courseC,
            CAST(MIN(CASE WHEN course.course_id = 'D' THEN course_time ELSE NULL END )AS DECIMAL(6,2)) AS courseD,
            CAST(MIN(CASE WHEN course.course_id = 'E' THEN course_time ELSE NULL END )AS DECIMAL(6,2)) AS courseE,
            CAST(MIN(CASE WHEN course.course_id = 'F' THEN course_time ELSE NULL END )AS DECIMAL(6,2)) AS courseF,
            IF(COUNT(driver_id) = 6, CAST(SUM(course_time) AS DECIMAL(6 ,2)), 'NQ') AS overall_result,
            
            CASE WHEN RANK() OVER (ORDER BY (IF(COUNT(driver_id) = 6,SUM(course_time),9999) )) = 1 
                    THEN 'cup'
                WHEN RANK() OVER (ORDER BY  (
                        IF(COUNT(driver_id) = 6,SUM(course_time),9999) )) BETWEEN 2 AND 5 THEN 'prize'
                ELSE ''
            END AS Award
        FROM driver
        JOIN car ON driver.car = car.car_num
        LEFT JOIN (
                SELECT dr_id, crs_id,
                CASE
                    WHEN MIN(run_total) IS NOT NULL THEN MIN(run_total)
                    WHEN MIN(run_total) IS NULL AND MAX(run_total) IS NOT NULL THEN MAX(run_total)
                    ELSE 'dnf'
                END AS course_time
                FROM (
                    SELECT dr_id, crs_id, seconds + IFNULL(cones, 0) * 5 + wd * 10 AS run_total
                    FROM run
                        ) AS run_total
                GROUP BY dr_id, crs_id
                ) AS results ON results.dr_id = driver.driver_id
        JOIN course ON course.course_id = results.crs_id
        WHERE course_time <> 'dnf'
        GROUP BY driver.driver_id, driver_name;"""
    # calcuate overall results in mysql, the query is complex, used couples window subqueries, only because the data volumn is small, if for huge volumn, can expolore more efficient way.
    # calcuate the driver's runtotal, then group by select the best course time of driver and mark who did not finish course
    # join driver>-car>-course>-subquery with best course time,mark junior driver, calcualte the overall reults, use'9999'to mark who did not finish, order by overall results.
    # rank() order by to call top 5 drivers and award 'cup' and 'prize',note,in this assess,top5 results are different, if top1 and top2 the same, who can get the'cup'? 
    # cast run time to decimal point 2
    connection.execute(sql)
    OverList = connection.fetchall()
    return render_template("overall.html", over_all = OverList)

@app.route("/graph")
def showgraph():
    connection = getCursor()
    sql = """SELECT driver.driver_id
        ,IF(driver.age IS NOT NULL,concat(driver.first_name,' ',driver.surname,'(J)')
        ,concat(driver.surname,' ',driver.first_name)) AS driver_name
       , if( count(driver_id) = 6, cast(sum(overresults) as decimal(6,2)),'NQ') AS overall
        FROM driver
        JOIN car on driver.car = car.car_num
        LEFT JOIN (select dr_id,
				        crs_id,
				        CASE WHEN MIN(run_total) is not null then min(run_total)
					        WHEN min(run_total) is null and max(run_total) is not null then max(run_total)
					        ELSE 'dnf'
					        END AS overresults
                    FROM (
                            SELECT dr_id,
                            crs_id,
                            seconds + ifnull(cones,0) *5 + wd*10 as run_total 
                            FROM run) as run_total
                            GROUP BY dr_id,crs_id
                        ) as reults
        ON reults.dr_id = driver.driver_id
        JOIN course ON course.course_id = reults.crs_id
        WHERE overresults <> 'dnf'
        GROUP BY driver.driver_id
                ,driver_name
        ORDER BY overall
        LIMIT 5;"""
    # similar to /overall route, but use liimit 5 to display top 5 results in the bar chart.
    connection.execute(sql)
    top5data = connection.fetchall()
    bestDriverList = [f"{driver[0]} {driver[1]}" for driver in top5data]
    # get top 5 drivers--> Names should include their ID and a trailing space, eg '133 Oliver Ngatai '

    resultsList = [driver[2] for driver in top5data]
    # resultsList containing the final result values

    return render_template("top5graph.html", name_list = bestDriverList, value_list = resultsList)

@app.route("/juniordrivers")
def junior_drivers():
    connection = getCursor()
    sql = """SELECT driver.driver_id,driver.surname, driver.first_name,driver.age,CONCAT(caregiver.first_name ,' ' , caregiver.surname) AS Caregiver
            FROM driver
            JOIN car on driver.car = car.car_num
            LEFT JOIN driver as caregiver on driver.caregiver= caregiver.driver_id
            WHERE driver.age between 12 and 25
            ORDER BY driver.age desc, driver.surname;"""
    # get junior driver in mysql
    connection.execute(sql)
    juniorList = connection.fetchall()
    print(juniorList)
    return render_template("juniordriver.html", junior_driver = juniorList)    

@app.route("/driversearch", methods=["GET","POST"])
def driversearch():
    driverName = request.form.get('driver')
    connection = getCursor()
    sql=""" SELECT driver.driver_id
            , concat(driver.first_name,' ',driver.surname) AS driverName
            FROM driver
            where concat(driver.surname,' ',driver.first_name) like %s
            ;"""
    parameters = (f'%{driverName}%',)
    # partial search for drivername in webpage ('like' is fuzzy match in mysql)
    connection.execute(sql,parameters)
    driverList = connection.fetchall()
    return render_template("driversearch.html", driver_list= driverList,driver_name = driverName)

@app.route("/editruns", methods = ["GET","POST"])
def editruns():
    connection = getCursor()
    sql = "SELECT * FROM run;"
    connection.execute(sql)
    runData = connection.fetchall()
    
    if request.method == "POST":
        driver_id = request.form.get("driver_id")
        course_id =request.form.get("course_id")
        run_num = request.form.get("run_num")
        print(driver_id,course_id,run_num)
        
        for run in runData:
            # if course missing
            if course_id == "<Select a course>":
                return "Please input a valid course."
            if run[0]== int(driver_id)and run[1]== course_id and run[2]== int(run_num):
                # if driver_id, course_id, and run_num match, then if seconds is null, then driver did not finish, admin can update the run details.
                if run[3] == None:
                    run_time = request.form.get("run_time")
                    cones = request.form.get("cones")
                  #  cones = 0  if cones == "" else cones
                    wd = request.form.get("wd")
                    wd = int(wd) if wd == '1' else 0
                    print(cones)
                    print(wd)
                    # incase the webpage crashed
                    try:
                        run_time = float(run_time)
                        if not(20<=run_time<=500): # assume 20 -500 is the valid runtime
                            return ("Invaild 'run time' value, please input between 20 and 500.")
                        if cones =="":
                            cones = None
                        elif cones is not None:
                            cones = int(cones)
                            if not(0 <= cones<= 25):
                                return ("Invaild 'cones' number, please input between 0 and 25.")
                            
                        cur = getCursor()
                        cur.execute("UPDATE run SET seconds = %s, cones = %s, wd = %s WHERE dr_id=%s AND crs_id = %s AND run_num=%s;",(run_time, cones,wd ,driver_id,course_id,run_num))
                        return "Add Driver run detail successfully"
                    except ValueError :
                        return ("Invaild data please input valid run time or cones.")
                    # existing rundetails are not allowed to updated.
        else:
            run_time = request.form.get("run_time",run[2])
            cones= request.form.get("cones",run[3])
            wd = request.form.get("wd",run[4])
            return( "Duplicate entries are not permitted. Please return to the run details and verify the information entered.")
  
    connection = getCursor()
    sql=""" SELECT driver.driver_id
            , concat(driver.first_name,' ',driver.surname) AS driverName
            FROM driver
            ;"""
    connection.execute(sql)
    driverList = connection.fetchall()

    connection = getCursor()
    sql = """SELECT *  FROM course ;"""
    connection.execute(sql)
    courseList = connection.fetchall()  
    
 
    return render_template("editruns.html",driver_list = driverList,course_list = courseList)

@app.route("/adddriver",methods =['GET','POST'])
def adddrivers():
    today = datetime.now()

    if request.method=="POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        car = request.form.get("car")
        date_of_birth = request.form.get("date_of_birth")
        caregiver_id = request.form.get("caregiver_id")
        birthdate = None
        age = None
        caregiver_id = None

        try:          
            if date_of_birth:
                # if date_of_birth is not none,
                birthdate = datetime.strptime(date_of_birth,"%Y-%m-%d")
                #format date of birth
                age = today.year - int(birthdate.year) - ((today.month, today.day)<(int(birthdate.month),int(birthdate.day)))
                #calcaute the driver age: consider junior or not, caregiver need or not.
                if 12<= age <=25:
                    age = age
                    birthdate= birthdate
                    if 12<= age<=16: #must have a caregiver
                        caregiver_id = request.form.get("caregiver_id")
                        if not caregiver_id:
                            return "Junior drivers aged 16 or younger must have a designed caregiver"      
                        #if not a junior don't need input the date of birth and caregiver input.              
                    else:
                        # 
                        return "Anyone under 16 needs a caregiver."
            else:
                birthdate = None
                age= None
                caregiver_id = None
        except ValueError:
            return "Invalid date of birth or wrong date format,please follow 'yyyy-mm-dd'"

        connection = getCursor()
        sql = """INSERT INTO  driver(first_name,surname,date_of_birth,age,caregiver,car)\
                VALUES(%s,%s,%s,%s,%s,%s);"""
        connection.execute (sql,(first_name,last_name,birthdate,age,caregiver_id,car))

       #get the auto-generated driver_id.
        driver_id = connection.lastrowid
        print(driver_id)
        
        connection = getCursor()
        sql = """SELECT *
            FROM course;"""
        connection.execute(sql)
        courseList = connection.fetchall()
        # insert 12 blanks run for each new added driver. for -->for loop 
        for course in courseList:
            for run_num in [1,2]:
                sql = """INSERT INTO run (dr_id,crs_id,run_num,seconds,cones,wd) \
                        VALUES(%s,%s,%s,null,null,0);"""
                connection.execute(sql,(driver_id,course[0],run_num))
        return "Driver added successfully."

    connection = getCursor()
    sql = """SELECT *
            FROM car;"""
    connection.execute(sql)
    carList = connection.fetchall()

    connection = getCursor()
    sql=""" SELECT driver.driver_id
            , concat(driver.first_name,' ',driver.surname) AS driverName
            FROM driver
            WHERE driver.age is null
            ;"""
    #get the caregiver list, only junior driver has an age
    connection.execute(sql)
    caregiverList = connection.fetchall()

    return render_template("adddrivers.html",caregiver_list = caregiverList,car_list = carList,today = today)
