from math import log10

ADC_resolution_bits = 16
ADC_resolution = (2**ADC_resolution_bits) - 1

def adc_to_voltage(adc_value, max_voltage, adc_resolution):
    return adc_value * (max_voltage/adc_resolution)


#######################################Sensor Functions##########################################


def sensor_MQ9(adc_value):
    MQ9_R0 = .2118
    max_voltage = 5

    print(adc_value)


    voltage_value = adc_to_voltage(adc_value, max_voltage, ADC_resolution)

    print(voltage_value)

    if voltage_value == 0.0:
        return (["Ozone Sensor (MQ131)","Chlorine Gas Sensor (MQ131)", "Nitrogen Gas Sensor (MQ131)"],
               ["ppm", "ppm", "ppm"],
               [-1.0, -1.0, -1.0])

    Rs_gas = (5-voltage_value)/voltage_value

    ratio = Rs_gas/MQ9_R0

    Butane_yint = 1.419
    Butane_slope = -.473
    CarbonMonoxide_yint = 1.356
    CarbonMonoxide_slope = -.484
    Methane_yint = 1.365
    Methane_slope = -.380

    if ratio <= 0:
        return (["Butane Sensor (MQ9)","Carbon Monoxide Sensor (MQ9)", "Methane Sensor (MQ9)"],
               ["ppm", "ppm", "ppm"],
               [-1.0, -1.0, -1.0])

    ppm_log_Butane = (log10(ratio)-Butane_yint)/Butane_slope
    ppm_log_CarbonMonoxide = (log10(ratio)-CarbonMonoxide_yint)/CarbonMonoxide_slope
    ppm_log_Methane =  (log10(ratio)-Methane_yint)/Methane_slope

    ppm_Butane = 10**ppm_log_Butane
    ppm_CarbonMonoxide = 10**ppm_log_CarbonMonoxide
    ppm_Methane = 10**ppm_log_Methane

    return (["Butane Sensor (MQ9)","Carbon Monoxide Sensor (MQ9)", "Methane Sensor (MQ9)"],
           ["ppm", "ppm", "ppm"],
           [-1.0, -1.0, -1.0]) #ppm_Butane


def sensor_MQ131(adc_value):
    MQ131_R0 = .1217
    max_voltage = 5

    voltage_value = adc_to_voltage(adc_value, max_voltage, ADC_resolution)

    if voltage_value == 0:
        return (["Ozone Sensor (MQ131)","Chlorine Gas Sensor (MQ131)", "Nitrogen Gas Sensor (MQ131)"],
               ["ppm", "ppm", "ppm"],
               [-1.0, -1.0, -1.0])

    Rs_gas = (5-voltage_value)/voltage_value

    ratio = Rs_gas/MQ131_R0

    Ozone_yint = 1.019
    Ozone_slope = -.856
    ChlorineGas_yint = 1.405
    ChlorineGas_slope = -.827
    NitrogenDioxide_yint = 1.256
    NitrogenDioxide_slope = -.367

    if ratio <= 0:
        return (["Ozone Sensor (MQ131)","Chlorine Gas Sensor (MQ131)", "Nitrogen Gas Sensor (MQ131)"],
               ["ppm", "ppm", "ppm"],
               [-1.0, -1.0, -1.0])

    ppm_log_Ozone = (log10(ratio)-Ozone_yint)/Ozone_slope
    ppm_log_ChlorineGas = (log10(ratio)-ChlorineGas_yint)/ChlorineGas_slope
    ppm_log_NitrogenDioxide =  (log10(ratio)-NitrogenDioxide_yint)/NitrogenDioxide_slope

    ppm_Ozone = 10**ppm_log_Ozone
    ppm_ChlorineGas = 10**ppm_log_ChlorineGas
    ppm_NitrogenDioxide = 10**ppm_log_NitrogenDioxide

    return (["Ozone Sensor (MQ131)","Chlorine Gas Sensor (MQ131)", "Nitrogen Gas Sensor (MQ131)"],
           ["ppm", "ppm", "ppm"],
           [-1.0, -1.0, -1.0])


def conversionFunctionTemplate(adc_value, inc):

    value = 0.0

    return (["Sensor Name" + inc],
           ["Units"],
           [value-1000])

def testing(adc_value):
    value = adc_value
    return (["Sensor Name_Test"],
           ["Units"],
           [value])


#######################################Assigning conversion functions to ADC/Channel Values##########################################

def adc_1_channel_1(voltage):
    return sensor_MQ9(voltage)
def adc_1_channel_2(voltage):
    return sensor_MQ131(voltage)
def adc_1_channel_3(voltage):
    return testing(voltage)
def adc_1_channel_4(voltage):
    return conversionFunctionTemplate(voltage,'a14')

def adc_2_channel_1(voltage):
    return conversionFunctionTemplate(voltage,'a21')
def adc_2_channel_2(voltage):
    return conversionFunctionTemplate(voltage,'a22')
def adc_2_channel_3(voltage):
    return conversionFunctionTemplate(voltage,'a23')
def adc_2_channel_4(voltage):
    return conversionFunctionTemplate(voltage ,'a4')

def adc_3_channel_1(voltage):
    return conversionFunctionTemplate(voltage,'a31')
def adc_3_channel_2(voltage):
    return conversionFunctionTemplate(voltage,'a32')
def adc_3_channel_3(voltage):
    return conversionFunctionTemplate(voltage,'a33')
def adc_3_channel_4(voltage):
    return conversionFunctionTemplate(voltage,'a34')

def adc_4_channel_1(voltage):
    return conversionFunctionTemplate(voltage,'a41')
def adc_4_channel_2(voltage):
    return conversionFunctionTemplate(voltage,'a42')
def adc_4_channel_3(voltage):
    return conversionFunctionTemplate(voltage,'a43')
def adc_4_channel_4(voltage):
    return conversionFunctionTemplate(voltage,'a44')


sensor_functions = {
                    1: {1: adc_1_channel_1, 2: adc_1_channel_2, 3: adc_1_channel_3, 4: adc_1_channel_4},
                    2: {1: adc_2_channel_1, 2: adc_2_channel_2, 3: adc_2_channel_3, 4: adc_2_channel_4},
                    3: {1: adc_3_channel_1, 2: adc_3_channel_2, 3: adc_3_channel_3, 4: adc_3_channel_4},
                    4: {1: adc_4_channel_1, 2: adc_4_channel_2, 3: adc_4_channel_3, 4: adc_4_channel_4}
                   }
