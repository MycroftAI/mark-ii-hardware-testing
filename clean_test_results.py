GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color


fh = open("test_results.csv")
for line in fh.readlines():
    line = line.replace(GREEN,'')
    line = line.replace(RED,'')
    line = line.replace(NC,'')
    if line.startswith("\0"):
        x = 0
        res = ''
        zero_ctr = 0
        while x < len(line):
            if line[x] == '\0':
                zero_ctr += 1
            res += str(ord( line[x] ))
            res += ' '
            x += 1
        print("Bad Line! len=%s, zero_ctr=%s, [0]=--->%s<--- [1]=--->%s<---, @%s=%s, @%s=%s" % (len(line), zero_ctr, line[0], line[1], zero_ctr, line[zero_ctr], zero_ctr+1, line[zero_ctr+1]))
        print(res)
    else:
        print(line.strip())
fh.close()

