from random import random

# Rainfall data from 1941 to 2025 for Slemani-Kurdistan
rain = [
    780, 470, 690, 640, 790, 835, 530, 360, 185, 40, 
    430, 620, 790, 880, 560, 455, 1240, 410, 580, 490, 
    820, 530, 980, 490, 490, 385, 670, 795, 1135, 430, 
    770, 820, 585, 995, 660, 750, 650, 700, 680, 570, 
    780, 970, 485, 705, 715, 725, 750, 902, 498, 945, 
    935, 1002, 880, 960, 665, 780, 850, 620, 330, 270, 
    510, 930, 875, 840, 630, 875, 874, 307, 415, 844, 
    661, 547, 826, 581, 691, 947, 561, 850, 1618, 931, 
    401, 420, 781, 724, 350
]

year = range(1941,1941+len(rain)+1)

# 1st order Markov Chain
markov = {}

bin_size=100
def b2r(n): # from bins to real
    return n*bin_size;
def r2b(n): # from real to bins
    return int(round(n/bin_size,0));

# turn into bins because there arent many data for direct use
bins = [r2b(n) for n in rain]

# generate markov chain like se
# markov = { 1:{3:1, 4:2} }
# meaning throughout the data, 1 jumped to 3 one time, and to 4 two times 
for b,n in zip(bins[:-1],bins[1:]):
    if b not in markov:
        markov[b]={}
    if n not in markov[b]:
        markov[b][n]=0
    markov[b][n]+=1

prob = {}
# store the result as probability, so the previous comment example
# is now  prob = {1:[[0.317,3], [0.952,4]]}
# so from 0 to 31.7% jump to 3
# from 31.7% to 95.2% jump to 4
# from 95.2% to 100% jump to a random data
for key, value in markov.items():
    prob[key]=[]

    # get sum of all probabilityies, in the example its 3
    sum=0
    for key2, value2 in value.items():
        sum+=value2

    
    sum*=1.05
    # from last probabilty to 100% do a random jump
    # so 3*1.05=3.15, without this the last element would be from n% to 100%

    this_sum=0
    for key2, value2 in value.items():
        this_sum+=value2/sum
        prob[key].append([this_sum,key2])

# get sorted unique list of data to jump to
unique=sorted(set(bins))

def next_data(data):
    # get random number to determine where to jump to
    r = random()
    data = r2b(data)

    # sometimes the required prediction isn't available due to lack of data
    # in this case use neighbouring items and average them, but stop if
    # you gover the edge of the data
    if data not in prob:
        a=data-1
        while a not in prob:
            a-=1
            if a<unique[0]:
                print("no data available for prediction")
                return
        b=data+1
        while b not in prob:
            a-=1
            if b>unique[-1]:
                print("no data available for prediction")
                return
        return (next_data(a)+next_data(b))/2
    p = prob[data]
    choice=None
    for i in p:
        if i[0]>r:
            choice=i[1]
    if choice==None:
        choice = random.choice(unique)
    return b2r(choice)

d=next_data(350) #2025
print("prediction for 2026",d)
# it says 400mm, i hope it's wrong because it would be two droughts in series
