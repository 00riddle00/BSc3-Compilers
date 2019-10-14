#! /usr/bin/env ruby

$KEYWORDS = {
  'if' => :KW_IF,
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
    @input = input
    @offset = 0
    @state = :START
    @line_no = 1
    @running = true
    @buffer = ""
    @tokens = []
    @token_start_ln = 1
  end

  def add
    @buffer << @curr_char
  end

  def begin_token(new_state)
    @state = new_state
    @token_start_ln = @line_no
  end

  def complete_token(token_type)
    @tokens << Token.new(token_type, @buffer, @token_start_ln)
    @buffer = ""
    @state = :START
  end

  def dump_tokens
    puts '%2s|%2s| %-12s | %s' % ['ID', 'LN', 'TYPE', 'VALUE']
    @tokens.each_with_index do |token, index|
      puts '%2i|%2i| %-12s | %s' % [
        index, token.line_no, token.type, token.value
      ]
    end
  end

  def error
    lexer_error("unexpected symbol %s" % [@curr_char.inspect])
    @running = false
  end

  def lex_all
    while @running && @offset < @input.size
      @curr_char = @input[@offset]
      # if @curr_char == "\n"; @line_no += 1; end # BAAAAD!!!!
      lex_char
      @offset += 1
    end

    if @running
      @curr_char = "\n"
      lex_char
      if @state != :START
        lexer_error("unterminated something %s" % [@state])
      end
    end
  end

  def lex_char
    case @state
    when :COMMENT; lex_comment
    when :IDENT; lex_ident
    when :LIT_INT; lex_lit_int
    when :LIT_STR; lex_lit_str
    when :LIT_STR_ESCAPE; lex_lit_str_escape
    when :OP_L; lex_op_l
    when :START; lex_start
    else; raise 'invalid state'
    end
  end

  def lex_comment
    case @curr_char
    when "\n"; @line_no += 1; @state = :START
    else; # ignore
    end
  end

  def lex_ident
    case @curr_char
    when 'a'..'z'; add; return
    end

    rewind
    if kw_type = $KEYWORDS[@buffer]
      @buffer = ""; complete_token(kw_type)
    else
      complete_token(:IDENT)
    end
  end

  def lex_lit_int
    case @curr_char
    when '0'..'9'; add
    else; rewind; complete_token(:LIT_INT)
    end
  end

  def lex_lit_str
    case @curr_char
    when "\n"; add; @line_no += 1
    when "\\"; @state = :LIT_STR_ESCAPE
    when '"'; complete_token(:LIT_STR)
    else; add
    end
  end

  def lex_lit_str_escape
    case @curr_char
    when "n"; @buffer << "\n"
    when "t"; @buffer << "\t"
    when "\""; @buffer << "\""
    else; lexer_error("invalid_escape symbol %s" % @curr_char.inspect)
    end
    @state = :LIT_STR
  end

  def lex_op_l
    case @curr_char
    when "="; complete_token(:OP_LE)
    else; rewind; complete_token(:OP_L)
    end
  end

  def lex_start
    case @curr_char
    when '#'; @state = :COMMENT
    when 'a'..'z'; add; begin_token(:IDENT)
    when '0'..'9'; add; begin_token(:LIT_INT)
    when '+'; begin_token(:START); complete_token(:OP_PLUS)
    when '<'; begin_token(:OP_L)
    when '='; begin_token(:START); complete_token(:OP_E)
    when '"'; begin_token(:LIT_STR)
    when ' '; # ignore
    when "\n"; @line_no += 1
    else; error
    end
  end

  def lexer_error(msg)
    STDERR.puts "sample2.tm:%i: lexer error: %s" % [@line_no, msg]
  end

  def rewind
    @offset -= 1
  end
end

input = File.read('sample2.tm')
lexer = Lexer.new(input)
lexer.lex_all
lexer.dump_tokens


