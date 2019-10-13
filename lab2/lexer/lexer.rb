#! /usr/bin/env ruby

$KEYWORDS = { 
  'if' => :KW_IF,
  'return' => :KW_RETURN,
  'while' => :KW_WHILE,
}

class Token
  attr_reader :type, :value, :line_no

  def initialize(type, value, line_no)
    @type = type
    @value = value
    @line_no = line_no
  end
end




class Lexer
  def initialize(input)
    @buffer = ""
    @input = input
    @line_no = 1
    @offset = 0
    @state = :START
    @tokens = []
    @token_start = 0
    @running = true
  end

  def add
    @buffer << @curr_char
  end

  def begin_token(new_state)
    @token_start = @line_no
    @state = new_state
  end

  def complete_ident
    if kw_type = $KEYWORDS[@buffer]
      @buffer = ""; complete_token(kw_type, false)
    else
      complete_token(:IDENT, false) 
    end
  end

  def complete_token(token_type, advance = true)
    @tokens << Token.new(token_type, @buffer, @token_start)
    #puts "token: %s %s" % [token_type, @buffer]
    @buffer = ""
    @state = :START
    if !advance
      @offset -= 1
    end
  end

  def dump_tokens
    puts "%3s|%3s| %-10s | %-10s" % ["ID", "LN", "TYPE", "VALUE"]
    @tokens.each_with_index do |token, index|
      puts "%3i|%3i| %-10s | %-10s" % [
        index, token.line_no, token.type, token.value
      ]
    end
  end

  def error(msg = nil)
    if msg.nil?
      msg = 'unexpected input character %s' % [@curr_char]
    end

    STDERR.puts 'sample.fx:%i: lexer error: %s' % [@line_no, msg]
    @running = false
  end

  def lex_all
    while @running && @offset < @input.size
      @curr_char = @input[@offset]
      # if @curr_char == "\n"; @line_no += 1; end # BAAAAAD!!!!
      lex_char
      @offset += 1
    end

    @curr_char = ' '
    lex_char

    case @state
    when :START; complete_token(:EOF)
    when :LIT_STR; error("unterminated string")
    else; error("unterminated token: %s" % [@state])
    end
  end

  def lex_char
    case @state
    when :COMMENT_SL; lex_comment_sl
    when :IDENT; lex_ident
    when :LIT_INT; lex_lit_int 
    when :LIT_STR; lex_lit_str
    when :LIT_STR_ESCAPE; lex_lit_str_escape
    when :OP_L; lex_op_l
    when :START; lex_start
    else; raise 'bad state %s' % [@state]
    end
  end

  def lex_comment_sl
    case @curr_char
    when "\n"; @line_no += 1; @state = :START
    else; # ignore
    end
  end

  def lex_ident
    case @curr_char
    when 'a'..'z'; add
    when 'A'..'Z'; add
    when '0'..'9'; add
    when '_'; add
    else; complete_ident
    end
  end

  def lex_lit_int
    case @curr_char
    when '0'..'9'; add
    else; complete_token(:LIT_INT, false) 
    end
  end
  
  def lex_lit_str
    case @curr_char
    when '"'; complete_token(:LIT_STR) 
    when "\\"; @state = :LIT_STR_ESCAPE
    when "\n"; add; @line_no += 1
    else; add
    end
  end

  def lex_lit_str_escape
    case @curr_char
    when '"'; @buffer << "\""
    when 't'; @buffer << "\t"
    when 'n'; @buffer << "\n"
    else; error("invalid escape sequence '\\%s'" % [@curr_char])
    end
    @state = :LIT_STR
  end

  def lex_op_l
    case @curr_char
    when '='; complete_token(:OP_LE)
    else; complete_token(:OP_L, false)
    end
  end

  def lex_start
    case @curr_char
    when 'a'..'z'; add; begin_token(:IDENT)
    when 'A'..'Z'; add; begin_token(:IDENT)
    when '_'; add; begin_token(:IDENT)
    when '0'..'9'; add; begin_token(:LIT_INT) # FIX
    when '"'; begin_token(:LIT_STR)

    when '#'; @state = :COMMENT_SL
    when ' '; # ignore
    when "\n"; @line_no += 1
    when '+'; begin_token(:START); complete_token(:OP_PLUS)
    when '<'; begin_token(:OP_L)
    when '='; begin_token(:START); complete_token(:OP_E)
    else; error
    end
  end
end

input = File.read('../sample.fx')
lexer = Lexer.new(input)
lexer.lex_all
lexer.dump_tokens



