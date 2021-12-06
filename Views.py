from tkinter import Button, Canvas, Entry, Frame, Label, Scrollbar, StringVar, Text, Tk, Toplevel, ttk
from tkinter.constants import END, LEFT, RIGHT, VERTICAL, WORD, YES
from PIL import Image, ImageTk
from Final_Project.Models import Priority_Q_Tickets
from Models import User, Ticket


#=============================================Frames========================================

class Login_Frame(Frame):
    def __init__(self, master):
        #Configuring frame
        bg_color="#393939"
        fg_color="#ffffff"
        main_font = "Calibri 18"
        super().__init__(master, bg=bg_color, pady=(100))
        
        #Configuring frame widgets
        title_label = Label(self, text="Ticket Management System", bg=bg_color, fg=fg_color, 
                            font="Calibri 26")
        title_label.pack()
        #Label and textbox for username login
        middleframe=Frame(self, bg="#6D3591", relief="raised")
        middleframe.pack(ipady=100, ipadx=100, padx=50)
        username_lbl = Label(middleframe, text="UserName:", font=main_font, bg="#6D3591", fg=fg_color)
        username_lbl.pack(pady=(50,0))
        username_input = Entry(middleframe, font=main_font)
        username_input.insert(END, "slayer232")
        username_input.pack(pady=(0, 20))
        
        #Label and textbox for password login
        password_lbl = Label(middleframe, text="Password:", font=main_font, bg="#6D3591", 
                            fg=fg_color)
        password_lbl.pack()
        password_input = Entry(middleframe, font=main_font, show="*")
        password_input.insert(END, "password")
        password_input.pack()
        
        #Error label I initialize this here so I can use this in my validation but only pack
        #it in the frame so it will go under the submit button
        #Error Label to display errors when logging in 
        error_lbl = Label(middleframe, text="", bg="#6D3591", fg=fg_color, font="Calibri 14")
        
        #Submit button with validation methods 
        def __validate_user(username, password):
            try:
                user = master.accepted_users[username]
                if(user.password != password):
                    error_lbl.config(text="That password does not match.")
                else:
                    if user.is_admin == True:
                        master.user_frame = Admin_Frame(master)
                        master.user_frame.grid(row=0, column=0, sticky="nsew")
                    else:
                        master.current_user = user
                        master.user_frame = User_Frame(master)
                        master.user_frame.grid(row=0, column=0, sticky="nsew")
            except(KeyError):
                error_lbl.config(text="That user does not exist.")
                
        submit_user_btn = Button(middleframe, text="Submit", bg=fg_color, font="Calibri 14",
                command=lambda:__validate_user(username_input.get(), password_input.get()))
        submit_user_btn.pack(pady=20)
        
        #Placing Error label
        error_lbl.pack()
            
        #My company logo since I own a corporation in this imaginary world
        co_lbl = Label(middleframe, text="Logan Co.", bg="#6D3591", fg=fg_color, 
                       font="Calibri 10")
        co_lbl.pack(side="bottom")

class User_Frame(Frame):
    main_font = "Calibri 18"
    def __init__(self, master):
        bg_color="#393939"
        fg_color="#ffffff"
        super().__init__(master, bg=bg_color)   
        message=f"{master.current_user.first_name}'s Ticket's"
        self.welcome_banner = Label(self, font="Calibri 25", text=message,
                                    bg=bg_color, fg=fg_color)
        self.welcome_banner.pack(pady=30)
        self.master = master
        
        #Getting current user and the user's tickets from the master window which acts as
        #a controller.
        current_user = master.current_user
        self.user_tickets = master.tickets[current_user.id]
        
        #Creating a frame to store a tree view table in to show users tickets
        #self.table_frame = Frame(self, bg="#6D3591")
        self.table_Frame = Frame(self, bg="#6D3591")
        #Configuring settings for treeview
        style = ttk.Style()
        style.configure("Treeview", font=(None, 14))
        style.configure("Treeview", rowheight=int(60))
        self.tree_columns = ["Id", "Title", "Problem", "Date Created", "Status"]
        self.tree_view = ttk.Treeview(self.table_Frame, columns=self.tree_columns, show="headings")
        self.__populate_tickets()
        
        self.tree_view.pack(expand=True, fill='both', padx=40)
        self.table_Frame.pack(ipadx=20, ipady=20, expand=True, fill="both")
        #Button area 
        self.button_area = Frame(self, bg="#393939")
        add_button = Button(self.button_area, text="Add", font="Calibri 18", command=lambda:self.__get_addpage()).grid(
            ipadx=10,row=0, column=0, padx=20, pady=20)
        delete_button = Button(self.button_area, text="Delete", font="Calibri 18", 
                               command=lambda:self.__delete_ticket()).grid(
            ipadx=5,row=0, column=1, padx=20, pady=20)
        self.button_area.pack(ipadx=20, ipady=20)
        delete_button = Button(self.button_area, text="Back To Login", font="Calibri 18", 
                               command=lambda:self.__backtologin()).grid(
            ipadx=5,row=0, column=2, padx=20, pady=20)
        self.button_area.pack(ipadx=20, ipady=20)
        
    def __get_addpage(self):
        add_frame = Add_Frame(self.master)
        add_frame.grid(row=0, column=0, sticky="nsew")
        
    def __populate_tickets(self):
        for col in self.tree_columns:
            self.tree_view.heading(col, text=col)
            self.tree_view.column(col, stretch=YES)
            
        #Populates the treeview with tickets information
        for ticket in self.user_tickets:
            ticket_info = (ticket.id, ticket.subject, ticket.problem, ticket.date_created,
                            ticket.status)
            self.tree_view.insert("", END, values=ticket_info)
            
    def __delete_ticket(self):
        selected_item = self.tree_view.selection()[0]
        ticket_id = self.tree_view.item(selected_item)["values"][0]
        for ticket in self.user_tickets:
            if ticket.id == ticket_id:
                self.user_tickets.remove(ticket)
        self.tree_view.delete(selected_item)
    
    def __backtologin(self):
        self.master.login_frame.tkraise()
        
class Admin_Frame(Frame):
    main_font = "Calibri 18"
    def __init__(self, master):
        bg_color="#393939"
        fg_color="#ffffff"
        super().__init__(master, bg=bg_color)   
        message="Admin Page"
        self.welcome_banner = Label(self, font="Calibri 25", text=message,
                                    bg=bg_color, fg=fg_color)
        self.welcome_banner.pack(pady=30)
        self.master = master
        
        #Getting current user and the user's tickets from the master window which acts as
        #a controller.
        self.current_user = master.current_user
        self.user_tickets = []
        for tickets in master.tickets.values():
            self.user_tickets += tickets   
        
        #Creating a frame to store a tree view table in to show users tickets
        #self.table_frame = Frame(self, bg="#6D3591")
        self.table_Frame = Frame(self, bg="#6D3591")
        #Configuring settings for treeview
        style = ttk.Style()
        style.configure("Treeview", font=(None, 14))
        style.configure("Treeview", rowheight=int(60))
        self.tree_columns = ["Id", "Title", "Problem", "Date Created", "Status", "Priority", "User"]
        self.tree_view = ttk.Treeview(self.table_Frame, columns=self.tree_columns, show="headings")
        self.__populate_tickets()
        
        self.tree_view.pack(expand=True, fill='both', padx=40)
        self.table_Frame.pack(ipadx=20, ipady=20, expand=True, fill="both")
        
        #Update area 
        self.update_area = Frame(self, bg="#6D3591")
        self.update_area.pack()
        #Button area 
        self.button_area = Frame(self, bg="#393939")
        delete_button = Button(self.button_area, text="DQ (Dequeue/Dairy Queen)", font="Calibri 18", 
                               command=lambda:self.__delete_ticket()).grid(
            ipadx=5,row=0, column=1, padx=20, pady=20)
        update_button = Button(self.button_area, text="Update", font="Calibri 18", 
                               command=lambda:self.__open_update()).grid(
            ipadx=5,row=0, column=2, padx=20, pady=20)
        sort_button = Button(self.button_area, text="Sort", font="Calibri 18", 
                               command=lambda:self.__sort_tickets()).grid(
            ipadx=5,row=0, column=3, padx=20, pady=20)
        self.button_area.pack(ipadx=20, ipady=20)
        
    def __populate_tickets(self):
        for col in self.tree_columns:
            self.tree_view.heading(col, text=col)
            self.tree_view.column(col, stretch=YES)
            
        #Populates the treeview with tickets information
        for ticket in self.user_tickets:
            ticket_info = (ticket.id, ticket.subject, ticket.problem, ticket.date_created,
                            ticket.status, ticket.priority, ticket.user_id)
            self.tree_view.insert("", END, values=ticket_info)
            
    def __delete_ticket(self):
        selected_item = self.tree_view.get_children()[0]
        user_id =self.tree_view.item(selected_item)["values"][-1]
        ticket_id = self.tree_view.item(selected_item)["values"][0]
        user_tickets = self.master.tickets[user_id]
        for ticket in user_tickets:
            if ticket_id == ticket.id:
                user_tickets.remove(ticket)
                self.user_tickets.remove(ticket)
                
        self.tree_view.delete(selected_item)
    
        
    def __open_update(self):
        font="Calibri 20"
        top = Toplevel(self, bg="#6D3591")
        top.geometry("660x800")
        #Grabs selected value
        selected = self.tree_view.item(self.tree_view.focus())["values"]
        widg_width=30
        header_lbl = Label(top, pady=20, text=f"Update Value For Ticket ID: {selected[0]}",
                           font="Calibri 25", bg="#6D3591", fg="white")
        header_lbl.grid(row=0, column=1)
        title_lbl = Label(top, text="Title: ", font=font, bg="#6D3591")
        title_lbl.grid(row=1, column=0,  padx=(20,0), pady=(20,0))
        title_text= StringVar(top)
        title_text.set(selected[1])
        title_entry = Entry(top, font=font, textvariable=title_text, width=widg_width)
        title_entry.grid(column=1, row=1, padx=(20,0), pady=(20,0))
        problem_lbl = Label(top, text="Problem: ", font=font, bg="#6D3591")
        problem_lbl.grid(row=2, column=0,  padx=(20,0), pady=(20,0), sticky="n")
        problem_text= selected[2]
        problem_entry = Text(top, font=font, wrap=WORD, height=10, width=widg_width)
        problem_entry.insert(END, problem_text)
        problem_entry.grid(column=1, row=2, padx=(20,0), pady=(20,0))
        status_lbl = Label(top, text="Status: ", font=font, bg="#6D3591")
        status_lbl.grid(row=3, column=0,  padx=(20,0), pady=(20,0))
        status_text= StringVar(top)
        status_text.set(selected[4])
        status_entry = Entry(top, font=font, textvariable=status_text, width=widg_width)
        status_entry.grid(column=1, row=3, padx=(20,0), pady=(20,0))
        priority_lbl = Label(top, text="Priority: ", font=font, bg="#6D3591")
        priority_lbl.grid(row=4, column=0,  padx=(20,0), pady=(20,0))
        priority_text= StringVar(top)
        priority_text.set(selected[5])
        priority_entry = Entry(top, font=font, textvariable=priority_text, width=widg_width)
        priority_entry.grid(column=1, row=4, padx=(20,0), pady=(20,0))
        
        #Button method to save the ticket
        def update_ticket():
            ticket = None
            for tick in self.user_tickets:
                if tick.id == selected[0]:
                    ticket = tick
                    break
                
            ticket.title = title_text.get()
            ticket.problem = problem_entry.get("1.0", END)
            ticket.status = status_text.get()
            ticket.priority = int(priority_text.get())
            self.__sort_tickets()
            top.destroy()
            
        submit= Button(top, font=font, text="Submit", command=lambda:update_ticket(), 
                       bg="black", fg="white")
        submit.grid(row=6, column=1, pady=20)
        
        
    def __update_treeview(self):
        selected_item = self.tree_view.selection()[0]
        ticket_id = self.tree_view.item(selected_item)["values"][0]
        the_ticket = None
        for ticket in self.user_tickets:
            if ticket.id ==ticket_id:
               the_ticket = ticket 
               break
           
    def __sort_tickets(self):
        for child in self.tree_view.get_children():
            self.tree_view.delete(child)
        
        #Insertion sort
        priority_q = Priority_Q_Tickets()
        for ticket in self.user_tickets:
            priority_q.enqueue(ticket)
            
        #Repopulate treeview
        for ticket in priority_q.items:
            ticket_info = (ticket.id, ticket.subject, ticket.problem, ticket.date_created,
                        ticket.status, ticket.priority, ticket.user_id)
            self.tree_view.insert("", END, values=ticket_info)
        
                      
class Add_Frame(Frame):
    def __init__(self, master):
        main_font = "Calibri 18"
        bg_color="#393939"
        fg_color="#ffffff"
        super().__init__(master, bg=bg_color)
        self.master = master
        #Getting current user info and tickets
        self.user_info = master.current_user
        self.user_tickets = master.tickets[self.user_info.id]
        #widgets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.heading = Label(
            self, fg=fg_color, text="Add Ticket", font="Calibri 25", bg=bg_color)
        
        self.heading.grid(columnspan=2, row=0, column=0, pady=40)
        self.title_lbl = Label(self, fg=fg_color, text="Title: ", font=main_font, bg=bg_color).grid(
            row=1, column=0, sticky="e") 
        self.title_input = Entry(self, font=main_font)
        self.title_input.grid(row=1, column=1, sticky="w")
        
        self.problem_lbl = Label(self, fg=fg_color, text="Issue: ",bg=bg_color, font=main_font) 
        self.problem_lbl.grid(row=2, column=0, sticky="ne", pady=20)
        self.problem_input = Text(self, font=main_font, height=8)
        self.problem_input.grid(row=2, column=1, sticky="w", pady=20, padx=(0,20))
        button_frame = Frame(self, bg="#393939")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.submit_btn = Button(button_frame, text="Submit", 
                command=lambda:self.add_ticket(self.title_input.get(), 
                                               self.problem_input.get("1.0", END)
        ), font=main_font)
        self.submit_btn.grid(row=0, column=0)
        self.cancel_btn = Button(button_frame, text="Cancel", 
                                 command=lambda:master.user_frame.tkraise(),font=main_font)
        self.cancel_btn.grid(row=0, column=1)
    
    def add_ticket(self, title, problem):
        ticket = Ticket(subject=title, problem=problem, user_id=self.user_info.id)
        self.user_tickets.append(ticket)
        self.master.user_frame.destroy()
        self.master.user_frame = User_Frame(self.master)
        self.master.user_frame.grid(row=0, column=0, sticky="nsew")
        
#========================================EndOfFrames==========================================

#Main Window hosts all Frames
class TicketManagementSystem(Tk):
    def __init__(self):
        super().__init__()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title("Ticket Management System")
        self.current_user = None
        
        #Seeding Users
        admin = User("admin", "password", "Logan", "Riedell")
        admin.is_admin = True
        reg_user = User("slayer232", "password", "Samantha", "Something")
        self.accepted_users={admin.username:admin, reg_user.username:reg_user}
        
        #Makeshift database with a dictionary
        self.tickets = {}
        
        #initializing frames
        self.login_frame = Login_Frame(self)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        
        self.user_frame = None
        self.login_frame.tkraise()
        
        

        
    
               