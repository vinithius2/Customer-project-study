#### Description:
In this project is possible to get a customers list or only a customer, with the name city your 
customers live is made an insertion of the latitude and longitude in database with Google API.

#### Get start
* First:
    * Download this project
    * Install PIP (https://pip.pypa.io/en/stable/installing/)
    * Create a virtualenv 
    (https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments)
* Second:
    * Activate your virtualenv
    * In your project path, install libs with commands:
        * **Command:** pip install -r requirements/dev.txt
        * **Note:** In production use just file common.txt, the dev.txt have library 
        model-bakery for test 
    * Ok, your project is ready!
* Third:
    * Create your database:
        * **Command:** python manage.py migrate
        * Populate your database with a csv file:
            * **Command:** python manage.py addcustomers <path_file>
            * Exemple csv file with structure acceptable bellow:
            
|id		       |first_name	    |last_name		    |email			                |gender		   |company	      |city			            |title			        |
|------------- |------------- 	|------------- 		|------------- 	                |------------- |------------- |------------- 	        |------------- 	        |
|1	           |Laura	        |Richards	        |lrichards0@reverbnation.com	|Female		   |Meezzy		  |Warner, NH		        |Biostatistician III	|
|2	           |Margaret        |Mendoza	        |mmendoza1@sina.com.cn		    |Female		   |Skipfire	  |East Natchitoches, PA	|VP Marketing		    |
|3	           |Craig	        |Mccoy		        |cmccoy2@bluehost.com		    |Male		   |Quatz		  |Lyon, WV		            |Senior Sales Associate	|

      
   * Wait insertion with csv file ...
   * Run this project your computer
        * **Command:** python manage.py runserver
* Fourth:
    * **Access:** http://localhost:8000/swagger/
    * Enjoy yourself...
    
**Extra points:**
* Automated Testing:
    * python manage.py test
       

