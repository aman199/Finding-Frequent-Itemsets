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
        # print("memory for hash table 1 counts for size 2 itemsets: ",bucketsize*4)
        # print(dpairs)
        # print("frequent itemsets of size 1:",fitemsets1)

        sys.stdout.write("memory for item counts: "+str(len(dsingles)*8)+"\n")
        sys.stdout.write("memory for hash table 1 counts for size 2 itemsets: "+str(bucketsize*4)+"\n")
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
        for i in range(97,124):
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

        dpairs2={i:0 for i in range(bucketsize)}
        f=open(sys.argv[1])
        for line in f:
            line=line.rstrip()
            items=line.split(',')
            items.sort()
            pairs=[]
            pair=itertools.combinations(items,2)
            for i in pair:
                pairs.append(list(i))
                items=[]
                hash=0
                for v in list(i):
                    hash=hash+ord(v)
                    items.append(v)
                dpairs2[(hash^7)%20]= dpairs2[(hash^7)%20]+1
        bitmap2=[]
        for items in dpairs2:
            if dpairs2[items]>=s :
                bitmap2.append(1)
            else:
                bitmap2.append(0)

        lookup22=collections.defaultdict(list)
        a=[]
        for i in range(97,124):
            a.append(i)
        values=itertools.combinations(a,2)
        for i in values:
            items=[]
            hash=0
            for v in list(i):
                hash=hash+v
                items.append(chr(v))
            lookup22[(hash^7)%bucketsize].append(items)

        candidatepairs2=[]

        for index,items in enumerate(bitmap2):
            if items==1:
                for item in lookup22[index]:
                    count=0
                    for i in item:
                        if i in fitemsets1:
                            count=count+1
                    if count==2:
                        candidatepairs2.append(item)

        if len(candidatepairs)!=0 or len(candidatepairs2)!=0:
            candidatepair=[]
            for pair in candidatepairs:
                if pair in candidatepairs2:
                    candidatepair.append(pair)

            # print("")
            # print("memory for frequent itemsets of size 1: ",len(fitemsets1)*8)
            # print("bitmap 1 size: ",bucketsize)
            # print("memory for hash table 2 counts of size 2: ",bucketsize*4)
            # print(dpairs2)

            sys.stdout.write("\n")
            sys.stdout.write("memory for frequent itemsets of size 1: "+str(len(fitemsets1)*8)+"\n")
            sys.stdout.write("bitmap 1 size: "+str(bucketsize)+"\n")
            sys.stdout.write("memory for hash table 2 counts of size 2: "+str(bucketsize*4)+"\n")
            sys.stdout.write(str(dpairs2)+"\n")

            pairs={i:0 for i in range(0,len(candidatepair))}
            f=open(sys.argv[1])
            for line in f:
                line=line.rstrip()
                items=line.split(',')
                items.sort()
                p=itertools.combinations(items,2)
                for item in p:
                    item=list(item)
                    for index,k in enumerate(candidatepair):
                        if item==k:
                            pairs[index]=pairs[index]+1
                            break

            fpairs=[]
            for item in pairs:
                if pairs[item]>=s:
                    fpairs.append(candidatepair[item])
            fpairs.sort()

            # print("")
            # print("memory for frequent itemsets of size 1: ",len(fitemsets1)*8)
            # print("bitmap 1 size: ",bucketsize)
            # print("bitmap 2 size: ",bucketsize)
            # print("memory for candidates of size 2: ",len(candidatepair)*12)
            # print("frequent itemsets of size 2: ",fpairs)

            sys.stdout.write("\n")
            sys.stdout.write("memory for frequent itemsets of size 1: "+str(len(fitemsets1)*8)+"\n")
            sys.stdout.write("bitmap 1 size: "+str(bucketsize)+"\n")
            sys.stdout.write("bitmap 2 size: "+str(bucketsize)+"\n")
            sys.stdout.write("memory for candidates of size 2: "+str(len(candidatepair)*12)+"\n")
            sys.stdout.write("frequent itemsets of size 2: "+str(fpairs)+"\n")



            return fpairs


#lookup3 lookup
#dtriplets ditemsets
    #triplets itemsets
    #triples=setitems
    #candidatetriples=candidateitemsets
    lookup=collections.defaultdict(list)
    a=[]
    for i in range(97,124):
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
    ditemsets2={i:0 for i in range(0,bucketsize)}
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
                hash=(index^7)%20
                ditemsets2[hash]=ditemsets2[hash]+1
    bitmap22=[]
    for items in ditemsets2:
        if ditemsets2[items]>=s:
            bitmap22.append(1)
        else:
            bitmap22.append(0)

    lookupn=collections.defaultdict(list)
    a=[]
    for i in range(97,124):
        a.append(i)
    values=itertools.combinations(a,k)
    for i in values:
        items=[]
        hash=0
        for v in list(i):
            hash=hash+v
            items.append(chr(v))
        lookupn[(hash^7)%bucketsize].append(items)

    candidateitemsets2=[]

    for index,items in enumerate(bitmap22):
        if items==1:
            for item in lookupn[index]:
                count=0
                i=itertools.combinations(item,k-1)
                for l in i:
                    if list(l) in prev:
                        count=count+1
                if count==k:
                    candidateitemsets2.append(item)

    if len(candidateitemsets)!=0 or len(candidateitemsets2)!=0:
            candidateitemset=[]
            for pair in candidateitemsets:
                if pair in candidateitemsets2:
                    candidateitemset.append(pair)

            # print("")
            # print("memory for frequent itemsets of size ",k-1,": ",len(prev)*(k)*4)
            # print("memory for hash table 1 counts for size ",k," itemsets: ",bucketsize*4)
            # print(ditemsets)

            sys.stdout.write("\n")
            sys.stdout.write("memory for frequent itemsets of size "+str(k-1)+": "+str(len(prev)*(k)*4)+"\n")
            sys.stdout.write("memory for hash table 1 counts for size "+str(k)+" itemsets: "+str(bucketsize*4)+"\n")
            sys.stdout.write(str(ditemsets2)+"\n")

            # print("")
            # print("bitmap 1 size: ",bucketsize)
            # print("memory for hash table 2 counts of size ",k,": ",bucketsize*4)
            # print(ditemsets2)

            sys.stdout.write("\n")
            sys.stdout.write("bitmap 1 size: "+str(bucketsize)+"\n")
            sys.stdout.write("memory for hash table 2 counts of size "+str(k)+": "+str(bucketsize*4)+"\n")
            sys.stdout.write(str(ditemsets2)+"\n")

            setitems={}
            i=0
            while i<len(candidateitemset):
                setitems[i]=0
                i=i+1

            f=open(sys.argv[1])
            for line in f:
                line=line.rstrip()
                items=line.split(',')
                items.sort()
                trip=itertools.combinations(items,k)
                for o in trip:
                    for index,p in enumerate(candidateitemset):
                        if list(o)==p:
                            setitems[index]=setitems[index]+1
                            break


            fitems=[]
            for item in setitems:

                if setitems[item]>=s:
                    fitems.append(candidateitemset[item])
            fitems.sort()

            # print("")
            # print("bitmap 1 size: ",bucketsize)
            # print("bitmap 2 size: ",bucketsize)
            # print("memory for candidates of size ",k,": ",len(candidateitemset)*(k+1)*4)
            # print("frequent itemsets of size ",k,": ",fitems)

            sys.stdout.write("\n")
            sys.stdout.write("bitmap 1 size: "+str(bucketsize)+"\n")
            sys.stdout.write("bitmap 2 size: "+str(bucketsize)+"\n")
            sys.stdout.write("memory for candidates of size "+str(k)+": "+str(len(candidateitemset)*(k+1)*4)+"\n")
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

