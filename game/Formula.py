# full structure for logical formulas
# is inductive in nature
class Formula:
    # op_type = 'binary' or 'unary' or None
    # formula args can be either of type Atom or Formula
    def __init__(self, form_left, form_right=None, op_type=None, op=None):
        self.op_type = op_type
        if op_type == None:
            self.form = form_left
        elif op_type == 'unary':
            self.op = op
            self.form = form_left
        elif op_type == 'binary':
            self.op = op
            self.form_left = form_left
            self.form_right = form_right
        else: raise Error("Formula instance incorrect")
    
    def __str__(self):
        if self.op_type == None:
            return f"{self.form}"
        elif self.op_type == 'unary':
            return f"{self.op} {self.form}"
        return f"{self.form_left} {self.op} {self.form_right}"