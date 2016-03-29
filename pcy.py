import collections
import itertools
import sys
prev=[]
k=1
s=int(sys.argv[2])
bucketsize=int(sys.argv[3])
f=open(sys.argv[1])


def frequentsets(k,prev,s,bucketsize,f):
    if k==1:
        dsingles={}
        dpairs={i:0 for i in range(bucketsize)}
        for line in f:
            line=line.rstrip()
            items=line.split(',')
            items.sort()
            for item in items:
                if item in dsingles:
                    dsingles[item]=dsingles[item]+1
                else:
                    dsingles[item]=1

            pairs=[]
            pair=itertools.combinations(items,2)
            for i in pair:
                pairs.append(list(i))
                items=[]
                hash=0
                for v in list(i):
                    hash=hash+ord(v)
                    items.append(v)
                dpairs[(hash^5)%20]= dpairs[(hash^5)%20]+1

        fitemsets1=[]

        for item in dsingles:
            if dsingles[item]>=s:
                fitemsets1.append(item)

        fitemsets1.sort()


        # print("memory for item counts: ",len(dsingles)*8)
        # print("memory for hash table counts for size 2 itemsets: ",bucketsize*4)
        # print(dpairs)
        # print("frequent itemsets of size 1:",fitemsets1)

        sys.stdout.write("memory for item counts: "+str(len(dsingles)*8)+"\n")
        sys.stdout.write("memory for hash table counts for size 2 itemsets: "+str(bucketsize*4)+"\n")
        sys.stdout.write(str(dpairs)+"\n")
        sys.stdout.write("frequent itemsets of size 1:"+str(fitemsets1)+"\n")

        bitmap1=[]
        for items in dpairs:
            if dpairs[items]>=s:
                bitmap1.append(1)
            else:
                bitmap1.append(0)

        lookup2=collections.defaultdict(list)
        a=[]
        for i in range(97,122):
            a.append(i)
        values=itertools.combinations(a,2)
        for i in values:
            items=[]
            hash=0
            for v in list(i):
                hash=hash+v
                items.append(chr(v))
            lookup2[(hash^5)%bucketsize].append(items)

        candidatepairs=[]

        for index,items in enumerate(bitmap1):

            if items==1:
                for item in lookup2[index]:
                    count=0
                    for i in item:
                        if i in fitemsets1:
                            count=count+1
                    if count==2:
                        candidatepairs.append(item)
        if len(candidatepairs)!=0:
            # print("")
            # print("memory for frequent itemsets of size 1: ",len(fitemsets1)*8)
            # print("bitmap size: ",bucketsize)
            # print("memory for candidate counts of size 2: ",len(candidatepairs)*12)

            sys.stdout.write("\n")
            sys.stdout.write("memory for frequent itemsets of size 1: "+str(len(fitemsets1)*8)+"\n")
            sys.stdout.write("bitmap size: "+str(bucketsize)+"\n")
            sys.stdout.write("memory for candidate counts of size 2: "+str(len(candidatepairs)*12)+"\n")


            pairs={i:0 for i in range(0,len(candidatepairs))}
            f=open(sys.argv[1])
            for line in f:
                line=line.rstrip()
                items=line.split(',')
                items.sort()
                p=itertools.combinations(items,2)
                for item in p:
                    item=list(item)
                    for index,k in enumerate(candidatepairs):
                        if item==k:
                            pairs[index]=pairs[index]+1
                            break

            fpairs=[]
            for item in pairs:
                if pairs[item]>=s:
                    fpairs.append(candidatepairs[item])
            fpairs.sort()
            #print("frequent itemsets of size 2: ",fpairs)
            sys.stdout.write("frequent itemsets of size 2: "+str(fpairs)+"\n")
            return fpairs



    lookup=collections.defaultdict(list)
    a=[]
    for i in range(97,122):
        a.append(i)
    values=itertools.combinations(a,k)
    for i in values:
        items=[]
        hash=0
        for v in list(i):
            hash=hash+v
            items.append(chr(v))
        lookup[(hash^5)%bucketsize].append(items)

    ditemsets={i:0 for i in range(0,bucketsize)}
    f=open(sys.argv[1])
    for line in f:
        line=line.rstrip()
        items=line.split(',')
        items.sort()
        itemsets=itertools.combinations(items,k)
        for item in itemsets:
            pairs=itertools.combinations(item,k-1)
            count=0
            for m in pairs:
                if list(m) in prev:
                    count=count+1

            if count>=k:
                index=0
                for i in item:
                    index=index+ord(i)
                hash=(index^5)%20
                ditemsets[hash]=ditemsets[hash]+1


    bitmap2=[]
    for items in ditemsets:
        if ditemsets[items]>=s:
            bitmap2.append(1)
        else:
            bitmap2.append(0)

    candidateitemsets=[]

    for index,items in enumerate(bitmap2):
        if items==1:
            for item in lookup[index]:
                count=0
                i=itertools.combinations(item,k-1)
                for l in i:
                    if list(l) in prev:
                        count=count+1
                if count==k:
                    candidateitemsets.append(item)

    if len(candidateitemsets)!=0:
            # print("")
            # print("memory for frequent itemsets of size ",k-1,": ",len(prev)*(k)*4)
            # print("memory for hash table counts for size ",k," itemsets: ",bucketsize*4)
            # print(ditemsets)
            # print("")
            # print("bitmap size: ",bucketsize)
            # print("memory for candidate counts of size ",k,": ",len(candidateitemsets)*(k+1)*4)

            sys.stdout.write("\n")
            sys.stdout.write("memory for frequent itemsets of size "+str(k-1)+": "+str(len(prev)*(k)*4)+"\n")
            sys.stdout.write("memory for hash table counts for size "+str(k)+" itemsets: "+str(bucketsize*4)+"\n")
            sys.stdout.write(str(ditemsets)+"\n")
            sys.stdout.write("\n")
            sys.stdout.write("bitmap size: "+str(bucketsize)+"\n")
            sys.stdout.write("memory for candidate counts of size "+str(k)+": "+str(len(candidateitemsets)*(k+1)*4)+"\n")

            setitems={}
            i=0
            while i<len(candidateitemsets):
                setitems[i]=0
                i=i+1

            f=open(sys.argv[1])
            for line in f:
                line=line.rstrip()
                items=line.split(',')
                items.sort()
                trip=itertools.combinations(items,k)
                for o in trip:
                    for index,p in enumerate(candidateitemsets):
                        if list(o)==p:
                            setitems[index]=setitems[index]+1
                            break


            fitems=[]
            for item in setitems:

                if setitems[item]>=s:
                    fitems.append(candidateitemsets[item])
            fitems.sort()
            #print("frequent itemsets of size ",k,": ",fitems)
            sys.stdout.write("frequent itemsets of size "+str(k)+": "+str(fitems)+"\n")
            return fitems
    a=[]
    return a





if k==1 and prev==[]:
    prev=frequentsets(k,prev,s,bucketsize,f)
    k=3

while prev!=[]:
    prev=frequentsets(k,prev,s,bucketsize,f)
    k=k+1

