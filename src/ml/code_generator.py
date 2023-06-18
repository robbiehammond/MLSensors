for sampleNum in range(10):
    for sensorNum in range(1):
        print('\'sample' + str(sampleNum) + 'sensor' + str(sensorNum) + 'ax\'', end=', ')
        print('\'sample' + str(sampleNum) + 'sensor' + str(sensorNum) + 'ay\'', end=', ')
        print('\'sample' + str(sampleNum) + 'sensor' + str(sensorNum) + 'az\'', end=', ')
        print('\'sample' + str(sampleNum) + 'sensor' + str(sensorNum) + 'gx\'', end=', ')
        print('\'sample' + str(sampleNum) + 'sensor' + str(sensorNum) + 'gy\'', end=', ')
        print('\'sample' + str(sampleNum) + 'sensor' + str(sensorNum) + 'gz\'', end=', ')

print()
print()

for sampleNum in range(10):
    for sensorNum in range(1):
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 'sensor' + str(sensorNum) + '\'][\'' + 'ax\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 'sensor' + str(sensorNum) + '\'][\'' + 'ay\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 'sensor' + str(sensorNum) + '\'][\'' + 'az\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 'sensor' + str(sensorNum) + '\'][\'' + 'gx\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 'sensor' + str(sensorNum) + '\'][\'' + 'gy\']', end=', ')
        print('obj[' + '\'sample' + str(sampleNum) + '\'][\'' + 'sensor' + str(sensorNum) + '\'][\'' + 'gz\']', end=', ')
print()