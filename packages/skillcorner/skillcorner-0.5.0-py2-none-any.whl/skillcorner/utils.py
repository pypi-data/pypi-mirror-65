from dateutil.parser import parse as parse_dt


def get_match_unique_name(match_data):
    """
    Get skillcorner unique name for a match

    Args:
        match_data (dict): should come from a request to match endpoint. Includes, date_time, and teams
            (with their short_name)

    Returns:
        str: unique name of the match
    """
    return u'{}_{}_{}'.format(
        parse_dt(match_data['date_time']).strftime('%Y%m%d'),
        match_data['home_team']['short_name'],
        match_data['away_team']['short_name'])
