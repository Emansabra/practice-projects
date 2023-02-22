import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bike share data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Would you like to see data for Chicago, New york city or Washington? "))
    while city.lower() not in ["chicago", "new york city", "washington"]:
        print("Make sure you've chosen from: Chicago, New york city or Washington. ")
        city = str(input("What is the name of city you'd like to know about? "))

    # get user input for month (all, january, february, ... , june)
    month = str(input("Which month? January - February - March - April - May - June or All to apply no filter. "))
    while month.lower() not in ["all", "january", "february", "march", "april", "may", "june"]:
        print("Make sure you've chosen from: January, February, March, "
              "April, May, June or All to apply no filter. ")
        month = str(input("What is the month you'd like to know about? "))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input("Which day? Monday - Tuesday - Wednesday - "
                    "Thursday - Friday - Saturday - Sunday or All to apply no filter. "))
    while day.lower() not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        print("Make sure you've chosen from: Monday, Tuesday, "
              "Wednesday, Thursday, Friday, Saturday, Sunday or All to apply no filter. ")
        day = str(input("What is the day you'd like to know about? "))
    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['month_name'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day
    df['day_name'] = df['Start Time'].dt.day_name()
    df['hour_start'] = df['Start Time'].dt.hour
    df['hour_end'] = df['End Time'].dt.hour
    df['trip'] = df['Start Station'] + df['End Station']
    if month != 'all':
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month_name'].mode().get(0)
    count_common_month = df['month_name'].value_counts().max()
    print('Most common month:', common_month, ',Count = ', count_common_month)

    # display the most common day of week
    common_day = df['day_name'].mode().get(0)
    count_common_day = df['day_name'].value_counts().max()
    print('Most common day:', common_day, ',Count = ', count_common_day)

    # display the most common start hour
    popular_hour = df['hour_start'].mode().get(0)
    count_common_hour = df['hour_start'].value_counts().max()
    print('Most common Start hour:', popular_hour, ',Count = ', count_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode().get(0)
    count_common_start_station = df['Start Station'].value_counts().max()
    print('Most common start station:', common_start_station, ',Count = ', count_common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode().get(0)
    count_common_end_station = df['End Station'].value_counts().max()
    print('Most common end station:', common_end_station, ',Count = ', count_common_end_station)

    # display most frequent combination of start station and end station trip
    common_trip = df['trip'].mode().get(0)
    count_common_trip = df['trip'].value_counts().max()
    print('Most common trip:', common_trip, ',Count = ', count_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    start_hour = df['hour_start']
    end_hour = df['hour_end']
    travel_time = end_hour - start_hour
    print('Total travel time = ', sum(travel_time))

    # display mean travel time
    print('Average travel time = ', travel_time.mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender, birth year
    try:
        print(df['Gender'].value_counts())
        common_year = df['Birth Year'].mode().get(0)
        count_common_year = df['Birth Year'].value_counts().max()
        print("Most common year of birth:", common_year, ",Count = ", count_common_year)
        most_recent_year = df['Birth Year'].max()
        print("Most recent year of birth:", most_recent_year)
        earliest_year = df['Birth Year'].min()
        print("Earliest year of birth:", earliest_year)
    except KeyError:
        print("Gender data not available")
        print("Birth year data not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def rows(df):
    start = 0
    end = 5
    answer = 'yes'
    while True:
        see_data = str(input("Would you like to see the row data? Yes or No. ").lower())
        if see_data == answer:
            print(df.iloc[start:end])
            start += 5
            end += 5
        else:
            break
    return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
