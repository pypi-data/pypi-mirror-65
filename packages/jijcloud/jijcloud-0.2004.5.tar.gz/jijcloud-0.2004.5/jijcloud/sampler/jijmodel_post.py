import dimod
from abc import ABCMeta
from jijcloud.post_api import post_to_solver


class JijModelingInterface(metaclass=ABCMeta):
    def sample_modeling(self, model, multipliers, conditions, timeout=None,
                        feed_dict: dict = None, **kwargs):
        m_seri = model.to_serializable()

        # calculate number of variables
        num_variables = 0
        for k, v in model.variables.items():
            if v['var_type'] == 'variable':
                num_variables += model.num_elements[k]

        parameters = kwargs
        parameters['feed_dict'] = feed_dict
        body = {
            'hardware': self.hardware,
            'algorithm': self.algorithm,
            'num_variables': num_variables,
            'problem': {
                'model': m_seri,
                'multipliers_constraint': multipliers,
                'conditions': conditions
            },
            'problem_type': 'jijmodel',
            'multipliers': multipliers,
            'parameters': parameters,
            'info': {}
        }

        timeout = self.timeout if timeout is None else timeout
        if timeout is None:
            raise ValueError('timeout is not None.')
        status_code, response = post_to_solver(
            self.url, self.token, body, timeout)
        res = response['response']
        additional_info = response['info']
        res = response['response']
        additional_info = response['info']
        sample_set = dimod.SampleSet.from_serializable(res)
        sample_set.info.update(additional_info)
        return sample_set
