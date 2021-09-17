import re

word_1, word_2 = input(), input()
matches = bool(re.match(word_1, word_2))
print(len(word_1) * 2 if matches else "no matching")
