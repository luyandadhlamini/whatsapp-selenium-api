#!/usr/bin/env python
# coding: utf-8

# * The navigate module allows you to interact with Whatsapp.

# In[1]:


# !pip install selenium
# !pip install chromedriver


# ### Import the necessary packages

# In[1]:


# os used to upload files
#import os 
import subprocess
import sys
import pandas as pd
import datetime
import pathlib

# For interacting with the browser
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# For delaying execution
import time
import log
import database as db

# Create a Global logger variable. Use it to log what happens as functions in this module are run.
# Because the logger is global, it need not be passed as a argument into functions in the module.

log_class = log.Log()
config = log_class.load_yaml() 
logger = log_class.create_logger(config=config)

# create a database connection
conn = db.create_db_connection(params=db.params)


# In[ ]:





# In[2]:


class Navigate(object):
    # The navigate class is used to navigate around the whatsapp web client.
    # Its functionas are accompanied by dictionaries that contain the class names that the functions use to navigate.
    # This is done so that the function just executes & dictionaries are used as devices to store info about the website.
    
    def driver_initiate(self, URL="https://web.whatsapp.com/"):
        """
        Function lanches the browser window to be controlled.

        Args:
            URL - a string object, the website url to open.

        Returns:
                driver - a WebDriver object, used to interact with the website.
        E.g: 
            driver = driver_initiate(URL="https://web.whatsapp.com/")
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        ##########################################################################################################
        # Make sure that you have chromedriver.exe file in the folder where this code is stored.
        # If not using Chrome (e.g Firefox), change webdriver.Chrome() to webdriver.Firefox()
        ##########################################################################################################
        driver = webdriver.Chrome()

        driver.refresh()
        driver.maximize_window()
        driver.get(URL)

        message = "{},Driver initiated for {}".format(function_name, URL)
        logger.info(message)

        return driver
    
    def check_element_exists(self, selenium_object, class_name):
        """
        Function checks if an element exists.

        Args:
            selenium_object - a WebElement, the element to check for existance of the class name passed in as argument.
            class_name - a string, the element will be checked if it contains a class that is names as class_name.

        Returns:
            state - Boolean variable, saying whether the element was found or not.
        E.g:
            result = check_element_exists(selenium_object=driver, class_name='3V-PN')
        LastMod:
            Luyanda Dhlamini   
        """
        try:
            element=selenium_object.find_element_by_class_name(class_name)
            state = True
        except NoSuchElementException:
            state = False
        return state

    def current_time_string(self):
        """
        Function returns the current time formatted as a string. This string can be used as a filename.
        E.g. You can use this string to save screenshots.

        Returns:
            string - a string object, the current date-time
        
        E.g:
            time_now = current_time_string()
        LastMod:
            Luyanda Dhlamini   
        """
        function_name = sys._getframe().f_code.co_name
        time_now = time.localtime()

        year = time_now.tm_year
        month = time_now.tm_mon
        day = time_now.tm_mday
        hour = time_now.tm_hour
        minute = time_now.tm_min
        seconds = time_now.tm_sec

        string = "{}-{}-{} {}-{}-{}".format(day, month, year, hour, minute, seconds)
        message = "{},Created current time string:'{}'".format(function_name, string)
        logger.info(message)

        return string

    landing_dict ={ "description": """Used in check_if_whatsapp_locked(). contains classes for when Whatsapp is locked or 
        not.""",
        "locked_class" : "_1pw2F", # locked class is the container for the qr code box.
        "unlocked_class" : "_3Jvyf", #  unlocked class looks for the profile menu box (top left corner).
        "qr_code_class" : "_1pw2F" # qr_code_class class is the container for the qr code box.
        }
    
    def implicit_wait(self, selenium_object, timeout, class_name):
        """
        Function implements an explicit wait for a given class object.
        It is useful for cases where you want your program to wait x number of seconds before trying to find any element.
        It is controlled using driver & a timeout.

        Args:
            self = a Navigate Class object, used to control the functions in the Navigate class.
            selenium_object - a Selenium WebElement object, contents searched for class_name given as input.
            timeout - the number of seconds to wait for
            class_name -  the name of the class to search for.

        Returns:
            returned_object - string or WebElement.
                If it is a WebElement, the web element will indicate that the class object (image, text or button) has been found.
                If it is a string, it will indicate that a class object has not been found.
        E.g:
            object - implicit_wait(selenium_object = driver, timeout = 1, class_name = "3V-PN")
        LastMod:
            Luyanda Dhlamini   
        """
        function_name = sys._getframe().f_code.co_name
        try:
            returned_object = WebDriverWait(driver = selenium_object,
                timeout=timeout).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        except NoSuchElementException:
                returned_object = "Element Not Found. Please ensure that dictionary obejcts have not changed."
        except TimeoutException:
                returned_object = "Class object not found."
        
        message = "{},Used implicit wait for class name: {}.".format(function_name, class_name)
        logger.info(message)
        return returned_object

    def implicit_wait_is_displayed(self, selenium_object, wait_type = "displayed", timeout=3, countdown=0.1):
        """
        Function implements an explicit wait for a class object to be displayed.
        It is useful for cases where you want your program to wait x number of seconds before trying to move on to next execution.
        It is controlled using a timeout.

        Args:
            selenium_object - a Selenium WebElement object, the object to check if displayed.
            wait_type - a string object, difines whether using implicit wait for is "displayed" or in "not_displayed".
            timeout - the number of seconds to wait for.
            countdown - a float object, number of seconds to incrementaly decrease the timeout by.

        Returns:
            message - a string object, says whether the selenium_object is displayed or not.
                If it is a string, it will indicate that a class object has not been found.
        E.g:
            is_displayed = nav.implicit_wait_is_displayed(selenium_object=button1, timeout=3, countdown=0.25)
        LastMod:
            Luyanda Dhlamini   
        """
        function_name = sys._getframe().f_code.co_name
        if wait_type == 'not_displayed':
            flag = False
        elif wait_type == 'displayed':
            flag = True
        else:
            flag = False

        delay_secs = timeout        
        try:
            while (selenium_object.is_displayed() != flag) & (delay_secs >0):
                delay_secs -= countdown

            if selenium_object.is_displayed() == True:
                message = "Object_displayed"
            else:
                message = "Object not displayed after {} seconds".format(round(timeout,2))
        
        except StaleElementReferenceException: # If the object was previously available & is no longer displayed
            #if timeout > delay_secs:
            message = "Object not displayed after {} seconds".format(round(timeout - delay_secs,2))
            
        except NoSuchElementException:
                message = "Element Not Found. Please ensure that selenium object exists"

        message = "{}, Used implicit_wait_is_displayed. Waited for {}.\nResult: {}".format(
            function_name, round(timeout - delay_secs,2), message)
        logger.info(message)
        return message

    def check_if_whatsapp_locked(self, driver, timeout = 4, landing_dictionary=landing_dict):
        """
        Function checks if whatsapp is locked (if the QR code is displayed).
        Checks against 3 conditions 1. The locked screen text is visible.
        2. A unlocked screen object is available.
        3. None of the above because an error is encountered.
        Function uses an inbuilt wrapper in order to control another function (implicit_wait).

        Args:
            self = a Navigate Class object, used to control the functions in the Navigate class.
            driver - a WebDriver object, used to interact with the website.
            timeout - the number of seconds to wait for
            landing_dict - a dictionary object, contains the names of classes used to check if locked.
            
        Returns:
            message - a string, contains a message about the condition of whatsapp.
        
        E.g:
            object - check_if_whatsapp_locked(driver = driver, timeout = 1, landing_dictionary = landing_dictionary)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        def wrapper_implicit_wait(driver, timeout, class_name):
            """
            See DocString for implicit_wait for details.
            This wrapper function controls the implicit wait function defined above.
            """
            result = self.implicit_wait(driver, timeout, class_name)
            if type(result) == selenium.webdriver.remote.webelement.WebElement:
                message = "Class object found"
            else:
                message = result
            return message

        # Find out if whatsapp locked or not.
        if wrapper_implicit_wait(driver, timeout, landing_dictionary["locked_class"]) == "Class object found":
            message = "Whatsapp Locked"
        elif wrapper_implicit_wait(driver, timeout, landing_dictionary["unlocked_class"]) == "Class object found":
            message = "Whatsapp not Locked"
        else:
            message = "Whatsapp status not clear. Check if class names haven't changed."
        

        message = "{},{}".format(function_name, message)
        logger.info(message)
        
        return message
    
    def initiate_login(self, driver,retries=5, timer = 30):
        """
        Function used to initiate Whatsapp login sequence.
        Uses a timer to countdown & check if Whatsapp has been logged in to.

        Args:
            self = a Navigate Class object, used to control the functions in the Navigate class.
            driver - a WebElement object, used to control browser.
            retries - an integer object, used to control how many times function loops for.
            timer -  a integer object, how long the countdown should be before refreshing driver.
            
        Returns:
            whatsapp_status - a string object, a string saying whether the login attempt was successful or not.
            driver - a WebElement object, used to control browser.
            
        E.g:
            object - initiate_login(driver = driver, retries =30, timer = 30)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        whatsapp_status = self.check_if_whatsapp_locked(driver)
        
        while whatsapp_status == "check_if_whatsapp_locked,Whatsapp Locked":
            message = "Retries remaining {}\n".format(retries)
            logger.info("{},{}".format(function_name, message))
            print(message)

            for i in range(timer):
                message = "Waited {} seconds.".format(i)
                logger.info("{},{}".format(function_name, message))
                print(message)
                time.sleep(1)
            
            driver.refresh()
            retries -= 1

            if retries == 0:
                whatsapp_status = "Max retries reached."
            else:
                whatsapp_status = self.check_if_whatsapp_locked(driver)
            logger.info('{},{}'.format(function_name,whatsapp_status))
        return whatsapp_status, driver

    search_dict = {
        "description" : """used in enter_text_in_searchbox() & cancel_search. Contains class names for finding elements
        in the contacts search bar on the left hand side of the screen""",
        'search_group_class' : 'ZP8RM', # search box, below profile pane on top left
        'search_button_class' : "_1XCAr", # Search button class, in search group, on left.
        'text_field_class' : '_2zCfw', # text field class, at centre of textbox, marked as label in Whatsapp html    
        'cancel_button' : '_2heX1' # cancel button class, in span tag below the search button. 
        }
    
    
    def enter_text_in_searchbox(self, driver, contact_name, search_dict =search_dict):
        """
        Function enters a contact's name in the search box.

        Args:
            driver - a WebDriver object, used to interact with the website.
            search_dict - a dictionary object, contains the names of classes found in the search box.
            contact_name - a string object,the name of the contact to search for.

        Returns:
            message - a string object, with information on whether the text was entered or not.
        
        E.g:
            message - enter_text_in_searchbox(driver = driver, contact_name ='Luyanda Dhlamimi', search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  

        """
        function_name = sys._getframe().f_code.co_name

        try:
            group = driver.find_element_by_class_name(search_dict['search_group_class'])
            search_button = group.find_element_by_class_name(search_dict['search_button_class'])
            text_field = group.find_element_by_class_name(search_dict['text_field_class'])
            self.implicit_wait_is_displayed(text_field)
            self.implicit_wait_is_displayed(search_button)
            search_button.click() # Click on search icon

            text_field.clear() # Clears the text field
            text_field.send_keys(contact_name) # Sends the name to search for.
            message = "{} entered in search box.".format(contact_name)

        except NoSuchElementException:
            message = "Error encountered when searching for {}".format(contact_name)
        logger.info('{},{}'.format(function_name,message))
        
        return message
    

    def cancel_search(self, search_dict=search_dict):
        """
        Function clicks on the cancel button in the contact search box.

        Args:
            search_dict - a dictionary object, contains the names of classes found in the search box.
            logger - a logging object, keeps a log of what happens in the function.
            
        Returns:
            message - a string, with information on whether the cancel button was clicked or not.

        E.g:
            message - cancel_search(search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  
        
        """
        function_name = sys._getframe().f_code.co_name
        try:        
            group = driver.find_element_by_class_name(search_dict['search_group_class'])
            cancel_button = group.find_element_by_class_name(search_dict['cancel_button'])

            cancel_button.click() # Clears search text
            message = "Cancel button clicked."
        except NoSuchElementException:
            message = "Error: Cancel button not clicked."

        logger.info('{},{}'.format(function_name,message))
        
        return message
    

    contacts_dict = {
        "description" : """used in fetch_displayed_items(). Dictionary contains class names
        used to fetch contacts & messages displayed under the search bar.""",
        'contact_group_class' : "_1uESL", # class identifies the the left pane with profile with contacts, search, profile
        'contact_group_subclass':"_1H6CJ", # grouping of contacts pane. Previous class name: "_3La1s"
        'contacts_list_class' : "X7YrQ", # class of contact type items (contacts, messages, groups, titles - chats),
        'cancel_button' : '_2heX1' # cancel button class, in span tag below the search button. 
        }
    

    def fetch_displayed_items(self, driver, contacts_dict=contacts_dict, search_dict = search_dict):
        """
        Class finds contact/message/ header objects displayed on a whatsapp contact list.
        -- Current implementation not able to look at the GROUPS section of the pane. Only looks at Chat pane.
        -- 

        Args:
            driver - a WebDriver object, used to interact with the website.
            contacts_dict - a dictionary object, contains the names of classes found in the left pane.
            logger - a logging object, keeps a log of what happens in the function.
            
        Returns:
            contact_list -  a list object, list with elements.
        E.g:
            message - fetch_displayed_items(driver = driver, contact_name ='Luyanda Dhlamimi', search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  
        
        """
        function_name = sys._getframe().f_code.co_name
        
        # Make program sleep for 1 second, then fetch all displayed contacts & messages
        # Implicit wait used to ensure that we wait for the cancel button to be available in search bar
        time.sleep(3)
        
        self.implicit_wait(selenium_object=driver, timeout=4, class_name=contacts_dict['cancel_button'])

        contact_list = [] # List stores returned objects
        try:
            # Fettch all displayed objects
            group = driver.find_element_by_class_name(contacts_dict['contact_group_class'])
            print(group)
            sub_group = group.find_element_by_class_name(contacts_dict['contact_group_subclass'])
            contact_list = sub_group.find_elements_by_class_name(contacts_dict['contacts_list_class'])
            message ="{} elements returned.".format(len(contact_list))

        except NoSuchElementException: # Potential bug, what if there are no contacts to display under the searched text?
            message ="{} elements returned.".format(len(contact_list))
        logger.info('{},{}'.format(function_name,message))
        
        return contact_list

    is_contact_dict ={
        "description" : """Used in the check_if_contact(). Dictionary contains class names that help identify an
        element as either a contact or not.""",
        "contact_type_class" : "_3vpWv", # object the picture on the left of a contact. Differentiates contact from msg.
        "contact_name_class" : "_19RFN", # the contact name text class, sevel levels down into the contact object
        "message_type_class" : "_2WP9Q", # div object found 2 levels below the contact object class for messages.
        "header_type_class" : "r7sRK" # div object found 1 level below the contact object class for headers.
    }    

    def check_if_contact(self, element_list, is_contact_dict = is_contact_dict):
        """
        Checks if Selenium objects passed as input are contact objects or not.
        If it is a contact, places that selenium object in a list.
        The other alternatives are that it can be a message item or header item (chats/ messages).

        Args:
            element_list - a list object, with elements to be checked.
            is_contact_dict -  a dictionary object, with classes used to identify contacts.

        Returns:
            elem_list -  a list object, contains objects that are identified as contacts.
        E.g:
            message - fetch_displayed_items(driver = driver, contact_name ='Luyanda Dhlamimi', search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        elem_list = [] # list of elements that are contacts & are to be returned.

        try:
            logger.info("Checking whether {} elements are contacts.".format(len(element_list)))
            for element in element_list:                
                if self.check_element_exists(element, is_contact_dict["contact_type_class"]):
                    # If an element has a picture, it is a contact. Get it's text.
                    elem_list.append(element)
                    name = element.find_element_by_class_name(is_contact_dict["contact_name_class"]).text
                    message = "Is contact: " + name
                    #print(message)
                    logger.info('{},{}'.format(function_name,message))

        except StaleElementReferenceException:
            message = "Contact elements are no longer available."
            #print(message)
            logger.info('{},{}'.format(function_name,message))
        
        logger.info("{},{} elements identified as contacts.".format(function_name,len(elem_list)))
        
        return elem_list

    text_class_dict ={ 
        "description" : """Used in find_target_element(). Dictionary contains classes for reading the name of a contact.""",
        "text_class_name" : "_19RFN" # CLass allows you to find the name text of a contact object.
                      }

    def find_target_element(self, element_list,  target_element_text, text_class_dict=text_class_dict):
        """
        Searches objects for a text, returns the object that matches that text.

        Args:
            element_list - a list object, with elements to be checked.
            text_class_dict - a dictionary object, with classes used to compare.
            target_element_text - a string object, the contact name to target.

        Returns:
            returned_list -  a list object, contains objects that have the same text as target_element_text.
        E.g:
            message - fetch_displayed_items(driver = driver, contact_name ='Luyanda Dhlamimi', search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        returned_list = []
        for element in element_list:
            try:
                # Check each element's text against the target_element_text
                # Untested code
                self.implicit_wait_is_displayed(element)
                element_text = element.find_element_by_class_name(text_class_dict["text_class_name"]).text

                if element_text == target_element_text:
                    returned_list.append(element)
                    message = "Found match for: {}".format(element_text)
                else:
                    message = "No match for: {}".format(element_text)

            except NoSuchElementException:
                message = "Element not found"

            except StaleElementReferenceException:
                message = "Contact elements are no longer available."
            logger.info('{},{}'.format(function_name,message))
        # If the list is still empty, print that no matches found.
        if len(returned_list) == 0:
            message = "No matches found"
            logger.info('{},{}'.format(function_name,message))
        return returned_list

    
    def click_on_element(self, element, logger = logger):
        """
        Function clicks on element.

        Args:
            element - a WebElement, containing the object to click on.

        Returns:
            message - a string, with results of the click attempt.
        
        E.g:
            message - fetch_displayed_items(driver = driver, contact_name ='Luyanda Dhlamimi', search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        try:
            # Untested code
            self.implicit_wait_is_displayed(element)
            element.click()
            message = "Clicked on target element"
            
        except ElementClickInterceptedException as e:
            message = e
        
        except NoSuchElementException:
            message = "{} not found".format(element)

        except StaleElementReferenceException:
            message = "Contact elements are no longer available."
        logger.info('{},{}'.format(function_name,message))
        return message
        ## Will need to come back to fully implement. Identify what might go wrong, especially with layering.

    def find_contact(self, driver,  contact_name, search_dict = search_dict):
        """
        Function searches for a contact_name. If that contact is found, it is clicked on.
        
        Args:
            contact_name - a string object, with the name to search for.
            
        Returns:
            message - a string object, contains response on whether the contact was found & clicked on or not.
            
        E.g: result = nav.find_contact("WLS Team")
        LastMod: Luyanda Dhlamini
        """
        driver = driver
        function_name = sys._getframe().f_code.co_name
        logger.info('{},Finding contact: {}.'.format(function_name,contact_name))

        message = self.enter_text_in_searchbox(driver=driver, contact_name=contact_name)
        displayed_item = self.fetch_displayed_items(driver)
        contacts = self.check_if_contact(element_list=displayed_item)
        target_contact = self.find_target_element(contacts, contact_name)
        if len(target_contact)>=1:
            message = self.click_on_element(target_contact[0])
        else:
            message = "Contact not found. Confirm if spelling is correct."
        
        self.cancel_search(driver)
        logger.info('{},{}.'.format(function_name,message))
        return message
        
    def take_element_screenshot(self, selenium_element, save_path, filename = '', logger = logger):
        # Need to change save_path to save to a 'screenshots' folder in a current path.
        """
        Function takes a screenshot of an element & then saves it to a desired path.

        Args:
            selenium_element - a WebElement object, to take a screenshot of.
            filename - the name to save the picture as. Name excludes file suffix. Will be saved as png.
            save_path - the filepath to save the screenshot to

        Returns:
            message - a string object, with information on whether a screenshot was taken or not.
        E.g:
            message - fetch_displayed_items(driver = driver, contact_name ='Luyanda Dhlamimi', search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        # Try statement here, to ensure element still active. Handle that.
        try:
            # Take screenshot
            if type(selenium_element) == selenium.webdriver.chrome.webdriver.WebDriver:
                screenshot = selenium_element.get_screenshot_as_png()
            
            else:
                screenshot = selenium_element.screenshot_as_png

            # Format filename & write to disk
            if filename == "":
                filename = self.current_time_string()
                
            full_path = save_path + filename + ".png"
            with open(full_path, "wb")  as outfile:  
                outfile.write(screenshot)
            message = "Screenshot saved as: {}".format(full_path)   

        except NoSuchElementException:
            message = "Screenshot not taken. Element not found"

        except StaleElementReferenceException:
            message = "Screenshot not taken. Element no longer active"
 
        logger.info('{},{}'.format(function_name,message))
        return message

    logout_dict = {
        "description" : """Dictionary used to store classes that allow you to click on the options button in the main-pane & 
        the n click on Log Out""",
        'menu_group_class' : "_3Jvyf", # left pane menu group class
        'options_button_class':"_3j8Pd", # the list of buttons on the left pane menu group. Is same for all 3 buttons.
        "float_menu_group_class": "_2hHc6", # the floating menu class that appears after clicking on options button. 
        'logout_button_class' : "_3cfBY" # the buttons class on the floating menu.
        }

    def logout_of_whatsapp(self, driver, logout_dict = logout_dict):
        """
        Function clicks on the attach button on the "main" pane 

        Args:
            self - a Class object, used to ensure that an instance of the Write class is available locally
            driver - a WebDriver object, used to interact with the website.
            attach_dict - a dictionary object, with classes used to click on the attach button.

        Returns:
            message - a string object, with information on whether the function execuded successfully.
        
        E.g:
            message - fetch_displayed_items(driver = driver, contact_name ='Luyanda Dhlamimi', search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        try:
            group = driver.find_element_by_class_name(logout_dict['menu_group_class'])
            options_button = group.find_elements_by_class_name(logout_dict['options_button_class'])
            menu_button = options_button[2]
            menu_button.click()

            floating_menu = menu_button.find_element_by_class_name(logout_dict['float_menu_group_class'])
                #logout_dict['float_menu_group_class'])
            options_buttons_list = floating_menu.find_elements_by_class_name(logout_dict['logout_button_class'])
            #    _2hHc6
            logout_button = options_buttons_list[5]
            time.sleep(1)
            logout_button.click()
            message = "Clicked on logout button"

        except NoSuchElementException:
            message = "Logout not clicked on. Element not found"

        except StaleElementReferenceException:
            message = "Logout button not clicked on. Element no longer active"
        logger.info('{},{}'.format(function_name,message))        

        return message

    create_group_dict = {
        "description" : """Dictionary used to store classes that allow you to click on  to create a new whatsApp group""",
        "profile_pane_class" : "_3Jvyf", # the class highlighting the entire profile pane on top left
        "drop_menu_class" : "_3j8Pd", # the class that contain a button menu
        "new_group_button_class" : "_3zy-4", #the class to new create new group
        "to_select_member" : "_1w-mX", #class name for pane that hold text field
        "add_contact_memb_class" : "_44uDJ.copyable-text.selectable-text", # class of a text field to enter text of a contact 
        "contacts_nam_block_class" : "_2WP9Q", #class name for contact name/block
        "procced_class" :"_1g8sv", #after selecting all contact for a group pressing next
        "focus_area_class":"rK2ei",
       "creation_class" : "_1g8sv", #class of a button that fanilies the creation and save your new group
        "Write_groupNam_class" :"_3u328.copyable-text.selectable-text" #class name of an element that enables you to write the group name
    }

    def create_whatsapp_group(self,driver, group_name, contact_names,
                              create_group_dict = create_group_dict):
        """
        Creating a new whatsapp group.

        Args:
            self - a Class object, used to ensure that an instance of the Write class is available locally
            driver - a WebDriver object, used to interact with the website.
            create_group_dict - a dictionary object, with classes used to click on create a new whatsapp group button.

        Returns:
            message - a string object, with information on whether the function execuded successfully.
        E.g:
            message - Create_whatsapp_Group(self,Driver,create_group_dict = create_group_dict)
        LastMod:
            Nokwazi Masindane, Edits: Luyanda Dhlamini
        """

        function_name = sys._getframe().f_code.co_name  
        message = "Creating group: {}".format(group_name)
#         print(message)
        logger.info('{},{}'.format(function_name,message))        

        try:
            is_displayed = self.implicit_wait_is_displayed(driver.find_element_by_class_name(create_group_dict["profile_pane_class"]))
            # The area where selenium will focus on to find element
            profile_pane = driver.find_element_by_class_name(create_group_dict["profile_pane_class"])

            # Use implicit wait until the floating menu with options is available
            self.implicit_wait(profile_pane,timeout=3,class_name= create_group_dict["drop_menu_class"])
            drop_menu =  profile_pane.find_elements_by_class_name(create_group_dict["drop_menu_class"])#element to be click
            drop_menu[2].click() #let your program click on a manu button that lead you to dropdown with new group button
            
            wait_group_floating_menu = self.implicit_wait_is_displayed(driver.find_element_by_class_name(create_group_dict["new_group_button_class"]))
            new_group_buttons = driver.find_elements_by_class_name(create_group_dict["new_group_button_class"])#element to be click

            for option in new_group_buttons: # Loop through menu buttons, ensure that click on button with text "New group"
#                 print(option.text)
                if option.text == "New group":
                    found_new_group_button = True
                    option.click()
                    break # After finding new group button, move to next steps. 

            if found_new_group_button == True:
                is_displayed = self.implicit_wait_is_displayed(driver.find_element_by_class_name(create_group_dict["focus_area_class"]))
                area_focus = driver.find_element_by_class_name(create_group_dict["focus_area_class"])#erea where you cna
                contact_1 = driver.find_element_by_class_name(create_group_dict["add_contact_memb_class"])

                for contact in contact_names:
                    contact_1.send_keys(contact)

                    area_focus = driver.find_element_by_class_name(create_group_dict["focus_area_class"])
                    contacts_nam_block = area_focus.find_elements_by_class_name(create_group_dict["contacts_nam_block_class"])
                    target_contact = self.find_target_element(element_list = contacts_nam_block,target_element_text=contact)    
                    if len(target_contact) >0:
                        target_contact[0].click()
                        message = "Added {} to group creation list.".format(contact)
#                         print(message)
                        logger.info('{},{}'.format(function_name,message))
                    else:
                        message = "{} not found in list. Check spelling.".format(contact)
#                         print(message)
                        logger.info('{},{}'.format(function_name,message))
                    contact_1.clear()

                procced_next_step = driver.find_element_by_class_name(create_group_dict["procced_class"])#takes you to a next step of group creation
                procced_next_step.click()
                area = driver.find_element_by_class_name(create_group_dict["focus_area_class"])
                text_field = area.find_element_by_class_name(create_group_dict['Write_groupNam_class'])
                text_field.clear() # Clears the text field
                text_field.send_keys(group_name) # Sends the name to search for.

                complite = driver.find_element_by_class_name(create_group_dict["creation_class"])
                complite.click()
                message = "Group {} created successfully".format(group_name) 
#                 print(message)
            else:
                message = "New group button not found in floating menu."
#                 print(message)
            time.sleep(3) # Allow group creation to complete before continuing to other operations.
        except  Exception as e:
            message = "Error: {}".format(e)
#             print(message)
        logger.info('{},{}'.format(function_name,message))        

        return message
    
    add_person_dict ={
        "description" : """Used in the Create_new_Group_Admin. Dictionary contains class names that help in steps of creating
        new group Admin.""",
        "search_erea_class" : "_3fs0K", #class name  for element you first click when seaching group or contat on whatsapp
        "panel_class_toFocus" : "_1c8mz.rK2ei", #telling the driver the class to look for
        "menu_groups_class" : "_2LSbZ._2j5ir", # claases for groups of menus visible after you click group info
        "participants_buttons_class" : "_2UaNq._2nQ7u", # participant oprions
        "floating_menu_class" : "_3RiLE", # floating menu visible after clicking add participant
        "proceed_button_class" : "_1AWh3" , # element that you click confirming selected new admin
        "fetch_displayed_pane_class": "_2xLKR", # search bar pane visible when searching for a participant
        "add_participant_button_class" : "_2eK7W._3PQ7V", # Button for adding participants (stage 2)
    }

    def add_person_to_group(self, driver, group_name, contact_names, add_person_dict=add_person_dict):

        function_name = sys._getframe().f_code.co_name
        message = "Adding {} to group: {}".format(contact_names, group_name)
        logger.info('{},{}'.format(function_name,message))

        try:
        #     result = self.find_contact(driver,group_name)
            result = "Clicked on target element"

            if result == "Clicked on target element":
                header = driver.find_element_by_class_name(add_person_dict["search_erea_class"])
                #click to access the  panel that contain group atribute and more detailed information
                header.click()
                #localising to the nearest area eliminate class name duplicate
                focus = driver.find_element_by_class_name(add_person_dict["panel_class_toFocus"])

                menu_groups=focus.find_elements_by_class_name(add_person_dict["menu_groups_class"])
                participant_menu_group = menu_groups[4]
                participant_buttons = participant_menu_group.find_element_by_class_name(add_person_dict["participants_buttons_class"])
                participant_buttons.click()

                floating_menu = self.implicit_wait_is_displayed(driver.find_element_by_class_name(add_person_dict["floating_menu_class"]))
                floating_menu = driver.find_element_by_class_name(add_person_dict["floating_menu_class"])

                for contact_name in contact_names:
                    contact_clicked_on = False
                    search_query = self.enter_text_in_searchbox(floating_menu, contact_name)
                    temp_contacts_dict = self.contacts_dict
                    temp_contacts_dict['contact_group_class'] = add_person_dict["fetch_displayed_pane_class"]

                    displayed_item = self.fetch_displayed_items(floating_menu, contacts_dict = temp_contacts_dict)
                    contacts = self.check_if_contact(element_list=displayed_item)
                    target_contact = self.find_target_element(contacts, contact_name)
                    if len(target_contact)>=1:
                        message = self.click_on_element(target_contact[0])
                        contact_clicked_on = True
                    else:
                        message = "Contact not found. Confirm if spelling is correct."

                    self.cancel_search()
                    if contact_clicked_on == True:
                        message = "{} added to staging admin list".format(contact_name)
                        logger.info('{},{}'.format(function_name,message))
                    else:
                        message = "{} not found. Not added to group admins.".format(contact_name)
                        logger.info('{},{}'.format(function_name,message))
                floating_menu = driver.find_element_by_class_name(add_person_dict["floating_menu_class"])
                proceed_button_wait = self.implicit_wait(selenium_object=driver,
                                                         class_name = add_person_dict["proceed_button_class"], timeout = 1)
                if type(proceed_button_wait) != str:
                    proceed = floating_menu.find_element_by_class_name(add_person_dict["proceed_button_class"])
                    proceed.click() # clicking the button to finalises admin creation
                    # second floating menu now displayed.
                    # Must check if adding menu buttons are there.
                    floating_menu = driver.find_element_by_class_name(add_person_dict["floating_menu_class"])
                    add_participant_button = floating_menu.find_element_by_class_name(add_person_dict["add_participant_button_class"])
                    add_participant_button.click()
                    message = "Participants added."
                    driver.refresh()
                else:
                    message = "Proceed button not visible. No participants added."
                    driver.refresh()
            else:
                message = "Group participants not changed. Group '{}' not found".format(group_name)

        except Exception as e:
            # catch any error & log it. Helps prevent code from crashing.
            message = "Error: {}".format(e)

        logger.info('{},{}'.format(function_name,message))
        time.sleep(3) # 3 second delay added to allow page to load after refresh.
        return message


    add_admin_dict ={
        "description" : """Used in the Create_new_Group_Admin. Dictionary contains class names that help in steps of creating
        new group Admin.""",
        "search_erea_class" : "_3fs0K", #class name  for element you first click when seaching group or contat on whatsapp
        "panel_class_toFocus" : "_1c8mz.rK2ei", #telling the driver the class to look for
        "message_type_class" : "_2x2XP", # element class name that contain group members
        "new_small_erea" : "rK2ei" ,# element that apear with a list of members to choose when want to set admin
        "setting_erea_class" : "_2kUhl" ,# element that apear with a list of members to choose when want to set admin
        "members_class" : "_2xLKR", #"_1KDYa" ,# element that apear with a list of members to choose when want to set admin
        "proceed_class" : "NOJWi" ,# element that you click confirming selected new admin
        "displayed_members_class": "X7YrQ", # Class finds contacts displayed after text entered in textbox.
        "contact_name_class": "_3H4MS" # class identifies search results that are actual contacts & not headers.
        }
    
    def add_admin(self, driver, group_name, contact_names, add_admin_dict=add_admin_dict):

        """
        Creating a new whatsapp group admin.

        Args:
            self - a Class object, used to ensure that an instance of the Write class is available locally
            driver - a WebDriver object, used to interact with the website.
            add_admin_dict - a dictionary object, with classes used to click on create a new whatsapp group admin button.

        Returns:
            message - message - a string object, with information on whether the function execuded successfully.
        E.g:
            message = add_admin(self,Driver,add_admin_dict = add_admin_dict)
        LastMod:
            Nokwazi Masindane, Edits: Luyanda Dhlamini 
        """ 
        function_name = sys._getframe().f_code.co_name
        message = "Adding {} to group admins for group: {}".format(contact_names, group_name)
        logger.info('{},{}'.format(function_name, message))

        try:
            result = self.find_contact(driver,group_name)
            if result == "Clicked on target element":        
                header = driver.find_element_by_class_name(add_admin_dict["search_erea_class"])
                #click to access the  panel that contain group atribute and more detailed information
                header.click()
                #localising to the nearest area eliminate class name duplicate
                focus = driver.find_element_by_class_name(add_admin_dict["panel_class_toFocus"])
                contact_erea=focus.find_elements_by_class_name(add_admin_dict["message_type_class"])
                contact_erea[2].click() # click on "Group Settings" option

                direct =driver.find_element_by_class_name(add_admin_dict["new_small_erea"])
                #here is a list of settings where you get optioncalled add admin
                settings = direct.find_elements_by_class_name(add_admin_dict["setting_erea_class"])
                settings[2].click()#click on the edit group admins wich is index 2 on a list collected
                for contact_name in contact_names:
                    contact_clicked_on = False # Used later to confirm that contact clicked on
                    message = self.enter_text_in_searchbox(driver, contact_name)#method to enter contact's name to searchbox 
                    # class displays contacts after entering name. We wait till contacts are displayed.
                    member = driver.find_element_by_class_name(add_admin_dict["members_class"]) 
                    self.implicit_wait_is_displayed(member.find_element_by_class_name(add_admin_dict["displayed_members_class"]))
                    # fetch displayed contacts
                    displayed_contacts = member.find_elements_by_class_name(add_admin_dict["displayed_members_class"])

                    for displayed_contact in displayed_contacts:
                        # loop through each displayed contact. If is text & not header, check text against contact name.
                        if self.check_element_exists(displayed_contact,add_admin_dict['contact_name_class']) == True:
                            contact_object_text = displayed_contact.find_element_by_class_name(add_admin_dict['contact_name_class']).text
                            if contact_name == contact_object_text:
                                displayed_contact.click()
                                contact_clicked_on = True
                                break # Stop executing, target contact has been found.
                    self.cancel_search()
                    if contact_clicked_on == True:
                        message = "{} added to staging admin list".format(contact_name)
                    else:
                        message = "{} not found. Not added to group admins.".format(contact_name)
                    print(message)
                    logger.info('{},{}'.format(function_name,message))

                focus = driver.find_element_by_class_name("_1KDYa")
                proceed = focus.find_element_by_class_name(add_admin_dict["proceed_class"])
                proceed.click() # clicking the button to finalises admin creation
                message = "Code executed successfully."
            else:
                message = "Group admin not changed. Group '{}' not found".format(group_name)
            driver.refresh()
            time.sleep(5) # 5 second delay added to allow page to load after refresh.
        except Exception as e:
            # catch any error & log it. Helps prevent code from crashing.
            message = "Error: {}".format(e)

        logger.info('{},{}'.format(function_name,message))
        return message


# In[ ]:





# In[3]:


class Write(object):
    # The navigate class will be used to navigate around the whatsapp web client.
    # Its functionas are accompanied by dictionaries that containt the class names that the functions use to navigate.
    
    # Create an instance of the Navigate Class in order to use some of it's functions.
    # Think about consequences of having Navigate in its own module/ file
    from Navigate import Navigate
    NavInstance = Navigate()

#     attach_executable_path = r"C:\Users\weightlossschool\Desktop\Live\attach_file.exe"
    attach_executable_path = r"C:\Users\ludhl\Desktop\AutoIT\attach_file.exe"
    
    click_attach_dict = {
        "description" : """Dictionary used to store classes that allow you to click on the attach button in the main-pane""",
        'menu_group_class' : "_3fs0K", # the 'in-contact' menu class on top of messaging pane when contact clicked on                             
        'menu_subgroup_class' : "_3lq69", # contains the 3 buttons in the menu
        'attach_button_class' : "_3j8Pd", # the menu buttons class, is list with 3 elements
    }

    def click_on_attach(self, driver, attach_dict = click_attach_dict):
        """
        Function clicks on the attach button on the "main" pane 
        
        Args:
            self - a Class object, used to ensure that an instance of the Write class is available locally
            driver - a WebDriver object, used to interact with the website.
            attach_dict - a dictionary object, with classes used to click on the attach button.

        Returns:
            message - a string object, with information on whether the function execuded successfully.

        E.g:
            message - fetch_displayed_items(driver = driver, contact_name ='Luyanda Dhlamimi', search_dict =search_dict)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        try:
            group = driver.find_element_by_class_name(attach_dict['menu_group_class'])
            subgroup = group.find_element_by_class_name(attach_dict['menu_subgroup_class'])
            buttons = subgroup.find_elements_by_class_name(attach_dict['attach_button_class'])
            attach_button = buttons[1]

            attach_button.click()
            message = "Clicked on attach button"
            
        except NoSuchElementException:
            message = "Attachment not clicked on. Element not found"
            
        except StaleElementReferenceException:
            message = "Attach button not clicked on. Element no longer active"
        
        logger.info('{},{}'.format(function_name,message))
        return message
        # Must have way of testing if button clicked. Will need function to check if floating 
        

    attachment_dict = {
        "description" : """Dictionary used to store classes that allow you to add a caption to a attachment post""",
        "main_class_grouping" : "_2CDPn", # the main class in the popup attachment menu
        #"caption_existing_text" : "_7HWvs",   
        "caption_text_class" : "_3u328" # the class name of the text field
        }
    
    def add_attachment_caption(self, driver, attachment_caption, attachment_dict = attachment_dict):
        """
        Function adds a text to a whatsapp attachment caption.
        
        Args:
            self - a Class object, used to ensure that an instance of the Write class is available locally
            driver - a WebDriver object, used to interact with the website.
            attachment_caption -  a string object, text to send as an attachment caption.
            attachment_dict - a dictionary object, with classes used to add attachment caption.

        Returns:
            message - a string object, with information on whether the function execuded successfully.
        E.g:
            message - add_attachment_caption(driver=driver, attachment_caption = 'this is an attachment caption',
                        attachment_dict = attachment_dict)
        LastMod:
            Luyanda Dhlamini              
        """
        function_name = sys._getframe().f_code.co_name
        time.sleep(3)
        try:
            self.NavInstance.implicit_wait(driver,timeout=10,class_name=attachment_dict['main_class_grouping'])
#             self.NavInstance.implicit_wait_is_displayed(driver.find_element_by_class_name(attachment_dict['main_class_grouping']))
            attachment_group = driver.find_element_by_class_name(attachment_dict['main_class_grouping'])
#             print('attachment_group:',attachment_group)
        
            self.NavInstance.implicit_wait(driver,timeout=10,class_name=attachment_dict['caption_text_class'])
            text_field = attachment_group.find_element_by_class_name(attachment_dict['caption_text_class'])
#             print("text_field: ",text_field)
            
            text_field.clear() # Clears the text field
            text_field.send_keys(attachment_caption) # Sends the name to search for.
            message = "Attachment caption added."
            
        except NoSuchElementException:
            message = "Element not found"

        except StaleElementReferenceException:
            message = "Element no longer active"
        logger.info('{},{}'.format(function_name,message))
        
        return message        

    send_attachment_dict = {
        "description" : """Dictionary used to store classes that allow you to click on the send attachment button""",
        "main_class_grouping" : "rK2ei", # the class highlighting the entire attachment pane
        "attachment_button" : "_1g8sv" # the attachment button class
    #    "caption_text_class" : "_2S1VP"
        }
    
    def click_send_attachment(self, driver, send_attachment_dict = send_attachment_dict):
        """
        Adds text to a whatsapp caption.
        
        Args:
            self - a Class object, used to ensure that an instance of the Write class is available locally
            driver - a WebDriver object, used to interact with the website.
            send_attachment_dict - a dictionary object, with classes used to click on the send attachment button.

        Returns:
            message - a string object, with information on whether the function execuded successfully.
        E.g:
            message - click_send_attachment(driver = driver, send_attachment_dict = send_attachment_dict)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        try:
            attachment_group = driver.find_element_by_class_name(send_attachment_dict['main_class_grouping'])

            attachment_button = attachment_group.find_element_by_class_name(send_attachment_dict['attachment_button'])

            attachment_button.click()
            message = "Send attachment button clicked"

        except NoSuchElementException:
            message = "Element not found"

        except StaleElementReferenceException:
            message = "Element no longer active"
        logger.info('{},{}'.format(function_name,message))
        return message

    def enter_formatted_text(self, driver, message_string, element = '',separator = '<br>'): # , element
        """
        Function takes a string input & formats it in a way that allows you to enter a message in multiple lines.
        E.g. For each word in the list, enter that word & then press shift enter to go to a new line.

        Args:
            message_string - a string object, the message to be sent.
            separator - a string object, the string sequence used to see when we need to go to a new line.

        Returns:
            text - a list object, a list of strings. 

        E.g: 
            list_of_strings = enter_formatted_text("First sentence.<br>Second sentence.")
        LastMod: Luyanda Dhlamini
        """
        text = message_string.split(sep= separator)    # Split the message using the separator
        print(text)
        chain =webdriver.ActionChains(driver)    # create a chain object, uses to input shift enter.
        # FOr each word in the list, enter that word & then press shift enter to go to a new line.
        for string in text:
            chain.send_keys(string)
            chain.key_down(Keys.SHIFT)
            chain.send_keys(Keys.ENTER)
            chain.key_up(Keys.SHIFT)
    #    chain.send_keys(Keys.ENTER)
        chain.perform()
        return text
    
    text_message_dict = {
        "description" : """Dictionary used to store classes that allow you to send a text message.""",
        'message_displayed_class':"_2i7Ej", # Class for the message box, including send & emoji button 
        'message_write_class' : "_3u328", # Class for entering text, marked as being called copyable-text
        'send_button_class' : '_3M-N-' # Button class, only appears once text box has been populated.
    }

    def send_text_message(self, driver, text_message, text_message_dict = text_message_dict):
        """
        Functions sends a text message

        Args:
            self - a Class object, used to ensure that an instance of the Write class is available locally
            driver - a WebDriver object, used to interact with the website.
            text_message -  a string object, with the text message to be sent.
            text_message_dict - a dictionary object, with classes used to click on the send attachment button.

        Returns:
            message - a string object, with information on whether the function execuded successfully.
        
        E.g:
            message - send_text_message(driver = driver, text_message = 'This is text message',
                    text_message_dict = text_message_dict)
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        try:
            # Would need to first test if message pane is visible.
            message_box = driver.find_element_by_class_name(text_message_dict['message_displayed_class'])

            message_box2 = driver.find_element_by_class_name(text_message_dict['message_write_class'])
#            message_box2.send_keys(text_message) # send message.
            message_box2.click()
            text = self.enter_formatted_text(driver, message_string = text_message, element = message_box2, separator = '<br>')

            # Send button
            btn_send_message = driver.find_element_by_class_name(text_message_dict['send_button_class'])
            btn_send_message.click()
            # Would need to use the read classes to confirm if message sent correctly.
            message = "Text message sent"
            
        except NoSuchElementException:
            message = "Element not found"

        except StaleElementReferenceException:
            message = "Element no longer active"
        logger.info('{},{}'.format(function_name,message))
        
        return message

    attach_file_dict ={ 
        "description" : """Dictionary stores classes that allow you to click on the gallery icon & attach a file""",
        # Class to check if message box open must be here.
        'float_menu_class' : "KSY4t", # Class is the main class of the attach file list of buttons
        "float_menu_list_class" : "_3z3lc", # Class is the list class of the attach file list of buttons
        "float_menu_buttons" : "Ijb1Q" # Class name of buttons in menu list
    }

    def attach_file(self, driver, attach_executable_path, attachment_link, attach_file_dict = attach_file_dict):
        """
        Function attaches a file from the Operating System onto Whatsapp.
        
        Args:
            self - a Class object, used to ensure that an instance of the Write class is available locally
            driver - a WebDriver object, used to interact with the website.
            attach_executable_path -  a string object, the file path to the executable script to upload an attachment.
            attach_file_dict - a dictionary object, with classes used to attach a file.

        Returns:
            message - a string object, with information on whether the function execuded successfully.
            
        E.g:
        results = writer.attach_file(driver,attach_executable_path= "C:/Users/ludhl/Desktop/AutoIT/autoit3.exe",
          attachment_link = r"C:/Users/ludhl/Desktop/AutoIT/10 days.jpg")        
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        #print("Got to attach")
        try:
            # Find and click on attach button.
            float_menu = driver.find_element_by_class_name(attach_file_dict["float_menu_class"])
            float_menu_list = float_menu.find_element_by_class_name(attach_file_dict["float_menu_list_class"])
            float_menu_buttons = float_menu_list.find_elements_by_class_name(attach_file_dict["float_menu_buttons"])
            #print(len(float_menu_buttons))
            time.sleep(1)
            float_menu_buttons[0].click()

            # Execute AutoIt script
            # Must allow to take in parameters
            # What other exceptions are possible from the below code?
            # THIS PART DOES NOT WORK> WILL NEED TO FIX!
            
            time.sleep(1)
            
            program_name = attach_executable_path # The autoit program that will run code
            arguments = [attachment_link]  # The attachment you want to attach.

            command = [program_name]  
            command.extend(arguments)  
            #print("Got to subprocess")
            
            output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]  
            #print(output)
            logger.info('{},{}'.format(function_name,output))
            
            message = "File attached"
            logger.info('{},{}'.format(function_name,message))
    
        except NoSuchElementException as e:
            #print(e)
            message = "File not attached sucessfully. Element not found"

        except StaleElementReferenceException:
            message = "File not attached. Element no longer active"
        logger.info('{},{}'.format(function_name,message))
        return message

    
    def send_attachment(self, driver, attach_executable_path, attachment_link, attachment_caption):
        """
        Function sends attachment using various sub-functions.
            formats:
            attach_executable_path= "C:/Users/ludhl/Desktop/AutoIT/autoit3.exe"
            attachment_link = r"C:/Users/ludhl/Desktop/10 days.jpg"
        Args:


        Returns:

        E.g:
            message - send_attachment(driver = driver, attach_executable_path = "C:/Users/ludhl/Desktop/AutoIT/autoit3.exe",
                attachment_link = r"C:/Users/ludhl/Desktop/10 days.jpg", attachment_caption = 'A')
        LastMod:
            Luyanda Dhlamini  
        """
        function_name = sys._getframe().f_code.co_name
        click_attach_output = self.click_on_attach(driver)
        
        attach_file_output = self.attach_file(driver, attach_executable_path = attach_executable_path, attachment_link = attachment_link)
        #print(attach_file_output)
        time.sleep(1)
        attach_attachment_caption_output = self.add_attachment_caption(driver, attachment_caption)
        print(attach_attachment_caption_output)
        click_send_attachment_output = self.click_send_attachment(driver)

        #logger.info('{},{}'.format(function_name,click_send_attachment_output))


# In[ ]:





# In[8]:


class Read(object):
    from Navigate import Navigate
    NavInstance = Navigate()
    
    # types of objects a user generated message can be. Excludes date dividers & notifications.
    MESSAGE_OBJECT_LIST = ["Text Message","Video","Image","Audio","Document","Contact","Location"]
  
    is_whatsapp_group_dict = {
        "description" : """Used to check is a contact is a whatsapp group.
        Assumes you've already clicked on the contact & in the message pane""",
        "contact_messages_class":"NuujD", # visible if a contact as been clicked on.identifies the main contact messages pane. 
        "group_participants_list_class":"_3Q3ui", # available in Whatsapp groups. Below the group's name.
        "message_pane_header_class": "_3fs0K", # Class in the main message pain, with group name & buttons.
        "message_pane_buttons_class":"_3j8Pd", # Class for buttons in headers
        "floating_menu_class": "_2hHc6", # Class for the floating buttons list that appears when you click on menu.
        "contact_info_button": "_3cfBY" # class for buttons in floating menu.
    }

    def is_whatsapp_group(self,driver, is_whatsapp_group_dict = is_whatsapp_group_dict):
        """
        Function checks if a contact that has been clicked on is a Whatsapp group or not.
        Args:
            driver - a WebDriver object, used to interact with the website.
            is_whatsapp_group_dict - a dictionary object, contains all the classes used in the function.
        Returns:
            status - a boolean object or string object, True if contact is group, otherwise false.
                    Will also inform you if no contact has been clicked on or the contact's state is unknown.
        E.g: Is_Group = self.is_whatsapp_group(driver)
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        if (self.NavInstance.check_element_exists(driver,is_whatsapp_group_dict["contact_messages_class"]) == False):
            status = "False, no contact clicked on"
        else:
            # Click on the messages menu button.
            message_pane_header = driver.find_element_by_class_name(is_whatsapp_group_dict["message_pane_header_class"])
            message_pane_buttons = message_pane_header.find_elements_by_class_name(
                                    is_whatsapp_group_dict["message_pane_buttons_class"])
            message_pane_menu_button = message_pane_buttons[2]
            message_pane_menu_button.click()
            
            # wait till float displayed menu displayed.
            floating_menu = self.NavInstance.implicit_wait(message_pane_header,3,is_whatsapp_group_dict["floating_menu_class"])
            self.NavInstance.implicit_wait_is_displayed(floating_menu,wait_type="displayed") 

            # Get first menu item text
            floating_menu_buttons = floating_menu.find_elements_by_class_name(is_whatsapp_group_dict["contact_info_button"])
            contact_info_button = floating_menu_buttons[0]
            self.NavInstance.implicit_wait_is_displayed(contact_info_button,wait_type="displayed")
            contact_info_button_text = contact_info_button.text
            if contact_info_button_text == "Contact info":
                status = False
            elif contact_info_button_text == "Group info":
                status = True
            else:
                status = "Unknown"
            
            # Press escape. Wait till the floating menu is no longer displayed.
            floating_menu.send_keys(Keys.ESCAPE)
            self.NavInstance.implicit_wait_is_displayed(floating_menu,wait_type="not_displayed")

        logger.info('{},Is Whatsapp: {}. '.format(function_name,status))
        return status

    whatsapp_divider_dict = {
        "description": """dictionary stores classes used to interact with whatsapp date divider objects and 
        scroll up whatsapp messages.""",
        "divider_message_class":"_3CGDY", # class in message objects that have date information. E.g: 'TODAY'
        "message_list_subgroup_class":"_1ays2", # Identifies messages sub_pane
    }


    def get_days_list(self, day_to_go_back=6):
        """
        Function creates a DataFrame with dates going back "day_to_go_back" times.
        Args:
            day_to_go_back -  a integer object, number of days to go back from today.
                              Used as a starting date & counts up to today.
        Returns:
            day_list_dataframe - a pd.DataFrame onbject, with list of days & their day names.
        E.g: days = get_days_list(day_to_go_back = 6)
        LastMod: Luyanda Dhlamini
        """        
        # Get today & the fist date, convert them from datetime.datetime to strings.
        end = datetime.datetime.today().strftime("%m/%d/%Y")
        start_date = datetime.datetime.today() - datetime.timedelta(day_to_go_back)
        start = start_date.strftime("%m/%d/%Y")

        # Create a date range for all days between satrt & end dates. Get the names of these day (MONDAY, TUESDAY)
        day_list_dataframe = pd.DataFrame(pd.date_range(start=start,end=end),columns=['date_list'])
        day_list_dataframe['day_name'] = day_list_dataframe.date_list.apply(lambda x : x.strftime("%A").upper())

        # Rename today & yesterday's day names to today & yesterday.
        day_list_dataframe.at[day_list_dataframe.index[-1],'day_name'] = "TODAY"
        if (day_list_dataframe.shape[0]>1):
            day_list_dataframe.at[day_list_dataframe.index[-2],'day_name'] = "YESTERDAY"

        # Sort values in descending order & reset the index.
        day_list_dataframe.sort_values(by=['date_list'],ascending=False,inplace=True)
        day_list_dataframe.reset_index(inplace=True,drop=True)
        return day_list_dataframe

    def check_whatsapp_date(self, input_object, day_list_df):
        """
        Function checks if a input_object string is a date, day name, encryption string or just a string.
        The string is then converted to its corresponding date string or "Not Date" is returned.
        Args:
            input_object - a string object, containes text fetched from divider.
            day_list_df - a pd.DataFrame oobject, with list of days and day names from today in descending order.
        Returns:
            input_object - a string object, with date as string or the words "Not Date".
        E.g: date = check_whatsapp_date("TODAY",get_days_list(day_to_go_back=6))
        LastMod: Luyanda Dhlamini
        """        
        day_list_df = day_list_df.copy()
        try:
            # Check if date input object is a date string (e.g. 1/1/2019)
            input_object = datetime.datetime.strptime(input_object,"%m/%d/%Y")
            input_object=input_object.strftime("%m/%d/%Y")

        except ValueError:
            # if the input_object is a day string (e.g FRIDAY), get it's corresponding date string from the day list dataframe.
            if input_object in ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY','YESTERDAY','TODAY']:
                actual_date_df = day_list_df[day_list_df['day_name'] == input_object]
                assert actual_date_df['date_list'].shape[0] == 1
                #convert date to string,take first value
                input_object = actual_date_df['date_list'].dt.strftime("%m/%d/%Y").values[0] 

            # If input object is the encryption notification sent at start of whatsapp chats, give it date (1/1/1970).
            elif (input_object == "Messages you send to this group are secured with end-to-end encryption. Click for more info."):
                input_object = "1/1/1970"
            # If input object is the encryption notification sent at start of whatsapp chats, give it date (1/1/1970).
            elif (input_object == "Messages you send to this chat and calls are secured with end-to-end encryption."):
                input_object = "1/1/1970"
            else: # The input_object is not a date.
                input_object = "Not Date"
        return input_object

    def check_if_date_available(self, driver, date, first_date = datetime.datetime(1970,1,1).strftime("%m/%d/%y"),
                               whatsapp_divider_dict = whatsapp_divider_dict):
        """
        Function checks if a given datetime object is available in the current list of whatsapp message divider.
        Used in conjunction with the upward scrolling function.
        Args:
            driver - a WebDriver object, used to interact with the website.
            date - a string object, the date to check if available. format (31/12/2019).
            first_date -  a string object, the minimum date where whatsapp conversations begin.
        Returns:
            result - a string object, with results of whether a given date is available in the current messaging window.
        E.g: available =  check_if_date_available(driver = driver, date='12/9/2019',
                                first_date = datetime.datetime(1970,1,1).strftime("%m/%d/%y"))
        LastMod: Luyanda Dhlamini
        """
        # Get list for days
        day_list = self.get_days_list()
        day_list
        # Find all notifications & divider in current message window
        self.NavInstance.implicit_wait(driver,timeout = 3,class_name = whatsapp_divider_dict["divider_message_class"])
        divider_list = driver.find_elements_by_class_name(whatsapp_divider_dict["divider_message_class"])
        dividers_df = pd.DataFrame(divider_list,columns=['dividers'])

        # Check if divider objects are dates
        dividers_df['text'] = dividers_df.dividers.apply(lambda x : x.text)
        dividers_df['dat'] = dividers_df.dividers.apply(lambda x : self.check_whatsapp_date(x.text,day_list))
        #print(dividers_df)
        dividers_df = dividers_df[dividers_df['dat'] != 'Not Date'] # Filter to only objects that are dates
        dividers_df['dat'] = pd.to_datetime(dividers_df.dat) # Convert date strings to datetimes

        date = pd.Timestamp(date)
        first_date = pd.Timestamp(first_date)
        # If the first date (1/1/1970) is in the date list, we're at the biginning.
        if first_date in list(dividers_df.dat):
            result = "At beginning of history"
        # If dates less than or equal to "date" are present, then our target "date" is now available.
        elif dividers_df[dividers_df['dat'] <= date].shape[0] >= 1:
            result = 'available'
        else: # Else the "date" is not available yet.
            result = 'not available'
        return result

    def scroll_up_messages(self, driver, number_days_to_go_back = 1, scroll_up_count=10,
                                                       whatsapp_divider_dict = whatsapp_divider_dict):
        """
        Function scrolls up to see older messages on Whatsapp.
        It clicks on the messages pane & then uses ActionChains to perform scroll ups.

        Args:
            driver - a WebDriver object, used to interact with the website.
            number_days_to_go_back - a integer object, how many days from today to scroll up to.
            whatsapp_divider_dict - a dictionary object, with the classes used in this function.
        Returns:
            result - a string object, with results of whether the date to scroll to has been found or not.
        E.g: result = scroll_up_messages(self, driver, number_days_to_go_back = 1, scroll_up_count=10,
                                                       whatsapp_divider_dict = read.whatsapp_divider_dict)
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        message = "Scrolling up for {} days.".format(number_days_to_go_back)
        logger.info('{},{}'.format(function_name,message))
        # Find the central message panel & click on it.
        scroller = driver.find_element_by_class_name(whatsapp_divider_dict["message_list_subgroup_class"])
        self.NavInstance.implicit_wait_is_displayed(scroller,wait_type='displayed')
        actions = ActionChains(driver)
        actions.move_to_element(scroller)
        actions.click()
        actions.perform()

        # Use number_days_to_go_back to get the date to target.
        date = datetime.datetime.today()-datetime.timedelta(number_days_to_go_back)
        date = date.strftime("%m/%d/%y")

        # While the date has not been found, keep scrolling up.
        result = self.check_if_date_available(driver = driver,date = date)
        while (result != 'At beginning of history') & (result != 'available'):
            actions = ActionChains(driver)
            for i in range(scroll_up_count):
                actions.send_keys(Keys.UP)
                actions.perform()
            time.sleep(2)
            result = self.check_if_date_available(driver=driver,date=date)
        message = "Scrolling results: {}.".format(result)
        logger.info('{},{}'.format(function_name,message))
        return result

    
    instance_phone_name_dict = {
        "description": """Dictionary contains class names used in the get_instance_phone_name.""",
        "left_header_pane_class":"_3Jvyf", # Left header.
        "left_header_buttons_class":"_3j8Pd", # Header button classes.
        "floating_menu_class": "_2hHc6", # Floating menu class. Only appears if floating menu now visible
        "floating_menu_buttons_class":"_3cfBY", # Floating menu buttons.
        "profile_names_pane_class": "_1KDYa", # Profile pane. Appears once profile button clicked on in floating menu.
        "profile_text_lists_class": "_2LSbZ", # Text groups, with label, name of user & option to edit name.
        "edit_user_name_class": "_30prC", # Edit name button.
        "back_button_class": "qfKkX" # Back button, pressed to close profile menu.
    }
    
    def get_instance_phone_name(self, driver, instance_phone_name_dict = instance_phone_name_dict):
        """
        Function gets the name of the phone's whatsapp account.
        Args:
            driver - a WebDriver object, used to interact with the website.
            instance_phone_name_dict - a dictionary object, with the classes used in this function.
        Returns:
            user_name - a string object, name of the phone's whatsapp account.
        E.g: owner_name = self.get_instance_phone_name(driver)
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        message = "Getting instance phone name."
        logger.info('{},{}'.format(function_name, message))

        left_header = driver.find_element_by_class_name(instance_phone_name_dict["left_header_pane_class"])
        menu_button = left_header.find_elements_by_class_name(instance_phone_name_dict["left_header_buttons_class"])[2]
        menu_button.click()
        floating_menu = self.NavInstance.implicit_wait(driver,timeout=3,
                                               class_name=instance_phone_name_dict["floating_menu_class"])
        # Check if the floating menu is displayed.
        if type(floating_menu) != str:
            profile_button = driver.find_elements_by_class_name(instance_phone_name_dict["floating_menu_buttons_class"])[1]
            self.NavInstance.implicit_wait_is_displayed(profile_button)
            profile_button.click()
            # Click to edit the phone's whatsapp account name. Done so that can read profile.
            profile_names_pane = driver.find_element_by_class_name(instance_phone_name_dict["profile_names_pane_class"])
            profile2 = profile_names_pane.find_elements_by_class_name(instance_phone_name_dict["profile_text_lists_class"])[0]
            edit_user_name = self.NavInstance.implicit_wait(driver,timeout=3,
                                                            class_name=instance_phone_name_dict["edit_user_name_class"])
            self.NavInstance.implicit_wait_is_displayed(edit_user_name)
            edit_user_name.click()
            user_name = profile2.text # Get account name
            user_name = user_name.split("\n")[1]

            back_button = self.NavInstance.implicit_wait(selenium_object=profile_names_pane, timeout = 3,
                                                         class_name=instance_phone_name_dict["back_button_class"])
            back_button.click() # Close profile pane
            message = "Instance phone name: {}.".format(user_name)
        else:
            user_name = "Unknown Onwer. No floating menu."
        logger.info('{},{}'.format(function_name, user_name))
        return user_name

    message_details_dict = {
        "description": """Dictionary used to store classes for fetching message details.""",
        "all_messages_class": "FTBzM", # main class for whatsapp messages
        "whatsapp_message_class": "_2Wx_5", # identifies messages coming from a user

        "chat_audio_class":"uqRgA", # Class name for an audio
        "document_class":"_1BN2j", # document sent in a group chat
        "chat_video_class":"_3Z-uK", # class name for a video
        "chat_picture_class":"_3mdDl", # class name for a picture sent
        "location_class": "_3s-xU", # class name for a location
        'contact_class': "_2kIVZ", # class name for a contact
        "message_text_class" : "_12pGw", # class for whatsapp message
        "notification_object_class": "_1_8_q", # class for whatsapp notification, e.g. users changing their phone numbers
        "encryption_notification_class": "S-bQb", # class for whatsapp encryption, sent at start of whatsapp convo
        "date_divider_class1": "_1zGQT", # class for message object
        "date_divider_class2": "a7otO", # class for message object
        "date_divider_class3": "tail", # class for message object, used to identify date dividers. Not in date divider

        "message_time_class": "_3fnHB", # Class for finding whatsapp time
        "copyable_text_class": "copyable-text", # Class for finding text in some whatsapp messages
        "message_text_attribute": "data-pre-plain-text", # Class for finding text in some whatsapp messages

        # Used in the get_message_from_to_context function
        "message_pane_header":"_3fs0K", # Main header, visible when a contact is clicked on
        "header_account_name_text": "_19vo_", # Name of contact clicked on (context)
        "existing_contact_class": "_1uQFN", # class finds message sender names in group
        "message_text_group_class": "-N6Gq", # class finds message details (name, time, date) in some messages
        "group_contact_class": "_1QjgA", # class finds names in groups
        "unsaved_contact_name_class": "ZObjg", # Used to find unsaved names 
        "read_status_class": "_370iZ" # Class finds read status in owner generated messages.
    }
    
    def get_messages(self,driver, is_whatsapp_group_dict=is_whatsapp_group_dict, message_details_dict=message_details_dict):
        """
        Function finds & returns message objects in a whatsapp chat as a pd.DataFrame object.
        Args:
            driver - a WebDriver object, used to interact with the website.
            is_whatsapp_group_dict - a dictionary object, contains classes used to determine if in whatsapp group.
            message_details_dict - a dictionary object, contains classes used to get message details.
        Returns
            message_objects_df - a pd.DataFrame object, list of message objects in a dataframe.
            result - a string object, if search for messages fails, communicates reason.
        E.g: messages_df =  read.get_messages(driver)
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        message = "Getting messages."
        logger.info('{},{}'.format(function_name, message))

        if (self.NavInstance.check_element_exists(driver,is_whatsapp_group_dict["contact_messages_class"]) == False):
            result = "No contact clicked on"
        else:
            try:
                message_objects = driver.find_elements_by_class_name(self.message_details_dict["all_messages_class"])
                message_objects_df = pd.DataFrame(message_objects,columns=['message_element'])
                result = "Messages found"
            except NoSuchElementException:
                result = "NoSuchElementException: No messages found"
            except StaleElementReferenceException:
                result =  "StaleElementReferenceException: Try clicking on contact again"

        if result =="Messages found":
            message = "{} {}".format(message_objects_df.shape[0], result)
            logger.info('{},{}'.format(function_name, message))
            return message_objects_df
        else:
            logger.info('{},{}'.format(function_name, result))
            return result
    
    def get_message_time(self, message_object, message_type, message_details_dict = message_details_dict):
        """
        Function gets the time that a whatsapp message was sent on.
        Args:
            message_object - a selenium WebElement object, contains message information.
            message_type - a string object, describes the type of message.
            message_details_dict - a dictionary object, contains classes used to get message details.
        Returns:
            time - a string object, time a message was sent or 12 am.
        E.g: time = self.get_message_time(message_object = driver.find_element_by_class_name("_2Wx_5"), message_type = "Image")
        LastMod: Luyanda Dhlamini
        """
        # Assumes objects in below list will always have a time attached to them.
        if message_type in self.MESSAGE_OBJECT_LIST:
            time = message_object.find_element_by_class_name(message_details_dict["message_time_class"]).text
        else:
            time = "00:00 AM"
        return time

    def get_message_type_and_text(self, message_object_df, message_details_dict = message_details_dict):
        """
        Function gets the message type and text on a whatsapp message object.
        Args:
            message_object_df - a pd.DataFrame object, list of message objects in a dataframe.
            message_details_dict - a dictionary object, contains classes used to get message details.
        Returns:
            message - a string object, text on a message.
            message_type_list - a list object, strings with message type
            message_text_list - a list object, strings with message type
        E.g: time = self.get_message_type_and_text(message_object_df = driver.find_elements_by_class_name("_2Wx_5"))
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        message = "Getting message type and text."
        logger.info('{},{}'.format(function_name, message))
        
        message_object_df = message_object_df.copy()
        message_type_list = []
        message_text_list = []

        # For each object, loop through it, get its type & then its message.
        for i in message_object_df.index:
            message_object = message_object_df.at[i,'message_element']
            if(self.NavInstance.check_element_exists(message_object,message_details_dict['chat_audio_class'])):
                message_type="Audio"
            elif(self.NavInstance.check_element_exists(message_object,message_details_dict['document_class'])):
                message_type="Document"
            elif(self.NavInstance.check_element_exists(message_object,message_details_dict['chat_video_class'])):
                message_type="Video"
            elif(self.NavInstance.check_element_exists(message_object,message_details_dict['chat_picture_class'])):
                message_type="Image"
            elif(self.NavInstance.check_element_exists(message_object,message_details_dict['contact_class'])):
                message_type="Contact"
            elif(self.NavInstance.check_element_exists(message_object,message_details_dict['location_class'])):
                message_type="Location"
            elif(self.NavInstance.check_element_exists(message_object,message_details_dict['message_text_class'])):
                message_type = "Text Message"
            elif(self.NavInstance.check_element_exists(message_object,message_details_dict["notification_object_class"])):
                message_type = "Notification"
                if self.NavInstance.check_element_exists(message_object, message_details_dict["copyable_text_class"]):
                    message=message_object.find_element_by_class_name(name=message_details_dict["copyable_text_class"]).text
                else:
                    message=""
            elif(self.NavInstance.check_element_exists(message_object,message_details_dict["encryption_notification_class"])):
                message_type = "Encryption Notification"
                if self.NavInstance.check_element_exists(message_object,message_details_dict["whatsapp_message_class"]):
                    message=message_object.find_element_by_class_name(message_details_dict["whatsapp_message_class"]).text
                else:
                    message=""
            elif (self.NavInstance.check_element_exists(message_object,
                       message_details_dict["date_divider_class1"]) & self.NavInstance.check_element_exists(message_object,
                       message_details_dict["date_divider_class2"]) & self.NavInstance.check_element_exists(message_object,
                       message_details_dict["date_divider_class3"]) == False):
                message_type = "Date Divider"
                if self.NavInstance.check_element_exists(message_object,message_details_dict["date_divider_class1"]):
                    message = message_object.find_element_by_class_name(name=message_details_dict["date_divider_class1"]).text
                else:
                    message = ""
            else:
                message_type = "Unknown Type"
                message = ""

            if message_type in self.MESSAGE_OBJECT_LIST: # Normal messages
                if self.NavInstance.check_element_exists(message_object, class_name = message_details_dict['message_text_class']):
                    message = message_object.find_element_by_class_name(message_details_dict['message_text_class']).text
                else:
                    message = ""
            message_type_list.append(message_type)
            message_text_list.append(message)

        message = "Fetched {} message types & {} message texts.".format(len(message_type_list),len(message_text_list))
        logger.info('{},{}'.format(function_name, message))
        return message_type_list, message_text_list

    def get_message_date(self, message_object_df, day_to_go_back=150):
        """
        Function assigns a date to when a message was sent.
        Uses Date Divider objects to determine breaks of dates.
        Args:
            message_object_df - a pd.DataFrame object, with message details
            day_to_go_back - an integer object, the number of days to go back in history & match for.
        Returns:
            date_list - a list object, list of days messages were sent on or strings explaining that send date unknown.
        E.g: time = self.get_message_date(message_object_df = 
                pd.DataFrame({'message_element':driver.find_elements_by_class_name("_2Wx_5"),'message_type':'Date Divider',
                'message_text': "TODAY"}),day_to_go_back=20)
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        day_list = self.get_days_list(day_to_go_back=day_to_go_back) # Get list of dates. Go back 5 months to cover most hist.
        # Convert days to whatsapp date format.
        day_list['date_list'] = day_list.date_list.apply(lambda x: "{}/{}/{}".format(round(x.month),round(x.day),round(x.year)))
        date_list = []
        latest_dates = "-"

        for index in message_object_df.index:
            message_type = message_object_df.at[index,'message_type']
            if message_type == 'Date Divider':
                message_text = message_object_df.at[index,'message_text']
                # Date is string (e.g Today).
                if message_text in list(day_list.day_name):
                    day_index = list(day_list.day_name).index(message_text)
                    latest_dates = day_list.at[day_index,'date_list']
                    date_list.append(latest_dates)
                # Date is date (e.g 10/26/2019).
                elif message_text in list(day_list.date_list):
                    day_index = list(day_list.date_list).index(message_text)
                    latest_dates = day_list.at[day_index,'date_list']
                    date_list.append(latest_dates)
                else: # Empty date divider object
                    date_list.append("Date not in date list")
            else:
                date_list.append(latest_dates)

        message = "Fetched {} message dates.".format(len(date_list))
        logger.info('{},{}'.format(function_name, message))
        return date_list

    def strip_message_name(self, message_object, message_details_dict=message_details_dict):
        """
        Function gets the name in a message object.
        Args:
            message_object - a selenium WebElement object, contains message information.
            message_details_dict - a dictionary object, contains classes used to get message details.
        Returns:
            sender - the name/ phone number of the person who sent the message.
        E.g: sender = read.strip_message_name(message_object)
        LastMod: Luyanda Dhlamini
        """
        details_group = message_object.find_element_by_class_name(message_details_dict["whatsapp_message_class"])
        details_tag_class = message_object.find_element_by_class_name(message_details_dict['copyable_text_class'])
        details_tag = details_tag_class.get_attribute(name=message_details_dict["message_text_attribute"])
        part_lists = details_tag.split("] ")
        sender = part_lists[1].split(":")[0]
        return sender

    def get_message_from_to_context(self, driver, message_object_df, message_details_dict=message_details_dict):
        """
        Function fetches details about who the message is from, who its to & the context [the contact name we're in].
        Args:
            message_object_df - a pd.DataFrame object, with message details
            message_details_dict - a dictionary object, contains classes used to get message details.
        Returns:
            context_list - a list object, list of the contact that we're in.
            sender_name_list - a list object, list of message senders.
            to_name_list - a list object, list of message recipients.
        E.g: context, from, to = get_message_from_to_context(message_object_df)
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        #driver.maximize_window() # Investigate this line. May cause crash if window already maximised.
        message_object_df = message_object_df.copy()
        context_list = []
        sender_name_list = []
        to_name_list = []

        message = "Getting message context, from and to."
        logger.info('{},{}'.format(function_name, message))
        # Check if in group.
        IN_WHATSAPP_GROUP = self.is_whatsapp_group(driver)
        # get sender name.
        #instance_phone_name = self.get_instance_phone_name(driver)
        instance_phone_name = 'instance 1'
        # If not, get sender name.
        #if IN_WHATSAPP_GROUP == False:
        header = driver.find_element_by_class_name("_3fs0K")
        receipient_name = header.find_element_by_class_name("_19vo_").text

        for i in message_object_df.index:
            message_object = message_object_df.at[i,'message_element']
            message_type = message_object_df.at[i,'message_type']
            state = message_type in self.MESSAGE_OBJECT_LIST
            if (state == True):
                if (IN_WHATSAPP_GROUP == True):
                    if self.NavInstance.check_element_exists(message_object,message_details_dict["existing_contact_class"]):
                        # Find contact names in groups
                        from_name = message_object.find_element_by_class_name(message_details_dict["existing_contact_class"]).text
                        to_name = receipient_name
                    elif self.NavInstance.check_element_exists(message_object,message_details_dict["message_text_group_class"]):
                        # when back to back texts sent by same person.
                        from_name = self.strip_message_name(message_object)
                        to_name = receipient_name
                    elif self.NavInstance.check_element_exists(message_object,message_details_dict["read_status_class"]):
                        # Get instance owner name in groups
                        from_name = instance_phone_name
                        to_name = receipient_name
                    elif self.NavInstance.check_element_exists(message_object,message_details_dict["group_contact_class"]):
                        # Get instance owner name in groups
                        from_name = message_object.find_element_by_class_name(message_details_dict["unsaved_contact_name_class"]).text
                        to_name = receipient_name
                    else:
                        from_name = "Name unknown"
                        to_name = receipient_name

                elif (IN_WHATSAPP_GROUP==False):
                    if (self.NavInstance.check_element_exists(message_object,"_370iZ") == False):
                        from_name = receipient_name
                        to_name = instance_phone_name
                    else:
                        from_name = instance_phone_name
                        to_name = receipient_name                    
                else:
                    from_name = "Name unknown"
                    to_name = receipient_name
            else:
                from_name = "Whatsapp"
                to_name = receipient_name
            
            context_list.append(receipient_name)
            sender_name_list.append(from_name)
            to_name_list.append(to_name)
            message = "{} message contexts, from & to details fetched.".format(len(sender_name_list))
            logger.info('{},{}'.format(function_name, message))
        return context_list, sender_name_list, to_name_list
    
    def add_new_messages_to_db(self, message_df, instance_id = 1):
        """
        Function adds new messages to the database. Assumes an existing connection is available.
        Args:
            message_df - a pd.DataFrame, messages that have been read.
            instance_id - a integer object, contains the id of the phone being used.
        Returns:
            no_duplicates - a pd.DataFrame, new messages that have been added to the database.
        # Potential future improvement: Take in connection as argument.
        """
        function_name = sys._getframe().f_code.co_name
        message = "Adding new messages to DB."
        logger.info('{},{}'.format(function_name, message))
        min_date = message_df.date.min()  # Get the earliest date in the incoming messages dataframe.

        # script used to fetch messages for an instance that meets the date criteria.
        message_script = """
        SELECT * FROM messages_table mt
        WHERE mt.instance_id = {}
        and mt.date >= '{}';""".format(instance_id,min_date)
        
        db_messages = pd.read_sql(message_script,conn) # read existing messages from database
        db_messages['date'] = pd.to_datetime(db_messages['date'])
        # Add existing db messages to messages that have just been read.
        appended_df = db_messages.append(message_df,ignore_index=True) 

        # Drop duplicates & ensure that only messages not in database remain.
        no_duplicates = appended_df.drop_duplicates()
        no_duplicates = no_duplicates.append(db_messages,ignore_index = True)
        no_duplicates = no_duplicates.drop_duplicates(keep=False)
        
        if no_duplicates.shape[0] >=1: # If any messages left, add them to the database.
            no_duplicates.to_sql("messages_table",conn,if_exists='append',index=False)
            message = "{} new messages added to database.".format(no_duplicates.shape[0])
            logger.info('{},{}'.format(function_name, message))
        else:
            message = "No new messages found."
            logger.info('{},{}'.format(function_name, message))        
        return no_duplicates


# In[ ]:





# In[12]:


class Functions(object):
    # Functions in this class combine other low level functions to perform complex tasks.
    
    def wrapper_send_media_messages(self, params_dict, event_dict):
        """
        Function puts together other underlying functions that allow you to send media messages to a contact or group.
        Media messages include items like images, videos & audio files.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, 
        Navigate, Writer & Read class objects.
        
        Args:
            params_dict - a dictionary object, that contains all of the objects needed to send a message.
            event_dict - a dictionary object, contails information on the message to be sent.        Returns:

        E.g: wrapper_send_media_messages(
            params_dict = {'driver' : driver, 'navigate_object': nav,'write_object': write,'read_object': read},
            event_dict = {'event_id': 1, 'instance_id': 1, 'event_date': 0, 'event_time': '01:00',
            'event_key': '4 - backup messages', 'function_id': 'wrapper_read_text_messages',
            'attachment_link': r'C:\\Users\\ludhl\\Desktop\AutoIT\\image1.jpg', 'attachment_type_id': '',
            'attachment_message': 'Please find a picture attached', 'target_user_id': 5, 'day_number': -2000, 'activity_date': Timestamp('1970-01-01 00:00:00'), 
            'execution_date': datetime.date(2019, 10, 12), 'executed': 0,
            'contact_names': ['WLS Team']}
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        driver = params_dict['driver']
        navigate_object = params_dict['navigate_object']
        write_object = params_dict['write_object']
        read_object = params_dict['read_object']

        contact_names = event_dict['contact_names']
        attachment_link = event_dict['attachment_link']
        attachment_caption = event_dict['attachment_message']
        target_user_id = event_dict['target_user_id']

        message = "Sending messages to user id: {}.".format(target_user_id)
        logger.info("{},{}".format(function_name, message))

        # Store contact names in a Series, so that can be checked for duplicity later.
        contact_names = pd.Series(contact_names)

        # Check if the file exists. If it does, continue

    #     p = pathlib.Path()
        attachment_path = pathlib.Path(attachment_link)
        print(attachment_path)
        if attachment_path.exists() == True:

            for contact_name in contact_names.values:
                try:
                    try_count = 2
                    search_result = navigate_object.find_contact(driver = driver,contact_name=contact_name)
                    while (search_result != 'Clicked on target element') & (try_count>0):
                        search_result = navigate_object.find_contact(driver = driver, contact_name=contact_name)
                        try_count-=1

                    if search_result == 'Clicked on target element':
                        message = write_object.send_attachment(driver = driver,
                            attach_executable_path = write_object.attach_executable_path,
                            attachment_link = attachment_link,
                            attachment_caption = attachment_caption)
                        #print("send result:",message)
                        message = "Sent media message to {}.".format(contact_name)
                        print(message)
                        logger.info('{},{}'.format(function_name, message))

                    else:
                        # Contact not found. Create an empty dataframe.
                        message = "No media message sent to {}. Contact not found.".format(contact_name)
                        print(message)
                        logger.info('{},{}'.format(function_name, message))       


                except StaleElementReferenceException as e:
                    logger.info('{},{}'.format(function_name, e))
                except NoSuchElementException as e:
                    logger.info('{},{}'.format(function_name, e))
                except ElementClickInterceptedException as e:
                    logger.info('{},{}'.format(function_name, e))
        else:
            message = "File path {} does not exist. Media messages not sent.".format(attachment_path)
            print(message)
            logger.info('{},{}'.format(function_name, message))       

        return message
    
    def wrapper_read_text_messages(self, params_dict, event_dict, number_days_to_go_back = 0, try_count = 1):
        """
        Function puts together other underlying functions that allow you to read & backup messages from whatsapp to our database.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, 
        Navigate, Writer & Read class objects.
        The messages to store to database are given in as input. How many days to read are also given as input.
        It also uses a event_dict, a dictionary with information on the contacts to read messages from..
        Args:
            params_dict - a dictionary object, that contains all of the objects needed to send a message.
            event_dict - a dictionary object, contails information on the message to be sent.
            number_days_to_go_back - a integer object, how many days of message history to read.
            try_count - a integer object, how many times to attempt to find a contact.
        Returns:

        E.g: wrapper_read_text_messages(
            params_dict = {'driver' : driver, 'navigate_object': nav,'write_object': write,'read_object': read},
            event_dict = {'event_id': 1, 'instance_id': 1, 'event_date': 5, 'event_time': '01:00',
            'event_key': '4 - backup messages', 'function_id': 'wrapper_read_text_messages',
            'attachment_link': '', 'attachment_type_id': '', 'attachment_message': '',
            'target_user_id': 8, 'day_number': -2000, 'activity_date': Timestamp('1970-01-01 00:00:00'), 
            'execution_date': datetime.date(2019, 10, 12), 'executed': 0,
            'contact_names': ['Weight Loss School - 110108','WLS Team']}
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        start_time = time.monotonic()
        driver = params_dict['driver']
        navigate_object = params_dict['navigate_object']
        write_object = params_dict['write_object']
        read_object = params_dict['read_object']

        # create a master dataframe.
        columns_list = ['instance_id','date','context','from','to','message_number','message_type','message_time','message_text']
        master_df = pd.DataFrame(columns=columns_list)
        contact_names = event_dict['contact_names']
        target_user_id = event_dict['target_user_id']

        message = "{},Reading messages for user id: {}".format(function_name, target_user_id)
        logger.info(message)
        
        default_try_count = try_count
        # Store contact names in a Series, so that can be checked for duplicity later.
        contact_names = pd.Series(contact_names)

        results_dict = {} # Dictionary stores the results of sending messages to contacts.
        for contact_name in contact_names.values:
            try:
                message = "Reading messages for user {}.".format(contact_name )
                # print(message)
                logger.info("{},{}".format(function_name,message))
                search_result = navigate_object.find_contact(driver =driver,contact_name=contact_name)
                try_count = default_try_count
                message = "Search result: {}.".format(search_result)
                logger.info("{},{}".format(function_name,message))
                while (search_result != 'Clicked on target element') & (try_count>0):
                    try_count-=1
                    search_result = navigate_object.find_contact(driver =driver,contact_name=contact_name)
                    message = "Search result: {}. Try count: {}.".format(search_result, try_count)
                    logger.info("{},{}".format(function_name,message))

                if search_result == 'Clicked on target element':
                    # print(search_result)
                    date_df = read_object.get_days_list(number_days_to_go_back)
                    read_object.scroll_up_messages(driver,number_days_to_go_back=number_days_to_go_back)
                    
                    message_df = pd.DataFrame(columns = ['message_element'])
                    message_df = read_object.get_messages(driver)

                    if type(message_df) != str:
                        message_df['message_type'], message_df['message_text'] = read_object.get_message_type_and_text(message_df)

                        message_df['context'], message_df['from'],message_df['to'] = read_object.get_message_from_to_context(driver,message_df)

                        message_df['message_time'] = message_df.apply(lambda x: read_object.get_message_time(x['message_element'],
                                                                                                     x['message_type']),axis=1)
                        message_df['date'] = read_object.get_message_date(message_df)
                        
                    date_df['whatsapp_date'] = date_df.date_list.apply(lambda x: "{}/{}/{}".format(round(x.month),
                                                                                                   round(x.day),round(x.year)))
                    usuku = date_df.at[number_days_to_go_back,'whatsapp_date']

                    message_df = message_df[message_df['date'] != 'Date not in date list'].copy()
                    message_df['date'] = pd.to_datetime(message_df.date)
                    usuku_date = pd.to_datetime(usuku)
                    message_df =  message_df[message_df['date'] >= usuku_date]

                    columns_list = ['instance_id','date','context','from','to','message_number',
                                                        'message_type','message_time','message_text']
                    message_df.reset_index(drop=True,inplace=True)
                    message_df['message_number'] = message_df.index
                    message_df['instance_id'] = event_dict['instance_id']
                    message_df = message_df[columns_list]

                    message = "{} messages read for {}.".format(message_df.shape[0], contact_name)
                    
                    logger.info('{},{}'.format(function_name, message))       
                else:
                    # Contact not found. Create an empty dataframe.
                    message_df = pd.DataFrame(columns=columns_list)
                    message = "No messages read for {}. Contact not found.".format(contact_name)
                    logger.info('{},{}'.format(function_name, message))       


            except StaleElementReferenceException as e:
                logger.info('{},{}'.format(function_name, e))
            except NoSuchElementException as e:
                logger.info('{},{}'.format(function_name, e))
            except ElementClickInterceptedException as e:
                logger.info('{},{}'.format(function_name, e))

            if message_df.shape[0] > 0:
                master_df = master_df.append(message_df, ignore_index=True)
        result = read_object.add_new_messages_to_db(master_df)
        duration = round(time.monotonic() - start_time,2)
        logger.info('{},{}'.format(function_name, "Time taken to run backups {}".format(str(duration))))
        return result
    
    def wrapper_send_text_message(self, params_dict, event_dict):
        """
        Function puts together other underlying functions that allow you to send a basic text message.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, Navigate & Writer class objects.
        It also uses a event_dict, a dictionary with information on the message to be sent & the people to send messages to.
        Args:
            params_dict - a dictionary object, that contains all of the objects needed to send a message.
            event_dict - a dictionary object, contails information on the message to be sent.

        E.g: 
        wrapper_send_text_message(
                params_dict = {'driver' : driver, 'navigate_object': nav,'write_object': write},
                event_dict = {'event_id': 111, 'instance_id': 1, 'event_date': 5, 'event_time': '11:30',
                'event_key': '3 - test event', 'function_id': 'wrapper_send_text_message',
                'attachment_link': '', 'attachment_type_id': '1 - text message',
                'attachment_message': 'This is a test. You are the guinee pig',
                'target_user_id': 6, 'day_number': -2000, 'activity_date': Timestamp('1970-01-01 00:00:00'), 
                'execution_date': datetime.date(2019, 10, 12), 'executed': 0, 'contact_names': ['Luyanda Dhlamini - 110101']})

        LastMod: Luyanda Dhlamini
        """
        # Must have option to use nicknames.
        function_name = sys._getframe().f_code.co_name

        driver = params_dict['driver']
        navigate_object = params_dict['navigate_object']
        write_object = params_dict['write_object']

        message_details = event_dict['attachment_message']
        contact_names = event_dict['contact_names']
        target_user_id = event_dict['target_user_id']

        message = "{},Sending to user id: {}".format(function_name, target_user_id)
        logger.info(message)

        # Store contact names in a Series, so that can be checked for duplicity later.
        contact_names = pd.Series(contact_names)

        input_text = message_details
        message = "{},Sending message: '{}'".format(function_name, input_text)
        logger.info(message)


        results_dict = {} # Dictionary stores the results of sending messages to contacts.
        for contact_name in contact_names.values:
            try:
                input_text = message_details
                message = "{},Sending message to contact: '{}'".format(function_name, contact_name)
                logger.info(message)

                result = navigate_object.enter_text_in_searchbox(driver, contact_name)

                displayed_item = navigate_object.fetch_displayed_items(driver)

                contacts = navigate_object.check_if_contact(element_list=displayed_item)

                target_contact = navigate_object.find_target_element(contacts, contact_name)

                if len(target_contact) == 0:
                    message = "{} not in contact list".format(contact_name)
                    results_dict[contact_name] = message                    
                    message = "{},{}".format(function_name, message)
                    logger.warning(message)

                else:
                    # function assumes there will always be one exact match returned from find target element.
                    # What this means is that we assume that find_target_element will only find one match for contact_name.
                    result = navigate_object.click_on_element(target_contact[0])

                    first_name = contact_name.split(" ")[0]

                    input_text = input_text.format(first_name)
                    message = "{},Sending input text: '{}'".format(function_name, input_text)
                    #print(input_text)
                    logger.info(message)

                    send_message = write_object.send_text_message(driver, input_text)
                    results_dict[contact_name] = send_message

            except NoSuchElementException:
                # Logic, if run fails, append to list & try again.
                # Change wanted: treat user names as Series
                # If has tried twice & still fails, skip

                if contact_names.value_counts()[contact_name] == 2:
                    # Log that has tried twice.
                    message = "Function has attempted send message & failed twice for {}".format(contact_name)
                else:
                    message = "Function has added {} to list to try sending again".format(contact_name)
                    contact_names.append(pd.Series(contact_name),ignore_index=True)
                logger.warning(message)
        message = "Operated on following contacts:\n" + contact_names.to_string()
        logger.info("{},{}".format(function_name,message))
        
    def wrapper_create_group(self, params_dict, event_dict):
        """
        Function creates a whatsapp group.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, Navigate & Writer class objects.
        It uses a event_dict, a dictionary with information on the message to be sent & the people to send messages to.
        It contains a get_user_class_name function for fetching the name to use as the whatsapp group's name.
        Args:
            params_dict - a dictionary object, that contains all of the objects needed to send a message.
            event_dict - a dictionary object, contails information on the message to be sent.
        Returns:
            message - a string object, the result of running the function.
        E.g: 
        wrapper_send_text_message(
                params_dict = {'driver' : driver, 'navigate_object': nav,'write_object': write},
                event_dict = {'event_id': 111, 'instance_id': 1, 'event_date': 5, 'event_time': '11:30',
                'event_key': '3 - test event', 'function_id': 'wrapper_send_text_message',
                'attachment_link': '', 'attachment_type_id': '1 - text message',
                'attachment_message': 'This is a test. You are the guinee pig',
                'target_user_id': 8, 'day_number': -2000, 'activity_date': Timestamp('1970-01-01 00:00:00'), 
                'execution_date': datetime.date(2019, 10, 12), 'executed': 0, 'contact_names': ['Luyanda Dhlamini - 110101']})
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        driver = params_dict['driver']
        navigate_object = params_dict['navigate_object']
        write_object = params_dict['write_object']
        read_object = params_dict['read_object']

        contact_names = event_dict['contact_names']
        target_user_id = event_dict['target_user_id']

        message = "Creating group for user_id: {}.".format(target_user_id)
        logger.info("{},{}".format(function_name, message))

        def get_user_class_name(user_id, user_table):
            """
            Function uses a user id to find their class_name.
            This is done by finding the user's class_id & then using it to join to the class stable to find the class name.
            # Script assumes that user is part of a class
            Args:
                user_id - a string object, the user whose class name we wish to get.
                user_table - a string object, the table to locate the user in
            Returns:
                class_name - a string object, the name of the class that the user belongs to.
            E.g class_name = get_user_class_name(user_id = "Luyanda Dhlamini - 110101", user_table = "employee")
            LastMod: Luyanda Dhlamini
            """
            try:
                function_name = sys._getframe().f_code.co_name
                message = 'Fetching class name for user: {}'.format(user_id)
                logger.info('{},{}'.format(function_name, message))

                script = """SELECT t.class_id, c.class_name from {user_table}_table t
                JOIN class_table c
                ON t.class_id = c.class_id
                where t.{user_table}_id = '{user_id}'""".format(user_id = user_id, user_table = user_table)

                result = pd.read_sql(script,conn)
                result = result.class_name.values[0]
                message = "Returned group_name: {}".format(result) # Temp
                logger.info('{},{}'.format(function_name, message))
            except IndexError as e:
                result = "Error"
                logger.info('{},{}'.format(function_name, e))
            return result


        first_countact = contact_names.values[0]
#         print(first_countact) # Temp
        contact_location = "customer"
        group_name = get_user_class_name(user_id=first_countact, user_table=contact_location)

        if group_name != "Error": # If group_name has been found, create the group using the class name.
            message = navigate_object.create_whatsapp_group(driver,group_name = group_name, contact_names = contact_names)
#             print(message)
        else:
            message = "{}'s group name not found. Not creating group".format(first_countact)
            logger.info('{},{}'.format(function_name, message))
#             print(message)
        return message

    def wrapper_add_person_to_group(self, params_dict, event_dict):
        """
        Function adds participants to a whatsapp group.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, Navigate & Writer class objects.
        It uses a event_dict, a dictionary with information on the message to be sent & the people to send messages to.
        Args:
            params_dict - a dictionary object, that contains all of the objects needed to send a message.
            event_dict - a dictionary object, contails information on the message to be sent.
        Returns:
            message - a string object, the result of running the function.
        E.g: 
        wrapper_send_text_message(
                params_dict = {'driver' : driver, 'navigate_object': nav,'write_object': write},
                event_dict = {'event_id': 111, 'instance_id': 1, 'event_date': 5, 'event_time': '11:30',
                'event_key': '3 - test event', 'function_id': 'wrapper_send_text_message',
                'attachment_link': '', 'attachment_type_id': '1 - text message',
                'attachment_message': 'WLS Team,
                'target_user_id': 8, 'day_number': -2000, 'activity_date': Timestamp('1970-01-01 00:00:00'), 
                'execution_date': datetime.date(2019, 10, 12), 'executed': 0, 'contact_names': ['Luyanda Dhlamini - 110101']})
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        driver = params_dict['driver']
        navigate_object = params_dict['navigate_object']
        write_object = params_dict['write_object']
        read_object = params_dict['read_object']

        contact_names = event_dict['contact_names']
        target_user_id = event_dict['target_user_id']

        message = "Adding participants for user_id: {}.".format(target_user_id)
        logger.info("{},{}".format(function_name, message))
        group_name = event_dict['attachment_message'] # The name of the group to add participants to is the event message text
        # Run navigate function below to add person to group.
        message = navigate_object.add_person_to_group(driver,group_name = group_name, contact_names = contact_names)
        logger.info('{},{}'.format(function_name, message))

        return message
    
    def wrapper_add_group_admin(self, params_dict, event_dict):
        """
        Function makes a participant a whatsapp group admin.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, Navigate & Writer class objects.
        It uses a event_dict, a dictionary with information on the message to be sent & the people to send messages to.
        Args:
            params_dict - a dictionary object, that contains all of the objects needed to send a message.
            event_dict - a dictionary object, contails information on the message to be sent.
        Returns:
            message - a string object, the result of running the function.
        E.g: 
        wrapper_send_text_message(
                params_dict = {'driver' : driver, 'navigate_object': nav,'write_object': write},
                event_dict = {'event_id': 111, 'instance_id': 1, 'event_date': 5, 'event_time': '11:30',
                'event_key': '3 - test event', 'function_id': 'wrapper_send_text_message',
                'attachment_link': '', 'attachment_type_id': '1 - text message',
                'attachment_message': 'WLS Team,
                'target_user_id': 8, 'day_number': -2000, 'activity_date': Timestamp('1970-01-01 00:00:00'), 
                'execution_date': datetime.date(2019, 10, 12), 'executed': 0, 'contact_names': ['Luyanda Dhlamini - 110101']})
        LastMod: Luyanda Dhlamini
        """
        function_name = sys._getframe().f_code.co_name
        driver = params_dict['driver']
        navigate_object = params_dict['navigate_object']
        write_object = params_dict['write_object']
        read_object = params_dict['read_object']

        contact_names = event_dict['contact_names']
        target_user_id = event_dict['target_user_id']

        message = "Adding participants for user_id: {}.".format(target_user_id)
        logger.info("{},{}".format(function_name, message))
        group_name = event_dict['attachment_message'] # The name of the group to add participants to is the event message text

        # Run navigate function below to add person to group.
        message = navigate_object.add_admin(driver,group_name = group_name, contact_names = contact_names)
        logger.info('{},{}'.format(function_name, message))

        return message


