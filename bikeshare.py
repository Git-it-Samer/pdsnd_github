import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid         inputs
    # Applying this filter will run repeatedly until user input is recognized.
    while True:
        # Applying the lower method below will create a standardization for user input and if the first letter is               capitalized, it will be recognized either way.
        print('\nWhich city would you like to explore data for?')
        city = input('1. Chicago 2. New York City 3. Washington\n').lower()
        if city.lower() not in CITY_DATA.keys():
            print('Input\’s invalid, please select one of the three cities provided')
        else:
            city = city.lower()
            # Breaking the loop will carry this statement over to the proceeding statements.
            break
    # Used title method to capitalize the first letter of user's answers for consistency, especially since city names       are involved.
    print('You chose {} '.format(city.title()))

    # TO DO: get user input for month (all, january, february, ... , june)
    # A dictionary is made to simplify accessing month data, including the option of 'all'.
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    while True:
        month = input('\nWhich month(s), between January and June, would you like to see data for? If you want all months, please type ‘all’.\n')
        if month.lower() not in MONTH_DATA.keys():
            print('Input\’s invalid, please select a month between January and June or ‘all’.')
        else:
            month = month.lower()
            break

    print('You chose {} '.format(month.title()))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    # A dictionary was also made for the days of the week, enabling another source to filter.
    DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',  'all']
    while True:
        day = input('\nWhich day(s) of the week would you like to see data for? If you want all days, please type ‘all’.\n')
        if day not in DAY_DATA.keys():
            print('Input\’s invalid, please select a month between January and June or ‘all’.')
        else:
            day = day.lower()
            break

    print('You chose {} '.format(day.title()))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Defined a function to load data from the .csv files.
    df=pd.read_csv(CITY_DATA[city])
    # The Start Time column includes a combination of time and date, so it's converted using datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # New columns are created to separate data by month and days, to provide users with filters to access data.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # An if loop was used for filtering months and day.
    if month != 'all':
        # An index for the months was created as well as adding 1 to access corresponding integer, since the first             element is recognized as 0 in Python.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        #New dataframe enables filtering by month.
        df = df[df['month'] == month]

    if day != 'all':
        # New dataframe enables filtering by weekdays.
        df = df[df['day_of_week'] == day.title()]

    # The files chosen will be called as a statement and returned as a dataframe.
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # Time method was used to convert time into seconds.
    start_time = time.time()

    # TO DO: display the most common month
    # Mode method was used find the month that occurred the most within the relevant data.
    common_month = df['month'].mode()[0]
    print('The most common month: {}'.format(common_month))

    # TO DO: display the most common day of week
    # Similar to the code above, the mode method was applied to the weekdays.
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week: {}'.format(common_day))

    # TO DO: display the most common start hour
    # A separate column was created for the hour extracted from the Start Time column.
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    # Mode method was applied on the Start Station column to find the most common starting station.
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station: {}'.format(common_start_station))

    # TO DO: display most commonly used end station
    # The mode method was applied on the End Station column to find the most common ending station.
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station: {}'.format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    # Combined the 'Start Station' and 'End Station' columns in the DataFrame by using str.cat
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=', ')
    # The results will transfer into a new column, 'Start To End'. Mode was used as well to find the most frequent         result.
    common_combination = df['Start To End'].mode()[0]
    print('The most frequent combination of start and end station trip: {}'.format(common_combination))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # The total travel time is calculated with the sum method.
    total_duration = df['Trip Duration'].sum()
    print('Total travel time: {}'.format(total_duration))

    # TO DO: display mean travel time
    # The average travel time is calculated with the mean method.
    mean_duration = df['Trip Duration'].mean()
    print('Mean travel time: {}'.format(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # User types are categorized and then quantified with the value_counts method.
    user_types = df['User Type'].value_counts()
    print('User Types\n', user_types)

    # TO DO: Display counts of gender
    # Used the if loop, since the 'Gender' column doesn't exist in the washington.csv file.
    if 'Gender' in df.columns:
        # Genders are categorized and then quantified with the value_counts method.
        gender_counts = df['Gender'].value_counts()
        print('\nThe counts of each gender type:\n', gender_counts)

    else:
        print('\nThere are no columns for the value in the file.')

    # TO DO: Display earliest, most recent, and most common year of birth
    # Used the if loop, since the 'Birth Year' column doesn't exist in the washington.csv file.
    if 'Birth Year' in df.columns:
        #Statistical functions of min, max, and mode are used as methods with the 'Birth Year' column.
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()
        print('\nThe earliest year of birth: {}'.format(earliest_year))
        print('The most recent year of birth: {}'.format(recent_year))
        print('The most common year of birth: {}'.format(common_year))

    else:
        print('\nThere are no columns for the value in the file.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays 5 rows of raw data for the csv file for the selected city. User has choice to view, as well as an           additional 5 rows until no longer desired"""

    row_length = df.shape[0]

    # iterate from 0 to the number of rows in intervals of 5
    for i in range(0, row_length, 5):

        yes = input('\nDo you want to see 5 lines of the raw data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break

        # Retrieved and converted data to json format and spliting each json row of data with the split method.
        # Used 'W3resource' as guidance in using Pandas DataFrame with json
        raw_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in raw_data:
            # Print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
