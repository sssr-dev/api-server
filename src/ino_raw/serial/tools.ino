// Functions
void print(char* text) {Serial.print(text);};
void println(char* text) {Serial.println(text);};
void println(String text) {Serial.println(text);};
void println(byte text) {Serial.println(text, DEC);};
String input() {return Serial.readString();};

void short_point() {
    digitalWrite(LED, HIGH);
    delay(800);
    digitalWrite(LED, LOW);
    delay(500);

}

void long_point() {
    digitalWrite(LED, HIGH);
    delay(1600);
    digitalWrite(LED, LOW);
    delay(500);

}

void sos() {

    // s
    short_point();
    short_point();
    short_point();

    // o
    long_point();
    long_point();
    long_point();

    // s
    short_point();
    short_point();
    short_point();

    delay(5000);

}

