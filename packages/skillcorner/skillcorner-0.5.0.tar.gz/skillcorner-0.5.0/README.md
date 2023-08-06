# Python SkillCorner Client
A client to access SkillCorner API.

SkillCorner API gives access to football (soccer) tracking data for the main european leagues.

## Overview

Tracking data are the positions of each player, the referee and the ball at any given time of the game. 
To find more information on SkillCorner, visit [our website](https://skillcorner.com/).
To test the data, apply for a test api key [here](https://skillcorner.com/#contact).

## Installation

Install with pip

	pip install skillcorner

The client has only been tested on Python 2.7.x for now and will be adapted to Python 3 in the near future.

## Usage

### API Call

Once you have your test or production token. Initialize a client:

	from skillcorner.client import SkillCornerClient
	skillcorner = SkillCornerClient(token=<YOUR_TOKEN>)

Say, you want the data for the Champion's League match Manchester City - Hoffenheim on December 12th 2018.

First, you need to find SkillCorner `match_id` for this match.

	client.get_matches_list(min_date='2018-12-12', max_date='2018-12-13')

Then searching for the match in the key `results`, you'll find:

	{
      "id": 734,
      "home_team": {
        "short_name": "Manchester City"
      },
      "away_team": {
        "short_name": "Hoffenheim"
      },
      "date_time": "2018-12-12T20:00:00Z",
      "coverage": "premium"
    },

Now, retrieve the match information, including the lineup of the match

	client.get_match_data(734)

Players information can be found in the key `players`. The `trackable_object` key of each player is his unique identifier that will enable you to match it in the tracking data.

Now, you're all set to request the tracking data

	client.get_tracking_data(734, verbose=True)

It may take two minutes to download the whole data for a full match, there are around 1M data point per match.

### Field Modelization

The pitch dimension can be retrieved in the `match_data` (`pitch_length` being the long side of the field and `pitch_width` the short side). The unit of the modelization is the meter, the center of the coordinates is at the center of the pitch.

The x axis is the long side and the y axis is the short side.

Here is an illustration for a field of size 105x68:
![Field](resources/field.jpg)
