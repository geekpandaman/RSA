list=[]


class CLA():
    def __init__(self,index):
        self.index=index

c1=CLA(1)
c2=CLA(2)
list.append(c1)
print(list[0].index)
for n in list:
    n=c2

print(list[0].index)