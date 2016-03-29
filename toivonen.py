import collections
import itertools
import random
import sys


def frequentsets(k,prev,s,f):
    
    if k==1:
        dsingles={}
        f=open("new_toivonen.txt")
        for line in f:
            line=line.rstrip()
            items=line.split(',')
            items.sort()
            for item in items:
                if item in dsingles:
                    dsingles[item]=dsingles[item]+1
                else:
                    dsingles[item]=1

        fitemsets1=[]
        negative_border1=[]
        for item in dsingles:
            if dsingles[item]>=s:
                fitemsets1.append(item)
            else:
                negative_border1.append(item)

        negative_border1.sort()
        fitemsets1.sort()

        candidatepairs=[]
        i=0
        while i<(len(fitemsets1)-1):
            j=i+1
            while j<len(fitemsets1):
                candidatepairs.append([fitemsets1[i],fitemsets1[j]])
                j=j+1
            i=i+1

        negative_border=[]
        pairs={i:0 for i in range(0,len(candidatepairs))}

        f=open("new_toivonen.txt")
        for line in f:
            line=line.rstrip()
            items=line.split(',')
            items.sort()
            p=itertools.combinations(items,2)
            for item in p:
                item=list(item)
                count=0
                for j in item:
                    if j in fitemsets1:
                        count=count+1
                if count==2:
                    if item not in negative_border:
                        negative_border.append(item)

                for index,k in enumerate(candidatepairs):
                    if item==k:
                        pairs[index]=pairs[index]+1
                        break

        negative_border.sort()

        fpairs=[]
        for item in pairs:
            if pairs[item]>=s:
                fpairs.append(candidatepairs[item])
        fpairs.sort()

        neg_bor2=[]

        for item in negative_border:
            if item not in fpairs:
                neg_bor2.append(item)

        return fitemsets1,fpairs, negative_border1, neg_bor2

    candidateitems=[]

    f=open("new_toivonen.txt")
    for line in f:
        line=line.rstrip()
        items=line.split(',')
        items.sort()
        trip=itertools.combinations(items,k)
        for o in trip:
            o=list(o)
            pai=itertools.combinations(o,k-1)
            count=0
            for u in pai:
                u=list(u)
                if u in prev:
                    count=count+1
            if count==k:
                if o not in candidateitems:
                    candidateitems.append(o)

    ditemsets={i:0 for i in range(len(candidateitems))}

    f=open("new_toivonen.txt")
    for line in f:
        line=line.rstrip()
        items=line.split(',')
        items.sort()
        trip=itertools.combinations(items,k)
        for o in trip:
            o=list(o)
            for index,i in enumerate(candidateitems):
                if o==i:
                    ditemsets[index]=ditemsets[index]+1
                    break

    fitems=[]
    ng_br=[]
    for item in ditemsets:
        if ditemsets[item]>=s:
            fitems.append(candidateitems[item])
        else:
            ng_br.append(candidateitems[item])
    fitems.sort()
    ng_br.sort()

    return fitems,ng_br


def sample_pass(s):
    prev=[]
    k=1
    s=float(s)
    size=0.5
    f=open(sys.argv[1])
    file1=open("new_toivonen.txt",'w')
    countlines=0
    d={}
    for line in f:
        d[countlines]=line
        countlines=countlines+1
        
    aman_items=[i for i in range(countlines)]
    random.shuffle(aman_items)
    for i in range(int(countlines*size)):
        file1.write(d[aman_items[i]])
    file1.close()

    ori_items={}
    neg_items={}

    if k==1 and prev==[]:
        res=frequentsets(k,prev,int(s*size*0.9),f)
        prev=res[1]
        singles=res[0]
        if prev==[] and singles==[]:
            return None

        neg1=res[2]
        neg2=res[3]
        ori_items[1]=singles
        neg_items[1]=neg1
        ori_items[2]=prev
        neg_items[2]=neg2
        k=3

    while prev!=[]:
        res=frequentsets(k,prev,int(s*size*0.9),f)
        prev=res[0]
        ori_items[k]=prev
        neg_items[k]=res[1]
        k=k+1

    return ori_items,neg_items




def whole_pass(dicts,s):
    fitems=dicts[0]
    neg_bord=dicts[1]
    fitems_list=[]
    neg_bord_list=[]
    for item in fitems:
        fitems_list.extend(fitems[item])
    for item in neg_bord:
        neg_bord_list.extend(neg_bord[item])

    fitems_dict={i:0 for i in range(len(fitems_list))}
    fneg_dict={i:0 for i in range(len(neg_bord_list))}
    f=open(sys.argv[1])

    for line in f:
        line=line.rstrip()
        items=line.split(',')
        items.sort()
        for k in fitems:
            trip=itertools.combinations(items,k)
            for o in trip:
                o=list(o)
                for index,q in enumerate(fitems_list):
                    if o==list(q):
                        fitems_dict[index]=fitems_dict[index]+1
                        break

            trip=itertools.combinations(items,k)
            for o in trip:
                o=list(o)
                for index,q in enumerate(neg_bord_list):
                    if o==list(q):
                        fneg_dict[index]=fneg_dict[index]+1
                        break

    freq_itemsets=[]

    for item in fitems_dict:
            if fitems_dict[item]>=s:
                freq_itemsets.append(fitems_list[item])

    for item in fneg_dict:
            if fneg_dict[item]>=s:
                a=[]
                return 0,a

    return 1,freq_itemsets



iterations=0
def toivonen():
    s=int(sys.argv[2])
    size_perc=0.5
    global iterations
    iterations=iterations+1
    dicts=sample_pass(s)
    if dicts == None:
        return toivonen()
    a,freq=whole_pass(dicts,s)
    if a==1:
        sys.stdout.write(str(iterations)+"\n")
        sys.stdout.write(str(size_perc)+"\n")
        max_len = max(map(len, freq))
        res = {i:[] for i in range(1, max_len + 1)}
        for item in freq:
            if len(item) == 1:
                res[len(item)].append([item])
            else:
                res[len(item)].append(item)

        for item in res:
            sys.stdout.write(str(res[item])+"\n")
        # sys.stdout.write(str(freq)+"\n")
        return
    else:
        toivonen()

toivonen()


