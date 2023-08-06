class Node:
    def __init__(self, val):
        self.val = val;
        self.left_child = None
        self.right_child = None

class Tree:
    def __init__(self):
        self.root = None
        self.stack = []

    def add(self, val):
        if self.root == None:
            self.root = Node(val)
            return 0
        else:
            return self.__add(self.root, val)

    def __add(self, cur_node, val):
        if val < cur_node.val:
            if cur_node.left_child == None:
                cur_node.left_child = Node(val)
                return 1
            else:
                return self.__add(cur_node.left_child, val)
        if val > cur_node.val:
            if cur_node.right_child == None:
                cur_node.right_child = Node(val)
                return 2
            else:
                return self.__add(cur_node.right_child, val)
        else:
            return -1

    def pre_order(self):
        if self.root != None:
            self.stack = []
            self.cur_ord = 'pre_order'
            self.cur_ord = None
            self.__pre_order(self.root)
            return 1
        return 0

    def __pre_order(self, cur_node):
        self.stack.append(cur_node)
        if cur_node.left_child != None:
            self.__pre_order(cur_node.left_child)
        if cur_node.right_child != None:
            self.__pre_order(cur_node.right_child)

    def in_order(self):
        if self.root != None:
            self.stack = []
            self.cur_ord = 'in_order'
            self.__in_order(self.root)
            return 1
        return 0

    def __in_order(self, cur_node):
        if cur_node.left_child != None:
            self.__in_order(cur_node.left_child)
        self.stack.append(cur_node)
        if cur_node.right_child != None:
            self.__in_order(cur_node.right_child)


    def post_order(self):
        if self.root != None:
            self.stack = []
            self.cur_ord = 'post_order'
            self.__post_order(self.root)
            return 1
        return 0

    def __post_order(self, cur_node):
        if cur_node.left_child != None:
            self.__post_order(cur_node.left_child)
        if cur_node.right_child != None:
            self.__post_order(cur_node.right_child)
        self.stack.append(cur_node)

    def show(self, order = 'pre_order'):
        if order == 'pre_order':
            self.pre_order()
        elif order == 'in_order':
            self.in_order()
        elif order == 'post_order':
            self.post_order()
        else:
            raise ValueError('Invalid order %s. valid options are {\"pre_order\", \"in_order\", \"post_order\"}'%(order))

        for node in self.stack:
            print(node.val, end = ' ')
        print()