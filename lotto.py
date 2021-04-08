from random import *
import sys
from time import *

class RangeError(Exception):
    pass

lotto_nums = [i+1 for i in range(45)]
lotto_prize = {6:1400000000, 5:1200000, 4:50000, 3:5000} 

PRINTER_MONEY_INPUT_ERROR_MESSAGE = "ERROR: 숫자만 입력해주세요."
PRINTER_MONEY_INPUT_MESSAGE = "> 구입금액을 입력해주세요."
PRINTER_NOMONEY_MESSAGE = "ERROR: 적어도 1000원 이상 입력해주세요."
PRINTER_PLEASE_INPUT_WINNER_MESSAGE = '\n> 지난주 당첨 번호를 입력해주세요. (랜덤으로 생성하려면 r 입력)'
PRINTER_LOTTO_NEEDS_SIX = "ERROR: 로또는 6개의 숫자로 이루어져 있습니다."
PRINTER_LOTTO_INPUT_ERROR_MESSAGE = "ERROR: 로또 숫자는 1 이상 45 이하의 정수입니다."
PRINTER_REPEATED_NUMBER_ERROR_MESSAGE = "ERROR: 로또 숫자는 중복될 수 없습니다."


def printer_space():
    print()

def printer_money_input():
    print(PRINTER_MONEY_INPUT_MESSAGE)

def printer_nomoney():
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
                printer_nomoney()
                continue
        except:
            printer_money_input_error()
        finally:
            sleep(0.5)
            printer_space()

def printer_lotto_bought(lotto_bought_number):
    print("> {}장의 로또를 구입하셨습니다.".format(lotto_bought_number))
    sleep(0.5)

def pick_lotto_number(lotto_bought_number):
    lotto_bought_list = []
    for i in range(lotto_bought_number):
        new_lotto_pick = sample(lotto_nums, 6)
        lotto_bought_list.append(sorted(new_lotto_pick))
    return lotto_bought_list

def printer_lotto_list(lotto_bought_list):
    for lotto in lotto_bought_list:
        print(lotto)

def printer_please_input_winner():
    sleep(0.5)
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

def get_winning_number(): # 유효성 검사들을, boolean을 return하는 함수로 따로 분리할걸.. 이라고 중간에 후회했을 때라도 다시 할걸.. 굉장히 불편하다
    while True:
        try:
            printer_please_input_winner()
            inputted_line = sys.stdin.readline().rstrip()
            if inputted_line == "r" or inputted_line == "R": # 당첨번호 자동추첨하기
                return get_random_winning_number()
            winning_number = list(map(int,inputted_line.split(',')))
            if len(winning_number) == 6: # 당첨번호 갯수확인
                if len(set(winning_number)) == 6: # 당첨번호 중복확인
                    for number in winning_number:
                        if number < 1 or number > 45: # 당첨번호 범위확인
                            raise RangeError # 분명 더 깔끔한 방법이 있을텐데.. 창의력의 한계
                    return winning_number
                else:
                    printer_repeated_number_error()
            else:
                printer_lotto_needs_six()
        except: # 당첨번호 정수 아니면 거르기
            printer_lotto_input_error()

def get_result(lotto_bought_list,winning_number):
    result = {6:0, 5:0, 4:0, 3:0, 2:0, 1:0, 0:0}
    for lotto in lotto_bought_list:
        count = 0
        for number in lotto:
            if number in winning_number:
                count += 1
        result[count] += 1
    return result

def printer_result(result,lotto_bought_number): #어떻게 쓰면 직관적일까 고민하다 뇌가 파업해버림
    sleep(0.5)
    print("\n> 로또 당첨 결과")
    sleep(0.5)
    for i in range(4):
        print("{0}등({1}개가 맞을 때) - {2:,}원 - {3}개".format(4-i, i+3, lotto_prize[i+3], result[i+3]))
        sleep(0.3)
    sleep(0.5)
    prize = sum([lotto_prize[i+3]*result[i+3] for i in range(4)])
    print("\n> 수익률")
    sleep(0.5)
    print("{0:0.2f}배".format(prize/(lotto_bought_number*1000)))


def run():
    lotto_bought_number = buy_lotto() # 구입할 로또 갯수 구하기
    lotto_bought_list = pick_lotto_number(lotto_bought_number) # 구입한 로또 갯수만큼 자동으로 번호 찍기
    printer_lotto_bought(lotto_bought_number) # 구입한 로또 갯수 출력하기
    printer_lotto_list(lotto_bought_list) # 자동으로 찍은 숫자들 출력하기
    winning_number = get_winning_number() # 당첨 번호 받기
    result = get_result(lotto_bought_list,winning_number) # 당첨 결과 구하기
    printer_result(result,lotto_bought_number) # 당첨 결과 출력하기

def main():
    run()

if __name__ == "__main__":
    main()