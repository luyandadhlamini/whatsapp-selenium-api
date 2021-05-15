# whatsapp-selenium-api

### A pythonic implementation of common Whatsapp Web functionality using Selenium Webdriver.
This code was written as a personal challenge to see if it was possible to use Selenium to automate basic functionality on Whatsapp Web. 

It is being shared as a learning resource to show others what is possible with Selenium. It is not in anyway meant to be used in ways that infringe on Whatsapp's terms of service (https://www.whatsapp.com/legal/updates/terms-of-service).

I learnt a great deal about software development, debugging & code maintenance while writing this code. Special thanks to the following people for their contributions to this code base: Nokwazi, Sinenhlanhla, Thandaza, Londiwe & Anele.

I do not intend to maintain this code.

### Available Functionality

Navigation Aids:
check_if_whatsapp_locked:
        Function checks if whatsapp is locked (if the QR code is displayed).
        Checks against 3 conditions 1. The locked screen text is visible.
        2. A unlocked screen object is available.
        3. None of the above because an error is encountered.
        Function uses an inbuilt wrapper in order to control another function (implicit_wait).

initiate_login:
        Function used to initiate Whatsapp login sequence.
        Uses a timer to countdown & check if Whatsapp has been logged in to.

enter_text_in_searchbox:
        Function enters a contact's name in the search box.

cancel_search:
        Function clicks on the cancel button in the contact search box.

fetch_displayed_items:
        Function finds contact/message/ header objects displayed on a whatsapp contact list.
        -- Current implementation not able to look at the GROUPS section of the pane. Only looks at Chat pane.

check_if_contact:
        Checks if Selenium objects passed as input are contact objects or not.
        If it is a contact, places that selenium object in a list.
        The other alternatives are that it can be a message item or header item (chats/ messages).

find_target_element:
        Searches objects for a text, returns the object that matches that text.

click_on_element
        Function clicks on element.

find_contact:
        Function searches for a contact_name. If that contact is found, it is clicked on.

take_element_screenshot:
        Function takes a screenshot of an element & then saves it to a desired path.

logout_of_whatsapp:
        Function logs out of current session.

create_whatsapp_group:
        Function creates a new whatsapp group.

add_person_to_group
        Function adds a contact to a group.

add_admin
        Add a new whatsapp group admin.

implicit_wait_is_displayed:
        Function implements an explicit wait for a class object to be displayed.
        It is useful for cases where you want your program to wait x number of seconds before trying to move on to next execution.
        It is controlled using a timeout.

implicit_wait:
        Function implements an explicit wait for a given class object.
        It is useful for cases where you want your program to wait x number of seconds before trying to find any element.
        It is controlled using driver & a timeout.

current_time_string:
        Function returns the current time formatted as a string. This string can be used as a filename.
        E.g. You can use this string to save screenshots.

Write Aids:
click_on_attach
        Function clicks on the attach button on the "main" pane 

add_attachment_caption
        Function adds a text to a whatsapp attachment caption.

click_send_attachment
        Adds text to a whatsapp caption.

enter_formatted_text
        Function takes a string input & formats it in a way that allows you to enter a message in multiple lines.
        E.g. For each word in the list, enter that word & then press shift enter to go to a new line.

send_text_message
        Functions sends a text message.

attach_file
        Function attaches a file from the Operating System onto Whatsapp.

send_attachment
        Function sends attachment using various sub-functions.

Read Aids:
is_whatsapp_group
        Function checks if a contact that has been clicked on is a Whatsapp group or not.

get_days_list
        Function creates a DataFrame with dates going back "day_to_go_back" times.

check_whatsapp_date
        Function checks if a input_object string is a date, day name, encryption string or just a string.
        The string is then converted to its corresponding date string or "Not Date" is returned.

check_if_date_available
        Function checks if a given datetime object is available in the current list of whatsapp message divider.
        Used in conjunction with the upward scrolling function.

scroll_up_messages
        Function scrolls up to see older messages on Whatsapp.
        It clicks on the messages pane & then uses ActionChains to perform scroll ups.

get_instance_phone_name
        Function gets the name of the phone's whatsapp account.

get_messages
        Function finds & returns message objects in a whatsapp chat as a pd.DataFrame object.

get_message_time
        Function gets the time that a whatsapp message was sent on.

get_message_type_and_text
        Function gets the message type and text on a whatsapp message object.

get_message_date
        Function assigns a date to when a message was sent.
        Uses Date Divider objects to determine breaks of dates.

strip_message_name
        Function gets the name in a message object.

get_message_from_to_context
        Function fetches details about who the message is from, who its to & the context [the contact name we're in].

add_new_messages_to_db
        Function adds new messages to the database. Assumes an existing connection is available.


Functions Aids: 
wrapper_send_media_messages
        Function puts together other underlying functions that allow you to send media messages to a contact or group.
        Media messages include items like images, videos & audio files.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, 
        Navigate, Writer & Read class objects.

wrapper_read_text_messages
        Function puts together other underlying functions that allow you to read & backup messages from whatsapp to our database.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, 
        Navigate, Writer & Read class objects.
        The messages to store to database are given in as input. How many days to read are also given as input.
        It also uses a event_dict, a dictionary with information on the contacts to read messages from..

wrapper_send_text_message
        Function puts together other underlying functions that allow you to send a basic text message.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, Navigate & Writer class objects.
        It also uses a event_dict, a dictionary with information on the message to be sent & the people to send messages to.

wrapper_create_group
        Function creates a whatsapp group.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, Navigate & Writer class objects.
        It uses a event_dict, a dictionary with information on the message to be sent & the people to send messages to.
        It contains a get_user_class_name function for fetching the name to use as the whatsapp group's name.

wrapper_add_person_to_group
        Function adds participants to a whatsapp group.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, Navigate & Writer class objects.
        It uses a event_dict, a dictionary with information on the message to be sent & the people to send messages to.

wrapper_add_group_admin
        Function makes a participant a whatsapp group admin.
        It uses a parameters dictionary to control Whatsapp. This dictionary comes with a driver, Navigate & Writer class objects.
        It uses a event_dict, a dictionary with information on the message to be sent & the people to send messages to.

