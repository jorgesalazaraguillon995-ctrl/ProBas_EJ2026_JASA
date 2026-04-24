try:
    filePointer = open('fname','r')
    try:
        content = filePointer.readline()
    finally:
        filePointer.close()
    except IOError as e:
print(str(e))