import sys
import math
import json
from datetime import datetime, timedelta
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from websocket import create_connection

BACKEND_URL = 'https://skillcorner.com'


class SkillCornerClientException(Exception):
    """
    Base Exception for SkillCornerClient
    """


class SkillCornerClient(object):
    """
    Manages requests to skillcorner api
    """
    def __init__(self, *args, **kwargs):
        """
        Token should be provided as kwargs (e.g. client = SkillCornerClient(token=<YOUR_TOKEN>))
        """
        self.backend_url = BACKEND_URL
        self.init_authorization(*args, **kwargs)

    def init_authorization(self, token):
        self.token = token

    def _request(self, session, method, url, json=None, params=None, timeout=5, **kwargs):
        """
        Wraps Session().request method to add authentication
        """
        if params is None:
            params = {}
        params['token'] = self.token
        return session.request(method=method, url=url, json=json, params=params,
                               timeout=timeout, **kwargs)

    def request(self, end_point, method='GET', params=None, json=None,
                retries=2, backoff_factor=0.5, timeout=5, session=None, **kwargs):
        """
        Wraps _request to call it with end_point, and eventually retry the request

        Args:
            end_point (str): backend endpoint
            retries (int, optional): number of time the request should be retried
                if an exception is raised or status code not ok
            backoff_factor (float, optional): time in second between retries of the request (will be multiplied by 2^k)
            method (str, optional): http method of the request
            params (dict, optional): any query param to pass to the request
            json (dict, optional): json payload to send
            timeout (float, optional): timeout of the request
            session (requests.Session, optional): pass a session if you want to use persistent HTTP connection
            **kwargs: any other kwargs will be pass to the _request method (then to Session.request)

        Returns:
            requests.Response: Response from the server

        Raises:
            requests.RequestException: http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
        """
        request_url = '{}{}'.format(self.backend_url, end_point)
        if not session:
            session = requests.Session()
        retry = Retry(total=retries, backoff_factor=backoff_factor, status_forcelist=(500, 502, 503, 504))
        session.mount('https://', HTTPAdapter(max_retries=retry))
        return self._request(session=session, method=method, url=request_url, json=json, params=params,
                             timeout=timeout, **kwargs)

    def paginated_requests(self, end_point, params=None, verbose=False):
        """
        Utility method to use for paginated response

        Args:
            end_point (str): backend endpoint
            params (dict, optional): any query param to pass to the request
            verbose (boolean, optional): add logging, useful if you want progress when there are a lot of pages

        Returns:
            dict: json parsed response from skillcorner api
        """
        results = []
        request_next = True
        if params is None:
            params = {}
        limit = params.get('limit')
        offset = params.get('offset')
        if verbose:
            page_nb = 0
        session = requests.Session()
        while request_next:
            if limit and offset:
                params['limit'] = limit
                params['offset'] = offset
            resp = self.request(end_point, params=params, session=session)
            if resp.status_code != 200:
                return resp.json()
            resp = resp.json()
            if resp['next']:
                qs = parse_qs(urlparse(resp['next']).query)
                limit = qs['limit'][0]
                offset = qs['offset'][0]
                if verbose:
                    page_nb += 1
                    sys.stdout.write("\rRequest to {}: {} / {}".format(
                        end_point, page_nb + 1, int(math.ceil(float(resp['count']) / int(limit)))))
                    sys.stdout.flush()
            else:
                request_next = False
            results += resp['results']
        if verbose and page_nb:
            sys.stdout.write('\n')
        return results

    def get_match_data(self, match_id, sr_matching=False):
        """
        Get match data from api
        Includes information about teams, jerseys, players, referees...

        Args:
            match_id (int): skillcorner match_id to be retrieved from matches endpoint (get_matches_list)
            sr_matching (bool, optional): whether to include sportradar matching id for players and match

        Returns:
            dict: json parsed response from skillcorner api
        """
        end_point = '/api/match/{}'.format(match_id)
        params = {}
        if sr_matching:
            params['matching'] = 'sportradar'
        return self.request(end_point, params=params).json()

    def get_video_data(self, match_id):
        """
        Get video data from api
        Includes all information of match plus specific information of video such as fps, and video_type

        Args:
            match_id (int): skillcorner match_id to be retrieved from matches endpoint (get_matches_list)

        Returns:
            dict: json parsed response from skillcorner api
        """
        end_point = '/api/match/{}/video'.format(match_id)
        return self.request(end_point).json()

    def get_match_live(self, match_id):
        """
        Get match_live data from api which essentially provides ws_url,
        to be used to receive live data with minimal latency from websocket
        The match_live only exists few minutes before the match start (around 20 minutes before)

        Args:
            match_id (int): skillcorner match_id to be retrieved from matches endpoint (get_matches_list)

        Returns:
            dict: json parsed response from skillcorner api
        """
        match_live_endpoint = '/api/match/{}/match_live'.format(match_id)
        return self.request(match_live_endpoint).json()

    def get_matches_list(
        self,
        min_date=datetime.now() - timedelta(days=30),
        max_date=None,
        sr_matching=False,
        verbose=False
    ):
        """
        Get matches list from api which provides team names and date for each match covered by SkillCorner

        Args:
            min_date (str, optional): iso datetime (ex: 2018-05-06T00:30:00Z) to filter matches starting after min_date
            max_date (str, optional): iso datetime (ex: 2018-05-12T00:30:00Z) to filter matches starting before max_date
            sr_matching (bool, optional): whether to include sportradar matching id for match
            verbose (boolean, optional): add logging, useful as the request can takes time

        Returns:
            dict: json parsed response from skillcorner api
        """
        end_point = '/api/matches'
        params = {'limit': 300}
        if sr_matching:
            params['matching'] = 'sportradar'
        if min_date:
            params['date_time__gte'] = min_date
        if max_date:
            params['date_time__lte'] = max_date
        return self.paginated_requests(end_point, params, verbose)

    def get_tracking_data(self, match_id, first_frame=None, verbose=False):
        """
        Get tracking_data from api which provides at each frame:
            * x and y coordinates for each object (player, referee, ball)
            * possession information (team and player)

        Args:
            match_id (int): skillcorner match_id to be retrieved from matches endpoint (get_matches_list)
            first_frame (int, optional): first_frame of data to receive
                to be used if you already fetched data until first_frame - 1
            verbose (boolean, optional): add logging, useful as the request can takes time

        Returns:
            dict: json parsed response from skillcorner api
        """
        end_point = '/api/match/{}/video/tracking'.format(match_id)
        params = {'limit': 3000}
        if first_frame:
            params['frame__gt'] = int(round(first_frame)) - 1
        data = self.paginated_requests(end_point, params, verbose)
        return data

    def get_ws(self, ws_url=None, match_id=None):
        """
        Open, authenticate, and return websocket to be used to get live frame on a match
        Note the socket only sends live information
        If you want to retrieve all data since match start, use get_tracking_data instead
        You can open the socket, look at the first frame you receive from the socket and
        call get_tracking_data with this frame - 1 as last_frame

        Args:
            ws_url (str, optional): websocket url to connect to
            match_id (int, optional): skillcorner match_id to be retrieved from matches endpoint (get_matches_list)
                pass match_id in case you don't already have ws_url
        Returns:
            dict: json parsed response from skillcorner api

        Raises:
            ValueError: If ws_url and match_id are None
            SkillCornerClientException: If there is no ws_url in match_live endpoint or the match is over
        """
        if not ws_url:
            if match_id is None:
                raise ValueError('You should provide either ws_url or match_id')
            match_live = self.get_match_live(match_id)
            if match_live['end_time']:
                raise SkillCornerClientException('Match is over, data should be retrieved with get_tracking_data')
            if not match_live.get('ws_url'):
                raise SkillCornerClientException('No ws_url specified for the match')
            ws_url = 'wss://{}'.format(match_live.get('ws_url'))
        ws = create_connection(ws_url, 1)
        ws.send(json.dumps({'token': self.token}))
        return ws
