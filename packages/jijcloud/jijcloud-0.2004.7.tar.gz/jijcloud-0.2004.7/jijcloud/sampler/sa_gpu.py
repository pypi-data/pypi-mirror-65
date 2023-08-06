from jijcloud.sampler import JijCloudSampler


class JijGPUSASampler(JijCloudSampler):
    hardware = 'gpu'
    algorithm = 'sa'

    def sample(self, bqm,
               beta_min=None, beta_max=None,
               num_reads=1, mc_steps=100,
               timeout=None):
        """sample ising
        Args:
            bqm (:obj:`dimod.BinaryQuadraticModel`): Binary quadratic model.
            beta_min (float, optional): minimum beta (initial beta in SA).
            beta_max (float, optional): maximum beta (final beta in SA).
            num_reads (int, optional): number of samples. Defaults to 1.
            mc_steps (int, optional): number of MonteCarlo steps.
            timeout (float optional): number of timeout for post request. Defaults to None. 
        Returns:
            dimod.SampleSet: store minimum energy samples
                             .info['energy'] store all sample energies
        """

        if beta_min and beta_max:
            if beta_min > beta_max:
                raise ValueError('beta_min < beta_max')

        return super().sample(
            bqm, num_reads, mc_steps,
            beta_min=beta_min, beta_max=beta_max,
            timeout=timeout
        )
