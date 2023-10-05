
import detectEnglish
import string


def decryptMessage(LETTERS, key, message):
    translated = ''

    for symbol in message:
        if symbol in LETTERS:
            num = LETTERS.find(symbol) # get the number of the symbol
            num = num - key

            if num >= len(LETTERS):
                num = num - len(LETTERS)
            elif num < 0:
                num = num + len(LETTERS)

            # add number's symbol at the end of translated
            translated = translated + LETTERS[num]

        else:
            # just add the symbol without encrypting/decrypting
            translated = translated + symbol

    return translated


def cryptoAnalysis(LETTERS, message):
    for key in range(len(LETTERS)):
        translated = decryptMessage(LETTERS, key, message)
        if(detectEnglish.isEnglish(translated)):
            print("Decryption Key : ", key, "\t \t MSG :", translated)

if __name__ == "__main__":
    LETTERS = string.ascii_letters
    print("LETTERS: ", LETTERS)
    message = "TcXLSR PERKYEKI MRJSVQEXMSR WIGYVMXc ERH TVSKVEQQMRK"
    print("Ciphertext: ", message)

    cryptoAnalysis(LETTERS, message)