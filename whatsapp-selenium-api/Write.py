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
    
    click_attach_dict = {
        "description" : """Dictionary used to store classes that allow you to click on the attach button in the main-pane""",
        'menu_group_class' : "",
            # the 'in-contact' menu class on top of messaging pane when contact clicked on                             
        'menu_subgroup_class' : "",
            # contains the 3 buttons in the menu
        'attach_button_class' : "",
            # the menu buttons class, is list with 3 elements
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
    
    attachment_dict = {
        "description" : """Dictionary used to store classes that allow you to add a caption to a attachment post""",
        "main_class_grouping" : "",
            # the main class in the popup attachment menu
        #"caption_existing_text" : "_7HWvs",   
        "caption_text_class" : ""
            # the class name of the text field
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
    
    send_attachment_dict = {
        "description" : """Dictionary used to store classes that allow you to click on the send attachment button""",
        "main_class_grouping" : "",
            # the class highlighting the entire attachment pane
        "attachment_button" : ""
            # the attachment button class
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
    
    text_message_dict = {
        "description" : """Dictionary used to store classes that allow you to send a text message.""",
        'message_displayed_class': "",
            # Class for the message box, including send & emoji button 
        'message_write_class' : "",
            # Class for entering text, marked as being called copyable-text
        'send_button_class' : ''
            # Button class, only appears once text box has been populated.
    }

    def send_text_message(self, driver, text_message, text_message_dict = text_message_dict):
        """
        Functions sends a text message.

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
    
    attach_file_dict ={ 
        "description" : """Dictionary stores classes that allow you to click on the gallery icon & attach a file""",
        # Class to check if message box open must be here.
        'float_menu_class' : "",
            # Class is the main class of the attach file list of buttons
        "float_menu_list_class" : "",
            # Class is the list class of the attach file list of buttons
        "float_menu_buttons" : ""
            # Class name of buttons in menu list
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
