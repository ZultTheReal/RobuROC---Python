# Motor controller object
motors = MotorControl()

# Logging object
log = Logging('measurements')

# Add logging variables and titles
log.addMeasurements( shit.data, ['X1','X2'])
log.addMeasurements( shit.other, [ 'X3','X4','X5'] )
log.begin()