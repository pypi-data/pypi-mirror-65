import dimod
from abc import ABCMeta
from jijcloud.post_api import post_to_solver


class JijModelingInterface(metaclass=ABCMeta):
    def sample_modeling(self, model, multipliers, conditions, timeout=None,
                        feed_dict: dict = None, **kwargs):
        m_seri = model.to_serializable()

        parameters = kwargs
        parameters['feed_dict'] = feed_dict
        body = {
            'hardware': self.hardware,
            'algorithm': self.algorithm,
            'num_variables': 1,
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

        status_code, response = post_to_solver(
            self.url, self.token, body, self.timeout)

        status_code, response = post_to_solver(
            self.url, self.token, body, self.timeout)
        res = response['response']
        additional_info = response['info']
        res = response['response']
        additional_info = response['info']
        sample_set = dimod.SampleSet.from_serializable(res)
        sample_set.info.update(additional_info)
        return sample_set
