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
    
## Assumptions and Design Decisions:
#### Assumptions

   Driver's Run Details Page:

At the beginning, display the "Driver's Run Details" page with a default view that doesn't show specific driver details yet.
Dropdown Selection:

Include a dropdown (e.g., <select>) on the "Driver's Run Details" page where users can select a driver.
Form Submission:

Enclose the dropdown within an HTML form.
When the user selects a driver from the dropdown and submits the form, use the POST method to send the selected driver's ID to the server.
Server-Side Handling (Flask):

In your Flask application, define a route that handles the POST request when the form is submitted.
Retrieve the selected driver's ID from the form data.
Query your data source (e.g., a database) to fetch the specific driver's run details.
Render the "Driver's Run Details" page again, but this time with the updated content based on the selected driver's information.
List of Drivers Page:

Provide a link or button on the "Driver's Run Details" page that users can click to navigate to the "List of Drivers" page. You can achieve this by simply including a hyperlink (<a> element) that points to the "List of Drivers" page.
This approach uses form submission and server-side processing to update the content on the same page without the need for JavaScript. It's a valid approach, and you can implement it using Flask and HTML to achieve your desired functionality.








#### Design Decisions
   GET Request for List of Drivers:

You use a GET request to retrieve the list of drivers. This makes sense because it's a straightforward retrieval of data, and it aligns with the common practice of using GET for read operations. This is typically used to populate the initial list of drivers on a page.
POST Request for Driver's Run Details:

You use a POST request to obtain detailed run information for a specific driver. This is suitable for actions that involve submitting form data, processing specific user requests, and displaying individual driver details.
By distinguishing between GET and POST requests in this way, you're following established web application conventions, which can lead to a more organized and user-friendly user experience. GET requests are used for displaying lists and basic data retrieval, while POST requests are used for more interactive and specific operations, such as displaying a driver's run details based on user selection. Your approach aligns well with typical web application design practices.






## Database questions:
**What SQL statement creates the car table and defines its three fields/columns? (Copy and paste the relevant lines of SQL.)**

       DROP TABLE IF EXISTS car;
       CREATE TABLE IF NOT EXISTS car
       (
       car_num INT PRIMARY KEY NOT NULL,
       model VARCHAR(20) NOT NULL,
       drive_class VARCHAR(3) NOT NULL
      );

**Which line of SQL code sets up the relationship between the car and driver tables?**

      FROM driver
        JOIN car on driver.car = car.car_num
      
**Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?**

      INSERT INTO car VALUES
      (11,'Mini','FWD'),
      (17,'GR Yaris','4WD'),

**Suppose the club wanted to set a default value of ‘RWD’ for the driver_class field. What specific change would you need to make to the SQL to do this? (Do not implement this change in your app.)**
   - If car table has been created:

         ALTER TABLE car ALTER drive_class SET DEFAULT 'RWD';
   
   - If need to create a car table:

            CREATE TABLE car (
             car_num int NOT NULL,
             car varchar(255) NOT NULL,
             drive_class varchar(255) DEFAULT 'RWD'
         );


                        
**Suppose logins were implemented. Why is it important for drivers and the club admin to access different routes? As part of your answer, give two specific examples of problems that could occur if all of the web app facilities were available to everyone.**

   
Implementing separate routes and access controls for drivers and the club admin is crucial for maintaining the security, privacy, and functionality of your web application. Here are two specific examples of problems that could occur if all web app facilities were available to everyone:

Data Privacy and Security: Without access controls, all users could potentially access and modify each other's data. For example:

Drivers might be able to view or alter the personal information (e.g., birthdates) of other drivers. This could lead to privacy violations and potentially misuse of personal data.
Drivers could tamper with their run results or the results of other drivers, compromising the integrity of the data and the fairness of competitions.
System Integrity and Misuse: Allowing unrestricted access to system administration functions can lead to:

Unauthorized modifications of the database schema: Users could potentially alter the structure of the database, leading to data corruption or making the system dysfunctional.
Abuse of administrative features: Users who aren't authorized as administrators might misuse features meant for system management. For example, they could add, modify, or delete drivers or runs without proper authorization.
In summary, implementing separate routes and access controls for drivers and administrators is essential to ensure data privacy, maintain system integrity, and prevent unauthorized access or misuse of the web application's features. It helps protect sensitive data, maintain data accuracy, and provide a secure and efficient user experience for both drivers and administrators.

## Image Sources:

Thanks to Sharon for designing all those awesome course images, and a shoutout to our amazing tutors. 




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



    

