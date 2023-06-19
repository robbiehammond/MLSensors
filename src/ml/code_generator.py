for sampleNum in range(10):
    for sensorNum in range(2):
        print('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'ax\'', end=', ')
        print('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'ay\'', end=', ')
        print('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'az\'', end=', ')
        print('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gx\'', end=', ')
        print('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gy\'', end=', ')
        print('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gz\'', end=', ')

print()
print()

for sampleNum in range(10):
    for sensorNum in range(2):
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 's' + str(sensorNum) + '\'][\'' + 'ax\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 's' + str(sensorNum) + '\'][\'' + 'ay\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 's' + str(sensorNum) + '\'][\'' + 'az\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 's' + str(sensorNum) + '\'][\'' + 'gx\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 's' + str(sensorNum) + '\'][\'' + 'gy\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 's' + str(sensorNum) + '\'][\'' + 'gz\']', end=', ')
print()