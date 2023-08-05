import json
import requests
from typing import Tuple


POST_SOLVER = {
    "hardware": str,
    "algorithm": str,
    "num_variables": int,
    "problem": dict,
    "problem_type": str,
    "parameters": dict,
    "info": dict
}


def post_to_solver(url: str, token: str, body: dict, timeout: float) -> Tuple[int, dict]:
    """Post to /solver endpoint

    Args:
        url (str): API URL which can be get Jij-Cloud-Web.
        token (str): Token string.
        body (dict): post dictionary.
        timeout (float): number of timeout for post request.

    Raises:
        requests.exceptions.HTTPError: [description]

    Returns:
        (int, dict): status_code, response json as dict.
    """
    endpoint = url if url[-1] != '/' else url[:-1]
    endpoint += '/solver/'
    headers = {'Authorization': 'Bearer ' + token,
               "Content-Type": "application/json"}

    # validation -------------------------------
    for k, v_type in POST_SOLVER.items():
        if k not in body:
            raise ValueError('body should have "{}".'.format(k))
        if not isinstance(body[k], v_type):
            raise TypeError('{} is type: "{}".'.format(k, v_type))
    # ------------------------------- validation

    json_data = json.dumps(body)
    res = requests.post(endpoint, headers=headers,
                        data=json_data, timeout=timeout)
    res.raise_for_status()
    data = res.json()
    if 'error' in data:
        message = res.json().get('error', res.text)
        if isinstance(message, dict):
            message = message['msg']
        raise requests.exceptions.HTTPError(
            str(res.status_code) + ' ' + message)

    return res.status_code, res.json()
