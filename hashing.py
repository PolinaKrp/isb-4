import hashlib
import logging
from work_with_file import read_settings, write_settings


def check_hash(card_center: int, card_begin: int) -> int:
    """
    Hash check function
    """
    logging.info("Hash check")
    card_number = f"{card_begin}{card_center}{settings['last_digits']}"
    card_hash = hashlib.sha224(card_number.encode()).hexdigest()
    if settings['hash'] == card_hash:
        return card_number
    return False


def algorithm_Luhn(number: str) -> bool:
    """
    A function that checks the card number with Luhn's algorithm
    """
    check = 7
    all_number = list(map(int, number))
    all_number = all_number[::-1]
    for i, num in enumerate(all_number):
        if i % 2 == 0:
            tmp = num*2
            if tmp > 9:
                tmp -= 9
            all_number[i] = tmp
    total_sum = sum(all_number)
    rem = total_sum % 10
    if rem != 0:
        check_sum = 10 - rem
    else:
        check_sum = 0
    return True if check_sum == check else False