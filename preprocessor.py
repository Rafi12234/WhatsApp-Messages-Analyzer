import re
import pandas as pd


def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm|AM|PM)\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Build DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # Convert message_date to datetime (matches your regex format)
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%y, %I:%M %p - ',
        errors='coerce'
    )
    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    # iterate over original 'user_message'
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) >= 3:  # if user + message exist
            users.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:  # system / group notification
            users.append('group_notification')
            messages.append(entry[0].strip())

    # Add new columns
    df['user'] = users
    df['message'] = messages

    # now drop user_message
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
