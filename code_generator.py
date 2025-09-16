# code_generator.py

from ast_nodes import *
from semantic_analyzer import AnalisadorSemantico, TIPO_NUMERO, TIPO_STRING, TIPO_ARRAY_NUMERO, TIPO_BOOL, ProgramNode

class CodeGenerator:
    def __init__(self, tabela_de_simbolos):
        self._indentation_level = 0
        self.tabela_de_simbolos = tabela_de_simbolos

    def _map_type_to_c(self, tipo):
        if tipo == TIPO_NUMERO: return "double"
        if tipo == TIPO_BOOL: return "bool"
        return "void"

    def _indent(self):
        return "    " * self._indentation_level

    def generate(self, ast_root):
        self._indentation_level = 1
        body_code_string = self.visit(ast_root)
        
        headers = ["#include <stdio.h>", "#include <stdbool.h>\n", "int main() {"]
        final_code = list(headers)
        
        declarations = []
        for nome, info in sorted(self.tabela_de_simbolos.simbolos.items()):
            if info['tipo'] == TIPO_ARRAY_NUMERO: continue
            tipo_c = self._map_type_to_c(info['tipo'])
            declarations.append(f"    {tipo_c} {nome};")

        if declarations:
            final_code.extend(declarations)
            final_code.append("")
        
        final_code.append(body_code_string)
        
        final_code.append(f"\n    return 0;")
        final_code.append("}")
        return "\n".join(final_code)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Nenhum método visit_{type(node).__name__} encontrado')

    def visit_ProgramNode(self, node):
        lines = []
        for statement in node.statements:
            result = self.visit(statement)
            if result:
                lines.append(result)
        return "\n".join(lines)

    def visit_AssignmentNode(self, node):
        var_name = node.variable.name
        info_var = self.tabela_de_simbolos.consultar(var_name)
        if info_var['tipo'] == TIPO_ARRAY_NUMERO:
            elements_code = self.visit(node.expression)
            tipo_c = self._map_type_to_c(TIPO_NUMERO)
            return f"{self._indent()}{tipo_c} {var_name}[] = {elements_code};"
        expr_code = self.visit(node.expression)
        return f"{self._indent()}{var_name} = {expr_code};"

    def visit_IfNode(self, node):
        cond_code = self.visit(node.condition)
        if_code = f"{self._indent()}if ({cond_code}) {{\n"
        self._indentation_level += 1
        if_code += self.visit(node.if_block)
        self._indentation_level -= 1
        if_code += f"\n{self._indent()}}}"
        if node.else_block:
            if_code += " else {\n"
            self._indentation_level += 1
            if_code += self.visit(node.else_block)
            self._indentation_level -= 1
            if_code += f"\n{self._indent()}}}"
        return if_code

    def visit_ForNode(self, node):
        iterator = node.iterator_var.name
        iterable = node.iterable_var.name
        code = f"{self._indent()}int size_{iterable} = sizeof({iterable}) / sizeof({iterable}[0]);\n"
        code += f"{self._indent()}for (int i = 0; i < size_{iterable}; i++) {{\n"
        self._indentation_level += 1
        code += f"{self._indent()}{iterator} = {iterable}[i];\n"
        code += self.visit(node.body)
        self._indentation_level -= 1
        code += f"\n{self._indent()}}}"
        return code

    def visit_PrintNode(self, node):
        format_parts = []
        args_parts = []
        
        temp_analyzer = AnalisadorSemantico(ProgramNode([]))
        temp_analyzer.tabela_de_simbolos = self.tabela_de_simbolos
        
        for arg_node in node.args:
            arg_type = temp_analyzer.visit(arg_node)
            arg_code = self.visit(arg_node)

            if arg_type == TIPO_STRING:
                format_parts.append("%s")
                args_parts.append(arg_code)
            elif arg_type == TIPO_NUMERO:
                format_parts.append("%f")
                args_parts.append(arg_code)
            elif arg_type == TIPO_BOOL:
                format_parts.append("%d")
                args_parts.append(arg_code)

        format_string = f'"{" ".join(format_parts)}\\n"'
        final_args = [format_string] + args_parts
        return f'{self._indent()}printf({", ".join(final_args)});'
    
    def visit_BinOpNode(self, node):
        left_code = self.visit(node.left)
        right_code = self.visit(node.right)
        return f"({left_code} {node.op} {right_code})"
    
    def visit_VariableNode(self, node): return node.name
    def visit_NumberNode(self, node): return node.value
    def visit_StringNode(self, node): return node.value

    def visit_ListNode(self, node):
        elementos = [self.visit(el) for el in node.elements]
        return f"{{{', '.join(elementos)}}}"