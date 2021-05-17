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