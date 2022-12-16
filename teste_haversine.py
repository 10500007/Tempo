from haversine import haversine

#lyon = (45.7597, 4.8422) # (lat, lon)
lyon = (-12.2311, -48.3891) # (lat, lon)
#paris = (48.8567, 2.3508)
#paris = (-46.8869, -11.5835)
paris = (-11.5835, -46.8869)

print(haversine(lyon, paris))