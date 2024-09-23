def update_data(connection, cursor):
    durations_dict = {
    "More than 4 years": [
        "4 Years (Part time)", "4 years", "4 years  (480 credits)", "4 Year",
        "4.5 Year", "4.5 Year", "4 Years", "4 Years (Part-time options available)", 
        "6 years", "5 Years", "4 yeasrs", "4.5Year"
    ],
    "0-1 years": [
        "40 Academic Weeks", "38 weeks", "40 weeks full-time", "17 weeks", 
        "Half year", "12 Weeks", "36 weeks", "1 Week", "18 Weeks", "34 Weeks", 
        "16 weeks", "30 Academic Weeks", "32 WEEKS", "1 Semester", "19 weeks, full-time", 
        "6 Weeks", "27 Weeks", "29 Weeks", "40 Weeks", " 30 Academic Weeks",
        "40 weeks including six weeks of study break", "\xa040 Academic Weeks", "1 Week","40 weeks"
    ],
    "1-2 years": [
        "1 Year", "1 year, full-time", "1/ 1.5 Year", "1.5 Year","1 year","1 year, full-time",
        "1 year to 2 years", "1 1/2 years (18 academic months)","1years","1,5 years(18 months)",
        "1.5 years(18 months)", "1 to 2 year", "1 to 2 years", "1 .5Year", "1  Year", 
        "76 -80 week", "1.3 Years", "1/ 2 Years", "18 Months full-time","1 Year ","1 year, full-time "
        "1 Year (part time)", "1 year part-time (36 weeks)", "1 year, full-time","FULL-TIME - 1 Year ",
        "1 to 1.5 years", "1 year/1.5 years", "1 to1.5 years", "1.5/ 2 Years", "1 Year"," 1 Year",
        "1.5/ 2 Year", "1-2 years", "1 Year to 2 Year", "1.5 Years", "1.3 Year","1 to 1,5 years",
        "1.5 years", "1/1.5 Year", "1/ 1.5 Years", "1/ 1.5 year", "1 - 1.5 years","1 to1.5 years " 
        "1.5 years(18 months)", "1/1.5/2 Years", "1.5 years(18 months)", "1/ 1.3 Years",
        "1 to 2year", "1 years", "1.5-2 years", "Full Time 1 Year", "1Year","1 year fill-time"
        "1 Year", "1,5 years", "1to 2 years", "FULL-TIME - 1.5 Years (Part-time options available)", 
        "18 Months", "62 weeks", "65 weeks", "32 - 52 weeks", "18 months", "1 year fill-time","""1 year, full-time
        ""","1 Year (part time)",
        "FULL-TIME - 1 Year (Part-time options available)", "18 months, full-time", "Full TIme 1 Year",
        "1 year, full-time","FULL-TIME - 1 Year"," 1.5 Year","1 to1.5 years ","1 year, full-time \n",
        "51 teaching weeks and up to 8 weeks of study breaks (1.5 years)", "1 to 1.5 Year","1 year full-time"
        
    ],
    "2-3 years": [
        "2 Years", "2 years", "2-3 Years", "2 to 3 years", "2.5 Years", "2Year", "FULL-TIME - 2 Years (Part-time options available)",
        "30 Months", "2.5 years", "2.5 Year", "2 year full-time", "2 years (full-time)", "FULL-TIME - 2 Years","2 years full-time",
        "2 years part-time", "2 Year (full-time)", "2 Year (part-time)", 
        "2 years (part-time)", "2 years - 3 years", "2 Year", "2Year", "2 year"
    ],
    "3-4 years": [
        "3 to 4 years", "3 years", "FULL-TIME - 3 Years", "3Years", "Three years","3 Years","3 Years(full time&part time)",
        "3yeasrs", "3 year full-time", "3years", "3 to 3.5 years", "3Years", "3  to 3.5 years",
        "3years", "3 year", "3 year", "FULL-TIME - 3 Years (Part-time options available)", 
        "3Years", "3 to 3.5 years", "FULL-TIME - 3 Years (Part-time options available)","3to 3.5 years",
        "3 to 4 Years", "3year", "3 Year","3 years  (360 credits)","3 years full-time","3 years, full-time",
        ]
    }


    # Mapping of duration categories to IDs
    duration_category_ids = {
        "0-1 years": 1,
        "1-2 years": 2,
        "2-3 years": 3,
        "3-4 years": 4,
        "More than 4 years": 5
    }

    # Prepare the update queries
    for category, values in durations_dict.items():
        for value in values:
            query = f"""UPDATE programs SET duration_category_id = {duration_category_ids[category]} WHERE duration ='{value}';"""
            print(query)
            cursor.execute(query)

    # Commit the changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
