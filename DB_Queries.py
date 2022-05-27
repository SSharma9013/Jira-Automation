import json

with open('./Files/Messages.txt', 'r+') as file_source:
    # read file
    data = json.load(file_source)  # Reading the file
    print('data=', data)
    for i in data:
        print('\n sender=',data[i]['sender'])
        print('\n reciever=', data[i]['reciever'])
        print('\n message=', data[i]['message'])