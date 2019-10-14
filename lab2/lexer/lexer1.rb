#! /usr/bin/env ruby

# == = !==
# != !
# >= > 

KEYWORDS = {
  'bool' => :KW_BOOL,
  'break' => :KW_BREAK,
  'fn' => :KW_FN,
  'if' => :KW_IF,
  'int' => :KW_INT,
  'let' => :KW_LET,
  'return' => :KW_RETURN,
  'while' => :KW_WHILE,
}

class Token
  attr_reader :type
  attr_reader :value
  attr_reader :line

  def initialize(type, value, line)
    @type = type
    @value = value
    @line = line
  end
end

class Lexer
  def initialize(input)
    @state = :MAIN
    @input = input
    @offset = 0
    @tokens = []
    @buffer = ''
    @curr_ln = 1
    @start_ln = 1
  end

  def add
    @buffer << current
  end

  def complete(type, delta=-1)
    @offset += delta
    @state = :MAIN
    @tokens << Token.new(type, @buffer, @start_ln)
    @buffer = ''
  end

  def complete_ident
    if keyword = KEYWORDS[@buffer]
      complete(keyword)
    else
      complete(:IDENT)
    end
  end

  def current
    @current
  end

  def error
    puts "lexer error in line %s" % [@curr_ln]
    exit 0  
  end

  def lex
    case @state
    when :COMMENT; lex_comment
    when :MAIN; lex_main
    when :IDENT; lex_ident
    when :LIT_INT; lex_lit_int
    when :LIT_STR; lex_lit_str
    when :LIT_STR_ESCAPE; lex_lit_str_escape
    when :OP_LESS; lex_op_less
    else; raise "internal error"
    end
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
 
    puts '%2s | %2s | %-12s | %s' % ['NO', 'LN', 'TYPE', 'VALUE']
    @tokens.each_with_index do |token, i|
      puts '%2i | %2i | %-12s | %s' % [i, token.line, token.type, token.value]
    end

    @tokens
  end

  def lex_comment
    case current
      when "\n"; newline; @state = :MAIN
      else; # ignore
    end
  end

  def lex_ident
    case current
      when 'a'..'z'; add
      else; complete_ident
    end
  end

  def lex_lit_int
    case current
      when '0'..'9'; add
      else; complete(:LIT_INT)
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
    when ' '; # ignore
    when "\n"; newline
    when "\t"; # ignore
    when "\""; start(:LIT_STR)
    when '#'; @state = :COMMENT
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

  def newline
    @curr_ln += 1
  end

  def start(new_state)
    @state = new_state
    @start_ln = @curr_ln
  end
end

input = File.read('../test1.fx')
lexer = Lexer.new(input)
lexer.lex_all


