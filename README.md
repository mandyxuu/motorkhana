# motorkhana
##Web Application Structure:
app.route(/) def base():
 --->base.html
app.route(/admin)--->admin.html
app.routr(/






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



    

