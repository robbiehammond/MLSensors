import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split

keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/']

BAUD_RATE = 922190
DEVICE_LOCATION = '/dev/tty.usbserial-02896C6F'
NUM_POSSIBILITIES = len(keys)
NUM_SENSORS = 4
NUM_SAMPLES = 20
ONLYPRINT = False 


# if actual training data exists
if sum(1 for _ in open('src/ml/csvs/mpu6050data.csv')) > 1:
    scaler = StandardScaler()
    df = pd.read_csv('src/ml/csvs/mpu6050data.csv')
    X = df.drop('key', axis=1)
    y = df['key']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, random_state=2
    )
    scaler.fit_transform(X_test)




fields = []
# append sample0s0ax, sample0s0ay, ... sampleNsMgz
for sampleNum in range(NUM_SAMPLES):
    for sensorNum in range(NUM_SENSORS):
        fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'ax\'')
        fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'ay\'')
        fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'az\'')
        fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gx\'')
        fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gy\'')
        fields.append('\'sample' + str(sampleNum) + 's' + str(sensorNum) + 'gz\'')