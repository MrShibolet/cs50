from cs50 import get_string

def main():
    word = 0
    letter = 0
    sentence = 0
    text =get_string("Text: ")
    word = len(text.split())
    sentence = text.count('.') + text.count('!') + text.count('?')
    for char in text:
        if char.isalpha():
            letter += 1
    index = 0.0588 * ((100/word)*letter) - 0.296 * ((100/word)*sentence) - 15.8
    if round(index) < 1:
        print("Before Grade 1")
    elif round(index) > 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(index)}")
main()