print('#b064--------------------------------------------------')
def f():
   return 1, 2, 3
x = f()
print(type(x))
print('#c065--------------------------------------------------')
def xyz():
    x=1
print(xyz())
print('#b066--------------------------------------------------')
def add(a,b=1):
   return a + b
print(add(3))
print('#a067--------------------------------------------------')
x=10
def f():
   x = 20
f()
print(x)
print('#b069--------------------------------------------------')
b=2
print(list(filter(lambda x: x>2,[1,b,3,4])))
print('#b070--------------------------------------------------')
print(sorted([3,1,2]))
print(reversed([5,7,12]))
print(list(reversed([5,7,12])))
print(list(reversed([3,1,2])))
print(sorted([3,1,2], key=lambda x:-x))
print('#b073--------------------------------------------------')
print({"a":1}["a"])
print('#b080--------------------------------------------------')
import math
# CHANGE THIS VALUE TO TEST DIFFERENT CASES:
# Options to try: [12, 18], (24, 36, "lcm"), or [45, 9]
data = (24, 36, "lcm") # [45, 9]  
match data:
    # CASE 1: Destructuring & Extraction with an 'if' Guard
    # Matches a list of exactly two integers, extracts them, and checks the 0-36 range.
    case [int(a), int(b)] if 0 <= a <= 36 and 0 <= b <= 36:
        print(f"🎯 Case 1 (Range 0-36) -> GCD of {a} and {b} is: {math.gcd(a, b)}")
    # CASE 2: Unpacking a mixed Tuple/List with a Command
    # Unpacks exactly 3 items where the last item must be the string "lcm".
    case [int(a), int(b), "lcm"]:
        print(f"🚀 Case 2 (LCM Mode) -> LCM of {a} and {b} is: {math.lcm(a, b)}")
    # CASE 3: The Wildcard Catch-All (Default)
    # Extracts whatever messy data was passed so we can flag it.
    case _:
        print(f"❌ Case 3 -> Data structure '{data}' did not match any allowed rules.")
print('#a081--------------------------------------------------')
def fak(n):
   if n<=1:
        return 1
   return n*fak(n-1)
print(fak(4))
print('#b083--------------------------------------------------')
import math
import time
print("🛫 Piper J3C rolling down the runway... (Press Ctrl+C to jump out!)")
time.sleep(1)
try:
    # 🌀 The Infinite Loop (The Spinning Propeller)
    while 1 == 0: #True:
        print("🛸 Flying mid-air... engine purring... loop spinning...")
        time.sleep(0.8)  # Just slowing it down so the terminal doesn't scroll too fast

except KeyboardInterrupt:
    # 🪂 The Parachute deploys here! No Nuke-Cloud, no ugly error traceback.
    print("\n🪂 JUMP! The side-door slams open! Parachute deployed safely.")
    print("👟 Soft landing right on the center line of the runway.")
print("🏁 Ground control: Script finished naturally and safely.")
print('#b085--------------------------------------------------')
try:
  raise ValueError("Michael")
except ValueError as e:
  print(str(e) + ":I'm bad bad bad")  
finally:
  print("so what?")
print('#c091-b092---------------------------------------------')
lst = [3,1,2]
print(lst.sort())
print(id(sorted(lst)))
print(id(lst))
print(lst)
print('#b093--------------------------------------------------')
print({"a":1,"b":2}.get("c",17))
print("is better than None..")
print({"a":1,"b":2}.get("b",17))
print("drops the fallback 17...")
print('#b095--------------------------------------------------')
a = 3
b = 4
ab =["a","b"]
cd =[ a, b ]
zipped=zip(ab,cd)
for i,j in zipped:
    print(i," zipped with ",j)
print('#b096--------------------------------------------------')
pairs = [(2*a+1, 3*b-3) for a, b in zip(range(3), range(3))]
print(pairs)
grid = [(2*a+1, 3*b-3) for a in range(3) for b in range(3)]
print(grid)
even = [x for x in range(9) if x%2==0]
print(even)
evodd = [(x, y) for x, y in zip(range(0, 10, 2), range(1, 10, 2))]
print(evodd)         
print('#b098--------------------------------------------------')
print("allTrue ",all([True,True,True,True]))
print("anyFalse",any([True,True,True,True]))
print("allTrue ",all([True,False,True,True]))
print("anyFalse",any([True,True,False,True]))
print('#b099--------------------------------------------------')
print(enumerate(["a","b","c"]))
enum=["a","b","c"]
print(enum)
for i in range(2):
   print(enum[i], end=" ")
print()   
for i in range(2):
   print("(",i,enum[i], end=")")
print()
print('#b100--------------------------------------------------')
print('append')
lst=[]
lst.append([])
print(len(lst),":",lst)
lst=[]
lst.append([4,5])
print(len(lst),":",lst)
lst=[1,2,3]
print('lst.append([4,5])')
lst.append([4,5])
print(len(lst),":",lst)
print('--------------')
lst=[1,2,3]
lst.append(4)
print(len(lst),":",lst)
print('insert')
lst=[1,2,3]
print('lst.insert([2,4])')
lst.insert(2,4)
print(len(lst),":",lst)
print('#c101--------------------------------------------------')
print('insert')
lst=[1,2,3]
lst.insert(0,5)
print('lst.insert(0,5)')
print(lst)
print('insert')
lst=[1,2,3]
lst.insert(1,5)
print('lst.insert(1,5)')
print(lst)
print('append')
lst=[1,2,3]
print('lst.append([4,5])')
lst.append([4,5])
print(lst)
print('extend')
lst=[1,2,3]
print('lst.extend([4,5])')
lst.extend([4,5])
print(lst)
print('#b102-a103----------------------------------------------')
lst=[1]
print(lst)
print('lst.pop()')
print(lst.pop())
lst=[1,2,3]
print(lst)
print('lst.pop()')
print(lst.pop())
lst=[1,2,3]
print(lst)
print('lst.pop(0)')
print(lst.pop(0))
lst=[1,2,3]
print(lst)
print('lst.pop(1)')
print(lst.pop(1))
lst=[1,2,3]
print(lst)
print('lst.pop(2)')
print(lst.pop(2))
lst=[1,2,3]
print(lst)
print('lst.pop(-1)')
print(lst.pop(-1))
print('#b104--------------------------------------------------')
lst=[1,2,3,4,2]
print(lst)
print('lst.remove(2)')
lst.remove(2)
print(lst)
print('#---------')
lst=[1,2,3,4,2]
print(lst)
print('lst.remove(3)')
lst.remove(3)
print(lst)
print('#---------')
lst=[1,2,3,4,2]
print(lst)
print('lst.remove(2)')
lst.remove(2)
print(lst)
print('#---------')
print('lst.remove(2)')
lst.remove(2)
print(lst)
print('#b105--------------------------------------------------')
lst=[1, 7, 3, 4, 2]
print(lst)
print('lst.index(7)')
print(lst.index(7))
print('#c106--------------------------------------------------')
lst=[1, 7, 3, 1, 4, 1]
print(lst)
print('lst.count(1)')
print(lst.count(1))
print('lst.count(7)')
print(lst.count(7))
print('#a107--------------------------------------------------')
lst=[1, 7, 3, 1, 4, 1]
print(lst)
print('lst.insert(2,99)')
lst.insert(2,99)
print(lst)
print('#c108--------------------------------------------------')
lst=[1, 7, 3, 1, 4, 1]
print(lst)
print('lst.reverse()')
lst.reverse()
print(lst)
print('#a109--------------------------------------------------')
ls1=[1, 7, 3]
ls2=[4, 1]
print(ls1)
print(ls2)
print('------')
print('ls1 + ls2')
print(ls1 + ls2)
print('------')
print('ls1.extend(ls2)')
ls1.extend(ls2)
print(ls1)
print('------')
ls1=[1, 7, 3]
ls2=[4, 1]
print(ls1)
print(ls2)
print('------')
print('ls2.extend(ls1)')
ls2.extend(ls1)
print(ls2)
print('#a110-------------------------------------------------')
strg ="hello"
print('strg:',strg)
print('strg[::2]')
print(strg[::2])
print('strg[:2]')
print(strg[:2])
print('strg[2::]')
print(strg[2::])
print('strg[2:]')
print(strg[2:])
print('strg[:]')
print(strg[:])
print('strg[0:]')
print(strg[0:])
print('strg[0::]')
print(strg[0::])
print('strg[:0]')
print(strg[:0])
print('str1=strg[:0]')
str1=strg[:0]
print(str1)
print('strg[::0]')
print(strg[::0])
print('ValueError: slice step cannot be zero')
print('#a111-------------------------------------------------')





