from typing import List
import gost.utils as utils


class GOST34122018:
    """
    Класс класса для шифрования/дешифрования при помощи ГОСТ 34.12-2018.

    """

    ENCRYPT_FLAG = 'encrypt'
    DECRYPT_FLAG = 'decrypt'

    def __init__(self, master_key):
        self.round_keys = self.get_round_keys(master=master_key)

    def get_round_keys(self, master: List[int]) -> List[list]:
        """
        Метод формирования раундовых ключей.

        Вычисляет 32 раунда сети Фейстеля, формируя 10 раундовых ключей.

        :param master: list, мастер-ключ K
        :return: list, список раундовых ключей, представленных в виде блоков
        """

        result_list = [master[:16], master[16:]]
        left_key, right_key = result_list[0], result_list[1]
        for i in range(4):
            for j in range(8):
                curr_index = 8 * i + j
                left_key, right_key = utils.feistel_network(left=left_key, right=right_key, const_ind=curr_index)
            result_list.extend([left_key, right_key])
        return result_list

    def message_prehandling(self, msg: List[int], flag: str) -> List[int]:
        """
        Метод предобработки сообщения.

        В зависимости от флага, определяет порядок индексов для итераций и порядок функций преобразований.
        Вызывает функцию криптографического преобразования.

        :param msg: list, сообщение, представленное в виде блоков
        :param flag: str, флаг, указывающий на шифрование/дешифрование сообщения
        :return: list, зашифрованное/дешифрованное сообщение, представленное в виде блоков
        """

        if flag not in [self.ENCRYPT_FLAG, self.DECRYPT_FLAG]:
            raise ValueError
        if flag == self.ENCRYPT_FLAG:
            curr_range = range(9)
            last_xor_ind = 9
            inverse = False
        else:
            curr_range = range(9, 0, -1)
            last_xor_ind = 0
            inverse = True
        result = utils.cryptographic_transformation(msg=msg,
                                                    keys=self.round_keys,
                                                    in_range=curr_range,
                                                    last_ind=last_xor_ind,
                                                    inverse=inverse)
        return result
