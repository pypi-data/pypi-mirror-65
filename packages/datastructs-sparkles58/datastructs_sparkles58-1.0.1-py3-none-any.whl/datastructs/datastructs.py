#Queues!
class queue:
    #Input: either nothing or an iterable to start with
    #Action: initializes the Queue object
    #Output: none
    def __init__(self, list_in=[]):
        self.list = list(list_in) #set to either an input list or an empty queue

    #Input: nothing
    #Action: gives it the string representation of the object for when you print a Queue object
    #Output: the aformentioned string representation
    def __str__(self):
        return "Queue(" + ", ".join(map(str, self.list)) + ")"  #when you print a Queue object, print "Queue(*items*)"; the map() function runs the function on every item in the list

    #Input: nothing
    #Action: gives the object representation of the Queue
    #Output: the aforementioned object represenation
    def __repr__(self):     #object representation of object
        return self.list    #return the list

    #Input: value to enqueue
    #Action: adds that to the queue
    #Output: nothing
    def enqueue(self, value):
        self.list.insert(0, value)  #add the value to beginning of the list

    #Input: nothing
    #Action: removes the last element
    #Output: that last element
    def dequeue(self):
        if self.list != []: #if there is an item
            return self.list.pop()  #remove last item and return it
        else:
            raise IndexError("The queue is empty.")


#nodes for tree
class node:
    #Input: parent node (or nothing for a base node), tree to put into, and value of the node
    #Action: initialize the node
    #Output: None
    def __init__(self, tree, value, parent=None):
        self.tree = tree #initialize tree
        self.parent = parent    #initialize prent
        self.children = []  #initialize children

    #Input: nothing
    #Action: gives it the string representation of the object for when you print a node object
    #Output: the aformentioned string representation
    def __str__(self):
        return "node(Tree=" + str(self.tree) + ", Value=" + str(self.value) + ")"

    #Input: nothing
    #Action: gives the object representation of the node
    #Output: the aforementioned object represenation
    def ___repr__(self):
        return {"Tree":str(self.tree), "Value":str(self.value)}

    #Input: value to change node to
    #Action: changes value and passes that change to every child
    #Output: nothing
    def set(self, value):
        self.value = value #change value
        if children != []:  #if it has children
            for child in children:  #for every child
                child.set_parent(self)  #set the child's parent to this
        try:
                self.tree.heapify() #try to heapify if it's in a heap
        except: #just a normal tree:
                self.tree.update()  #update tree

    #Input: parent node to change to
    #Action: changes parent node and recusively fixes tree
    #Output: nothing
    def set_parent(self, node):
        self.parent = node  #set parent
        if children != []:  #if it has children
            for child in children:  #for every child
                child.set_parent(self)  #set the child's parent to this
        try:
                self.tree.heapify() #try to heapify if it's in a heap
        except: #just a normal tree:
                self.tree.update()  #update tree

    #Input: same for __init__ function (see above) but no parent or tree
    #Action: creates child
    #Output: nothing
    def add_child(self, value):
        children.append(node(self.tree, value, self))   #add a child node
        try:
                self.tree.heapify() #try to heapify if it's in a heap
        except: #just a normal tree:
                self.tree.update()  #update tree

    #Input: child to remove
    #Action: remove child
    #Output: nothing
    def remove_child(child):
        if isinstance(child, node) and child in children:   #if it truly is a node and a child of this node
            children.remove(child)  #remove child
            try:
                self.tree.heapify() #try to heapify if it's in a heap
            except: #just a normal tree:
                self.tree.update()  #update tree
        elif not isinstance(child, node):   #not a node
            raise TypeError("Not a node")
        else:   #it's not a child of this node
            raise ValueError("Not a child of this node")


#Trees!
class tree:
    #Input: value for base node (defaults to none)
    #Action: initializes tree
    #Output: none
    def __init__(self, base=None):
        self.base = node(self, base)    #initialize base node
        self.nodes = [[base]]   #list of nodes. the index in the list is their layer in the tree, with the highest being the leaves, and 0 being the base node

    #Input: optional new base node
    #Action: updates the tree
    #Output: nothing
    def update(self, base=self.base):
        self.base = base #set base
        self.nodes = [[self.base]]   #start new nodes list
        next_node = self.base   #set next node to base
        #get depth:
        depth = 0
        while next_node.children != []: #while you still have to explore more depth
            depth += 1 #add depth
            next_node = next_node.children[0]   #pick first child to always guarantee that you will get a node
        #create node list:
        for i in range(depth):
            self.nodes.append([])   #add empty 
            for node in self.nodes[depth]:  #for every node in the previous layer
                if node.children != []: #if it has children
                    self.nodes[-1] += node.children #add the nodes children to the latest layer
        
        
