#!/usr/bin/python3
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    try:
        f = open('stats.json', 'r')
        stats = json.loads(f.read())
    except:
        print("Stats file missing or corrupt, please run donumbers.py")
        exit()
    while True:
        ans = input("Select view: counts(1) or times(2): ").strip().lower()
        if ans == 'exit' or ans == 'quit':
            break
        if ans not in ('1', '2'):
            continue
        if ans == '1':
            xAxis = [key for key, val in stats.items()]
            yAxis = [val[0] for key, val in stats.items()]
        else:
            xAxis = [key for key, val in stats.items()]
            yAxis = [val[1]/val[0] for key, val in stats.items()]
        fig = plt.figure()
        plt.bar(xAxis,yAxis, color='brown')
        plt.xlabel('method')
        if ans == '1':
            plt.ylabel('count')
        else:
            plt.ylabel('ave time')
        plt.show()
