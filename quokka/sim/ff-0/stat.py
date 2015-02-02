cnt = [0]*500
with open('ffdelay1', 'r') as f:
    for line in f:
        src, dst, dis = [int(x) for x in line.split()]
        if dis < 500:
            cnt[dis] += 1
    for j in range(499):
        cnt[j+1] += cnt[j]
    for j in range(500):
        cnt[j] = 1.0*cnt[j]/cnt[499]
    print 'ffdelay1=%s;' %(cnt)
    
