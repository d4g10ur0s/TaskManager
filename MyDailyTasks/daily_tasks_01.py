import datetime as dt
import os
import json

# base Class of your App inherits from the App class.
from kivy.app import App
# GridLayout arranges children in a matrix.
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.lang import Builder

# Label is used to label something
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
# used to take input from users
from kivy.uix.textinput import TextInput

Builder.load_file('daily_tasks_01.kv')


'''

This is  an open source task manager.
Everything is stored every time the app boots or exits.

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

Basic Functions :
                1)Show your pending tasks
                2)Manage your expired tasks
                3)Show periodic tasks
                4)Create Task
                5)Create Periodic Task
                6)Exit
                7)Menu

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

I. Show Pending Tasks

1. get path of day
2. is path valid
3. read file
4. is file written
5. create pending tasks
6. show pending tasks

*I.1
    2.1 path not valid
    2.2 create path
    2.3 create file
    2.4 Menu

*I.2
    4.1 file is not written
    4.2 print
    4.3 Menu

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

II.

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

III.

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

IV. Create Task

1. name, when, state
2. create task
3. store task in pending list
4. menu

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

'''




f = __file__

class Task :
    when = None
    name = None
    state = 'Pending'
    mnum = 0

    def __init__(self,name = None,state = 'Pending', when = None,mnum = 0):
        self.name = name
        self.when = when
        self.state = state
        self.mnum = mnum

    def toDict(self):
        return {
        "name" : self.name,
        "when" : str(self.when),
        "state" : self.state
        }

    def toString(self):
        return str(self.mnum) + " ) " + self.name + " " + self.whenString() + " " + self.state
    def whenString(self):
        return str(self.when)
    def is_old(self):
        if self.when < dt.datetime.today():
            self.expired()
            return True
        else:
            return False
    def expired(self):
        self.state = 'Expired'
    def done(self):
        self.state = 'Done'
    #setter
    def set_name(self,name):
        self.name = name
    def set_when(self,when):
        self.when = when
    def set_state(self,state):
        self.state = state
    #getter
    def get_name(self):
        return self.name
    def get_when(self):
        return self.when
    def get_state(self):
        return self.state

def get_date_path(f):
    temp = str(f).split('\\')
    next_path = ""
    for i in temp[:len(temp)-1]:
        next_path += str(i) + '\\'#ara sto telos exw  \\ mono onoma menei

    return next_path

def todays_tasks(f):
    temp = f + "Days\\"
    td = dt.datetime.today()#pairnw thn shmerinh hmera kai ftiaxnw antistoixo file
    #path --> year/month/day
    #gia year
    if os.path.exists(temp+str(td.year)):
        pass
    else:
        os.mkdir(temp+str(td.year))
    temp += str(td.year) + '\\'
    #gia month
    if os.path.exists(temp+str(td.strftime("%B"))):
        pass
    else:
        os.mkdir(temp+str(td.strftime("%B")))
    temp += str(td.strftime("%B")) + '\\'
    #gia day
    if os.path.exists(temp+str(td.day)):
        pass
    else:
        os.mkdir(temp+str(td.day))
    temp += str(td.day)
    #to personal file einai ta personal tasks
    #format : name - time - state
    if os.path.exists(temp+'\\PersonalTasks.json'):
        return (temp,True)
    else:
        f = open(temp+'\\PersonalTasks.json','w+')
        f.close()
        return (temp,False)

def check_file(path):
    #1 anoigw file
    opened_file = open(path,'r+')
    #2 diavazw
    tasks = opened_file.readlines()
    opened_file.close()
    if len(tasks) > 0 :
        #3 elegxos
        return (tasks, True)
    else:
        return (None, False)

def date_input():
    #date
    while 1 :
        try :
            day = int(input("Day : "))
            month = int(input("Month : "))
            year = int(input("Year : "))
            break
        except ValueError :
            pass
    #time
    while 1 :
        try :
            hour = int(input("Hour : "))
            minute = int(input("Minute : "))
            seconds = int(input("Seconds : "))
            break
        except ValueError :
            pass

    return dt.datetime(year,month,day,hour,minute,seconds)

def add_task():
    task = Task()
    task.set_name(str(input("Name : ")))
    print(task.get_name())
    task.set_when(date_input())
    print(task.get_when().strftime('%Y-%B-%d %H:%M:%S'))
    return task

def save_task(path,tasks):
    #set up path
    tpath = path
    for task in tasks :
        path += "Days\\"
        path += task.get_when().strftime('%Y') + '\\' + task.get_when().strftime('%B') + '\\' + task.get_when().strftime('%d') + '\\PersonalTasks.json'
        opened_file = open(path,'r+')
        opened_file.seek(0,2)
        json.dump(task.toDict(),opened_file)
        opened_file.close()
        path = tpath#arxikopoihsh

def merge_old_tasks(path):
    contents = []
    path += "Days\\"
    #check posous fakelous
    for i in os.listdir(path):
        #pernaw se mhnes
        for j in os.listdir(path + str(i) + '\\'):
            #pernaw se hmeres
            for k in os.listdir(path + str(i) + '\\' + str(j) + '\\'):
                print(str(k))
                if k == dt.datetime.today().day :
                    pass
                else:
                    if os.path.exists(path + str(i) + '\\' + str(j) + '\\' + k +'\\'):
                        if os.path.exists(path + str(i) + '\\' + str(j) + '\\' + k +'\\PersonalTasks.json'):
                            #pairnw content apo arxeio
                            fl = open(path + str(i) + '\\' + str(j) + '\\' + k +'\\PersonalTasks.json', 'r+')
                            contents += fl.readlines()
                            fl.close()
                            #diagrafw arxeio
                            os.remove(path + str(i) + '\\' + str(j) + '\\' + k +'\\PersonalTasks.json')
                        os.rmdir(path + str(i) + '\\' + str(j) + '\\' + str(k)+'\\')
    return create_tasks_from_json(contents)

def create_tasks_from_json(tasks):
    to_ret = []
    for i ,v in zip(tasks ,range(1,1+len(tasks))) :
        t = json.loads(i)
        to_ret.append(Task(name = t["name"],when = dt.datetime.strptime(t["when"], '%Y-%m-%d %H:%M:%S'), state = t["state"],mnum = v ))
    return to_ret

def combined_functionality():

    #main loop
    path = get_date_path(f)
    tasks = merge_old_tasks(path)
    save_task(path,tasks)
    path, ex = todays_tasks(path)#to path gia thn shmerinh hmera kai an uparxoun tasks
    tasks,ex = check_file(path+'\\PersonalTasks.json')#an uparxoun tasks
    if ex :
        #print ola ta tasks
        tasks = create_tasks_from_json(tasks)
    else:
        print('No Tasks')

    while 1 :
        #printarw
        if tasks == None :
            tasks = []
        elif len(tasks) == 1:
            print("1" + " "*2 +"--"*2+">"+" "*2 + tasks[0].toString() )
        else:
            for i ,v in zip(tasks ,range(1,1+len(tasks))) :
                print(str(v) + " "*2 +"--"*2+">"+" "*2 + i.toString() )
        #promt menu
        main_functions = ['Add Task', 'Delete Task', 'Task Done', 'Quit']
        for i in main_functions:
            print('*'*10)
            print(i)
            print('*'*10)

        #choose functionality
        choose_function = int(input("What Would You Like To Do Today ?\n\n"))
        if choose_function == 1:
            #dhmiourgia task
            tasks.append(add_task())
        elif choose_function == 2 :
            pass
        elif choose_function == 3 :
            choose_function = int(input("Finished Task : "))
            tasks[choose_function-1].done()
        elif choose_function == 4:
            save_task(get_date_path(f),tasks)#apo8hkeush ke eksodos
            exit()

class Create_Task_Layout(BoxLayout):
    pass

class Task_Layout(BoxLayout):
    def __init__(self,task = Task() ,**var_args):
        super(Task_Layout, self).__init__(**var_args)
        self.task_info.text = task.toString()

class MainScreen(BoxLayout):
    tasks = []
    deikths = 0#gia na vlepw pu eimai

    def __init__(self, **var_args):
        super(MainScreen, self).__init__(**var_args)
        #bindings
        self.ids.options_layout.bind(text = self.operation)#dialogh operation
        #main things
        path = get_date_path(f)
        self.tasks = merge_old_tasks(path)
        save_task(path,self.tasks)
        path, ex = todays_tasks(path)#to path gia thn shmerinh hmera kai an uparxoun tasks
        self.tasks,ex = check_file(path+'\\PersonalTasks.json')#an uparxoun tasks
        if ex :
            #topo8etw ola ta tasks
            self.tasks = create_tasks_from_json(self.tasks)
        else:
            #vazw keno
            pass
        self.put_tasks()
        #event.cancel()
    def put_tasks(self):
        try :
            for i in self.tasks:
                self.main_content.put_data.add_widget(Task_Layout(i))
            event = Clock.schedule_interval(self.go_upwards, 1.5)
        except TypeError:
            self.main_content.put_data.add_widget(Label(text = ' No Tasks '))

    def go_upwards(self,k):
        self.main_content.put_data.remove_widget(self.main_content.put_data.children[self.deikths])
        self.main_content.put_data.add_widget(Task_Layout(self.tasks[self.deikths]))
        if len(self.tasks) - 1 == self.deikths:
            self.deikths = 0
        else:
            self.deikths+=1

    def operation(self,instance,pos,**kwargs):
        if str(self.ids.options_layout.text) == 'Add' :
            #dhmiourgia
            self.ids.main_content.clear_widgets()
            self.ids.main_content.add_widget(Create_Task_Layout())
            self.ids.options_layout.text = 'Control Buttons'
            pass
        elif str(self.ids.options_layout.text) == 'Done' :
            #oloklhrwsh
            self.ids.options_layout.text = 'Control Buttons'
            pass
        elif str(self.ids.options_layout.text) == 'Delete':
            #diagrafh
            self.ids.options_layout.text = 'Control Buttons'
            pass
        elif str(self.ids.options_layout.text) == 'Quit':
            exit()
# the Base Class of our Kivy App
class MyApp(App):
    def build(self):
        # return a LoginScreen() as a root widget
        return MainScreen()


if __name__ == '__main__':
    MyApp().run()
