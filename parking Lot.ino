#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

int replyblock = 5000;

void setup()
{
  Serial.begin(9600);
  servo1.attach(9); // servo pin 9
  servo1.write(150);
  servo2.attach(8); // servo pin 8
  servo2.write(150);
  servo3.attach(7); // servo pin 7
  servo3.write(150);
  servo4.attach(6); // servo pin 6
  servo4.write(150);
}

void loop()
{
  if (Serial.available())
  {
    String str = Serial.readStringUntil('\n'); // 讀取傳入的字串直到"\n"結尾

    if (str == "1")
    {
      Serial.println("OBSTACLE!!, OBSTACLE!!");
      servo1.write(90);
      Serial.println("down");
      delay(replyblock);
      servo1.write(150);
      Serial.println("up");
    }
  else if (str == "2")
  {
    Serial.println("OBSTACLE!!, OBSTACLE!!");
    servo2.write(90);
    Serial.println("down");
    delay(replyblock);
    servo2.write(150);
    Serial.println("up");
  }

  else if (str == "3")
  {
    Serial.println("OBSTACLE!!, OBSTACLE!!");
    servo3.write(90);
    Serial.println("down");
    delay(replyblock);
    servo3.write(150);
    Serial.println("up");
  }

  else if (str == "4")
  {
    Serial.println("OBSTACLE!!, OBSTACLE!!");
    servo4.write(90);
    Serial.println("down");
    delay(replyblock);
    servo4.write(150);
    Serial.println("up");
  }
  delay(200);
  }
}