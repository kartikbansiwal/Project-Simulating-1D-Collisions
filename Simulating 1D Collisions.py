class pq():#I have taken from lecture slides for this class
    #however the implementation is completely mine
    class _item:
        __slots__='_key','_value'
        def __init__(self,time,i):
            self._key=time;self._value=i
        def __lt__(self,other):#overloading the operator to compare between the nodes
            if type(self._key)==str:
                return False
            elif type(other._key)==str:
                return True
            elif self._key<other._key:
                return True
            elif self._key==other._key:
                if self._value<other._value:
                    return True
                else:
                    return False
            else:
                return False
        def cng(self,new):#this function updates the key value of the node
            self._key=new
        def val(self):#returns the value of the node
            return self._key
        def ind(self):#returns the index of the node
            return self._value
    def empty(self):#checks if heap is empty or not
        return len(self)==0
    def _parent(self,j):#parent of the node
        return (j-1)//2
    def _left(self,j):
        return 2*j+1
    def _right(self,j):
        return 2*j+2
    def _isleft(self,j):
        return self._left(j)<len(self._d)
    def _isright(self,j):
        return self._right(j) < len(self._d)
    def _swap(self,i,j):
        self._d[i], self._d[j] = self._d[j], self._d[i]
        self._pos[self._d[i].ind()],self._pos[self._d[j].ind()]=self._pos[self._d[j].ind()],self._pos[self._d[i].ind()]#updating the position list
    def _up(self,j):
        parent = self._parent(j)
        if j > 0 and self._d[j] < self._d[parent]:
            self._swap(j, parent)
            self._up(parent)
    def _down(self,j):
        if self._isleft(j):
            left=self._left(j)
            small_child=left
            if self._isright(j):
                right=self._right(j)
                if self._d[right]<self._d[left]:
                    small_child=right
            if self._d[small_child]<self._d[j]:
                self._swap(j,small_child)
                self._down(small_child)
    def __init__(self,contents):
        self._d=[self._item(p,q) for p,q in contents]
        self._pos=[i for i in range (0,len(contents))]#initialisng and storing the positions of the nodes
        if len(self._d)>1:
            self._build()
    def _build(self):
        start=self._parent(len(self)-1)
        for j in range (start,-1,-1):
            self._down(j)
    def __len__(self):
        return len(self._d)
    def add(self,time,i):
        self._d.append(self._item(time,i))
        self._pos.append(len(self._d)-1)
        self._up(len(self._d)-1)
    def min(self):
        if self.empty():
            return("Empty priority queue")
        item=self._d[0]
        return (item._key, item._value)
    def extractmin(self):
        if self.empty():
            return ("Empty priority queue")
        self._swap(0,len(self._d)-1)
        item=self._d.pop();self._pos.pop()
        self._down(0)
        return (item._key,item._value)
    def update(self,i,new):#function to update the node with the index i
        if type(new)==str:
            self._d[self._pos[i]].cng(new)
            self._down(self._pos[i])
        elif type(self._d[self._pos[i]].val())==str:
            self._d[self._pos[i]].cng(new)
            self._up(self._pos[i])
        elif new>=self._d[self._pos[i]].val():
            self._d[self._pos[i]].cng(new)
            self._down(self._pos[i])
        else:
            self._d[self._pos[i]].cng(new)
            self._up(self._pos[i])
    def posi(self):#returns the position list
        print(self._pos)
        return None
    def data(self):
        for i in self._d:
            print(i.val(),i.ind())
        return None
def isc(i,v):#checks whether a collision is happening or not
    if v[i]<v[i+1]:
        return False
    elif v[i]*v[i+1]<=0:
        if v[i+1]<0:
            return True
        elif v[i]>0:
            return True
        else:
            return False
    elif v[i]==v[i+1]:
        return False
    else:
        return True
def time(i,x,v):#gives the time taken in a collision
    if isc(i,v):
        return abs(x[i]-x[i+1])/abs(v[i]-v[i+1])
    else:
        return 'INF'
def fvp(i,x,m,v):#gives the final velocities and positions after a collision
    if isc(i,v):
        v1=((m[i]-m[i+1])/(m[i]+m[i+1]))*v[i]+((2*m[i+1])/(m[i]+m[i+1]))*v[i+1]
        v2=((2*m[i])/(m[i]+m[i+1]))*v[i]-((m[i]-m[i+1])/(m[i]+m[i+1]))*v[i+1]
        fp=x[i]+v[i]*time(i,x,v)
        return (v1,v2,fp)
    else:
        return (v[i],v[i+1],"NC")
def change(i,t,v1,x,v,lu):
    x[i]+=v[i]*(t-lu[i])
    v[i]=v1;lu[i]=t;return None
def listCollisions(M,x,v,m,T):
    l=[]
    for i in range (0,len(x)-1):
        l.append([time(i,x,v),i])
    main=pq(l)#initiating a heap to store (time,index)
    lu=[0 for i in range (0,len(x))]
    ans=[];col=[[time(i,x,v),i,fvp(i,x,M,v)[2]] for i in range (0,len(x)-1)]#stores all the initial collisions irrrespective of the other factors.
    if len(M)==1:
        return ans
    else:
        n=0;t=0#n is the number of collisions, t is the current time
        while n<m and t<=T:
            #main.data()
            k=main.min()#the minimum element of the heap
            tim,i=k[0],k[1]
            if tim=='INF':#since the minimum time is infinity no more collisions can occur
                break
            else:
                if i==len(M)-2:
                    if i==0:
                        n+=1;t=tim#updating the collision and time
                        v1,v2,fp=fvp(i,x,M,v);ans.append(col[i])#adding the current collision to an answer list
                        change(i,t,v1,x,v,lu);change(i+1,t,v2,x,v,lu)#changing the position and velocities after collision
                        if time(i,x,v)=="INF":
                            col[i]=[time(i,x,v),i,fvp(i,x,M,v)[2]];main.update(i,time(i,x,v))#I now change the collision list to update the collisions of i-1,i,i+1
#----------------THE SAME THING IS DONE FOR THE OTHER CASES----------------------------------#
                    else:
                        n+=1;t=tim
                        v1,v2,fp=fvp(i,x,M,v);ans.append(col[i])
                        change(i,t,v1,x,v,lu);change(i+1,t,v2,x,v,lu);change(i-1,t,v[i-1],x,v,lu)
                        if time(i-1,x,v)=="INF":
                            col[i-1]=[time(i-1,x,v),i-1,fvp(i-1,x,M,v)[2]];main.update(i-1,time(i-1,x,v))
                        if time(i-1,x,v)!="INF":
                            col[i-1]=[time(i-1,x,v)+t,i-1,fvp(i-1,x,M,v)[2]];main.update(i-1,time(i-1,x,v)+t)
                        if time(i,x,v)=="INF":
                            col[i]=[time(i,x,v),i,fvp(i,x,M,v)[2]];main.update(i,time(i,x,v))
                    
                elif i==0:
                    if i!=len(M)-2:
                        n+=1;t=tim
                        v1,v2,fp=fvp(i,x,M,v);ans.append(col[i])
                        change(i,t,v1,x,v,lu);change(i+1,t,v2,x,v,lu);change(i+2,t,v[i+2],x,v,lu)
                        if time(i,x,v)=="INF":
                            col[i]=[time(i,x,v),i,fvp(i,x,M,v)[2]];main.update(i,time(i,x,v))
                        if time(i+1,x,v)!="INF":
                            col[i+1]=[time(i+1,x,v)+t,i+1,fvp(i+1,x,M,v)[2]];main.update(i+1,time(i+1,x,v)+t)
                        if time(i+1,x,v)=="INF":
                            col[i+1]=[time(i+1,x,v),i+1,fvp(i+1,x,M,v)[2]];main.update(i+1,time(i+1,x,v))
                    else:
                        n+=1;t=tim
                        v1,v2,fp=fvp(i,x,M,v);ans.append(col[i])
                        change(i,t,v1,x,v,lu);change(i+1,t,v2,x,lu)
                        if time(i,x,v)=="INF":
                            col[i]=[time(i,x,v),i,fvp(i,x,M,v)[2]];main.update(i,time(i,x,v))
                else:
                    n+=1;t=tim
                    v1,v2,fp=fvp(i,x,M,v);ans.append(col[i])
                    change(i,t,v1,x,v,lu);change(i+1,t,v2,x,v,lu);change(i-1,t,v[i-1],x,v,lu);change(i+2,t,v[i+2],x,v,lu)
                    if time(i-1,x,v)=="INF":
                        col[i-1]=[time(i-1,x,v),i-1,fvp(i-1,x,M,v)[2]];main.update(i-1,time(i-1,x,v))
                    if time(i-1,x,v)!="INF":
                        col[i-1]=[time(i-1,x,v)+t,i-1,fvp(i-1,x,M,v)[2]];main.update(i-1,time(i-1,x,v)+t)
                    if time(i,x,v)=="INF":
                        col[i]=[time(i,x,v),i,fvp(i,x,M,v)[2]];main.update(i,time(i,x,v))
                    if time(i+1,x,v)!="INF":
                        col[i+1]=[time(i+1,x,v)+t,i+1,fvp(i+1,x,M,v)[2]];main.update(i+1,time(i+1,x,v)+t)
                    if time(i+1,x,v)=="INF":
                        col[i+1]=[time(i+1,x,v),i+1,fvp(i+1,x,M,v)[2]];main.update(i+1,time(i+1,x,v))
        final=[]
        for i in ans:
            if i[0]<=T:
                final.append((round(i[0],4),i[1],round(i[2],4)))
        return final
                    
    
        
            
        
        
    
    
