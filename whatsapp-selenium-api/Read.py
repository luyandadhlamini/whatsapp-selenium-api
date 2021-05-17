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
    
    is_whatsapp_group_dict = {
        "description" : """Used to check is a contact is a whatsapp group.
        Assumes you've already clicked on the contact & in the message pane""",
        "contact_messages_class":"",
            # visible if a contact as been clicked on.identifies the main contact messages pane. 
        "group_participants_list_class": "",
            # available in Whatsapp groups. Below the group's name.
        "message_pane_header_class": "",
            # Class in the main message pain, with group name & buttons.
        "message_pane_buttons_class": "",
            # Class for buttons in headers
        "floating_menu_class": "",
            # Class for the floating buttons list that appears when you click on menu.
        "contact_info_button": ""
            # class for buttons in floating menu.
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
    
    whatsapp_divider_dict = {
        "description": """dictionary stores classes used to interact with whatsapp date divider objects and 
        scroll up whatsapp messages.""",
        "divider_message_class": "",
            # class in message objects that have date information. E.g: 'TODAY'
        "message_list_subgroup_class": "",
            # Identifies messages sub_pane
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
    
    instance_phone_name_dict = {
        "description": """Dictionary contains class names used in the get_instance_phone_name.""",
        "left_header_pane_class": "",
            # Left header.
        "left_header_buttons_class": "",
            # Header button classes.
        "floating_menu_class": "",
            # Floating menu class. Only appears if floating menu now visible
        "floating_menu_buttons_class": "",
            # Floating menu buttons.
        "profile_names_pane_class": "",
            # Profile pane. Appears once profile button clicked on in floating menu.
        "profile_text_lists_class": "",
            # Text groups, with label, name of user & option to edit name.
        "edit_user_name_class": "",
            # Edit name button.
        "back_button_class": ""
            # Back button, pressed to close profile menu.
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