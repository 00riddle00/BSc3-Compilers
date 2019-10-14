#! /usr/bin/env ruby

# <

$keywords = {
  'bool' => :KW_BOOL,
  'break' => :KW_BREAK,
  'fn' => :KW_FN,
  'if' => :KW_IF,
  'int' => :KW_INT,
  'let' => :KW_LET,
  'while' => :KW_WHILE,
  'return' => :KW_RETURN,
}

class Input
  attr_accessor :input
  attr_accessor :offset
  attr_accessor :curr_ln
  attr_accessor :first_ln

  def initialize(input)
    @input = input
    @offset = 0
    @curr_ln = 1
    @first_ln = 1
  end
end

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
    @inputs = [Input.new(input)]
    @current = ''
    @state = :MAIN
    @tokens = []
    @buffer = ''
  end

  def add
    @buffer << @current
  end

  def curr_input
    @inputs.last
  end

  def complete(type, delta=-1)
    # puts "COMP %s %s" % [curr_input.offset, type]
    curr_input.offset += delta
    @state = :MAIN
    token = Token.new(type, @buffer, curr_input.first_ln)
    @buffer = ''
    @tokens << token
  end

  def complete_ident
    if keyword_type = $keywords[@buffer]
      complete(keyword_type)
    else
      complete(:IDENT)
    end
  end

  def current
    @current
  end

  def error(msg=nil)
    puts "lexer error in state %s, position %s, line %s" % [@state, curr_input.offset, curr_input.curr_ln]
    if msg
      puts "reason: %s" % [msg]
    end
    exit 0
  end

  def lex
    case @state
    when :COMMENT_SINGLE; lex_comment_single
    when :MAIN; lex_main
    when :LIT_INT; lex_lit_int
    when :LIT_STR; lex_lit_str
    when :LIT_STR_ESCAPE; lex_lit_str_escape
    when :IDENT; lex_ident
    when :OP_L; lex_op_l
    when :INCLUDE; lex_include
    else; raise "invalid state"
    end
  end

  def lex_all
    loop do
      input = @inputs.last
      if input.offset < input.input.size
        @current = input.input[input.offset]
        lex
        input.offset += 1
      elsif @inputs.size == 1
        break
      else
        @inputs.pop
      end
    end

    @current = -1
    lex

    #puts "%2s | %2s | %12s | %s" % ['NO', 'LN', 'TYPE', 'VALUE']
    #@tokens.each_with_index do |token, index|
    #  puts "%2i | %2i | %-12s | %s" % [index, token.line, token.type, token.value]
    #end

    #puts "FINAL POS/STATE %s %s" % [curr_input.offset, @state]
    @tokens
  end

  def lex_comment_single
    case current
    when "\n"; newline; @state = :MAIN
    else; # do nothing
    end
  end

  def lex_ident
    case current
    when 'a'..'z'; add
    else; complete_ident
    end
  end

  def lex_include
    case current
    when "\n"; 
      newline; 
      @state = :MAIN
      new_input = File.read(@buffer)
      new_input = Input.new(new_input)
      @buffer = ''
      @inputs.push(new_input)
    else; add
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
    when '"'; complete(:LIT_STR, 0)
    when "$"; @state = :LIT_STR_ESCAPE
    when "\n"; add; newline
    when -1; error("unterminated string")
    else; add
    end
  end

  def lex_lit_str_escape
    case current
    when '"'; add; @state = :LIT_STR
    when '$'; add; @state = :LIT_STR
    when 'n'; @buffer << "\n"; @state = :LIT_STR
    when 't'; @buffer << "\t"; @state = :LIT_STR
    else; error("invalid escape sequence: $%s" % [current])
    end
  end


  # <=
  def lex_main
    case current
    when ' '; # do nothing
    when "\t"; # do nothing
    when "\n"; newline
    when '#'; @state = :COMMENT_SINGLE
    when 'a'..'z'; add; start(:IDENT)
    when '0'..'9'; add; start(:LIT_INT)
    when "\""; start(:LIT_STR)
    when '<'; start(:OP_L)
    when '>'; complete(:OP_G, 0)
    when '='; complete(:OP_EQ, 0)
    when '%'; start(:INCLUDE)
    when '+'; complete(:OP_PLUS, 0)
    when '-'; complete(:OP_MINUS, 0)
    when '*'; complete(:OP_MULT, 0)
    when '{'; complete(:BRACE_OPEN, 0)
    when '}'; complete(:BRACE_CLOSE, 0)
    when '('; complete(:PAREN_OPEN, 0)
    when ')'; complete(:PAREN_CLOSE, 0)
    when ';'; complete(:SEMICOLON, 0)
    when ':'; complete(:COLON, 0)
    when ','; complete(:COMMA, 0)
    when -1; 
      curr_input.first_ln = curr_input.curr_ln; 
      complete(:EOF, 0)
    else; error
    end
  end

  def lex_op_l
    case current
    when '='; complete(:OP_LE, 0) # <=
    else; complete(:OP_L)
    end
  end

  def newline
    curr_input.curr_ln += 1
  end

  def start(new_state)
    @state = new_state
    curr_input.first_ln = curr_input.curr_ln
  end
end

# = ==
# < <=
# > >=
# ! !=
# 

# input = File.read('main.mr')
# lexer = Lexer.new(input)
# lexer.lex_all


