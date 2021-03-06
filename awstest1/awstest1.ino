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
int brightness = 0.50;  // range 0..1

int red = 0;
int green = 0;
int blue = 0;

//output
//initialize strand, connected to pin 14
Adafruit_NeoPixel strand = Adafruit_NeoPixel(numpixels, 14);

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
  String line = client.readString();
  client.stop();
  Serial.println(String("Result: ") + line);
  Serial.println();
  
  int thecount = line.toInt(); 
  if (thecount == 0) {
    return;
  }

  if (thecount < 5) {
    //white
    red = 255;
    green = 255;
    blue = 255;
  } else if (thecount < 10) {
    //red
    red = 255;
    green = 0;
    blue = 0;
  } else if (thecount < 12) {
    //yellow
    red = 255;
    green = 255;
    blue = 0;
  } else if (thecount < 14) {
    //green
    red = 0;
    green = 255;
    blue = 0;
  } else if (thecount < 16) {
    //blue
    red = 0;
    green = 0;
    blue = 255;
  } else if (thecount < 18) {
    //magenta
    red = 255;
    green = 0;
    blue = 255;
  } else {
    //cyan
    red = 0;
    green = 255;
    blue = 255;
  }

  

  Serial.println(String("red: ") + red);
  Serial.println(String("green: ") + green);
  Serial.println(String("blue: ") + blue);
  
  for(int i = 0; i < numpixels; i++){
    strand.setPixelColor(i, red, green, blue);
    strand.show();
  }

  yield();
  delay(100);  // wait 0.1 seconds
}
