import math
# input values
LengthHA = 2000     
LengthKA = 2000      
LengthSA = 2000    

Ha_Wi = 8.41          
Ka_Wi = -19.77     

# calculate sine values (degrees to radians)
sin_Ha_Wi = math.sin(math.radians(Ha_Wi))
sin_Ha_Wi_Ka_Wi = math.sin(math.radians(Ha_Wi + Ka_Wi))

# calculate lengths
i32SinLenHA = LengthHA * sin_Ha_Wi
i32SinLenKASA = (LengthKA + LengthSA) * sin_Ha_Wi_Ka_Wi
r_hook = LengthHA * math.cos(math.radians(Ha_Wi)) + (LengthKA + LengthSA) * math.cos(math.radians(Ha_Wi + Ka_Wi)) - 500


# output 
print(f"i32SinLenHA = {i32SinLenHA:.1f}")
print(f"i32SinLenKASA = {i32SinLenKASA:.1f}")
print(f"Sum = {i32SinLenHA + i32SinLenKASA:.1f}")
print(f"r_hook = {r_hook:.1f}")