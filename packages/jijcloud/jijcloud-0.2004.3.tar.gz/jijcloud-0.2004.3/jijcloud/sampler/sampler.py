import dimod

from jijcloud.post_api import post_to_solver
from jijcloud.setting import load_config


class JijCloudSampler(dimod.Sampler):
    """JijCloudSampler
    another Sampler is based on this class
    """

    hardware = ''
    algorithm = ''

    def __init__(self, token=None, url=None, timeout=None, config_file=None, config_env='default'):
        """setting token and url

        Args:
            token (str, optional): token string. Defaults to None.
            url (str, optional): API URL. Defaults to None.
            timeout (float, optional): timeout for post request. Defaults to None.
            config_file (str, optional): Config file path. Defaults to None.

        Raises:
            TypeError: token, url, config_file is not str
        """

        if isinstance(config_file, str):
            _config = load_config(config_file)[config_env]
            self.token = _config['token']
            self.url = _config['url']
            self.timeout = _config.get('timeout', 1)
        else:
            if not isinstance(token, str):
                raise TypeError('token is string')
            self.token = token

            if not url:
                self.url = 'https://dev-api.jij-cloud.com'
            elif isinstance(url, str):
                self.url = url
            else:
                raise TypeError('url is string')

            if not timeout:
                self.timeout = timeout
            elif isinstance(timeout, float):
                self.timeout = timeout
            else:
                raise TypeError('timeout is float number')

    def sample(self, bqm, num_reads=1, num_sweeps=100, timeout=None, **kwargs):
        parameters = {'num_reads': num_reads, 'num_sweeps': num_sweeps}

        parameters.update(kwargs)
        post_body = {
            'hardware': self.hardware,
            'algorithm': self.algorithm,
            'num_variables': bqm.num_variables,
            'problem_type': 'BinaryQuadraticModel',
            'problem': bqm.to_serializable(),
            'parameters': parameters,
            'info': {}
        }

        # if timeout is defined in script, use this value
        if timeout:
            self.timeout = timeout
        
        status_code, response = post_to_solver(self.url, self.token, post_body, self.timeout)
        res = response['response']
        additional_info = response['info']
        sample_set = dimod.SampleSet.from_serializable(res)
        sample_set.info.update(additional_info)
        return sample_set

    @property
    def properties(self):
        return dict()

    @property
    def parameters(self):
        return dict()
