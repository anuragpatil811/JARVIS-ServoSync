
#include <Servo.h>

// Six SG90 servo motors
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

// Existing Arduino connections
const int servoPins[6] = {3, 5, 6, 9, 10, 11};

Servo* servos[6] = {
  &servo1, &servo2, &servo3,
  &servo4, &servo5, &servo6
};

// Motor control
bool motorsRunning = false;

int currentAngle = 90;
int direction = 1;

// Servo movement limits
const int MIN_ANGLE = 20;
const int MAX_ANGLE = 160;

// Servo movement speed
const unsigned long interval = 20;
unsigned long previousMillis = 0;

// Move all six servos together
void moveAllServos(int angle) {
  for (int i = 0; i < 6; i++) {
    servos[i]->write(angle);
  }
}

void setup() {

  Serial.begin(9600);
  Serial.setTimeout(50);

  // Attach all six servo motors
  for (int i = 0; i < 6; i++) {
    servos[i]->attach(servoPins[i]);
  }

  // Initial center position
  moveAllServos(90);

  Serial.println("JARVIS ServoSync AI Ready");
  Serial.println("Waiting for voice commands...");
}

void loop() {

  // Receive Python commands
  if (Serial.available() > 0) {

    String command = Serial.readStringUntil('\n');

    command.trim();
    command.toUpperCase();

    // START MOVING
    if (command == "START") {

      motorsRunning = true;
      previousMillis = millis();

      Serial.println("All six servos STARTED");
    }

    // TURN OFF
    else if (command == "STOP") {

      motorsRunning = false;

      moveAllServos(currentAngle);

      Serial.println("All six servos STOPPED");
    }
  }

  // Continuous synchronized movement
  if (motorsRunning) {

    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= interval) {

      previousMillis = currentMillis;

      currentAngle += direction;

      if (currentAngle >= MAX_ANGLE) {
        currentAngle = MAX_ANGLE;
        direction = -1;
      }

      else if (currentAngle <= MIN_ANGLE) {
        currentAngle = MIN_ANGLE;
        direction = 1;
      }

      moveAllServos(currentAngle);
    }
  }
}
