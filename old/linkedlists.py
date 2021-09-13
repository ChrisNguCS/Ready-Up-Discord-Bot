class node:
    def __init__(self,data = None):
        self.data = data
        self.next = None

class linked_list:
    def __init__(self):
        self.head = node()

    # def append(self, data):
    #     new_node = node(data)
    #     cur = self.head
    #     while cur.next!=None:
    #         cur =cur.next
    #     cur.next = new_node
    
    def append(self, newElement):
        newNode = node(newElement)
        if(self.head == None):
         self.head = newNode
         return
        else:
            temp = self.head
        while(temp.next != None):
         temp = temp.next
        temp.next = newNode

    def length(self):
        cur = self.head
        total = 0
        while cur.next !=None:
            total+=1
            cur = cur.next
        return total
    
    def display(self):
        temp = self.head
        while (temp != None):
            print(temp.data, end=" ")
            temp = temp.next
            print()
        else:
            print("The list is empty.")
        # elems = []
        # cur_node = self.head
        # while cur_node.next!=None:
        #     cur_node = cur_node.next
        #     elems.append(cur_node.data)
        # print(elems)

    def get(self, index):
        if index >=self.length():
            return None
        cur_idx = 0
        cur_node=self.head
        while True:
            cur_node = cur_node.next
            if cur_idx==index:
                return cur_node.data
            cur_idx+= 1

    def deleteList(self):
        current = self.head
        while current:
            prev = current.next
            del current.data
            current = prev
    
    def delNodes(self):
        while(self.head != None):
            temp = self.head
            self.head = self.head.next
            temp = None

# list = linked_list()
# list.append(1)
# list.append(2)
# list.display()
# list.delNodes()
# list.append(1)
# list.display()
# list.length()


