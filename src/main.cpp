#include <Arduino.h>

#include "flags.h"

void discardLineEnding() {
  if (!Serial.available()) {
    return;
  }
  char c = Serial.peek();
  if (c == '\r' || c == '\n') {
    Serial.readStringUntil('\n');
  }
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(15000);
  pinMode(LED_BUILTIN, OUTPUT);
}

void flag0() {
  auto c = Serial.readStringUntil('\n');
  c.trim();
  if (c == "A") {
    Serial.println("B");
  }
  c = Serial.readStringUntil('\n');
  c.trim();
  if (c == "C") {
    Serial.println("DSU{2320_15_0n3}");
  }
}

void flag1() { Serial.println(FLAG1); }

void flag2() {
  auto msg = Serial.readStringUntil('\n');
  msg.trim();
  if (msg == "hello, world") {
    Serial.println(FLAG2);
  }
}

bool server_handshake() {
  auto c = Serial.readStringUntil('\n');
  c.trim();
  if (c == "S") {
    Serial.println("A");
  }
  c = Serial.readStringUntil('\n');
  c.trim();
  if (c == "SA") {
    return true;
  }
  return false;
}

bool client_handshake() {
  Serial.println("S");
  auto c = Serial.readStringUntil('\n');
  c.trim();
  if (c == "A") {
    Serial.println("SA");
    return true;
  }
  return false;
}

void flag3() {
  if (server_handshake()) {
    Serial.println(FLAG3);
  }
}

void flag4() {
  int num;
  if (server_handshake()) {
    for (int i = 0; i < BLINKS; i++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(300);
      digitalWrite(LED_BUILTIN, LOW);
      delay(300);
    }
  }
  if (client_handshake()) {
    num = Serial.parseInt();
    discardLineEnding();
  }
  if (server_handshake()) {
    if (num == BLINKS) {
      Serial.println(FLAG4);
    } else {
      Serial.println("Incorrect.");
    }
  }
}

void loop() {
  int c = Serial.parseInt();
  discardLineEnding();

  switch (c) {
    case 0:
      flag0();
      break;
    case 1:
      flag1();
      break;
    case 2:
      flag2();
      break;
    case 3:
      flag3();
      break;
    case 4:
      flag4();
      break;
    default:
      break;
  }
}