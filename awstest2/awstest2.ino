#include <Adafruit_NeoPixel.h>
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

#ifndef STASSID
#define STASSID "Sonia's iPhone"
#define STAPSK "f3dzuhmmvsvbe"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

const String url = "/szeton-capstone/tweetcounter.txt";
const char* host = "s3.us-east-2.amazonaws.com";
const int httpsPort = 443;

int numpixels = 49;

// values read in from s3 bucket
int values[] = {0, 0, 0, 0, 0, 0, 0};

// RGB values for 7 emotions, red, orange, yellow... anger, fear, happiness...
int redValues[]   = {255, 211, 255,   0,   0,   0, 148};
int greenValues[] = {  0, 128, 255, 255, 255,   0,   0};
int blueValues[]  = {  0,   0,   0,   0, 255, 255, 211};

// max expected value for each emotion
int maxValues[] = {100, 25, 75, 38, 60, 50, 310};

//initialize  NeoPixel strand, connected to pin 14
Adafruit_NeoPixel strand = Adafruit_NeoPixel(numpixels, 14);

//runs once when feather is booting
void setup() {
  Serial.begin(115200);
  strand.begin();
  Serial.println();
  Serial.print("connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    yield();
    delay(100);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}

//calculate brightness based on the read in value of specific emotion
float calculateBrightness(int emotion) {
  float brightness = (float)values[emotion]/(float)maxValues[emotion];
  if (brightness > 1.0) brightness = 1.0;
  return brightness;
}

// set LED colors by emotion value
void setColors() {
  for(int i = 0; i < numpixels; i++){
    int emotion = i % 7;
    float brightness = calculateBrightness(emotion);
    Serial.println(brightness);
    strand.setPixelColor(
      i, 
      redValues[emotion] * brightness, 
      greenValues[emotion] * brightness, 
      blueValues[emotion] * brightness
    );
    strand.show();
  }
}

//This loop runs continuously
void loop() {
  WiFiClientSecure client;
  Serial.print("connecting to ");
  Serial.println(host);

  if (!client.connect(host, httpsPort)) {
    Serial.println("connection failed");
    return;
  }

  client.setTimeout(1);

  Serial.print("requesting URL: ");
  Serial.println(url);

  // send the request to retrieve the latest data
  client.println(String("GET ") + url + " HTTP/1.1");
  client.println(String("Host: ") + host); 
  client.println("Connection: close");
  client.println();
  Serial.println("request sent");

  // read the response
  Serial.println("Header:");
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
    if (line == "\r") {
      break;
    }
  }
  for (int i = 0; i < 7; i++) {
    String line = client.readStringUntil('\n');
    Serial.println(String("Result: ") + line);
    Serial.println();
    if (line.length() > 0) {
      values[i] = line.toInt();
    }
  }
  client.stop();
 
  setColors();

  yield(); // give time for wifi process
  delay(100);  // wait 0.1 seconds
}
