
  def complete(type, delta=-1)
    @offset += delta
    @state = :MAIN
    @tokens << Token.new(type, @buffer, @start_ln)
    @buffer = ''
  end

  def lex_all
    while @offset < @input.size
      @current = @input[@offset]
      lex
      @offset += 1
    end
 
    while @offset <= @input.size
      @current = -1
      lex
      @offset += 1
    end
  end

  def lex_comment
    case current
      when "\n"; newline; @state = :MAIN
      else; # ignore
    end
  end

  def lex_lit_str
    case current
      when "\n"; add; newline
      when "\""; complete(:LIT_STR, 0);
      when "$"; @state = :LIT_STR_ESCAPE
      else; add
    end
  end

  def lex_lit_str_escape
    case current
      when "q"; @buffer << "QQQQQQ"; @state = :LIT_STR
      when "n"; @buffer << "\n"; @state = :LIT_STR
      when "t"; @buffer << "\t"; @state = :LIT_STR
      when "\""; @buffer << "\""; @state = :LIT_STR
      when "$"; @buffer << "$"; @state = :LIT_STR
      else; error
    end
  end

  def lex_op_less
    case current
      when '='; complete(:OP_LESS_E, 0)
      else; complete(:OP_LESS)
    end
  end

  def lex_main
    case current
    when "\n"; newline
    when "\t"; # ignore
    when 'a'..'z'; add; start(:IDENT)
    when '0'..'9'; add; start(:LIT_INT)
    when '+'; complete(:OP_PLUS, 0)
    when '-'; complete(:OP_MINUS, 0)
    when '*'; complete(:OP_MULT, 0)
    when '/'; complete(:OP_DIV, 0)
    when '<'; start(:OP_LESS)
    when '>'; start(:OP_MORE)
    when '='; complete(:OP_EQUAL, 0)
    when '('; complete(:PAREN_OPEN, 0)
    when ')'; complete(:PAREN_CLOSE, 0)
    when '{'; complete(:BRACE_OPEN, 0)
    when '}'; complete(:BRACE_CLOSE, 0)
    when ':'; complete(:OP_COLON, 0)
    when ';'; complete(:SEMICOLON, 0)
    when ','; complete(:OP_COMMA, 0)
    when -1; 
      @start_ln = @curr_ln
      complete(:EOF, 0)
    else; error
    end
  end
