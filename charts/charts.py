
with open('running.log','r') as f:
    line = f.readline()
    while( '[' not in line):
        line = f.readline()
    while(line):
        line1 = f.readline()

        linedata = line.strip()
        # for r in ['[',']',"'"]:
        #     linedata = linedata.replace(r,'')
        linedata = linedata.split(',')
        line1data = float(line1.strip())

        targetsize = len(linedata)
        spreadsize = line1data

        line = f.readline()
        
        with open('greedy_charts.csv','a') as f1:
            f1.write(','.join([ str(elem) for elem in [targetsize,spreadsize]])+'\n')