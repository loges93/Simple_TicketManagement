from unittest import main
from Final_Project.Models import Ticket
from Views import TicketManagementSystem, Login_Frame, User_Frame, Admin_Frame, Add_Frame
import random 

main_program = TicketManagementSystem()
#Seed premade tickets into program
ticket1 = Ticket(subject="Mouse Not Working", problem="Refer to Subject", user_id=1)
ticket2 = Ticket(subject="Keyboard Not Working", problem="Refer to Subject", user_id=1)
ticket3 = Ticket(subject="Phone Not Working", problem="Refer to Subject", user_id=4)
ticket4 = Ticket(subject="Toilet Not Working", problem="Refer to Subject", user_id=1)
ticket5 = Ticket(subject="Program Not Working", problem="Refer to Subject", user_id=6)
ticket6 = Ticket(subject="Life Not Working", problem="Refer to Subject", user_id=2)
tickets = [ticket1, ticket2, ticket3, ticket4, ticket5, ticket6]
#Assigns random priority and adds them to main program tickets 
for ticket in tickets:
    ticket.priority = random.randint(1, 4)
    if ticket.user_id in main_program.tickets.keys():
        main_program.tickets[ticket.user_id].append(ticket)
    else:
        main_program.tickets[ticket.user_id] = [ticket]

main_program.mainloop()

