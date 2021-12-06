import unittest
from Final_Project.Models import Priority_Q_Tickets, PQueueEmptyException, PQueueFullException, Ticket

class PQ_Tests(unittest.TestCase):
        
    def test_enqueue(self):
        q = Priority_Q_Tickets()
        ticket1 = Ticket("blah,", "blah", 1)
        ticket1.priority = 4
        q.enqueue(ticket1)
        self.assertEqual(q.get_size(), 1)
    
    def test_dequeue(self):
        q = Priority_Q_Tickets()
        ticket2 = Ticket("blah,", "blah", 1)
        ticket3 = Ticket("blah,", "blah", 1)
        q.enqueue(ticket2)
        q.enqueue(ticket3)
        q.dequeue()
        self.assertEqual(q.get_size(), 1)
        q = Priority_Q_Tickets()
        with self.assertRaises(PQueueEmptyException):
            q.dequeue()
    
    def test_peek(self):
        q = Priority_Q_Tickets()
        ticket4 = Ticket("Ticket4", "blah", 1)
        ticket4.priority = 3
        ticket5 = Ticket("Ticket5", "blah", 1)
        ticket5.priority = 4
        q.enqueue(ticket4)
        q.enqueue(ticket5)
        print(q)
        #Highest priority should be on top
        self.assertEqual(ticket5, q.peek())
        q.dequeue()
        q.dequeue()
        with self.assertRaises(PQueueEmptyException):
            q.peek()
            
    def test_size(self):
        q = Priority_Q_Tickets()
        ticket6 = Ticket("blah,", "blah", 1)
        ticket7 = Ticket("blah,", "blah", 1)
        ticket8 = Ticket("blah,", "blah", 1)
        q.enqueue(ticket6)
        q.enqueue(ticket7)
        q.enqueue(ticket8)
        self.assertEqual(3, q.get_size())
        
    def test_empty(self):
        q = Priority_Q_Tickets()
        self.assertEqual(True, q.is_empty())
        
    def test_print(self):
        q = Priority_Q_Tickets()
        ticket9 = Ticket("Printers", "blah", 1)
        ticket9.priority = 3
        ticket10 = Ticket("Phone", "blah", 1)
        ticket10.priority = 2
        q.enqueue(ticket9)
        q.enqueue(ticket10)
        
        #should print in order of priority
        self.assertEqual("Subject:Printers, Priority: 3; Subject:Phone, Priority: 2;", str(q))
         
        
if __name__ == "__main__":
    unittest.main()
        