import string

message = "hanshin university computer engineering information security and programming 2023"

f = open('dictionary.txt', 'r')

englishDic = {}
splitedFile = f.read().split()
splitedMessage = message.split()
matchCount = 0
for word in splitedMessage:
    if word.upper() in splitedFile:
        matchCount+=1
f.close()
print(matchCount)



print("wordPercentage: ", float(matchCount/len(splitedMessage))*100,"%")

LETTERS = string.ascii_letters
message_only_letters = ""

for char in message:
    if char in LETTERS:
        message_only_letters += char

print("letterPercentage : ", float(len(message_only_letters) / len(message) * 100))
