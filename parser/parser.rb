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

  def parse_decl
    parse_decl_fn
  end

  def parse_decl_fn
    expect(:KW_FN)
    name = expect(:IDENT)
    expect(:OP_PAREN_0)
    params = parse_params
    expect(:OP_PAREN_1)
    expect(:OP_COLON)
    ret_type = parse_type
    body = parse_stmt_block
    DeclFn.new(name, params, ret_type, body)
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

  def parse_expr_paren
    expect(:OP_PAREN_0)
    result = parse_expr
    expect(:OP_PAREN_1)
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

  def parse_param
    name = expect(:IDENT)
    expect(:OP_COLON)
    type = parse_type
    Param.new(name, type)
  end

  def parse_params
    params = []

    if test_token(:OP_PAREN_1)
      return params
    end

    params << parse_param
    while accept(:OP_COMMA)
      params << parse_param
    end

    params
  end

  def parse_program
    decls = []

    loop do
      case token_type
      when :EOF; break
      else; decls << parse_decl
      end
    end

    Program.new(decls)
  end

  def parse_stmt
    case token_type
    when :KW_IF; parse_stmt_if
    when :KW_RETURN; parse_stmt_ret
    else; error
    end
  end

  def parse_stmt_block
    stmts = []

    loop do
      if accept(:KW_END)
        break
      else
        stmts << parse_stmt
      end
    end

    StmtBlock.new(stmts)
  end

  def parse_stmt_if
    expect(:KW_IF)
    cond = parse_expr
    body = parse_stmt_block
    StmtIf.new(cond, body)
  end

  def parse_stmt_ret
    return_kw = expect(:KW_RETURN)
    value = token_type != :OP_SEMI ? parse_expr : nil
    expect(:OP_SEMI)
    StmtReturn.new(return_kw, value)
  end

  def parse_type
    case token_type
    when :KW_BOOL; expect(:KW_BOOL); TypePrim.new(:BOOL)
    when :KW_FLOAT; expect(:KW_FLOAT); TypePrim.new(:FLOAT)
    when :KW_INT; expect(:KW_INT); TypePrim.new(:INT)
    when :KW_VOID; expect(:KW_VOID); TypePrim.new(:VOID)
    else; error
    end
  end

  def test_token(token_type)
    curr_token = @tokens[@offset]
    if curr_token.type == token_type
      curr_token
    end
  end

  def token_type
    @tokens[@offset].type
  end
end



class Program < Node
  # std::vector<Decl*>
  attr_reader :decls

  def initialize(decls)
    @decls = decls
  end

  def print_node(p)
    p.print('decls', @decls)
  end
end