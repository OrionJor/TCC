def a():
   global b
   b = "teste"
   b = 10

a()

b = 100
print(b)