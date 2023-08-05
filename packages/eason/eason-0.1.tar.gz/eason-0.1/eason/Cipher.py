def CaesarEncoder(text):
    text = list(str(text))
    for i in range(len(text)):
        temp = ord(str(text[i]))
        temp = temp * (i+1)
        temp = temp - 2*i
        temp = temp + 90
        text[i] = chr(temp)
    text = "".join(text)
    return text

def CaesarDecoder(text):
    text = list(str(text))
    for i in range(len(text)):
        temp = ord(str(text[i]))
        temp = temp - 90
        temp = temp + 2*i
        temp = temp / (i+1)
        text[i] = chr(int(temp))
    text = "".join(text)
    return text