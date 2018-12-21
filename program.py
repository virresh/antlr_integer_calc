import antlr4
from antlr4.InputStream import InputStream
from python_files.ExprLexer import ExprLexer
from python_files.ExprParser import ExprParser
from python_files.ExprVisitor import ExprVisitor
import sys

class MyCalculator(ExprVisitor):

    def visitProg(self, node):
        results = []
        for child in node.getChildren():
            res = child.accept(self)
            if res != '\n':
                results.append(res)
        return results

    def visitExpr(self, node):
        childs = list(node.getChildren())
        if node.getChildCount()==1:
            return self.visitChildren(node)
        elif node.getChildCount() >=3 and node.getChild(0).getText() == '(':
            return childs[1].accept(self)
        else:
            left = int(childs[0].accept(self))
            operator = childs[1].accept(self)
            right = int(childs[2].accept(self))

        answer = None

        # Add your logic for calculation here
        answer = left + right

        return answer

    def visitTerminal(self, node):
        return node.getText()

def handleExpression(tree):
    visitor = MyCalculator()
    results = visitor.visit(tree)
    print(*results)

if __name__ == '__main__':
    # Get input from STDIN
    input_stream = InputStream(sys.stdin.readline())

    # Attach this input to a lexer object
    lexer = ExprLexer(input_stream)

    # Convert it into a stream of tokens (output from a lexer)
    stream = antlr4.CommonTokenStream(lexer)

    # Push this output into a parser
    parser = ExprParser(stream)

    # Invoke the tree construction function on root node of the parser
    # Note the "parser.prog()", the .prog() is signifying the root node as
    # specified in the grammar
    tree = parser.prog()

    # Parse this tree manually now:
    handleExpression(tree)
