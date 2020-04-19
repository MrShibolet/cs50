from cs50 import get_int
from cs50 import get_string
import sys
def main():
    card = get_card()
    validate(card)

def get_card():
    credit = get_int("Number: ")
    length = len(str(credit))
    if length != 13 and length != 15 and length != 16:
        print("INVALID\n")
        sys.exit()
    else:
        return credit

def validate(card):
    length = len(str(card))
    dig1 = 0
    dig2 = 0
    sum1 = 0
    sum2 = 0
    digcount = 0
    while card > 0:
        dig2 = dig1
        dig1 = card % 10
        if digcount % 2 == 0:
            sum1 += dig1
        else:
            sum2 = sum2 + ((dig1*2)//10) + ((dig1*2)%10)
        card = card // 10
        digcount += 1
    validtest = (sum1 + sum2) % 10
    fdig = (dig1*10) + dig2
    if length >= 13 and length <=16 and dig1 ==4 and validtest == 0:
        print("VISA\n")
    elif fdig <=55 and fdig >= 51 and length == 16 and validtest ==0:
        print("MASTERCARD\n")
    elif length == 15 and validtest == 0 and (fdig == 34 or fdig == 37):
        print("AMEX\n")
    else:
        print("INVALID\n")

main()