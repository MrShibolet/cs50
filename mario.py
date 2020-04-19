from cs50 import get_int
def main():
    height = 0
    while height >= 9 or height <= 0:
        height = get_int("Height: ")
    for i in range(1,height +1):
        block = i
        space = height - block
        print(" " * space, end="")
        print("#" * block, end="")
        print("  ",end="")
        print("#" * block)
main()