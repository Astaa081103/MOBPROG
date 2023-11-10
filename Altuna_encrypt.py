def secret_key_gen(secret_phrase):

    secret_key = "DEADBEEF"

    # Half ng secret phrase
    half_index = len(secret_phrase) // 2

    # left_binary = left side binary value ng secret phrase (nung naka half na)
    # right_binary = right side binary value ng secret phrase (nung naka half na)
    # left_xor = naka xor ng left side sa "DEADBEEF"
    # right_xor = naka xor ng right side sa "DEADBEEF"
    # secret_key_binary = binary characters ng "DEADBEEF"
    # combine_xor = pinag-add na value ng "left_xor" and "right_xor"
    left_binary = []
    right_binary = []
    left_xor = []
    right_xor = []
    secret_key_binary = []
    combine_xor = []

    # left_side = left side ng secret key
    # right_side = right side ng secret key
    left_side = secret_phrase[:half_index]
    right_side = secret_phrase[half_index:]

    # _bits_conversion = ginawa kong bits yung character ng arrays
    # _binary_conversion_input = ginawa kong binary yung bits ng character ng array
    # _binary.append() = in-append ko na yung binary value nung character sa respective array nila

    for i in left_side:
        left_bits_conversion = ord(i)
        L_binary_conversion_input = bin(left_bits_conversion)[2:].zfill(8)
        left_binary.append(L_binary_conversion_input)
        
    for j in right_side:
        right_bits_conversion = ord(j)
        R_binary_conversion_input = bin(right_bits_conversion)[2:].zfill(8)
        right_binary.append(R_binary_conversion_input)

    for k in secret_key:
        sk_bits_conversion = ord(k)
        sk_binary_conversion = bin(sk_bits_conversion)[2:].zfill(8)
        secret_key_binary.append(sk_binary_conversion)

    # dito ako nag xor ng left and right side ng secret key sa "DEADBEEF"

    for l in range(len(left_binary)):
        res_left = int(left_binary[l], 2) ^ int(secret_key_binary[l], 2)
        xor_left = bin(res_left)[2:].zfill(8)
        left_xor.append(xor_left)

        if l < len(right_binary):
            res_right = int(right_binary[l], 2) ^ int(secret_key_binary[l], 2)
            xor_right = bin(res_right)[2:].zfill(8)
            right_xor.append(xor_right)

    # pinagsama ko na yung 2 values ng array sa isang array (naka xor na sa "DEADBEEF")
    combine_xor = left_xor + right_xor
    
    return combine_xor

def open_file(filename):
    try:
        # pag open ng input file (.txt) 
        with open(filename, 'r') as f:
            text = f.read()
            if text is None:
                print("No value")
                exit()
        # naka group into 4 siya (every 4 character)
        grouped_text = [text[i:i + 4] for i in range(0, len(text), 4)]

        # dito ako nag padding ng '\x00' (null)
        grouped_text = [value.ljust(4, '\x00') for value in grouped_text]

        if len(grouped_text) % 2 == 1:
            grouped_text.append('\x00\x00\x00\x00')

        return grouped_text
    except FileNotFoundError:
        print(f"The input file '{filename}' was not found. Please make sure the file exists in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

def padding_0s(grouped_text, secret_key):
    mixed_binary = []
    
    if grouped_text is None:
        exit()
        # same din na padding (nakakatakot burahin baka kasi di na gumana)
    for hex in grouped_text:
        for binary in hex:
            dec_grouped = ord(binary)
            binary_grouped = bin(dec_grouped)[2:].zfill(8)
            mixed_binary.append(binary_grouped)
    
    grouped_4 = []
    for i in range(0, len(mixed_binary), 4):
        group_of_4 = mixed_binary[i:i + 4]
        while len(group_of_4) < 4:
            group_of_4.append("0" * 8)
        grouped_4.append(group_of_4)

    combine_xor = secret_key_gen(secret_key)
    binary_to_int(grouped_4, combine_xor)

def binary_to_int(grouped, combined_xor):

    # grouped = multi-dimensional array ng binary values ng input text (.txt file input)
    # a = kinuha ko yung 'a' kapag even yung grouped (binary values ng text)

    a = []
    sub_a = []
    int_a_arr = []
    b = []
    sub_b = []
    int_b_arr = []

    # seperating 'a' and 'b'
    for i in range(len(grouped)):
        if i % 2 == 0:
            a.append(grouped[i])
        else:
            b.append(grouped[i])

    for i in range(len(a)):
        for j in range(4):
            a_arr = a[i][j]
            int_a = int(a_arr, 2)
            sub_a.append(int_a)

    for i in range(len(b)):
        for j in range(4):
            b_arr = b[i][j]
            int_b = int(b_arr, 2)
            sub_b.append(int_b)

    start = 0
    end = 4
    for i in range(len(sub_a) // 4):
        sublist = sub_a[start:end]
        int_a_arr.append(sublist)
        start = end
        end += 4

    start1 = 0
    end1 = 4

    for i in range(len(sub_b) // 4):
        sublist1 = sub_b[start1:end1]
        int_b_arr.append(sublist1)
        start1 = end1
        end1 += 4

    feistel_cipher(int_a_arr, int_b_arr, combined_xor)


def nibble_shuffle_decimal(hex_string):
    q = ""
    q += hex_string[3]
    q += hex_string[7]
    q += hex_string[1]
    q += hex_string[5]
    q += hex_string[2]
    q += hex_string[4]
    q += hex_string[0]
    q += hex_string[6]
    
    return q

def feistel_cipher(a, b, combined_xor):
    key3 = combined_xor[12:16]
    key2 = combined_xor[8:12]
    key1 = combined_xor[4:8]
    key0 = combined_xor[0:4]

    key0_int_arr = [int(k, 2) for k in key0]
    key1_int_arr = [int(k, 2) for k in key1]
    key2_int_arr = [int(k, 2) for k in key2]
    key3_int_arr = [int(k, 2) for k in key3]

    # Nibble shuffle

    # i = rounds for nibble shuffle
    # j = Indexes ng a/b

    shuffled_a_values = []
    shuffled_b_values = []
    shuffled_a_final = []
    shuffled_b_final = []
    c = []

    for i in range(len(a)):
        for j in range(4):
            plain_a = a[i][j]
            xor_a = plain_a ^ key0_int_arr[j]
            hex_string = '{:02x}'.format(xor_a)
            shuffled_a_values.append(hex_string)
    result_string = ''.join(shuffled_a_values)

    chunks = [result_string[i:i+8] for i in range(0, len(result_string), 8)]
    for i in range(len(chunks)):
        res = chunks[i]
        for j in range(2):
            res = nibble_shuffle_decimal(res)
        shuffled_a_final.append(res)


    for k in range(len(b)):
        for l in range(4):
            plain_b = b[k][l]
            xor_b = plain_b ^ key1_int_arr[l]
            hex_string = '{:02x}'.format(xor_b)
            shuffled_b_values.append(hex_string)
    result_string1 = ''.join(shuffled_b_values)

    chunks1 = [result_string1[i:i+8] for i in range(0, len(result_string1), 8)]
    for i in range(len(chunks1)):
        res1 = chunks1[i]
        for j in range(2):
            res1  = nibble_shuffle_decimal(res1)
        shuffled_b_final.append(res1)


    a_into_4 = []
    b_into_4 = []
    int_a_arr = []
    int_b_arr = []
    int_a_arr_4 = []
    int_b_arr_4 = []
    final_a_arr_sana = []
    final_b_arr_sana = []

    for item in shuffled_a_final:
        groups_of_four = [item[i:i + 2] for i in range(0, len(item), 2)]
        a_into_4.append(groups_of_four)

    for item in shuffled_b_final:
        groups_of_four = [item[i:i + 2] for i in range(0, len(item), 2)]
        b_into_4.append(groups_of_four)


    for y in range(len(a_into_4)):
        for z in range(4):
            res2 = a_into_4[y][z]
            int_value = int(res2, 16)
            binary_string = bin(int_value)[2:].zfill(len(res2) * 4)
            int_a_arr.append(int(binary_string, 2))

    for w in range(len(b_into_4)):
        for x in range(4):
            res3 = b_into_4[w][x]
            int_value = int(res3, 16)
            binary_string = bin(int_value)[2:].zfill(len(res3) * 4)
            int_b_arr.append(int(binary_string, 2))
    
    for i in range(0, len(int_a_arr), 4):
        subgroup = int_a_arr[i:i + 4]
        int_a_arr_4.append(subgroup)

    for i in range(0, len(int_b_arr), 4):
        subgroup = int_b_arr[i:i + 4]
        int_b_arr_4.append(subgroup)

    for p in range(len(int_a_arr_4)):
        for q in range(4):
            z_a = int_a_arr_4[p][q]
            int_z_a = z_a ^ key2_int_arr[q]
            hex_string = '{:02x}'.format(int_z_a)
            final_a_arr_sana.append(hex_string)
    
    for r in range(len(int_b_arr_4)):
        for s in range(4):
            z_b = int_b_arr_4[r][s]
            int_z_b = z_b ^ key3_int_arr[s]
            hex_string = '{:02x}'.format(int_z_b)
            final_b_arr_sana.append(hex_string)

    c = []
    for i in range(0, len(final_a_arr_sana), 4):
        c.extend(final_a_arr_sana[i:i+4])
        c.extend(final_b_arr_sana[i:i+4])

    output_filename = input("Enter output file name: ")
    write_output(c, output_filename)

def write_output(val, output_filename):
    with open(output_filename + ".ctx", 'wb') as f:
        int_values = [int(hex_str, 16) for hex_str in val]
        byte_values = bytes(int_values)
        f.write(byte_values)
            
secret_key = input("Enter a secret key: ")
while len(secret_key) != 16:
    print("Secret key must be exactly 16 characters")
    secret_key = input("Enter a secret key: ")

filename = input("Enter file name: ")
grouped_characters = open_file(filename)
padding_0s(grouped_characters, secret_key)