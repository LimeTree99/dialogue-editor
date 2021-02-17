import json

def run(senario):
    curr = senario['0']
    while True:
        print(curr["text"])
        for i in range(len(curr['choices'])):
            print(f"{i}: {curr['choices'][i][0]}")
        
        if len(curr['choices']) == 0:
            break

        choice = input('>>> ')
        curr = senario[curr['choices'][int(choice)][1]]

    print()
    print('End of senario')

def loop():
    while True:
        fp = input("Enter file path: ")
        try:
            fh = open(fp, "r")
            senario = json.load(fh)
            fh.close()
            print()
            run(senario)
            print()
            
        except OSError:
            print('Error opening file')


if __name__ == '__main__':
    loop()


