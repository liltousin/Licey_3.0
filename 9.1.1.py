bmp_input = open('input.bmp', 'rb')
bmp_res = open('res.bmp', 'wb')

bmp_res.write(bmp_input.read(54))

bmp_input_data = bmp_input.read(1)

while bmp_input_data:
    bmp_res.write(bytes([255 - bmp_input_data[0]]))
    bmp_input_data = bmp_input.read(1)

bmp_input.close()
bmp_res.close()
