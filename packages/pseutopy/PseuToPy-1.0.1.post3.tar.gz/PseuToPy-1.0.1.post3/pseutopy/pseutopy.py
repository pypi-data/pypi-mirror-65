from textx.metamodel import metamodel_from_file
import ast
from classes.arithmetic import *
from classes.boolean import *
from classes.controls import *
from classes.functions import *
from classes.keywords import *
from classes.lists import *
from classes.statements import *
from classes.values import *


class PseuToPy:
    def __init__(self):
        self.py_ast = ast.Module(body=[])
        self.variables = []
        self.wrapper_node_classes = [WhileStatement, ForStatement, Module]
        self.pseudo_mm = metamodel_from_file('./grammar/pseudocode.tx',
                                             classes=[
                                                 # Values
                                                 Num,
                                                 Name,
                                                 Boolean,
                                                 Range,
                                                 # Arithmetic Expressions
                                                 AddSubExpression,
                                                 MultDivExpression,
                                                 PowExpression,
                                                 BaseValue,
                                                 ExponentValue,
                                                 # Boolean Expressions
                                                 Expression,
                                                 AndExpression,
                                                 ComparisonExpression,
                                                 BooleanTerm,
                                                 # -- Statements start here --
                                                 Module,
                                                 Statement,
                                                 # Assignment Statements
                                                 AssignmentStatement,
                                                 DeclarationStatement,
                                                 # Standard IO Statements
                                                 PrintStatement,
                                                 PromptStatement,
                                                 # Control Structures
                                                 IfStatement,
                                                 ElseStatement,
                                                 ElseIfStatement,
                                                 WhileStatement,
                                                 ForStatement,
                                                 # Function call and definition
                                                 FunctionDefinitionStatement,
                                                 FunctionCallStatement,
                                                 ReturnStatement,
                                                 # Keyword statements
                                                 BreakStatement,
                                                 ContinueStatement,
                                                 PassStatement,
                                                 # List statements
                                                 List,
                                                 ListGetElement,
                                                 ListAddElementStatement,
                                                 ListRemoveElementStatement,
                                                 ListRemoveAndGetElementStatement,
                                                 ListRemoveFirstElementStatement,
                                                 ListRemoveAndGetFirstElementStatement,
                                                 ListRemoveLastElementStatement,
                                                 ListRemoveAndGetLastElementStatement,
                                                 ListLengthStatement,
                                                 ListMinStatement,
                                                 ListMaxStatement,
                                                 ListSumStatement])
        self.pseudo_mm.register_obj_processors({
            'RootStatement': self.handle_root_statement,
        })

    def reset_ast(self):
        self.py_ast = ast.Module(body=[])
        self.variables = []

    def convert_from_file(self, filename):
        """This function reads and converts the contents of the input file into
        an AST
        """
        self.reset_ast()
        self.pseudo_mm.model_from_file(filename)
        return self.py_ast

    def convert_from_string(self, pseudo_str):
        """This function takes a string as input and builds the equivalent AST
        describing the input
        """
        self.reset_ast()
        self.pseudo_mm.model_from_str(pseudo_str)
        return self.py_ast

    def add_to_ast(self, node):
        self.py_ast.body.append(node)
        return node

    def handle_root_statement(self, root_statement):
        if type(root_statement) is FunctionCallStatement:
            self.add_to_ast(
                ast.Expr(value=self.statement_to_node(root_statement)))
        else:
            self.add_to_ast(self.statement_to_node(root_statement))

    def statement_to_node(self, statement):
        if type(statement) is PrintStatement:
            node = self.print_to_node(statement)
        elif type(statement) is PromptStatement:
            node = ast.Expr(value=self.to_node(statement))
        elif type(statement) is DeclarationStatement:
            node = self.declaration_to_node(statement)
        elif type(statement) is AssignmentStatement:
            node = self.assignment_to_node(statement)
        elif type(statement) is IfStatement:
            node = self.if_to_node(statement)
        elif type(statement) is WhileStatement:
            node = self.while_to_node(statement)
        elif type(statement) is FunctionDefinitionStatement:
            node = self.func_def_to_node(statement)
        elif type(statement) is FunctionCallStatement:
            node = self.func_call_to_node(statement)
        elif type(statement) is ForStatement:
            node = self.for_to_node(statement)
        elif type(statement) is BreakStatement:
            node = ast.Break()
        elif type(statement) is ContinueStatement:
            node = ast.Continue()
        elif type(statement) is PassStatement:
            node = ast.Pass()
        elif type(statement) is ReturnStatement:
            node = ast.Return(self.to_node(statement.value))
        elif type(statement) is ListAddElementStatement:
            node = self.list_add_element_statement_to_node(statement)
        elif type(statement) is ListRemoveElementStatement:
            node = self.list_remove_element_statement_to_node(statement)
        elif type(statement) is ListRemoveFirstElementStatement:
            node = self.list_remove_first_element_statement_to_node(statement)
        elif type(statement) is ListRemoveLastElementStatement:
            node = self.list_remove_last_element_statement_to_node(statement)
        elif type(statement) is ListRemoveAndGetElementStatement:
            node = ast.Expr(value=self.to_node(statement))
        elif type(statement) is ListRemoveAndGetFirstElementStatement:
            node = ast.Expr(value=self.to_node(statement))
        elif type(statement) is ListRemoveAndGetLastElementStatement:
            node = ast.Expr(value=self.to_node(statement))
        elif type(statement) is ListLengthStatement:
            node = ast.Expr(value=self.to_node(statement))
        elif type(statement) is ListMinStatement:
            node = ast.Expr(value=self.to_node(statement))
        elif type(statement) is ListMaxStatement:
            node = ast.Expr(value=self.to_node(statement))
        elif type(statement) is ListSumStatement:
            node = ast.Expr(value=self.to_node(statement))
        else:
            raise Exception("No matching statement for ", statement)
        return node

    def declaration_to_node(self, declaration_statement):
        var_id = declaration_statement.name.id

        if var_id not in self.variables:
            self.variables.append(var_id)
        else:
            raise Exception('You cannot declare the same variable twice')

        node = ast.Assign(
            targets=[ast.Name(id=var_id, ctx='Store')],
            value=ast.Constant(None))
        return node

    def print_to_node(self, print_statement):
        args = print_statement.args
        args_node = []
        for arg in args:
            args_node.append(self.to_node(arg))
        node = ast.Expr(value=ast.Call(func=ast.Name(
            id='print', ctx='Load'), args=args_node, keywords=[]))
        return node

    def assignment_to_node(self, assignment):
        target_id = assignment.target.id
        value = assignment.value

        # UNCOMMENT TO FORCE DECLARATION OF VARIABLES
        # if target_id not in self.variables:
        #     raise Exception(
        #         'You must declare variable ' + target_id + 'before assigning '
        #                                                    'it a value')

        node = ast.Assign(
            targets=[ast.Name(id=target_id, ctx='Store')],
            value=self.to_node(value))
        return node

    def if_to_node(self, if_statement):
        test_node = self.to_node(if_statement.test)
        body_node = list(
            map(lambda stmt: self.statement_to_node(stmt), if_statement.body))
        orelse_node = self.orelse_to_node(if_statement.orelse)
        node = ast.If(test=test_node, body=body_node, orelse=orelse_node)
        return node

    def orelse_to_node(self, orelse_list):
        if len(orelse_list) == 0:
            return orelse_list
        current_orelse = orelse_list.pop(0)
        if isinstance(current_orelse, ElseIfStatement):
            new_if = IfStatement(
                current_orelse.parent, current_orelse.test, current_orelse.body,
                orelse_list)
            node = [self.if_to_node(new_if)]
        elif isinstance(current_orelse, ElseStatement):
            node = list(
                map(lambda stmt: self.to_node(stmt), current_orelse.body))
        else:
            raise
        return node

    def while_to_node(self, while_statement):
        test_node = self.to_node(while_statement.test)
        body_node = list(
            map(lambda stmt: self.to_node(stmt), while_statement.body))
        orelse_node = self.orelse_to_node(while_statement.orelse)
        node = ast.While(test=test_node, body=body_node, orelse=orelse_node)
        return node

    def func_def_to_node(self, def_stmt):
        name_node = self.to_node(def_stmt.name)
        args_node = ast.arguments(
            args=list(map(lambda stmt: self.to_node(stmt), def_stmt.args)),
            defaults=[], vararg=None, kwarg=None)
        body_node = list(map(lambda stmt: self.to_node(stmt), def_stmt.body))
        node = ast.FunctionDef(name=name_node.id, args=args_node,
                               body=body_node,
                               decorator_list=[], returns=None,
                               type_comment=None)
        return node

    def func_call_to_node(self, call):
        name_node = self.to_node(call.name)
        args_node = list(map(lambda stmt: self.to_node(stmt), call.args))
        node = ast.Call(func=name_node, args=args_node, keywords=[])
        if type(call.parent) in self.wrapper_node_classes:
            node = ast.Expr(value=node)
        return node

    def list_to_node(self, l):
        elements_node = list(map(lambda e: self.to_node(e), l.elements))
        return ast.List(ctx="Load", elts=elements_node)

    def list_get_element_method_to_node(self, get_expr: ListGetElement):
        return ast.Subscript(
            self.to_node(get_expr.list_expr),
            ast.Index(self.to_node(get_expr.index)),
            ast.Load()
        )

    def list_remove_and_get_to_node(self, remove_and_get_expr, args):
        return ast.Call(
            func=ast.Attribute(
                self.to_node(remove_and_get_expr.list_expr),
                "pop",
                ast.Load()
            ),
            args=args,
            keywords=[]
        )

    def list_add_element_statement_to_node(self,
                                           list_add_stmt: ListAddElementStatement):
        if (list_add_stmt.index == None):
            method = "append"
            args = [self.to_node(list_add_stmt.element)]
        else:
            method = "insert"
            args = [
                self.to_node(list_add_stmt.index),
                self.to_node(list_add_stmt.element)
            ]
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    self.to_node(list_add_stmt.list_expr),
                    method,
                    ast.Load()
                ),
                args=args,
                keywords=[]
            )
        )

    def list_remove_element_statement_to_node(self,
                                              list_remove_stmt: ListRemoveElementStatement):
        return ast.Expr(
            value=ast.Delete(
                [
                    ast.Subscript(
                        ctx=ast.Del(),
                        slice=ast.Index(self.to_node(list_remove_stmt.index)),
                        value=self.to_node(list_remove_stmt.list_expr)
                    )
                ]
            )
        )

    def list_remove_first_element_statement_to_node(self,
                                                    list_remove_first_elt_stmt: ListRemoveFirstElementStatement):
        listRmStmt = ListRemoveElementStatement(
            parent=list_remove_first_elt_stmt.parent, list_expr=list_remove_first_elt_stmt.list_expr,
            index=Num(parent=list_remove_first_elt_stmt, n=0))
        return self.list_remove_element_statement_to_node(listRmStmt)

    def list_remove_last_element_statement_to_node(self,
                                                   list_remove_last_elt_stmt: ListRemoveLastElementStatement):
        listRmStmt = ListRemoveElementStatement(
            parent=list_remove_last_elt_stmt.parent, list_expr=list_remove_last_elt_stmt.list_expr,
            index=Num(parent=list_remove_last_elt_stmt, n=-1))
        return self.list_remove_element_statement_to_node(listRmStmt)

    def for_to_node(self, for_statement):
        target_node = self.to_node(for_statement.target)
        iterations_node = self.to_node(for_statement.iterations)
        body_node = list(
            map(lambda stmt: self.to_node(stmt), for_statement.body))
        orelse_node = self.orelse_to_node(for_statement.orelse)
        node = ast.For(target=target_node, iter=iterations_node,
                       body=body_node, orelse=orelse_node)
        return node

    def to_node(self, value):
        if isinstance(value, Num):
            node = ast.Num(n=value.n)
        elif isinstance(value, Expression):
            node = self.create_expression_node(value)
        elif isinstance(value, AndExpression):
            node = self.create_and_expression_node(value)
        elif isinstance(value, BooleanTerm):
            node = self.create_boolean_term_node(value)
        elif isinstance(value, ComparisonExpression):
            node = self.create_comparison_expression_node(value)
        elif isinstance(value, AddSubExpression):
            node = self.create_add_sub_expression_node(value)
        elif isinstance(value, MultDivExpression):
            node = self.create_mult_div_expression_node(value)
        elif isinstance(value, PowExpression):
            node = self.create_pow_expression_node(value)
        elif isinstance(value, BaseValue):
            node = self.create_base_value_node(value)
        elif isinstance(value, ExponentValue):
            node = self.create_exponent_value_node(value)
        elif isinstance(value, Statement):
            node = self.statement_to_node(value)
        elif isinstance(value, Name):
            node = ast.Name(id=value.id, ctx='Load')
        elif isinstance(value, Boolean):
            node = ast.NameConstant(value=value.boolean_value == 'true')

        elif isinstance(value, PromptStatement):
            node = ast.Call(func=ast.Name(
                id='input', ctx='Load'), args=[self.to_node(value.text)],
                keywords=[])

            if (value.cast_type != None):

                if (value.cast_type == 'number'):
                    cast_func_name = 'float'
                elif (value.cast_type == 'integer'):
                    cast_func_name = 'int'

                node = ast.Call(func=ast.Name(
                    id=cast_func_name, ctx='Load'), args=[node],
                    keywords=[])

        elif isinstance(value, List):
            node = self.list_to_node(value)

        elif isinstance(value, ListGetElement):
            node = self.list_get_element_method_to_node(value)

        elif isinstance(value, ListRemoveAndGetElementStatement):
            node = self.list_remove_and_get_to_node(
                value, [self.to_node(value.index)])

        elif isinstance(value, ListRemoveAndGetFirstElementStatement):
            node = self.list_remove_and_get_to_node(
                value, [ast.Constant(0)])

        elif isinstance(value, ListRemoveAndGetLastElementStatement):
            node = self.list_remove_and_get_to_node(
                value, [])

        elif isinstance(value, ListLengthStatement):
            node = ast.Call(func=ast.Name(
                id='len', ctx='Load'), args=[self.to_node(value.list_expr)],
                keywords=[])

        elif isinstance(value, ListMinStatement):
            node = ast.Call(func=ast.Name(
                id='min', ctx='Load'), args=[self.to_node(value.list_expr)],
                keywords=[])

        elif isinstance(value, ListMaxStatement):
            node = ast.Call(func=ast.Name(
                id='max', ctx='Load'), args=[self.to_node(value.list_expr)],
                keywords=[])

        elif isinstance(value, ListSumStatement):
            node = ast.Call(func=ast.Name(
                id='sum', ctx='Load'), args=[self.to_node(value.list_expr)],
                keywords=[])

        elif isinstance(value, Range):
            range_args = [self.to_node(value.start), self.to_node(value.stop)]
            if value.step:
                range_args.append(self.to_node(value.step))
            node = ast.Call(func=ast.Name(
                id='range', ctx='Load'), args=range_args, keywords=[])
        else:
            node = ast.Str(s=value.s)

        return node

    def create_expression_node(self, expression):
        if len(expression.logical_terms) == 1:
            return self.to_node(expression.logical_terms[0])
        logical_terms_nodes = []
        for t in expression.logical_terms:
            logical_terms_nodes.append(self.to_node(t))
        return ast.BoolOp(ast.Or(), logical_terms_nodes)

    def create_and_expression_node(self, logical_term):
        if len(logical_term.logical_factors) == 1:
            return self.to_node(logical_term.logical_factors[0])
        logical_factors_nodes = []
        for f in logical_term.logical_factors:
            logical_factors_nodes.append(self.to_node(f))
        return ast.BoolOp(ast.And(), logical_factors_nodes)

    def create_boolean_term_node(self, logical_factor):
        if logical_factor.sign in ['!', 'not']:
            return ast.UnaryOp(ast.Not(), self.to_node(logical_factor.operand))
        elif logical_factor.sign is None:
            return self.to_node(logical_factor.operand)
        else:
            raise

    def create_comparison_expression_node(self, boolean_entity):
        left_node = self.to_node(boolean_entity.left)
        if boolean_entity.operator is None:
            return left_node
        elif boolean_entity.operator in ['==', 'is equal to']:
            python_cmp_op = ast.Eq()
        elif boolean_entity.operator in ['!=', 'is not equal to',
                                         'is different from']:
            python_cmp_op = ast.NotEq()
        elif boolean_entity.operator in ['>', 'is greater than']:
            python_cmp_op = ast.Gt()
        elif boolean_entity.operator in ['>=', 'is greater or equal to']:
            python_cmp_op = ast.GtE()
        elif boolean_entity.operator in ['<', 'is lower than']:
            python_cmp_op = ast.Lt()
        elif boolean_entity.operator in ['<=', 'is lower or equal to']:
            python_cmp_op = ast.LtE()
        else:
            raise

        right_node = self.to_node(boolean_entity.right)
        return ast.Compare(left_node, (python_cmp_op,), (right_node,))

    def create_add_sub_expression_node(self, arith_expr):
        last_term_index = len(arith_expr.terms)
        node = self.to_node(arith_expr.terms[0])
        if last_term_index == 0:
            return node
        for i in range(1, last_term_index):
            if arith_expr.operators[i - 1] in ['+', 'plus']:
                node = ast.BinOp(
                    node, ast.Add(), self.to_node(arith_expr.terms[i]))
            elif arith_expr.operators[i - 1] in ['-', 'minus']:
                node = ast.BinOp(
                    node, ast.Sub(), self.to_node(arith_expr.terms[i]))
        return node

    def create_mult_div_expression_node(self, term):
        last_factor_index = len(term.factors)
        node = self.to_node(term.factors[0])
        if last_factor_index == 0:
            return node
        for i in range(1, last_factor_index):
            if term.operators[i - 1] in ["*", "times"]:
                node = ast.BinOp(node, ast.Mult(),
                                 self.to_node(term.factors[i]))
            elif term.operators[i - 1] in ["/", "divided by"]:
                node = ast.BinOp(
                    node, ast.Div(), self.to_node(term.factors[i]))
            elif term.operators[i - 1] in ["%", "modulo"]:
                node = ast.BinOp(
                    node, ast.Mod(), self.to_node(term.factors[i]))
            else:
                raise
        return node

    def create_pow_expression_node(self, factor):
        base_node = self.to_node(factor.base)
        # When no parenthesis, exponentiations are read from right to left
        if len(factor.exponents) != 0:
            last_exponent_index = len(factor.exponents) - 1
            right_node = self.to_node(factor.exponents[last_exponent_index])
            for i in range(last_exponent_index - 1, -1, -1):
                right_node = ast.BinOp(self.to_node(
                    factor.exponents[i]), ast.Pow(), right_node)
            base_node = ast.BinOp(base_node, ast.Pow(), right_node)

        if factor.sign in ['-', 'minus']:
            return ast.UnaryOp(ast.USub(), base_node)
        elif factor.sign in ['+', 'plus']:
            return ast.UnaryOp(ast.UAdd(), base_node)
        elif factor.sign is None:
            return base_node
        else:
            raise

    def create_base_value_node(self, base):
        return self.to_node(base.operand)

    def create_exponent_value_node(self, exponent):
        node = self.to_node(exponent.operand)
        if exponent.sign in ['-', 'minus']:
            return ast.UnaryOp(ast.USub(), node)
        elif exponent.sign in ['+', 'plus']:
            return ast.UnaryOp(ast.UAdd(), node)
        elif exponent.sign is None:
            return node
        else:
            raise
