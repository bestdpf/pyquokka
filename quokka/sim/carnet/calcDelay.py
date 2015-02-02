f = open('delay3', 'r')
delay = 0.0
for line in f:
    s, t, lat = [float(x) for x in line.split()]
    delay += lat
print delay
