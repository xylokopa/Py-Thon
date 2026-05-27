print('#b062--------------------------------------------------')
print(list(range(3,3)))
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
d = {"a":1,"b":2}
e = d.get("c",17)
print(d)
print(e)
print({"a":1,"b":2}.get("c",0))
print("is better than None..")
print({"a":1,"b":2}.get("b",0))
print("drops the fallback 0...")
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
lst=[1, 2, 3]
print(lst)
print('lst.reverse()')
lst.reverse()
print("lst.reverse() in-place gives none for ",lst)
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
#print('strg[::0]')
#print(strg[::0])
#print('ValueError: slice step cannot be zero')
print('#a111-------------------------------------------------')
print('3 in [1,2,3]')
print(3 in [1,2,3])
print('#b112-------------------------------------------------')
print('a,b =(1,2)')
a,b =(1,2)
print('a:',a,'b:',b)
print('#b113-------------------------------------------------')
a = 1
b = 2
print('a:',a,'b:',b)
print('a,b = b,a')
a,b = b,a
print('a:',a,'b:',b)
print('#c114-------------------------------------------------')
print('(5):' ,(5) )
print('[5]:' ,[5] )
print('(5,):',(5,))
print('{5}:' ,{5} )
print('#b115-------------------------------------------------')
print('a=()')
a=()
print('():',type(a))
print('#b116-------------------------------------------------')
print('a={}')
a={}
print('{}:',type(a))
print('#c117-------------------------------------------------')
print('a={}')
a={}
print('a:',type(a))
print('b=[]')
b=[]
print('b:',type(b))
print('c=set()')
c=set()
print('c:',type(c))
print('c=empty_set()')
#c=empty_set()
#print('c:',type(c),'name empty_set is not defined')
print('#b118a119---------------------------------------------')
print('s={1,2,3}')
print('t={3,4}')
s={1,2,3}
t={3,4}
print('s|t=',s|t)
print('s-t=',s-t)
print('#a120-------------------------------------------------')
print('d={"a":1,"b":2}')
d={"a":1,"b":2}
print('d["a"]:',d["a"])
print('#b121-------------------------------------------------')
print('d={"a":1,"b":2}')
d={"a":1,"b":2}
print('list(d.keys()',list(d.keys()))
print('#b122-------------------------------------------------')
print('d={"a":1,"b":2}')
d={"a":1,"b":2}
print('list(d.values()',list(d.values()))
print('#a123-------------------------------------------------')
print('d={"a":1,"b":2}')
d={"a":1,"b":2}
print('list(d.items()',list(d.items()))
print('#a124-------------------------------------------------')
print('e = {x: x**2 for x in range(4)}')
e = {x: x**2 for x in range(4)}
print('e =',e)
print('#b125-------------------------------------------------')
print('d={"a":1,"b":2}')
d={"a":1,"b":2}
d.update({"c":3})
print('d.update({"c":3})')
print('d:',d)
print('#b126-------------------------------------------------')
d={"a":1,"b":2}
del d["a"]
print('d:',d)
print('#b127-------------------------------------------------')
print('any([False,0,None,""])')
print("anyFalse=",any([False,0,None,""]))
print('#a128-------------------------------------------------')
print('min([3,1,2,5]):',min([3,1,2,5]))
print('#b129-------------------------------------------------')
print('sorted(["banana","pie","apple"],key=len):',sorted(["banana","pie","apple"],key=len))
print('#a130-------------------------------------------------')
d={"a":[1,2],"b":[3,4]}
for k,v in d.items():
   print(k,sum(v))
print('#b131-------------------------------------------------')
print('t=(1 , 2 , 3)')
t=(1 , 2 , 3)
print('t[0] = 10')
# t[0] = 10
print('tuple object does not support item assignment')
print('#a132-------------------------------------------------')
print('set([1,2,2,3]):',set([1,2,2,3]))
print('#b133-------------------------------------------------')
lst =[ 1,2,3,4,5,6,7,8,9]
print('lst:',lst)
print('lst[1::2]',lst[1::2])
print('lst[::2]',lst[::2])
print('lst[2::]',lst[2::])
print('lst[::-2]',lst[::-2])
print('#c134-------------------------------------------------')
mat =[[1,2],[3,4],[5,6]]
print('mat:',mat)
print('mat[1][0]:',mat[1][0])
print('#a135-------------------------------------------------')
print('"".join(["a","b","c"])',"".join(["a","b","c"]))
print('#c136-------------------------------------------------')
print('from one import myConst()')
print('#c137-------------------------------------------------')
print('import math gives access to math.pi')
print('#b138-------------------------------------------------')
import datetime
print('str="21.4.26, 12:15"')
str="21.4.26, 12:15"
print('dt = datetime.datetime.strptime(str, "%d.%m.%y, %H:%M")')
dt = datetime.datetime.strptime(str, "%d.%m.%y, %H:%M")
print('dt=',dt)
print('#b139-------------------------------------------------')
print('dt + 7 =',' str is not a datetime object')
print('dt + datetime.timedelta(days=7)',dt + datetime.timedelta(days=7))
print('dt.add(7)',' no add attribute')
print('dt + datetime.date(7) ','missing required argument')
print('#a140-------------------------------------------------')
from decimal import Decimal
z = 0.2
def dual_16(z):
    return f"0.{bin(int(z * 65536))[2:]:0>16}" 
def dsum_16(a, b):
    return f"0.{bin(int(a[2:], 2) + int(b[2:], 2))[2:]:0>16}"
fsum_16 = lambda a, b: f"0.{bin(int((a + b) * 65536))[2:]:0>16}"
#---------------------------------------------------------------
print(' s =  Decimal( 0.1 )+Decimal( 0.2 )')
print(' s = ',Decimal('0.1')+Decimal('0.2'))
print(' z =  0.1 + 0.2')
print(' z = ',0.1+0.2)
print('#c141-------------------------------------------------')
print(' os    : Files , Folders Env.Vars Paths')
print(' pickle: Py-Objects Persistent Storage State Reload ')
print(' re    : Adv.PatternMatch Str Parse & Extract Search&Replace')
print(' math  : Trigs & Logs Spec.Const Prec.Number.Controls')
print('#b142-------------------------------------------------')
print(' pickle: Py-Objects Persistent Storage State Reload ')
print(' Serializing Py-Objects to file & load globally back')
print('#c143-------------------------------------------------')
# Eine einfache Funktion
def addiere(a, b):
    return a + b
# Ein Test, der WAHR ist (Code läuft einfach weiter)
assert addiere(2, 3) == 5
# Ein Test, der FALSCH ist (löst den AssertionError aus)
# assert addiere(1, 1) == 3, "Fehler: 1 + 1 sollte 2 sein, nicht 3!"
print('assert addiere(1, 1) == 3, "Fehler: 1 + 1 sollte 2 sein, nicht 3!"')
print('#b144-------------------------------------------------')
import math
print('math.sqrt(16)=',math.sqrt(16))
print('#a145-------------------------------------------------')
print('math.e=',math.e)
print('#b146-------------------------------------------------')
print('math.log(math.e)=',math.log(math.e))
print('#b147-------------------------------------------------')
print('math.sin(math.pi/2)=',math.sin(math.pi/2))
print('#a148-------------------------------------------------')
print('str="21.4.26, 12:15"')
str="21.4.26, 12:15"
print('dt = datetime.datetime(2026,3,27,12,0)')
dt = datetime.datetime(2026,3,27,12,0)
print('dt.strftime("%Y-%m-%d")',dt.strftime("%Y-%m-%d"))
print('#b149-------------------------------------------------')
print('dt1 = datetime.datetime(2026,3,27,12,0)')
dt1 = datetime.datetime(2026,3,27,12,0)
print('dt2 = datetime.datetime(2026,5,19,12,0)')
dt2 = datetime.datetime(2026,5,19,12,0)
dt  = dt2 - dt1
print('dt2 - dt1',dt2 - dt1)
print(type(dt2 - dt1))
print('#c150-------------------------------------------------')
print('re : Adv.PatternMatch Str Parse & Extract Search&Replace')
import re
print('re.match   : sucht erste ("Anfangs") Zeichen ')
print('re.search  : sucht Muster im string bis Ende / stoppt bei Erfolg')
print('re.findall : durchsucht Gesamt-Text mit Trefferliste ')
print('re.split   : Bereinigen und Zerlegen unstrukturierter Daten')
print('#a151-------------------------------------------------')
print('os     : OS-Prozess Dirs IDs System-Env.Variablen, API-Keys')
print('sys    : Vars. und Funcs. des Py-Interpreters Imports Paths')
print('io     : Str & Bytes in RAM Buffer Binärdaten HD-in/out')
print('pathlib: Obj.Or. Pfadverwaltung Pfad-Syntax Datei-Endungen')
print('#a152-------------------------------------------------')
print(' pickle: Py-Objects Persistent Storage State Reload ')
import pickle
print('with open("data.pkl", "wb") as f:pickle.dump(obj, f)')
print('Write obj to open bin file f / pickle.dump()')
print('Print obj')
print('Return obj as a string')
print('Read obj from f / pickle.load()')










