import numpy as np


class Spreading:
    @staticmethod
    def get_modeling_spreading_time(timer, model, num_iter, comm=None):
        times = []
        for _ in np.arange(num_iter):
            n = model.iteration_bunch(comm)
            df_times = timer.get_times(n)
            times.append(np.sum(df_times))
        return times

    @staticmethod
    def get_modeling_spreading_time_complex(timer, model, num_iter, comm):
        times = []
        comm_times = []

        for _ in np.arange(num_iter):
            k, n = model.iteration_bunch_complex(comm)
            df_times = timer.get_times(n)
            times.append(np.sum(df_times))
            comm_times.append(np.sum(df_times[:k]))
            print("iteration", _)
        return comm_times, times
