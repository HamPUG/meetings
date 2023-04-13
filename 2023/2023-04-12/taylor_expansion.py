# taylor_expansion.py
# From: https://github.com/micropython/micropython/blob/master/ports/rp2/machine_adc.c
# Scale raw reading to 16 bit value using a Taylor expansion (for 8 <= bits <= 16)
def taylor_series(raw_value):
    bits = 12    
    return raw_value << (16 - bits) | raw_value >> (2 * bits - 16)

list_16_bit = []    
taylor_value = 0    
for i in range(4097):
    taylor_previous = taylor_value 
    taylor_value = taylor_series(i)
    print(i, taylor_value, taylor_value-taylor_previous )

    # Uncomment for just the difference of 17
    #if  taylor_value-taylor_previous == 17:
    #    print(i, taylor_value, taylor_value-taylor_previous )
    list_16_bit.append(taylor_value)
#print(list_16_bit)

for bit_16 in list_16_bit:
    bit_12 = bit_16 >> 4
    print(bit_16, bit_12)
    
    
"""    
# Increment = 16, except...
0 0 0
1 16 16

256 4097 17
512 8194 17
768 12291 17
1024 16388 17
1280 20485 17
1536 24582 17
1792 28679 17
2048 32776 17
2304 36873 17
2560 40970 17
2816 45067 17
3072 49164 17
3328 53261 17
3584 57358 17
3840 61455 17

4095 65535 16

4096 65552 17
====

65391 4086
65407 4087
65423 4088
65439 4089
65455 4090
65471 4091
65487 4092
65503 4093
65519 4094
65535 4095
65552 4097

"""

