from math import log10

ADC_resolution_bits = 16
ADC_resolution = (2**ADC_resolution_bits) - 1

def adc_to_voltage(adc_value, max_voltage, adc_resolution):
    return adc_value * (max_voltage/adc_resolution)


#######################################Sensor Functions##########################################


def sensor_MQ9(adc_value):
    MQ9_R0 = .2118
    max_voltage = 5

    voltage_value = adc_to_voltage(adc_value, max_voltage, ADC_resolution)

    Rs_gas = (5-voltage_value)/voltage_value

    ratio = Rs_gas/MQ9_R0

    Butane_yint = 1.419
    Butane_slope = -.473
    CarbonMonoxide_yint = 1.356
    CarbonMonoxide_slope = -.484
    Methane_yint = 1.365
    Methane_slope = -.380

    ppm_log_Butane = (log10(ratio)-Butane_yint)/Butane_slope
    ppm_log_CarbonMonoxide = (log10(ratio)-CarbonMonoxide_yint)/CarbonMonoxide_slope
    ppm_log_Methane =  (log10(ratio)-Methane_yint)/Methane_slope

    ppm_Butane = 10**ppm_log_Butane
    ppm_CarbonMonoxide = 10**ppm_log_CarbonMonoxide
    ppm_Methane = 10**ppm_log_Methane

    return (ppm_Butane, ppm_CarbonMonoxide, ppm_Methane)


def sensor_MQ131(adc_value):
    MQ131_R0 = .1217
    max_voltage = 5

    voltage_value = adc_to_voltage(adc_value, max_voltage, ADC_resolution)

    Rs_gas = (5-voltage_value)/voltage_value

    ratio = Rs_gas/MQ131_R0

    Ozone_yint = 1.019
    Ozone_slope = -.856
    ChlorineGas_yint = 1.405
    ChlorineGas_slope = -.827
    NitrogenDioxide_yint = 1.256
    NitrogenDioxide_slope = -.367

    ppm_log_Ozone = (log10(ratio)-Ozone_yint)/Ozone_slope
    ppm_log_ChlorineGas = (log10(ratio)-ChlorineGas_yint)/ChlorineGas_slope
    ppm_log_NitrogenDioxide =  (log10(ratio)-NitrogenDioxide_yint)/NitrogenDioxide_slope

    ppm_Ozone = 10**ppm_log_Ozone
    ppm_ChlorineGas = 10**ppm_log_ChlorineGas
    ppm_NitrogenDioxide = 10**ppm_log_NitrogenDioxide

    return (ppm_Ozone, ppm_ChlorineGas, ppm_NitrogenDioxide)

print(sensor_MQ131(10000))
