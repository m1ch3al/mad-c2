from PyQt5.Qt import *
from m1ch3al.pyqt5_widgets.thermo import Thermometer
from ui_forms.main_window_ui import Ui_MainWindow
import yaml
from utils import calculate_pitch_roll
from madis.network.udp_client import UDPClient


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, config_file):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._config_file = config_file
        self._is_connected = False

        self.altitude_thermo = Thermometer(min_value=0, max_value=10, steps=20)
        self.pressure_thermo = Thermometer(min_value=990, max_value=1080, steps=10)
        self.temperature_thermo = Thermometer(min_value=0, max_value=50, steps=10)
        self.humidity_thermo = Thermometer(min_value=0, max_value=100, steps=10)

        self._motor_image_filepath = "ui_forms/images/brushless_motor_icon_02.png"
        self.label_motor_1.setPixmap(QPixmap(self._motor_image_filepath))
        self.label_motor_2.setPixmap(QPixmap(self._motor_image_filepath))
        self.label_motor_3.setPixmap(QPixmap(self._motor_image_filepath))
        self.label_motor_4.setPixmap(QPixmap(self._motor_image_filepath))

        self._initialize_ui_events()

        self._update_methods = dict()
        self._update_methods["gps"] = self._update_navigation
        self._update_methods["environmental"] = self._update_environment
        self._update_methods["inclinometer"] = self._update_vehicle_stability

        self._network_configuration = dict()
        self._create_network_udp_client()

    def _create_network_udp_client(self):
        with open(self._config_file, "r") as yaml_file_descriptor:
            network_configuration = yaml.safe_load(yaml_file_descriptor)
        yaml_file_descriptor.close()
        for element in network_configuration["network-configuration"]:
            sensor_name = element["udp-client-configuration"]["sensor"]
            host = element["udp-client-configuration"]["host"]
            port = element["udp-client-configuration"]["port"]
            self._network_configuration[sensor_name] = UDPClient(host, port, self._update_methods[sensor_name])

    def _initialize_ui_events(self):
        self.pushButton_connect.clicked.connect(self._connect)
        self.pushButton_exit.clicked.connect(exit_program)
        self._initialize_altitude_thermo()
        self._initialize_pressure_thermo()
        self._initialize_temperature_thermo()
        self._initialize_humidity_thermo()

    def _initialize_altitude_thermo(self):
        altitude_thermo_layout = QVBoxLayout()
        altitude_thermo_layout.addWidget(self.altitude_thermo)
        self.frame_altitude.setLayout(altitude_thermo_layout)

    def _initialize_pressure_thermo(self):
        pressure_thermo_layout = QVBoxLayout()
        pressure_thermo_layout.addWidget(self.pressure_thermo)
        self.frame_pressure.setLayout(pressure_thermo_layout)

    def _initialize_temperature_thermo(self):
        temperature_thermo_layout = QVBoxLayout()
        temperature_thermo_layout.addWidget(self.temperature_thermo)
        self.frame_temperature.setLayout(temperature_thermo_layout)

    def _initialize_humidity_thermo(self):
        humidity_thermo_layout = QVBoxLayout()
        humidity_thermo_layout.addWidget(self.humidity_thermo)
        self.frame_humidity.setLayout(humidity_thermo_layout)

    def _connect(self):
        #self.temperature_thermo.set_value(24.5)
        for sensor_name in self._network_configuration:
            self._network_configuration[sensor_name].initialize_connection()
        self.label_Status.setText("Status : CONNECTED - MAD System is on-line")

    def _update_vehicle_stability(self, data):
        stabilizer_data = yaml.safe_load(data.decode())
        accel_x = stabilizer_data["acceleration_x"]
        accel_y = stabilizer_data["acceleration_y"]
        accel_z = stabilizer_data["acceleration_z"]
        self.lineEdit_accel_X.setText("{}".format(accel_x))
        self.lineEdit_accel_Y.setText("{}".format(accel_y))
        self.lineEdit_accel_Z.setText("{}".format(accel_z))
        pitch_deg, roll_deg = calculate_pitch_roll(accel_x, accel_y, accel_z)
        self.lineEdit_pitch.setText("{}".format(round(pitch_deg, 3)))
        self.lineEdit_roll.setText("{}".format(round(roll_deg, 3)))

    def _update_navigation(self, data):
        navigation_data = yaml.safe_load(data.decode())
        self.lineEdit_latitude.setText("{}".format(navigation_data["latitude"]))
        self.lineEdit_longitude.setText("{}".format(navigation_data["longitude"]))
        self.lineEdit_speed.setText("{}".format(navigation_data["speed"]))
        self.lineEdit_gps_status.setText("{}".format(navigation_data["status"]))
        self.lineEdit_gps_mode.setText("{}".format(navigation_data["mode"]))
        self.lineEdit_gps_time.setText("{}".format(navigation_data["gps-time"]))

    def _update_environment(self, data):
        environmental_data = yaml.safe_load(data.decode())
        altitude = environmental_data["altitude"]
        self.altitude_thermo.set_value(altitude)
        self.lineEdit_altitude.setText("{}".format(altitude))
        pressure = environmental_data["pressure"]
        self.pressure_thermo.set_value(pressure)
        self.lineEdit_pressure.setText("{}".format(pressure))
        temperature = environmental_data["temperature"]
        self.temperature_thermo.set_value(temperature)
        self.lineEdit_temperature.setText("{}".format(temperature))
        humidity = environmental_data["humidity"]
        self.humidity_thermo.set_value(humidity)
        self.lineEdit_humidity.setText("{}".format(humidity))


def exit_program():
    exit(0)
