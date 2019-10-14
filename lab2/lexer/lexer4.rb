#! /usr/bin/env ruby

#   0-99  a.txt  100 b
# 100-149 b.txt  50 b
# 150-199 c.txt  50 b

# 125 130-137

$keyword = {
  'bool' => :KW_BOOL,
  'break' => :KW_BREAK,
  'fn' => :KW_FN,
  'if' => :KW_IF,
  'int' => :KW_INT,
  'let' => :KW_LET,
  'return' => :KW_RETURN,
  'while' => :KW_WHILE,
}

class Input
  attr_accessor :data
  attr_accessor :offset
  attr_accessor :curr_ln
  attr_accessor :first_ln

  def initialize(data)
    @data = data
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
    @state = :MAIN
    @tokens = []
    @buffer = ''
  end

  def add
    @buffer << @current
  end

  def complete(token_type, delta=-1)
    curr_input.offset += delta
    @state = :MAIN
    @tokens << Token.new(token_type, @buffer, curr_input.first_ln)
    @buffer = ''
  end

  def complete_ident
    if keyword = $keyword[@buffer]
      complete(keyword)
    else
      complete(:IDENT)
    end
  end

  def curr_input
    @inputs.last
  end

  def error(msg=nil)
    puts "lexer error in state %s, position %s" % [@state, curr_input.offset]
    puts "reason: %s" % [msg] if msg
    exit 0
  end

  def lex
    case @state
    when :COMMENT_SINGLE; lex_comment_single
    when :IDENT; lex_ident
    when :INCLUDE; lex_include
    when :MAIN; lex_main
    when :LIT_INT; lex_lit_int
    when :LIT_STR; lex_lit_str
    when :LIT_STR_ESCAPE; lex_lit_str_escape
    when :OP_L; lex_op_l
    else; raise 'internal error: invalid state'
    end
  end

  def lex_all
    loop do
      input = @inputs.last

      if input.offset < input.data.size
        @current = input.data[input.offset]
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

    #puts "final state: %s" % [@state]
    @tokens
  end

  def lex_comment_single
    case @current 
    when "\n"; newline; @state = :MAIN
    else; # do nothing
    end
  end

  def lex_ident
    case @current 
    when 'a'..'z'; add
    else; complete_ident
    end
  end

  def lex_include
    case @current 
    when "\n"; 
      content = File.read(@buffer)
      input = Input.new(content)
      @inputs.push(input)
      @buffer = ''
      @state = :MAIN
    else; add
    end
  end

  def lex_lit_int
    case @current 
    when '0'..'9'; add
    else; complete(:LIT_INT)
    end
  end

  def lex_lit_str
    case @current 
    when '"'; complete(:LIT_STR, 0)
    when '$'; @state = :LIT_STR_ESCAPE
    when "\n"; add; newline
    else; add
    end
  end

  def lex_lit_str_escape
    case @current 
    when '"'; add; @state = :LIT_STR
    when '$'; add; @state = :LIT_STR
    when 'n'; @buffer << "\n"; @state = :LIT_STR
    when 't'; @buffer << "\t"; @state = :LIT_STR
    else; error('invalid escape sequence $%s' % [@current])
    end
  end

  def lex_main
    case @current
    when ' '; # do nothing
    when "\t"; # do nothing
    when "\n"; newline
    when 'a'..'z'; add; start(:IDENT)
    when '0'..'9'; add; start(:LIT_INT)
    when '"'; start(:LIT_STR)
    when '#'; start(:COMMENT_SINGLE)
    when '%'; start(:INCLUDE)
    when '<'; start(:OP_L)
    when '+'; complete(:OP_PLUS, 0)
    when '-'; complete(:OP_MINUS, 0)
    when '*'; complete(:OP_MULT, 0)
    when '='; complete(:OP_EQ, 0)
    when '('; complete(:PAREN_OPEN, 0)
    when ')'; complete(:PAREN_CLOSE, 0)
    when '{'; complete(:BRACE_OPEN, 0)
    when '}'; complete(:BRACE_CLOSE, 0)
    when ';'; complete(:SEMICOLON, 0)
    when ':'; complete(:COLON, 0)
    when ','; complete(:COMMA, 0)
    when -1; curr_input.first_ln = curr_input.curr_ln; complete(:EOF, 0)
    else; error
    end
  end

  def lex_op_l
    case @current 
    when '='; complete(:OP_LE, 0)
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

