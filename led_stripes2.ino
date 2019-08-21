#include <SPI.h>

#include <LPD8806.h>

//LPD8806 strip = LPD8806(nLEDs, dataPin, clockPin);

// You can optionally use hardware SPI for faster writes, just leave out
// the data and clock pin parameters.  But this does limit use to very
// specific pins on the Arduino.  For "classic" Arduinos (Uno, Duemilanove,
// etc.), data = pin 11, clock = pin 13.  For Arduino Mega, data = pin 51,
// clock = pin 52.  For 32u4 Breakout Board+ and Teensy, data = pin B2,
// clock = pin B1.  For Leonardo, this can ONLY be done on the ICSP pins.

// Hardware SPI on the nano uses clock = 13, data = 11
int nLEDs = 50; // leds per strip
LPD8806 strip = LPD8806(nLEDs);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(1000000);
  strip.begin();
  strip.show();
}
int protocol=-1;
int input=-1;
int wire=-1;
int ser_leds = -1;
int red = -1;
int green = -1;
int blue = -1;
int counter = 0;
bool initial = false;
void reset(){
  protocol = -1;
  wire = -1;
  ser_leds = -1;
  red = -1;
  green = -1;
  blue = -1;
  counter = 0;
  strip.show();
}
void colorWipe(uint32_t color){
  for (int i =0; i< nLEDs; i++){
    strip.setPixelColor(i, color);
  }
  strip.show();
}
void loop() {
  // put your main code here, to run repeatedly:
  
  if(Serial.available() >= 1) {
    input = Serial.read();
    if (!initial || input == 300){
      Serial.println("OK");
      initial = true;
      reset();
    } else if (wire == -1){
      wire = input;
    } else if (protocol == -1){
      protocol = input;
    } else {
      if (protocol == 1){ // Color wipe
        if (red == -1){
          red = input;
        } else if (green == -1){
          green = input;
        } else if (blue == -1){
          blue = input;
          // execute the color wipe
          reset();
        }    
      } else if (protocol == 0){ // individual LEDS
        if (ser_leds == -1) { // get the # of leds to set
          ser_leds = input;
        } else if (red == -1){
          red = input;
        } else if (green == -1){
          green = input;
        } else if (blue == -1){
          blue = input;
          //Serial.println("Strip:");
          //Serial.println(wire);
          //Serial.println("LED:");
          //Serial.println(counter);

          strip.setPixelColor(counter, strip.Color(red, green, blue));
          counter++;
          if (counter == ser_leds){
            reset();
          } else{
            red = -1;
            green = -1;
            blue = -1;
          }
        }
        
      }
    }
    //Serial.println(input);
  }
  
}


