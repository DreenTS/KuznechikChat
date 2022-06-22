from typing import List
from gost import consts


def data_splitting(data: str) -> List[list]:
    """
    Функция "конвертации" сообщения из строки в блоки данных.

    :param data: str, текст отправляемого сообщения
    :return: list, сообщение, представленное в виде блоков
    """

    int_list_msg = list(data.encode(encoding='utf-8'))
    remain = len(int_list_msg) % 16
    data_blocks = [[0] * (16 - remain) + int_list_msg[:remain]]
    for i in range(remain, len(int_list_msg[remain:]), 16):
        data_blocks.append(int_list_msg[i:i + 16])
    return data_blocks


def xor_transform(a: List[int], b: List[int]) -> List[int]:
    """
    Функция побитового сложения по модулю 2 (XOR).

    :param a: A-блок данных
    :param b: B-блок данных
    :return: list, результирующий блок
    """

    return [a[i] ^ b[i] for i in range(len(a))]


def nonlinear_transform(x_list: List[int], inverse: bool = False) -> List[int]:
    """
    Функция нелинейного биективного преобразования.

    :param x_list: list, входной блок данных
    :param inverse: bool, флаг, указывающий, является ли преобразование обратным (при дешифровании)
    :return: list, результирующий блок
    """

    _consts = consts.INVERSE_NONLINEAR_CONSTS if inverse else consts.NONLINEAR_CONSTS
    return [_consts[x % 256] for x in x_list]


def linear_transform(x_list: List[int], inverse: bool = False) -> List[int]:
    """
    Функция линейного преобразования в поле Галуа GF(2^8).

    :param x_list: list, входной блок данных
    :param inverse: bool, флаг, указывающий, является ли преобразование обратным (при дешифровании)
    :return: list, результирующий блок
    """

    galois_cs = consts.GALOIS_FIELD_CONSTS
    linear_cs = consts.LINEAR_CONSTS
    result_list = x_list[:]
    for i in range(len(result_list)):
        xor_sum = 0
        if inverse:
            result_list.append(result_list.pop(0))
        for j in range(len(result_list)):
            if result_list[j] != 0:
                x_power = galois_cs.index(result_list[j])
                const_power = galois_cs.index(linear_cs[j])
                xor_sum ^= galois_cs[(x_power + const_power) % 255]
        if inverse:
            result_list[-1] = xor_sum
        else:
            result_list.insert(0, xor_sum)
            result_list.pop(-1)
    return result_list


def feistel_network(left: List[int], right: List[int], const_ind: int) -> List[list]:
    """
    Функция отработки ячейки сети Фейстеля.

    :param left: list, L-блок сети Фейстеля
    :param right: list, R-блок сети Фейстеля
    :param const_ind: int, индекс для текущей итерационной константы
    :return: list, результирующая пара ключей [K(i)', K(i+1)']
    """

    const = consts.ITER_CONSTS[const_ind]
    temp_res = xor_transform(a=left, b=const)
    temp_res = nonlinear_transform(x_list=temp_res)
    temp_res = linear_transform(x_list=temp_res)
    temp_res = xor_transform(a=temp_res, b=right)
    return [temp_res, left]


def cryptographic_transformation(msg: List[int], keys: List[list], in_range: range,
                                 last_ind: int, inverse: bool = False) -> List[int]:
    """
    Функция криптографического преобразования сообщения.

    Выполняет шифрование/дешифрование сообщения (блока данных).

    :param msg: list, блок сообщения
    :param keys: list, блоки раундовых ключей
    :param in_range: range, диапазон индексов для раундовых ключей
    :param last_ind: int, индекс раундового ключа для 10 раунда
    :param inverse: bool, флаг, указывающий, является ли преобразование обратным (при дешифровании)
    :return: list, результирующий блок
    """

    result = msg[:]
    func_list = [nonlinear_transform, linear_transform]
    if inverse:
        func_list.reverse()
    for i in in_range:
        result = xor_transform(a=result, b=keys[i])
        result = func_list[0](x_list=result, inverse=inverse)
        result = func_list[1](x_list=result, inverse=inverse)
    result = xor_transform(a=result, b=keys[last_ind])
    return result
