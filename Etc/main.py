# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    for i in name:
        print(i)

# Press the green button in the gutter to run the script.
def func():
    dataList = [10,20,30,40,50]
    sum = 0
    for i in dataList:
        sum += i
    print(sum)


def enc(plainText, key):
    pass


if __name__ == '__main__':
    print_hi(' PyCharm')
    func()
    plainText = input('PlainText : ')
    key = int(input('Key :'))
    enc(plainText, key)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
