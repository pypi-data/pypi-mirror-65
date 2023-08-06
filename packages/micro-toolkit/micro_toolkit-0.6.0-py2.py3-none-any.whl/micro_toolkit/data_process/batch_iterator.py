class BatchingIterator(object):
    def __init__(self, batch_size):
        self.batch_size = batch_size

    def __call__(self, data, *args, **kwargs):
        if isinstance(data, list):
            return self._do_iterate_list(data)
        if isinstance(data, dict):
            return self._do_iterate_dict(data)

        raise ValueError(
            "{} is not supported. Supported type: list and dict".format(type(data))
        )

    def _do_iterate_list(self, data):
        mini_batch = []

        for i in data:
            mini_batch.append(i)

            if len(mini_batch) == self.batch_size:
                yield mini_batch

                # reset
                mini_batch = []

        if mini_batch:  # if there are some residual data
            yield mini_batch

    def _do_iterate_dict(self, data):
        # import pdb; pdb.set_trace()

        keys = data.keys()
        out_of_range = False

        mini_batch = {k: [] for k in keys}

        idx = 0
        counter = 0

        while not out_of_range:
            for k, v in data.items():
                try:
                    i = v[idx]
                except IndexError:
                    out_of_range = True
                    break

                mini_batch[k].append(i)

            if counter == self.batch_size:
                yield mini_batch

                # reset
                mini_batch = {k: [] for k in keys}
                counter = 0

            idx += 1
            counter += 1

        if counter:  # if there are some residual data
            yield mini_batch
