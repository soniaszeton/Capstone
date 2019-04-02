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

int numpixels = 29;

int red = 0;
int green = 0;
int blue = 0;

//output
//initialize strand, connected to pin 15
Adafruit_NeoPixel strand = Adafruit_NeoPixel(numpixels, 15);



void setup() {
  Serial.begin(115200);
  strand.begin();
  Serial.println();
  Serial.print("connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
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

  Serial.print("requesting URL: ");
  Serial.println(url);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" + 
               "Host: " + host + "\r\n" + 
               "User-Agent: BuildFailureDetectorESP8266\r\n" +
               "Connection: close\r\n\r\n");

  Serial.println("request sent");
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("headers received");
      break;
    }
  }
  String line = client.readStringUntil('\n');
  Serial.println(line);
  if (line.startsWith("{\"state\":\"success\"")) {
    Serial.println("esp8266/Arduino CI successful!");
  } else {
    Serial.println("esp8266/Arduino CI has failed");
  }

  Serial.println("reply was:");
  Serial.println("==========");
  Serial.println(line);
  Serial.println("==========");
  Serial.println("closing connection");

  int thecount = line.toInt(); 

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

  for(int i = 0; i < numpixels; i++){
    strand.setPixelColor(i, red, green, blue);
    strand.show();
  }

  delay(100);  // wait 1 second
}
