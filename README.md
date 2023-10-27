# motorkhana
COMP 636 Assessment: BRMM car club runs monthly Motorkhana competitive event. My task is to develop a website to record all driver's run details.

## Web Application Structure:
#### app.route(/)-def base() ---> base.html showing the home webpage, as the public link:
   - List Course: **app.route("/listcourses")--def listcourses():---> courselist.html**
     - Fetch all courses, and pass the course_ID and course name from the MySQL Motorkhana database to courselist.html.
     - Fetch all course images from the 'static/' folder and pass them to courselist.html.
   - List Driver: **app.route("/listdrivers")--def listdrivers():--->driverlist.html**
     - Fetch drivers' id, drivers' names, car models, car classes, and junior status. Pass this information to driverlist.html.
     - fetch, drivers' id, drivers'name,car model, car class,is junior pass to driverlist.html.
   - Driver Run Details: **app.route("/listdrivers/filter", methods = ['GET','POST'])--def listdriversfilter():--> dropdriverlist.html & driverlist.html**
      - For GET requests from driverlist.html, retrieve driver details and car details and pass them to dropdriverlist.html.
      - For POST requests from dropdriverlist.html, fetch driver details and car details and pass them to dropdriverlist.html.
   - Overall Results: **app.route("/overall")--def overall():-->overall.html**
     - Retrieve driver run details, such as seconds, cones, and wd, and pass them to overall.html.
   - Top 5 Drivers(bar chart): **app.route("/graph")--def showgraph():--->top5graph.html**
     - Retrieve the top 5 drivers and their results in order. Pass this information to top5graph.html.
#### app.route(/admin)- def admin() --->admin.html showing the admin page, which is not pubilc:
   - Junior Driver List: **app.route("/juniordrivers")--def junior_drivers():-->juniordriver.html**
     - Fetch junior driver details and pass them to juniordriver.html.
   - Driver Search: **app.route("/driversearch", methods=["GET","POST"])--def driversearch()-->driversearch.html**
     - For GET requests, perform a fuzzy match on driver names, retrieve full driver names, and pass them to driversearch.html.
     - Clicking on a driver name redirects to editruns.html.
   - Edit Runs: **app.route("/editruns", methods = ["GET","POST"])--def editruns()-->editruns.html**
     - For GET requests, fetch driver details and pass them to editruns.html.
     - For POST requests, update driver's run details in the MySQL Motorkhana database.
   - Add Drivers: **app.route("/adddriver",methods =['GET','POST'])--def adddrivers()-->adddrivers.html**
     - For GET requests, render the adddrivers.html page for inputting new driver information.
     - For POST requests, insert new driver info and generate 12 blank runs, then INSERT it into the Motorkhana database.
    





1. navigation page  9/10/2023 create url and url name in base.html
2. list of courses add the course images 10/10
insert the image path in courselist,            <td><img src="/static/{{ course.2}}" alt="" width='200' ></td>

3. list junior driver list 10/10
        create juniordriver html junior driver name,age, caregiver from database to webpage
        create new route use mysql to query the junior driver info. 
        from driver table join caregiver table.
                {% for driver in junior_driver %} 'junior_driver'juniorList in return clause
4. list of driver

            <tr {% if driver.2 == 1 %} class="table-warning"{% endif %}>
highlight the junior driver in the list,create the dervier name clickable
5. driver's run details
@app.route("/Rundetails", methods = ['GET']) connect to the list of driver app route.
in driverlist.html    <td><a href="Rundetails?driverName={{driver.1}}">{{driver.1}}</a></td>
so when click in the drivername tehen display the driver's run details.
6.overall reresults i think run_total,
the headers are driver_id,driver_name (J if exist),car model, sum of 6 courses time (cup/prize)
then show each driver's 6 course times.
create two sql query in one route, and marry to one html
show all the overall results in the same query

assumption: share driver list from junior list to driver list, then to run details then overall results.

reuse the driver list in public and admin webapge

in pubilc webpage: click to driver list, use driver drop down, to see the specific driver name, and run details and overall results buttons on the top.saving route?

when i created the pulldown of driver list, when i failed to selct a driver, every time would jump to <select a driver>

driver[0]|string == driver_id
in edit run, do I need insert to run table after editing??
dont need to, 



    

