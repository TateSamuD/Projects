import time
import board
import adafruit_dht
import json
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

UPDATE_DELAY_MIN = 5

while True:
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        dictionary = {}
        dictionary["date"] = time.strftime("%m/%d/%Y %I:%M:%S%p", time.gmtime())
        dictionary["temperature_f"] = temperature_f
        dictionary["temperature_c"] = temperature_c
        dictionary["humidity"] = humidity
        outfile = open("data.json", "w")
        json.dump(dictionary, outfile, indent=4)
        outfile.close()
        print("Temp {:.1f} F / {:.1f} c     Humidity: {}%".format(temperature_f, temperature_c, humidity))
        time.sleep(UPDATE_DELAY_MIN * 60.0)
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)