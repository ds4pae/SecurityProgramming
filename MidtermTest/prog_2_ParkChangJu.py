import random
import string

def randomString():
    string_pool = string.ascii_letters
    result = ""
    for i in range(8):
        result += random.choice(string_pool)
    return result

def main():
    print('Random String (StringLength : 8) is  ', randomString())
    print('Random String (StringLength : 8) is  ', randomString())

if __name__ == "__main__":
    main()



