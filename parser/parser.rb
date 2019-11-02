
class Parser
  def initialize(tokens)
    @tokens = tokens
    @offset = 0
  end

  def error
    raise 'parse error'
  end

  def accept(token_type)
    curr_token = @tokens[@offset]
    if curr_token.type == token_type
      @offset += 1
      curr_token
    end
  end

  def expect(token_type)
    curr_token = @tokens[@offset]
    if curr_token.type == token_type
      @offset += 1
      curr_token
    else
      raise 'expected: %s, got: %s' % [token_type, curr_token.inspect]
    end
  end


  def parse_expr
    parse_expr_add
  end

  # <ADD> ::= <MULT> | <ADD> "+" <MULT>
  # <ADD> ::= <MULT> {("+" | "-") <MULT>}
  def parse_expr_add
    result = parse_expr_mult

    loop do
      if accept(:OP_PLUS)
        result = ExprBinary.new(:ADD, result, parse_expr_mult)
      elsif accept(:OP_MINUS)
        result = ExprBinary.new(:SUB, result, parse_expr_mult)
      else
        break
      end
    end

    result
  end

  def parse_expr_lit_int
    lit = expect(:LIT_INT)
    ExprLit.new(lit)
  end

  # <MULT> ::= <PRIMARY> | <MULT> "*" <PRIMARY>
  # <MULT> ::= <PRIMARY> {"*" <PRIMARY>}
  def parse_expr_mult
    result = parse_expr_primary

    while accept(:OP_MULT)
      result = ExprBinary.new(:MULT, result, parse_expr_primary)
    end

    result
  end

  # <PRIMARY> ::= <LIT_INT> | <VAR> | <PAREN>
  def parse_expr_primary
    case token_type
    when :IDENT; parse_expr_var
    when :LIT_INT; parse_expr_lit_int
    when :OP_PAREN_0; parse_expr_paren
    else; error
    end
  end

  def parse_expr_var
    name = expect(:IDENT)
    ExprVar.new(name)
  end


# abstract
class Node
  def print_node(p)
    raise 'print not implemented for %s' % [self.class]
  end
end

class ExprBinary < Expr
  attr_reader :op, :left, :right

  def initialize(op, left, right)
    @op = op
    @left = left
    @right = right
  end

  def print_node(p)
    p.print_single('op', @op)
    p.print('left', @left)
    p.print('right', @right)
  end
end

class ExprLit < Expr
  attr_reader :lit

  def initialize(lit)
    @lit = lit
  end

  def print_node(p)
    p.print('lit', @lit)
  end
end

class ExprVar < Expr
  attr_reader :name

  def initialize(name)
    @name = name
  end

  def print_node(p)
    p.print('name', @name)
  end
end



class ASTPrinter
  def initialize
    @indent_level = 0
  end

  def print(title, object)
    if object.is_a?(Node)
      print_node(title, object)
    elsif object.is_a?(Array)
      print_array(title, object)
    elsif object.is_a?(Token)
      print_token(title, object)
    elsif object.nil?
      print_single(title, 'NIL')
    else
      raise 'bad print argument %s' % [object.class]
    end
  end

  def print_array(title, array)
    if array.empty?
      return print_single(title, '[]')
    end

    array.each_with_index do |elem, index|
      print('%s[%i]' % [title, index], elem)
    end
  end

  def print_node(title, node)
    print_single(title, '%s:' % [node.class])
    @indent_level += 1
    node.print_node(self)
    @indent_level -= 1
  end

  def print_single(title, text)
    prefix = '  ' * @indent_level
    STDOUT.puts '%s%s: %s' % [prefix, title, text]
  end

  def print_token(title, token)
    text = '%s (l=%i)' % [token.value, token.line_no]
    print_single(title, text)
  end
end






