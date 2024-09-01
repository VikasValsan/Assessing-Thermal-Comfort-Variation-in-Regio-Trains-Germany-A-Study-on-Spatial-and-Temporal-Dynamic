import csv
import time
import logging as log
from datetime import datetime
import pytz
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge.bricklet_industrial_ptc import BrickletIndustrialPTC
from tinkerforge.bricklet_co2_v2 import BrickletCO2V2
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

# Configure logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variables for the device UIDs and host settings
HOST = "localhost"
PORT = 4223
UID_airtemp1 = "TH"  # Air Temp 1 @ 1.10m
UID_airtemp2 = "TK"  # Air Temp 2 @ 1.70m
UID_airtemp3 = "TB"  # Air Temp 3 @ 0.10m
UID_globe1 = "ZC5"  # Globe Temp 1 @ 1.10m
UID_globe2 = "213N"  # Globe Temp 2 @ 0.10m
UID_globe3 = "213J"  # Globe Temp 3 @ 1.70m
UID_CO2 = "29r5"    # CO2 @ 1.10m
UID_hum = "TxR"     # Humidity @ 1.10m

# File and interval settings
filename = "SLBox_DB_mobiletestunit"
new_file_name = filename + ".csv"
csv_write_interval = 60  # seconds
log_print_interval = 60  # seconds

# Timezone setting
berlin_tz = pytz.timezone('Europe/Berlin')

def write_to_csv(new_file_name, data):
    """Writes sensor data to CSV, adding headers if the file is newly created."""
    with open(new_file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        is_empty = file.tell() == 0
        if is_empty:
            writer.writerow([
                "Datetime", "UNIX",
                "Globe Temp @0.10m", "Air Temp @0.10m",
                "Globe Temp @1.10m", "Air Temp @1.10m", "Humidity @1.10m", "CO2 Concentration @1.10m", "CO2 Temp @1.10m", "CO2 RH @1.10m",
                "Globe Temp @1.70m", "Air Temp @1.70m"
            ])
        writer.writerow(data)

def main():
    ipcon = IPConnection()  # Create IP connection
    airtemp1 = BrickletTemperatureV2(UID_airtemp1, ipcon)
    airtemp2 = BrickletTemperatureV2(UID_airtemp2, ipcon)
    airtemp3 = BrickletTemperatureV2(UID_airtemp3, ipcon)
    globe1 = BrickletIndustrialPTC(UID_globe1, ipcon)
    globe2 = BrickletIndustrialPTC(UID_globe2, ipcon)
    globe3 = BrickletIndustrialPTC(UID_globe3, ipcon)
    CO2 = BrickletCO2V2(UID_CO2, ipcon)
    humidity = BrickletHumidityV2(UID_hum, ipcon)

    try:
        ipcon.connect(HOST, PORT)  # Connect to the IP connection
        log.info("Connection established")

        csv_timer = time.time()
        log_timer = time.time()
        while True:
            if time.time() - csv_timer >= csv_write_interval:
                now = datetime.now(berlin_tz)  # Capture the current local time
                unixtime = int(now.timestamp())
                # Fetch new values
                temp_globe1 = globe1.get_temperature() / 100.0
                temp_globe2 = globe2.get_temperature() / 100.0
                temp_globe3 = globe3.get_temperature() / 100.0
                temp_air1 = airtemp1.get_temperature() / 100.0
                temp_air2 = airtemp2.get_temperature() / 100.0
                temp_air3 = airtemp3.get_temperature() / 100.0
                rh = humidity.get_humidity() / 100.0
                co2_conc, co2_temp, co2_rh = CO2.get_all_values()

                data = [
                    now.strftime('%Y-%m-%d %H:%M:%S'), unixtime,
                    temp_globe2, temp_air3,
                    temp_globe1, temp_air1, rh, co2_conc, co2_temp / 100.0, co2_rh / 100.0,
                    temp_globe3, temp_air2
                ]
                write_to_csv(new_file_name, data)
                csv_timer = time.time()  # Reset the CSV timer

            if time.time() - log_timer >= log_print_interval:
                log.info(f"Logging temperatures and sensor data...")
                log.info(f"Globe and Air Temperatures at various heights logged successfully.")
                log_timer = time.time()  # Reset the log timer

            time.sleep(1)

    except Exception as e:
        log.error(f"An error occurred: {e}")
    finally:
        ipcon.disconnect()
        log.info("Disconnected from IP Connection")

if __name__ == "__main__":
    main()
