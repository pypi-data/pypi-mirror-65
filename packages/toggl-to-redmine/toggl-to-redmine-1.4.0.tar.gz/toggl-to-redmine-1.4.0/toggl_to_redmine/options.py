import datetime
import click

def validate_date(ctx, param, date):
    if date == None:
        return
    try:
        day, month, year = date.split('-')
        iso_date = f'{year}-{month}-{day}'
        datetime.date.fromisoformat(iso_date)
        return iso_date
    except ValueError:
        raise click.BadParameter('Dates must follow this pattern: DD-MM-YYYY')

def get_options_hash(first_date, last_date):
    options = {}
    if first_date != None:
        options['toggl_start_date'] = first_date
    if last_date != None:
        options['toggl_end_date'] = last_date
    return options