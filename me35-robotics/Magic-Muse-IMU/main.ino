float startTime = 0;
float currTime = 0;
float oldTime = 0;

void setup() {
    Serial.begin(9600)
    while (!Serial);
    Serial.println("and we begin")
    if (!IMU.beginz()) {
        Serial.println("Failed to initialize IMU")
        while(true);
    }
    startTime = millis();
}

void loop() {

    float xGyro, yGyro, zGyro;
    float xAcc, yAcc, zAcc;
    float elapsedTime;

    currTime = millis();
    elapsedTime = currTime - oldTime;
    oldTime = currTime;

    // if both accelerometer and gyrometer are ready to be read:
    if (IMU.accelerationAvailable() && 
    IMU.gyroscopeAvailable()) {
        // read accelerometer and gyrometer:
        IMU.readAcceleration(xAcc, yAcc, zAcc)

        //print the results:
        IMU.readGyroscope(xGyro, yGyro, zGyro);
        Serial.print(xAcc);
        Serial.print(",");
        Serial.print(yAcc);
        Serial.print(",");
        Serial.print(zAcc);
        Serial.print(",");
        Serial.print(xGyro);
        Serial.print(",");
        Serial.print(yGyro);
        Serial.print(",");
        Serial.print(zGyro);
        Serial.print(",");
        Serial.println(elapsedTime);
    }
    delay(1);
}