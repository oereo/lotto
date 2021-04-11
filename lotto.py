from random import *
import sys
from time import sleep as delay_time

PRINTER_MONEY_INPUT_ERROR_MESSAGE = "ERROR: 숫자만 입력해주세요."
PRINTER_MONEY_INPUT_MESSAGE = "> 구입금액을 입력해주세요."
PRINTER_NOMONEY_MESSAGE = "ERROR: 적어도 1000원 이상 입력해주세요."
PRINTER_PLEASE_INPUT_WINNER_MESSAGE = '\n> 지난주 당첨 번호를 입력해주세요. (랜덤으로 생성하려면 r 입력)'
PRINTER_LOTTO_NEEDS_SIX = "ERROR: 로또는 6개의 숫자로 이루어져 있습니다."
PRINTER_LOTTO_INPUT_ERROR_MESSAGE = "ERROR: 로또 숫자는 1 이상 45 이하의 정수입니다."
PRINTER_REPEATED_NUMBER_ERROR_MESSAGE = "ERROR: 로또 숫자는 중복될 수 없습니다."

lotto_nums = [i+1 for i in range(45)]
lotto_prize = {1: 1400000000, 2: 1200000, 3: 50000, 4: 5000} #등수별 상금
lotto_score = {1: 6, 2: 5, 3: 4, 4: 3} #등수별 맞춘 갯수


class NotSixError(Exception):
    pass


class RepeatedNumberError(Exception):
    pass


def printer_space():
    print()


def printer_money_input():
    print(PRINTER_MONEY_INPUT_MESSAGE)


def printer_no_money():
    print(PRINTER_NOMONEY_MESSAGE)


def printer_money_input_error():
    print(PRINTER_MONEY_INPUT_ERROR_MESSAGE)


def printer_lotto_input_error():
    print(PRINTER_LOTTO_INPUT_ERROR_MESSAGE)


def printer_repeated_number_error():
    print(PRINTER_REPEATED_NUMBER_ERROR_MESSAGE)


def buy_lotto():
    while True:
        try:
            printer_money_input()
            money = int(sys.stdin.readline().rstrip())
            lotto_bought_number = money//1000
            if lotto_bought_number >= 1:
                return lotto_bought_number
            else:
                printer_no_money()
                continue
        except:
            printer_money_input_error()
        finally:
            delay_time(0.5)
            printer_space()


def printer_lotto_bought(lotto_bought_number):
    print("> {}장의 로또를 구입하셨습니다.".format(lotto_bought_number))
    delay_time(0.5)


def pick_lotto_number(lotto_bought_number):
    lotto_bought_list = []

    # 이럴 때 counter 처럼 사용되지 않을 변수명은 뭐로 하는게 일반적인가요?
    for counter in range(lotto_bought_number):
        new_lotto_pick = sample(lotto_nums, 6)
        lotto_bought_list.append(sorted(new_lotto_pick))

    return lotto_bought_list


def printer_lotto_list(lotto_bought_list):
    for lotto in lotto_bought_list:
        print(lotto)


def printer_please_input_winner():
    delay_time(0.5)
    print(PRINTER_PLEASE_INPUT_WINNER_MESSAGE)


def printer_lotto_needs_six():
    print(PRINTER_LOTTO_NEEDS_SIX)


def printer_random_winning_number(random_winning_number):
    print("당첨 번호:", end=" ")
    print(random_winning_number)


def get_random_winning_number():
    random_winning_number = sorted(sample(lotto_nums, 6))
    printer_random_winning_number(random_winning_number)
    return random_winning_number


def get_winning_number():
    # 이렇게 오류 만들어서 예외처리 하는 건 장기적으로 안 좋을까요?

    while True:
        try:
            printer_please_input_winner()
            inputted_line = sys.stdin.readline().rstrip()
            if inputted_line == "r" or inputted_line == "R":  # 당첨번호 자동추첨하기
                return get_random_winning_number()
            winning_number = list(map(int, inputted_line.split(',')))
            if len(winning_number) != 6:
                raise NotSixError
            if len(set(winning_number)) != len(winning_number):
                raise RepeatedNumberError
            for number in winning_number:
                if number < 1 or number > 45:
                    raise ValueError
            return winning_number
        except NotSixError:
            printer_lotto_needs_six()
        except RepeatedNumberError:
            printer_repeated_number_error()
        except ValueError:
            printer_lotto_input_error()


def get_result(lotto_bought_list, winning_number):

    #  바로 밑의 printer_result 함수를 직관적으로 만드려고 하니 반대로 이쪽이 번잡해졌네요. 마치 풍선효과 ^^..
    correct_number_counter = {6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
    result = {1: 0, 2: 0, 3: 0, 4: 0}
    for lotto in lotto_bought_list:
        count = 0
        for number in lotto:
            if number in winning_number:
                count += 1
        correct_number_counter[count] += 1
    for rank in range(1, 5):
        result[rank] = correct_number_counter[lotto_score[rank]]
    return result


def printer_result(result, lotto_bought_number):
    delay_time(0.5)
    print("\n> 로또 당첨 결과")
    delay_time(0.5)
    for rank in range(4, 0, -1):
        print("{0}등({1}개가 맞을 때) - {2:,}원 - {3}개".format(rank, lotto_score[rank], lotto_prize[rank], result[rank]))
        delay_time(0.3)
    delay_time(0.5)
    prize = sum([lotto_prize[rank]*result[rank] for rank in range(1 ,5)])
    print("\n> 수익률")
    delay_time(0.5)
    print("{0:0.2f}배".format(prize/(lotto_bought_number*1000)))


def run():
    lotto_bought_number = buy_lotto()  # 구입할 로또 갯수 구하기
    lotto_bought_list = pick_lotto_number(lotto_bought_number)  # 구입한 로또 갯수만큼 자동으로 번호 찍기
    printer_lotto_bought(lotto_bought_number)  # 구입한 로또 갯수 출력하기
    printer_lotto_list(lotto_bought_list)  # 자동으로 찍은 숫자들 출력하기
    winning_number = get_winning_number()  # 당첨 번호 받기
    result = get_result(lotto_bought_list, winning_number)  # 당첨 결과 구하기
    printer_result(result, lotto_bought_number)  # 당첨 결과 출력하기


def main():
    run()


if __name__ == "__main__":
    main()
