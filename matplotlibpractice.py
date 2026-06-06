import matplotlib.pyplot as plt
import numpy as np
#task 1
def plot_line(title,labelx,labely,x,y):
    plt.plot(x,y,marker='*',color= 'red',linestyle='--')
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
# plot_line("Weekly Temperature Trend","Days","Temperature",[1,2,3,4,5,6,7],[27,29,26,32,45,38,40])

#task 2
def plot_bar(title,labelx,labely,x,y):
    plt.bar(x,y,color = 'yellow')
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
def plot_barh(title,labelx,labely,x,y):
    plt.barh(x,y,color = 'yellow')
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()

# plt.figure(figsize = (12,6))
# plt.subplot(1,2,1)
# plot_bar("Employee/Department Distribution","Departments","Number of Employees",["HR","IT","Sales","Marketing"],[10,25,15,20])
# plt.subplot(1,2,2)
# plot_barh("Employee/Department Distribution","Departments","Number of Employees",["HR","IT","Sales","Marketing"],[10,25,15,20])
# plt.tight_layout()
# plt.show()

#task 3
def plot_histogram(title,labelx,labely,data,bins):
    plt.hist(data,bins = bins,color = 'cyan',edgecolor = 'black')
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
# data = np.random.randint(0,101,size = 30)
# plot_histogram("Marks Distribution","Marks","Number of Students",data,bins = [0,10,20,30,40,50,60,70,80,90,100])

#task 4
def plot_scatter(title,labelx,labely,x,y):
    plt.scatter(x,y,color = 'magenta',marker = 'o')
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
# study_hours = [2,3,4,5,6,7,8,9,10,11]
# gpa = [2.5,2.7,3.0,3.2,3.5,3.7,3.8,4.0,4.0,4.0]
# plot_scatter("Study Hours vs GPA","Study Hours","GPA",study_hours,gpa)

#task 5
labels = ["Salaries","Equipments","Research","Maintenance"]
sizes = [40,20,25,15]
def plot_pie(title,labels,sizes):
    plt.pie(sizes, labels=labels, colors=['gold','lightcoral','lightskyblue','lightgreen'])
    plt.title(title)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
plot_pie("Allocations",labels,sizes)