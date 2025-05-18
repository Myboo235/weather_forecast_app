from datetime import datetime, timedelta


# def get_next_hours():
#     utc_now = datetime.utcnow()
#     vietnam_offset = timedelta(hours=7)
#     now = utc_now + vietnam_offset
#     next_hours = []

#     fixed_hours = [0, 3, 6, 9, 12, 15, 18, 21]
#     current_hour = now.hour

#     next_hour = next((h for h in fixed_hours if h > current_hour), None)
#     if next_hour is None:
#         next_hour = fixed_hours[0]
#         now += timedelta(days=1)

#     base_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)

#     for i in range(8):
#         next_hours.append(base_time + timedelta(hours=3 * i))

#     return next_hours

def get_next_hours(from_datetime):
    fixed_hours = [0, 3, 6, 9, 12, 15, 18, 21]
    current_hour = from_datetime.hour

    next_hour = next((h for h in fixed_hours if h > current_hour), None)
    if next_hour is None:
        next_hour = fixed_hours[0]
        from_datetime += timedelta(days=1)

    base_time = from_datetime.replace(hour=next_hour, minute=0, second=0, microsecond=0)

    return [base_time + timedelta(hours=3 * i) for i in range(8)]
