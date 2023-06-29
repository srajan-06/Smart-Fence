#define BLYNK_TEMPLATE_ID "TMPL3-FvHWuQn"
#define BLYNK_TEMPLATE_NAME "project"
#define BLYNK_AUTH_TOKEN "W9_mkzK-UAARsRds1s5LmOFWlyNd0hPO"

#include <Servo.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

char auth[] = "W9_mkzK-UAARsRds1s5LmOFWlyNd0hPO";
char ssid[] = "Srajan";
char pass[] = "qwertyui";


int ledPin = D1;
int buzzerPin = D2;
int servoPin = D3;

Servo myservo;

void setup()
{
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  myservo.attach(servoPin);

  Serial.begin(9600);
  Blynk.begin(auth, ssid, pass);
}

void loop()
{
  Blynk.run();
}

BLYNK_WRITE(V0)
{
  int buttonState = param.asInt();
  if (buttonState == HIGH) {
    digitalWrite(ledPin, HIGH);
    digitalWrite(buzzerPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
    digitalWrite(buzzerPin, LOW);
  }
}

BLYNK_WRITE(V1)
{
  int buttonState = param.asInt();
  if (buttonState == HIGH) {
    myservo.write(180);
  } else {
    myservo.write(0);
  }
}