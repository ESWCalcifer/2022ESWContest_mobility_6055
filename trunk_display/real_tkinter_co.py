import tkinter as tk
import serial
ser=serial.Serial('/dev/ttyACM0',9600, timeout=1)
ser.reset_input_buffer()

root=tk.Tk()
root.title('Trunk display')
root.geometry("600x500+100+100")
lab11=tk.Label(root, text="CO:",width=8,height=1)
lab11.grid(row=0, column=0,padx=5, pady=10)
#ent12=tk.Entry(font=('맑은 고딕',16,'bold'),bg='white',width=8)
#ent12.grid(row=0,column=1,padx=5,pady=10)

#co농도 받아온 변수 e
#entco=80.

#=80

#entco.set(80.0)

coppm = 0.
a=tk.DoubleVar(root,8.0)
b=tk.DoubleVar(root,9.0)
c=tk.DoubleVar(root,10.0)
entco=tk.DoubleVar(root,coppm)
#entco=tk.DoubleVar(root,coppm)
def read_serial():
    while True:
        if ser.in_waiting>0:
            line=ser.readline().decode('utf-8').rstrip()
            if(line[0:3]=='PPM'):
                coppm=float(line[6:])
                #lab12['textvariable']=str(coppm)
                print(coppm)
                entco=tk.DoubleVar(root,coppm)
                lab12=tk.Label(root, textvariable=entco, width=8,height=1)
                lab12.grid(row=0, column=1,padx=5, pady=10)
                if entco.get()<a.get():
                    lab14=tk.Label(root, text=" ", width=2,height=1,bg='#228B22',fg='white')
                    lab14.grid(row=0, column=4,padx=5, pady=10)
                elif entco.get()<b.get() and  entco.get()>=a.get():
                    lab14=tk.Label(root, text=" ", width=2,height=1,bg='#FFFF00',fg='white')
                    lab14.grid(row=0, column=4,padx=5, pady=10)
                elif entco.get()<c.get() and entco.get()>=b.get():
                    lab14=tk.Label(root, text=" ", width=2,height=1,bg='#FF8C00',fg='white')
                    lab14.grid(row=0, column=4,padx=5, pady=10)
                else:
                    lab14=tk.Label(root, text=" ", width=2,height=1,bg='#FF0000',fg='white')
                    lab14.grid(row=0, column=4,padx=5, pady=10)

                break
    root.after(10,read_serial)
    #print(coppm)
#root.after(10,read_serial)
#entco=tk.DoubleVar(root,coppm)
#lab12=tk.Label(root, textvariable=entco, width=8,height=1,bg='#2F5597',fg='white')
#lab12.grid(row=0, column=1,padx=5, pady=10)
# while True:
    #lab12=tk.Label(root, textvariable=entco, width=8,height=1,bg='#2F5597',fg='white')
    #lab12.grid(row=0, column=1,padx=5, pady=10)
    #break
lab13=tk.Label(root, text="ppm",width=8,height=1)
lab13.grid(row=0, column=3,padx=5, pady=10)

                #a=tk.DoubleVar(root,80.0)
                #b=tk.DoubleVar(root,150.0)
                #c=tk.DoubleVar(root,200.0)
###
if entco.get()<a.get():
    lab14=tk.Label(root, text=" ", width=2,height=1,bg='#228B22',fg='white')
    lab14.grid(row=0, column=4,padx=5, pady=10)
        
elif entco.get()<b.get() and  entco.get()>=a.get():
    lab14=tk.Label(root, text=" ", width=2,height=1,bg='#FFFF00',fg='white')
    lab14.grid(row=0, column=4,padx=5, pady=10)
        

elif entco.get()<c.get() and entco.get()>=b.get():
    lab14=tk.Label(root, text=" ", width=2,height=1,bg='#FF8C00',fg='white')
    lab14.grid(row=0, column=4,padx=5, pady=10)

else:
    lab14=tk.Label(root, text=" ", width=2,height=1,bg='#FF0000',fg='white')
    lab14.grid(row=0, column=4,padx=5, pady=10)
###

#double_variable = tk.DoubleVar(root,55.2)
 
#lab12 = tk.Label(root, textvariable=double_variable, width=8,height=1)
#lab12.grid(row=0, column=1,padx=5, pady=10)


root.after(100,read_serial)   
root.mainloop()
# root.after(10,read_serial)  
