from typing import List


class TextSequencePadding:
    def __init__(self, value: str, length: int=None):
        self.length = length
        self.value = value

    def fit(self, input_data: List[List[str]]) -> List[List[str]]:
        if self.length is None:
            self.length = max([len(i) for i in input_data])

        result_list = []
        for line_data in input_data:
            result = self._process_line(line_data)
            result_list.append(result)

        return result_list

    def _process_line(self, line_data: List[str]) -> List[str]:
        # early stop
        if len(line_data) == self.length:
            return line_data

        if len(line_data) > self.length:  # truncate
            return line_data[:self.length]

        # need padding now
        padding_list = [self.value] * (self.length - len(line_data))

        return line_data + padding_list

