from datetime import datetime

class User():
    id = 1
    def __init__(self, username, password, first=None, last=None):
        self.id = User.id
        self.username = username
        self.password = password
        self.first_name = first
        self.last_name = last
        self.is_admin = False
        User.id += 1
        
class Ticket():
    id = 1
    def __init__(self, subject, problem, user_id):
        self.user_id = user_id
        self.subject = subject
        self.date_created = datetime.now().strftime("%m-%d-%Y - %I:%M %p")
        self.problem = problem
        self.status = "Pending"
        self.priority = 1
        self.id = Ticket.id
        Ticket.id += 1
        

class Priority_Q_Tickets():
    def __init__(self):
        self.items = []
        
    def is_empty(self):
           return len(self.items) == 0
    # def is_full(self): No need no max size 

    def enqueue(self, item):
        found_lower = False
        #iterates through items to find the item that has less priority and inserts it 
        #before it
        if not self.is_empty():
            for i in range(len(self.items)):
                if item.priority > self.items[i].priority:
                    print(item.priority, self.items[i].priority)
                    self.items.insert(i, item)
                    found_lower = True
                    break
        
        #Appends to end of queue if no priority was greater in existing items       
        if(not found_lower):
            self.items.append(item)
        
    def dequeue(self):
        if not self.is_empty():
            item = self.items.pop(0)
        else:
            raise PQueueEmptyException

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            raise PQueueEmptyException

    def get_size(self):
        return len(self.items)

    def __str__(self):
        pq_string = ""
        for ticket in self.items:
             pq_string += f" Subject:{ticket.subject}, Priority: {ticket.priority};"
        
        return pq_string.strip()

class PQueueEmptyException(Exception):
    pass

class PQueueFullException(Exception):
    pass
        
        