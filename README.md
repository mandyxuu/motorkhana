# Competitive Motorkhana event
COMP 636 Assessment: BRMM car club runs monthly Motorkhana competitive event. A small website developed to record and update drivers and driver's run details.

## Web Application Structure:
#### app.route(/)-def base() ---> base.html showing the home webpage, as the public link:

   - List of Courses: **app.route("/listcourses")--def listcourses():---> courselist.html**
     
     - Fetch all courses, and pass the course_ID and course name from the MySQL Motorkhana database to courselist.html.
     - Fetch all course images from the 'static' folder and pass them to courselist.html.
       
   - List of Drivers: **app.route("/listdrivers")--def listdrivers():--->driverlist.html**
     
     - Fetch drivers' id, drivers' names, car models, car classes, and junior status. Pass this information to driverlist.html.
  
   - Driver's Run Details: **app.route("/listdrivers/filter", methods = ['GET','POST'])--def listdriversfilter():<--> dropdriverlist.html & driverlist.html**
     
      - For GET requests from driverlist.html, retrieve driver details and car details and pass them to dropdriverlist.html.
      - For POST requests from dropdriverlist.html, fetch driver details and car details and pass them to dropdriverlist.html.
   
   - Overall Results: **app.route("/overall")--def overall():-->overall.html**
     
     - Retrieve driver run details, such as seconds, cones, and wd, and pass them to overall.html.
   - Top 5 Drivers(bar chart): **app.route("/graph")--def showgraph():--->top5graph.html**
     
     - Retrieve the top 5 drivers and their results in order. Pass this information to top5graph.html.
#### app.route(/admin)- def admin() --->admin.html showing the admin page, which is not pubilc:

   - Junior Driver List: **app.route("/juniordrivers")--def junior_drivers():-->juniordriver.html**
     
     - Fetch junior driver details and pass them to juniordriver.html.
   - Driver Search: **app.route("/driversearch", methods=["GET","POST"])--def driversearch()<-->driversearch.html**

     - For GET requests, perform a fuzzy match on driver names, retrieve full driver names, and pass them to driversearch.html.
     - Clicking on a driver name redirects to editruns.html.
   - Edit Runs: **app.route("/editruns", methods = ["GET","POST"])--def editruns()<-->editruns.html**

     - For GET requests, fetch driver details and pass them to editruns.html.
     - For POST requests, update driver's run details in the MySQL Motorkhana database.
   - Add Drivers: **app.route("/adddriver",methods =['GET','POST'])--def adddrivers()<-->adddrivers.html**

     - For GET requests, render the adddrivers.html page for inputting new driver information.
     - For POST requests, insert new driver info and generate 12 blank runs into the Motorkhana database.
    
## Assumptions and Design Decisions:

#### Assumptions

In the application project, made the assumption that only consider individuals aged 12 or above, so individuals under the age of 12 is outside of the project scope.

All completed runs have no accidents, such as car crashes or running out of petrol. All the drivers' run times are valid.

Each course permits a maximum of two run attempts, and no third attempt is allowed.

A driver's name may include numbers or special characters, and it's not limited to just 26 letters.

Driver's name is not mononym.

Anyone who is not junior can be a caregiver.

Valid run times must fall within the range of 20 to 500.



#### Design Decisions

##### Navigation section

In the navigation section, ensure that 'Rakaia Motorkhana Mavens - Competition Event' serves as the title, making it clear to users the purpose of the webpage. Provide 'Home' and 'Admin' buttons for easy navigation.

This web application employs a flat hierarchy broad layout. Users can easily access information without navigating through multiple levels, making it a user-friendly experience.  It's designed for efficiently displaying course lists, driver lists, driver's run details, overall results, and top 5 drivers. Additionally, administrators have the ability to add and manage data. This ensures a seamless and intuitive experience for administrators, ideal options to add drivers, search for drivers, and edit runs. 

##### List of Driver & Driver's Run Details

Leveraged the shared 'Driver's Run Details' functionality for both the 'List of Drivers' and 'Driver's Run Details' views by utilizing the same app.route('/listdrivers/filter'). In this design, gathered arguments from the 'List of Drivers' page (listdriver.html) using GET requests and employed form data from the 'Driver's Run Details' page (dropdriverlist.html) through POST requests and form submissions. Additionally, the driver pulldown on the 'Driver's Run Details' page is linked to app.route('/listdrivers/filter'), while driver details on the 'List of Drivers' page are accessed via app.route("/listdrivers"). This decision promotes code reuse, enhances readability, and maintains a coherent webpage structure.

GET requests are ideal for safe and idempotent operations, primarily data retrieval, without causing side effects on the server. Fetching the list of drivers is a read-only operation that doesn't modify the server's state.

GET requests can be cached, improving performance by reducing the need to repeatedly fetch the same data, which is valuable for a frequently accessed list of drivers.

POST requests are commonly used for operations that involve submitting data or actions that may have side effects on the server. When a user selects a driver and submits the form, it triggers an action to fetch the run details for that specific driver.POST requests are well-suited for sending data to the server. It's necessary to submit the selected driver's ID to retrieve specific driver information. POST requests keep sensitive data within the request body, enhancing security by preventing data exposure in URLs.

##### editrun route

The route supports both HTTP Method GET and POST. GET fetches driver and course details for the page, while POST handles form submissions for updating run details. It retrieves data from the database, checks for matching driver's ID, course ID, and run attempt in the database. If a match is found and the run was not completed (seconds is null), administrators can update run details, including run time, cones, and WD. Data validation, including checking the range of run times (20-500) and cones(0-25), and errors due to invalid data are handled using if-else and try-except constructs. If there's no match for the driver's ID, course ID, and run number, or if the run is already completed, a message warns against duplicate entries, ensuring administrators input correct data.

The same method is applied to the adddriver route, with some distinctions. Only junior driver's date of birth and age are visible. To enforce this, age selection for other drivers is disabled by setting the minimum year (1998) and maximum year (2011). Additionally, for drivers aged falls outside the range of 12 to 16, inputting the caregiver ID is blocked. This ensures that caregiver information is entered only when necessary, further streamlining the data entry process. 

To enhance clarity and streamline data management, I've chosen to combine the car model and drive type for the MX-5, which comes in both Rear-Wheel Drive (RWD) and Front-Wheel Drive (FWD) variants. This decision is intended to provide a clearer and more informative identifier for each variant within the web application.

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

       ON driver.car = car.car_num
      
**Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?**

      INSERT INTO car VALUES
      (11,'Mini','FWD'),
      (17,'GR Yaris','4WD'),

**Suppose the club wanted to set a default value of ‘RWD’ for the drive_class field. What specific change would you need to make to the SQL to do this? (Do not implement this change in your app.)**

         ALTER TABLE car 
         ALTER drive_class SET DEFAULT 'RWD';
                        
**Suppose logins were implemented. Why is it important for drivers and the club admin to access different routes? As part of your answer, give two specific examples of problems that could occur if all of the web app facilities were available to everyone.**

Implementing separate routes and access controls for drivers and the club admin is crucial for maintaining the security, privacy, and functionality of web application. 


**Scenario 1**

If all facilities were accessible to everyone, there would be a risk of exposing sensitive data to unauthorized users. Driver Jack might be able to view or alter Tina's personal information (e.g.birthdate, age, caregiver name), he could use the confidential information to do soemthing not legal. This could lead to privacy violations and potentially misuse of personal data.

**Scenario 2**

Allowing unrestricted access to web app facilities could lead to unauthorized actions and potential misuse. Mandy who is outside of the club might be able to modify or delete Tina's records, leading to data corruption or disputes.

By segregating access based on user roles (in this case, drivers and club admin), the web app ensures that each user can only perform actions relevant to their role, enhancing security and preventing unauthorized access and data breaches.

## Image Sources:

Thanks to Sharon for designing all those awesome course images, and a shoutout to Richard and our other amazing tutors. 
