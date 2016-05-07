# this python script parses and preps the necessary fields from the Yelp data set for use in the
# Kellogg MBA Big Data Competition on **/**/**** at Northwestern University.

import json
import csv
from tqdm import tqdm


def parse_data(source1, source2, source3, output_path):
    # setup an array for writing each row in the csv file
    rows = []
    # extract fields from business json data set #
    # setup an array for storing each json entry
    business_data = []
    # setup an array for headers we are not using strictly
    business_header_removals = ['attributes', 'categories', 'hours', 'neighborhoods', 'open']
    # setup an array for headers we are adding
    business_header_additions = ['Sunday_Open', 'Sunday_Close', 'Monday_Open', 'Monday_Close', 'Tuesday_Open',
                                 'Tuesday_Close', 'Wednesday_Open', 'Wednesday_Close', 'Thursday_Open',
                                 'Thursday_Close', 'Friday_Open', 'Friday_Close', 'Saturday_Open', 'Saturday_Close',
                                 'Noise Level', 'Attire', 'Alcohol', 'Price_Range', 'Delivery', 'Outdoor_Seating',
                                 'Drive-Thru', 'Good_for_Groups', 'Has_TV', 'Caters', 'Waiter_Service',
                                 'Good_for_Kids', 'Accepts_Credit_Cards', 'Takes_Reservations', 'Wi_Fi', 'Happy_Hour',
                                 'Good_for_Dancing', 'Smoking', 'BYOB', 'Corkage', 'Take_Out', 'Coat_Check',
                                 'Parking_Street', 'Parking_Valet', 'Parking_Lot', 'Parking_Garage',
                                 'Parking_Validated', 'Music_DJ', 'Music_Karaoke', 'Music_Video', 'Music_Live',
                                 'Music_Jukebox', 'Music_Background_Music', 'Is_Restaurants', 'Sandwiches', 'Fast Food',
                                 'Nightlife', 'Pizza', 'Bars', 'Mexican', 'Food', 'American (Traditional)',
                                 'Burgers', 'Chinese', 'Italian', 'American (New)', 'Breakfast & Brunch', 'Thai',
                                 'Indian', 'Sushi Bars', 'Korean', 'Mediterranean', 'Japanese', 'Seafood',
                                 'Middle Eastern', 'Pakistani', 'Barbeque', 'Vietnamese', 'Asian Fusion', 'Diners',
                                 'Greek', 'Vegetarian']
    # open the business source file
    with open(source1) as f:
        # for each line in the json file
        for line in f:
            # store the line in the array for manipulation
            business_data.append(json.loads(line))
    # close the reader
    f.close()
    # append the initial keys as csv headers
    header = sorted(business_data[0].keys())
    # remove keys from the business data that we are not using strictly
    for headers in business_header_removals:
        header.remove(headers)
    # append the additional business related csv headers
    for headers in business_header_additions:
        header.append(headers)
    print('processing data in the business dataset...')
    # for every entry in the business data array
    for entry in tqdm(range(0, len(business_data))):
        row = []
        row.append(business_data[entry]['business_id'])
        row.append(business_data[entry]['city'])
        row.append(business_data[entry]['full_address'])
        row.append(business_data[entry]['latitude'])
        row.append(business_data[entry]['longitude'])
        row.append(business_data[entry]['name'])
        row.append(business_data[entry]['review_count'])
        row.append(business_data[entry]['stars'])
        row.append(business_data[entry]['state'])
        row.append(business_data[entry]['type'])
        # set up an array for the days of the week
        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        # iterate through the days of the week to extract the open and close times
        for time in days_of_week:
            # if a time is available
            if time in business_data[entry]['hours']:
                # append the open time
                row.append(business_data[entry]['hours'][time]['open'])
                # append the closing time
                row.append(business_data[entry]['hours'][time]['close'])
            # else if a time is not available
            else:
                # append NA for the open time
                row.append('NA')
                # append NA for the closing time
                row.append('NA')
        # extract the attributes of interest
        attributes = ['Noise Level', 'Attire', 'Alcohol', 'Price Range', 'Delivery', 'Outdoor Seating', 'Drive-Thru',
                      'Good For Groups', 'Has TV', 'Caters', 'Waiter Service', 'Good for Kids', 'Accepts Credit Cards',
                      'Takes Reservations', 'Wi-Fi', 'Happy Hour', 'Good For Dancing', 'Smoking', 'BYOB', 'Corkage',
                      'Take-out', 'Coat Check']
        # for each attribute that is not nested
        for attribute in attributes:
            # if there is an attribute
            if attribute in business_data[entry]['attributes']:
                # if the attribute contains true
                if business_data[entry]['attributes'][attribute] is True:
                    row.append(1)
                # else if the attribute contains false
                elif business_data[entry]['attributes'][attribute] is False:
                    row.append(0)
                # else if the attribute is non-empty and not true of false
                elif business_data[entry]['attributes'][attribute] is not None:
                    row.append(business_data[entry]['attributes'][attribute])
            # else of the attribute is not available
            else:
                # append NA for the attribute
                row.append('NA')
        # extract the parking attributes
        parking_attributes = ['street', 'valet', 'lot', 'garage', 'validated']
        # for each parking attribute
        for attribute in parking_attributes:
            # if there are parking attributes
            if 'Parking' in business_data[entry]['attributes']:
                # if the parking attribute exists
                if attribute in business_data[entry]['attributes']['Parking']:
                    # if the parking attribute is true
                    if business_data[entry]['attributes']['Parking'][attribute] is True:
                        row.append(1)
                    # if the parking attribute is false
                    elif business_data[entry]['attributes']['Parking'][attribute] is False:
                        row.append(0)
                    # note that the parking attributes are all true/false so no need for is not None elif
                # else if the specific attribute is not available
                else:
                    row.append('NA')
            # else if the parking attribute is not available
            else:
                row.append('NA')
        # extract the music attributes
        music_attributes = ['dj', 'karaoke', 'video', 'live', 'jukebox', 'background_music']
        # for each music attribute
        for attribute in music_attributes:
            # if there are music attributes
            if 'Music' in business_data[entry]['attributes']:
                # if the music attribute exists
                if attribute in business_data[entry]['attributes']['Music']:
                    # if the music attribute is true
                    if business_data[entry]['attributes']['Music'][attribute] is True:
                        row.append(1)
                    # if the music attribute is false
                    elif business_data[entry]['attributes']['Music'][attribute] is False:
                        row.append(0)
                    # note that the music attributes are all true/false so no need for is not None elif
                # else if the specific attribute is not available
                else:
                    row.append('NA')
            # else if the music attribute is not available
            else:
                row.append('NA')

        # extract the categories
        categories_of_interest = ['Restaurants', 'Sandwiches', 'Fast Food', 'Nightlife', 'Pizza', 'Bars', 'Mexican',
                                  'Food', 'American (Traditional)', 'Burgers', 'Chinese', 'Italian',
                                  'American (New)', 'Breakfast & Brunch', 'Thai', 'Indian', 'Sushi Bars', 'Korean',
                                  'Mediterranean', 'Japanese', 'Seafood', 'Middle Eastern', 'Pakistani', 'Barbeque',
                                  'Vietnamese', 'Asian Fusion', 'Diners', 'Greek', 'Vegetarian']
        # for each category of interest
        for category in categories_of_interest:
            # if the category is in the category entry
            if category in business_data[entry]['categories']:
                row.append(1)
            # else if the category is not in the entry
            else:
                row.append(0)
        # remove stray text, such as "\n" form address
        # set up an array for the cleaned row entries
        row_clean = []
        # for every item in the row
        for item in row:
            # scan and replace for nasty text
            row_clean.append(str(item).replace('\n', ' '))
        # after all fields have been extracted and cleaned, append the row to the rows array for writing to csv
        rows.append(row_clean)

    # extract fields from check in data set #
    # setup an array for storing each json entry
    checkin_data = []
    # open the business source file
    with open(source2) as f:
        # for each line in the json file
        for line in f:
            # store the line in the array for manipulation
            checkin_data.append(json.loads(line))
    # close the reader
    f.close()
    # setup an array for headers we are adding
    checkin_header_additions = ['Number_of_Checkins']
    # append the checkin related csv headers
    for headers in checkin_header_additions:
        header.append(headers)
    print('processing data in the check in dataset...')
    # iterate through rows and check in data to count check ins
    # for every row in our collected data
    for i in tqdm(range(0, len(rows))):
        # set the initial number of check ins at 0
        num_checkins = 0
        # for every row in the check in data
        for j in range(0, len(checkin_data)):
            if rows[i][0] == checkin_data[j]['business_id']:
                num_checkins += sum(checkin_data[j]['checkin_info'].values())
            else:
                num_checkins = num_checkins
        rows[i].append(num_checkins)

    # extract fields from tips data set #
    # setup an array for storing each json entry
    tip_data = []
    # open the business source file
    with open(source3) as f:
        # for each line in the json file
        for line in f:
            # store the line in the array for manipulation
            tip_data.append(json.loads(line))
    # close the reader
    f.close()
    # setup an array for headers we are adding
    tip_header_additions = ['Number_of_Tips', 'Number_of_Tip_Likes']
    # append the tip related csv headers
    for headers in tip_header_additions:
        header.append(headers)
    print('processing data in the tips dataset...')

    # iterate through rows and check in data to count tips and tip likes
    # for every row in our collected data
    for i in tqdm(range(0, len(rows))):
        # set the initial number of tips and tip likes at 0
        num_tips = 0
        num_tip_likes = 0
        # for every row in the tip data
        for j in range(0, len(tip_data)):
            if rows[i][0] == tip_data[j]['business_id']:
                num_tips += 1
                num_tip_likes += tip_data[j]['likes']
            else:
                num_tips = num_tips
                num_tip_likes = num_tip_likes
        rows[i].append(num_tips)
        rows[i].append(num_tip_likes)

    # write to csv file
    # print(header)
    with open(output_path, 'w') as out:
        writer = csv.writer(out)
        # write the csv headers
        writer.writerow(header)
        # for each entry in the row array
        print('writing contents to csv...')
        for entry in tqdm(range(0, len(rows))):
            try:
                # write the row to the csv
                writer.writerow(rows[entry])
            # if there is an error, continue to the next row
            except UnicodeEncodeError:
                continue
    out.close()

parse_data('Raw Data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json',
           'Raw Data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_checkin.json',
           'Raw Data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_tip.json',
           'Prepped Data/test.csv')
