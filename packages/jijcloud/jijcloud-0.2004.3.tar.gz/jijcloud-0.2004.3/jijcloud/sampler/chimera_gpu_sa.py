from jijcloud.sampler import JijCloudSampler


# class JijChimeraSASampler(JijCloudSampler):
#     hardware = 'GPU'
#     algorithm = 'SA'

#     def sample_ising(self, h, J,
#                      beta_min=None, beta_max=None,
#                      num_reads=1, mc_steps=100):
#         """sample ising
#         Args:
#             h (dict): linear term of the Ising model.
#             J (dict): quadratic term of the Ising model.
#             beta_min (float, optional): minimum beta (initial beta in SA).
#             beta_max (float, optional): maximum beta (final beta in SA).
#             num_reads (int, optional): number of samples. Defaults to 1.
#             mc_steps (int, optional): number of MonteCarlo steps.

#         Returns:
#             dimod.SampleSet: store minimum energy samples
#                              .info['energy'] store all sample energies
#         """

#         if beta_min and beta_max:
#             if beta_min > beta_max:
#                 raise ValueError('beta_min < beta_max')

#         return super().sample_ising(
#             h, J, num_reads, mc_steps,
#             beta_min=beta_min, beta_max=beta_max,
#         )


# def chimera_graph_validation(graph, num_row, num_col):
#     for i, j in graph.keys():
#         ri, ci zi = index_to_chimera(i, num_row, num_col)
#         rj, cj zj = index_to_chimera(j, num_row, num_col)
#         # connect in same cell
#         if ri == rj and ci == cj:
#             pass


# def index_to_chimera(index: int, num_row: int, num_col: int):
#     if index >= num_col * num_row * 8:
#         raise ValueError('0 <= index <= num_col * num_row * 8')
#     row = index // (8 * num_col)
#     col = (index % (8 * num_col)) // 8
#     z = index - (row * (num_col * 8) + col * 8)
#     return row, col, z
