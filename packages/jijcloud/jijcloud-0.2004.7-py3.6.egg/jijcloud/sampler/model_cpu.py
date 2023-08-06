from jijcloud.sampler import JijCloudSampler


class JijModelSampler(JijCloudSampler):
    hardware = 'cpu'
    algorithm = 'sa'

    def sample_model(self, model,
                     conditions, multipliers,
                     vartype,
                     beta_min=None, beta_max=None,
                     num_reads=1, mc_steps=100):

        problem = _pyqubo_to_dict(model)
        problem['multipliers'] = multipliers
        problem['conditions'] = conditions

        parameters = {
            'num_reads': num_reads,
            'mc_steps': mc_steps,
            'beta_min': beta_min, 'beta_max': beta_max,
            'num_reads': num_reads, 'mc_steps': mc_steps
        }

        request_json = self._make_requests_dict(
            problem, 'model qubo', parameters=parameters
        )
        status_code, response = self._post_requests(
            request_json, self.url, self.token)
        sample_set = self.recieve_result(response, vartype)
        return sample_set


def _pyqubo_to_dict(model):
    qubo = model.compiled_qubo.qubo
    dict_qubo = {}
    for key, value in qubo.items():
        serierized_value = [0, {}]
        for k, v in value.terms.items():
            serierized_value[0] = v
            serierized_value[1] = k.keys
        dict_qubo[key] = serierized_value

    constraints = {}
    for label, const in model.constraints.items():
        constraints[label] = []
        for key, v in const.polynomial.items():
            constraints[label].append([v] + list(key.keys))

    return {
        'qubo': dict_qubo,
        'constraints': constraints
    }
