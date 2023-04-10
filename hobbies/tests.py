#from RK import Lit
from unittest.result import failfast
from selenium import webdriver 
from django.core import management   
from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
import time
from .models import * 
from datetime import datetime
from dateutil import parser
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

TEST_USERNAME = "robert"
TEST_PASSWORD = "superhardpassword"


## All tests are self contained so thats why you will see repeating code !!!


# January 2nd
NEW_DOB = "02/01/2022"
NEW_HOBBY = "Sleep"
 

class UserCreationTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chrome = webdriver.Chrome(
            ChromeDriverManager().install())
        cls.chrome.implicitly_wait(10)
        print("Test main account stuff--")

    @classmethod
    def tearDownClass(cls):
        cls.chrome.quit()
        super().tearDownClass()

    def setUp(self):
        # flush - new database
        #  verbosity - explanation
        # interactive - no need to do confirmation 
        management.call_command('flush', verbosity=0, interactive=False)
    
        #self._load_test_data()
    # Test methods
    def test03_success_signup(self):
        '''
        Here we will be entering new details if it success it will stay in go to members page 
        '''
        # Go to Signup  page
        #Live server url means current one
        self.chrome.get(self.live_server_url+"/signup/")
        ussernameField = self.chrome.find_element_by_name("username")
        passwordField = self.chrome.find_element_by_name("password")
        passwordFieldConfirm = self.chrome.find_element_by_name("password_confirm")
        ussernameField.send_keys(TEST_USERNAME)
        passwordField.send_keys(TEST_PASSWORD)
        passwordFieldConfirm.send_keys(TEST_PASSWORD)

        signupButton = self.chrome.find_element_by_css_selector("input[type='submit']")
        signupButton.click()
        # HERE if account created it will stay in the same page
        self.is_url(self.live_server_url + "/members/")


    def test04_failed_signup(self):
        '''
        Here if you enter already existant username it will still stay in signup page 
        '''
        # Go to Signup  page
        #Live server url means current one
        time.sleep(1) 
        self.chrome.get(self.live_server_url+"/signup/")
        ussernameField = self.chrome.find_element_by_name("username")
        passwordField = self.chrome.find_element_by_name("password")
        passwordFieldConfirm = self.chrome.find_element_by_name("password_confirm")
        ## using same information 
        ussernameField.send_keys(TEST_USERNAME)
        passwordField.send_keys(TEST_PASSWORD)
        passwordFieldConfirm.send_keys(TEST_PASSWORD)

        signupButton = self.chrome.find_element_by_css_selector("input[type='submit']")
        signupButton.click()
         
        self.is_url(self.live_server_url + "/members/")
        logout = self.chrome.find_element_by_name("logout")
        logout.click()

        self.chrome.get(self.live_server_url+"/signup/")
        ussernameField = self.chrome.find_element_by_name("username")
        passwordField = self.chrome.find_element_by_name("password")
        passwordFieldConfirm = self.chrome.find_element_by_name("password_confirm")
        ## using same information 
        ussernameField.send_keys(TEST_USERNAME)
        passwordField.send_keys(TEST_PASSWORD)
        passwordFieldConfirm.send_keys(TEST_PASSWORD)

        signupButton = self.chrome.find_element_by_css_selector("input[type='submit']")
        signupButton.click()    
        # HERE if account created it will stay in the same page
        self.is_url(self.live_server_url + "/signup/")
    def test02_good_login(self):
        '''
        Here we will be entering good credentials it should redirect to members, but first we are creating new user 
        '''
         
        # Go to Signup  page
        self.chrome.get(self.live_server_url+"/signup/")
        ussernameField = self.chrome.find_element_by_name("username")
        passwordField = self.chrome.find_element_by_name("password")
        passwordFieldConfirm = self.chrome.find_element_by_name("password_confirm")
        ussernameField.send_keys(TEST_USERNAME)
        passwordField.send_keys(TEST_PASSWORD)
        passwordFieldConfirm.send_keys(TEST_PASSWORD)

        signupButton = self.chrome.find_element_by_css_selector("input[type='submit']")
        signupButton.click()

        self.is_url(self.live_server_url + "/members/")
        logout = self.chrome.find_element_by_name("logout")
        logout.click()


        self.chrome.get(self.live_server_url+"/login/")
        # Input username and password
       
        user_field = self.chrome.find_element_by_name("username")
        password_field = self.chrome.find_element_by_name("password")
        user_field.send_keys(TEST_USERNAME)
        password_field.send_keys(TEST_PASSWORD)
        login_button = self.chrome.find_element_by_css_selector(   "input[type='submit']")
        login_button.click()
        self.is_url(self.live_server_url +   "/members/")    
    
     
    def test01_fail_login(self):
        '''
        Here we will be entering wrong credentials if it fails it will still stay in login page 
        '''
        self.chrome.get(self.live_server_url+"/login/")
        # Input username and password
       
        user_field = self.chrome.find_element_by_name("username")
        password_field = self.chrome.find_element_by_name("password")
        user_field.send_keys("randomUser")
        password_field.send_keys("randonpassword")
        login_button = self.chrome.find_element_by_css_selector(   "input[type='submit']")
        login_button.click()
       
        self.is_url(self.live_server_url +   "/login/")

    def test05_change_dob(self):
        '''
        Changing dob but first we are creating new user as every time database is flushed
        '''
        self.chrome.get(self.live_server_url+"/signup/")
        ussernameField = self.chrome.find_element_by_name("username")
        passwordField = self.chrome.find_element_by_name("password")
        passwordFieldConfirm = self.chrome.find_element_by_name("password_confirm")
        ussernameField.send_keys(TEST_USERNAME)
        passwordField.send_keys(TEST_PASSWORD)
        passwordFieldConfirm.send_keys(TEST_PASSWORD)

        signupButton = self.chrome.find_element_by_css_selector("input[type='submit']")
        signupButton.click()

        self.is_url(self.live_server_url + "/members/")
        profileButton = self.chrome.find_element_by_name("profile")
        profileButton.click()
        dobLocation = self.chrome.find_element_by_name("dob")
        dobLocation.send_keys(NEW_DOB)
        saveChanges = self.chrome.find_element_by_name("saveChanges")
        saveChanges.click()

        self.chrome.refresh()
        dobLocation = self.chrome.find_element_by_name("dob")

        # converting and then comparing
        dob11 = parser.parse(NEW_DOB)
        dob22 = parser.parse(dobLocation.get_attribute("value"))
        dob111 = dob11.strftime("%d/%m/%Y")
        dob222 = dob22.strftime("%d/%m/%Y")

 
        self.assertEqual(dob111,dob222)
        
    def test06_add_hobby(self):
        '''
        changing city, also first we  are creating new user as every time database is flushed
        '''
        self.chrome.get(self.live_server_url+"/signup/")
        ussernameField = self.chrome.find_element_by_name("username")
        passwordField = self.chrome.find_element_by_name("password")
        passwordFieldConfirm = self.chrome.find_element_by_name("password_confirm")
        ussernameField.send_keys(TEST_USERNAME)
        passwordField.send_keys(TEST_PASSWORD)
        passwordFieldConfirm.send_keys(TEST_PASSWORD)

        signupButton = self.chrome.find_element_by_css_selector("input[type='submit']")
        signupButton.click()

        self.is_url(self.live_server_url + "/members/")
        profileButton = self.chrome.find_element_by_name("profile")
        profileButton.click()
        hobbyLocation = self.chrome.find_element_by_id("newHobby")
        hobbyLocation.send_keys(NEW_HOBBY)
        newHobby = self.chrome.find_element_by_name("newHobbyButton")
        newHobby.click()
        
        self.chrome.refresh()
        # here getting all info from dropdown  
        allHobbies = self.chrome.find_element_by_id("hobbies")
        #checking if it actually changed
       
        hobbiesList = allHobbies.text.split("\n")

        # error message in case if test case got failed
        message = "First value and second value are not unequal !"
        # assertNotEqual() to check equality of first & second value 
        # finding that hobby
        # removing first element because it is "select a hobby"
        for i in hobbiesList[1:]: 
            temp = i.strip()
            self.assertEqual(temp, NEW_HOBBY, message)
    
    def test07_remove_hobby(self):
        '''
        changing city, also first we  are creating new user as every time database is flushed
        '''
    
        self.chrome.get(self.live_server_url+"/signup/")
        ussernameField = self.chrome.find_element_by_name("username")
        passwordField = self.chrome.find_element_by_name("password")
        passwordFieldConfirm = self.chrome.find_element_by_name("password_confirm")
        ussernameField.send_keys(TEST_USERNAME)
        passwordField.send_keys(TEST_PASSWORD)
        passwordFieldConfirm.send_keys(TEST_PASSWORD)

        signupButton = self.chrome.find_element_by_css_selector("input[type='submit']")
        signupButton.click()

        self.is_url(self.live_server_url + "/members/")
        profileButton = self.chrome.find_element_by_name("profile")
        profileButton.click()
        hobbyLocation = self.chrome.find_element_by_id("newHobby")
        hobbyLocation.send_keys(NEW_HOBBY)
        newHobby = self.chrome.find_element_by_name("newHobbyButton")
        newHobby.click()
        
        self.chrome.refresh()
        # here getting all info from dropdown  
        allHobbies = self.chrome.find_element_by_id("hobbies")
        #checking if it actually changed
       
        hobbiesList = allHobbies.text.split("\n")

        # error message in case if test case got failed
        message = "First value and second value are not unequal !"
        # assertNotEqual() to check equality of first & second value 
        # finding that hobby
        # removing first element because it is "select a hobby"
        for i in hobbiesList[1:]: 
            temp = i.strip()
            self.assertEqual(temp, NEW_HOBBY, message)

        allHobbies = self.chrome.find_element_by_id("hobbies")
    
        allHobbies.send_keys(NEW_HOBBY)

        # populating as you can't have empty ones
        tempEmail = self.chrome.find_element_by_id("email")
        tempLocation = self.chrome.find_element_by_id("city")
        tempEmail.send_keys("robert@robert.lt")
        tempLocation.send_keys("Vilnius")
        tempDob = self.chrome.find_element_by_name("dob")
        tempDob.send_keys(NEW_DOB)
        saveChanges = self.chrome.find_element_by_name("saveChanges")
        saveChanges.click()
        ## here we will be removing 
        hobby = self.chrome.find_element_by_name(NEW_HOBBY)
        hobby.click()       
           
        
        
    def is_url(self, match_url):
        current_url = self.chrome.current_url
        self.assertEqual(current_url, match_url)

    def _load_test_data(self):
        '''
        Loading one user as pre-load
        '''

        TEST_USERNAME1 = "robert"
        TEST_PASSWORD1 = "test_passwordR"

        test_user = User.objects.create(
            id=1,
            username=TEST_USERNAME1,
            password=TEST_PASSWORD1,
        )

        test_profile = Profile.objects.create(
            user=test_user,
            email="email@email.com",
        )
