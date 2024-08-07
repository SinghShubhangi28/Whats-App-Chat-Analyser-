import pandas as pd
import re


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s'

    messages = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)
    df=pd.DataFrame({'user_message':messages,'message_date':dates})


    #convert message_date type
    # df['message_date']=pd.to_datetime(df['message_date'],format='%d/%m/%Y,%H:%M -')
    # df.rename(columns={'message_date':'date'},inplace=True)
    #

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # Extract date and time separately
    df['date'] = df['message_date'].apply(lambda x: x.split(',')[0].strip())
    df['time'] = df['message_date'].apply(lambda x: x.split(',')[1].split('-')[0].strip().replace(' ', ' '))
    # Convert date and time to datetime
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')
    df['time'] = pd.to_datetime(df['time'], format='%I:%M %p', errors='coerce').dt.time
    # Drop the original message_date column
    df.drop(columns=['message_date'], inplace=True)


    # separate users and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df

