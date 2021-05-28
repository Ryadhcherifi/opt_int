import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
def plotcycle(points,route,cout,file_path):
    font1 = {'family':'serif','color':'blue','size':20}
    font2 = {'family':'serif','color':'darkred','size':15}
    custom_line = [Line2D([0], [0], color='blue', lw=4)]
    axx=plt.figure(1, figsize=(15, 15)) 
    
    plt.title("Graphe du cycle des villes visitées",fontdict = font1)
    plt.ylabel('ordonnées des villes',fontdict = font2)
    plt.xlabel('abscisses des villes',fontdict = font2)

    sorted_list1=[]
    for i in range(len(route)):
        sorted_list1.append([points[route[i]-1][0],points[route[i]-1][1]])
    x=list(list(zip(*sorted_list1))[0])
    y=list(list(zip(*sorted_list1))[1])
    axx=plt.plot(x, y, '-p', color='blue',
             markersize=8, linewidth=2,
             markerfacecolor='white',
             markeredgecolor='red',
             markeredgewidth=2)
    phrase="Cout total du cycle:"+str(cout)
    plt.legend(custom_line, [phrase],prop={'size': 14},loc="upper left")
    i=1
    for elem in points:
        plt.annotate (str(i),(elem[0],elem[1]))
        i=i+1
    plt.savefig(file_path+'.png')