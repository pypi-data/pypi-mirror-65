
# my_lambdata/my_script.py

import pandas
import sys
import time

from my_lambdata.my_mod import enlarge

print("______________")



x = 5
print("NUMBER", x)
print("ENLARGED NUMBER", enlarge(x))  # invoking our function


print("Hello World")

df = pandas.DataFrame({"state": ["CT", "CO", "CA", "TX"]})
print(df.head())


def slowprint(s):
  for c in s + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(1./10)

if __name__ == "__main__":
  slowprint("Hello again, old friend, Come and listen to my story about a man named Jed, A poor mountaineer, barely kept his family fed, And then one day he was shootin at some food,And up through the ground come a bubblin crude.")

  slowprint("Oil that is, black gold, Texas tea., Well the first thing you know ol Jed's a millionaire, The kinfolk said Jed move away from there Said Californy is the place you ought to be")

  slowprint("So they loaded up the truck and they moved to Beverly, Hills, that is. Swimmin pools, movie stars.")

  slowprint("Well now it's time to say good bye to Jed and all his kin, And they would like to thank you folks fer kindly droppin in, You're all invited back next week to this locality")

  slowprint("To have a heapin helpin of their hospitality, Hillbilly that is. Set a spell, Take your shoes off, Y'all come back now, y'hear?")
