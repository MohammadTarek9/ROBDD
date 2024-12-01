
from graphviz import Digraph

# Node class for ROBDD nodes
class ROBDDNode:
    def __init__(self, var=None, low=None, high=None):
        self.var = var        # Variable name (None for terminals)
        self.low = low        # Low child (0 edge)
        self.high = high      # High child (1 edge)

    def is_terminal(self):
        return self.var is None

    def __hash__(self):
        return hash((self.var, self.low, self.high))

    def __eq__(self, other):
        return (self.var, self.low, self.high) == (other.var, other.low, other.high)

def build_robdd(expr, ordering):
    unique_table = {}
    apply_cache = {}

    # Predefine terminal nodes
    terminal_0 = ROBDDNode(var=None, low=None, high=0)
    terminal_1 = ROBDDNode(var=None, low=None, high=1)
    unique_table[terminal_0] = terminal_0
    unique_table[terminal_1] = terminal_1

    def mk(var, low, high):
        if var is None:
            # Terminal node
            if high == 0:
                return terminal_0
            elif high == 1:
                return terminal_1
            else:
                raise Exception('Invalid terminal node value')
        if low == high:
            return low
        node = ROBDDNode(var=var, low=low, high=high)
        if node in unique_table:
            return unique_table[node]
        else:
            unique_table[node] = node
            return node

    def apply_op(op, u1, u2=None):
        key = (op, u1, u2)
        if key in apply_cache:
            return apply_cache[key]

        # Handle unary operation (NOT)
        if op == 'NOT':
            if u1.is_terminal():
                val = apply_operator(op, u1.high)
                result = mk(None, None, val)
            else:
                low = apply_op(op, u1.low)
                high = apply_op(op, u1.high)
                result = mk(u1.var, low, high)

        # Handle binary operations (AND, OR, XOR, etc.)
        else:
            if u1.is_terminal() and u2.is_terminal():
                val = apply_operator(op, u1.high, u2.high)
                result = mk(None, None, val)
            elif u1.is_terminal():
                low = apply_op(op, u1, u2.low)
                high = apply_op(op, u1, u2.high)
                result = mk(u2.var, low, high)
            elif u2.is_terminal():
                low = apply_op(op, u1.low, u2)
                high = apply_op(op, u1.high, u2)
                result = mk(u1.var, low, high)
            elif ordering.index(u1.var) == ordering.index(u2.var):
                low = apply_op(op, u1.low, u2.low)
                high = apply_op(op, u1.high, u2.high)
                result = mk(u1.var, low, high)
            elif ordering.index(u1.var) < ordering.index(u2.var):
                low = apply_op(op, u1.low, u2)
                high = apply_op(op, u1.high, u2)
                result = mk(u1.var, low, high)
            else:
                low = apply_op(op, u1, u2.low)
                high = apply_op(op, u1, u2.high)
                result = mk(u2.var, low, high)

        apply_cache[key] = result
        return result

    def build(node_expr, env):
        if isinstance(node_expr, str):
            if node_expr == '1':
                return terminal_1
            elif node_expr == '0':
                return terminal_0
            else:
                var = node_expr
                index = ordering.index(var)
                low = terminal_0
                high = terminal_1
                return mk(node_expr, low, high)
        elif isinstance(node_expr, tuple):
            op = node_expr[0]
            if op == 'NOT':
                operand = build(node_expr[1], env)
                return apply_op('NOT', operand)
            else:
                left = build(node_expr[1], env)
                right = build(node_expr[2], env)
                return apply_op(op, left, right)
        else:
            raise Exception('Invalid expression node')

    return build(expr, {})

def apply_operator(op, val1, val2=None):
    if op == 'NOT':
        return int(not val1)
    elif op == 'AND':
        return val1 & val2
    elif op == 'OR':
        return val1 | val2
    elif op == 'XOR':
        return val1 ^ val2
    elif op == 'NAND':
        return int(not (val1 & val2))
    elif op == 'NOR':
        return int(not (val1 | val2))
    else:
        raise Exception('Unknown operator')

def parse_boolean_function(tokens):
    stack = []
    for token in tokens:
        if token in {'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR'}:
            if token == 'NOT':
                operand = stack.pop()
                node = ('NOT', operand)
            else:
                right = stack.pop()
                left = stack.pop()
                node = (token, left, right)
            stack.append(node)
        else:
            stack.append(token)
    if len(stack) != 1:
        raise Exception('Invalid expression')
    return stack[0]

def visualize_robdd(robdd, filename='robdd'):
    dot = Digraph()
    visited = set()

    def add_node(node):
        if node in visited:
            return
        visited.add(node)
        node_id = str(id(node))

        if node.is_terminal():
            label = f"{node.high}"
            dot.node(node_id, label=label, shape='box')
        else:
            dot.node(node_id, label=node.var)
            add_node(node.low)
            add_node(node.high)
            dot.edge(node_id, str(id(node.low)), label='0')
            dot.edge(node_id, str(id(node.high)), label='1')

    add_node(robdd)
    dot.render(filename, view=True)

def main():
    print("Enter the variable ordering (e.g., A B C):")
    ordering_input = input().strip()
    ordering = ordering_input.split()

    print("Enter the first Boolean function in RPN (e.g., A B AND):")
    func1_input = input().strip()
    tokens1 = func1_input.split()
    expr1 = parse_boolean_function(tokens1)

    print("Enter the second Boolean function in RPN (e.g., A B OR):")
    func2_input = input().strip()
    tokens2 = func2_input.split()
    expr2 = parse_boolean_function(tokens2)

    # Build ROBDDs
    robdd1 = build_robdd(expr1, ordering)
    robdd2 = build_robdd(expr2, ordering)

    #
    # # Compare ROBDDs
    equivalent = robdd1 == robdd2
    if equivalent:
        print("The two Boolean functions are equivalent.")
    else:
        print("The two Boolean functions are NOT equivalent.")

    # Visualize ROBDDs
    visualize_robdd(robdd1, filename='robdd1')
    visualize_robdd(robdd2, filename='robdd2')

if __name__ == "__main__":
    main()