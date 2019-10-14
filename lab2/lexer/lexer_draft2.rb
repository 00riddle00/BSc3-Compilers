#! /usr/bin/env ruby

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
  end

  def add
    @buffer << @curr_char
  end

  def begin_token(new_state)
    @token_start = @line_no
    @state = new_state
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

  def error
    STDERR.puts 'file.txt:?: lexer error: invalid character at %i' % [@offset]
    exit 0
  end

  def lex_all
    while @offset < @input.size
      @curr_char = @input[@offset]
      lex_char
      @offset += 1
    end

    @curr_char = ' '
    lex_char

    if @state != :START
      puts 'unterminated token'
    else
      complete_token(:EOF)
    end
  end

  def lex_char
    case @state
    when :IDENT; lex_ident
    when :INT_LIT; lex_int_lit
    when :START; lex_start
    else; raise 'bad state %s' % [@state]
    end
  end

  def lex_ident
    case @curr_char
    when 'a'..'z'; add
    when 'A'..'Z'; add
    when '0'..'9'; add
    when '_'; add
    else; complete_token(:IDENT, false) 
    end
  end

  def lex_int_lit
    case @curr_char
    when '0'..'9'; add
    else; complete_token(:INT_LIT, false) 
    end
  end

  def lex_start
    case @curr_char
    when 'a'..'z'; add; begin_token(:IDENT)
    when 'A'..'Z'; add; begin_token(:IDENT)
    when '_'; add; begin_token(:IDENT)
    when '0'..'9'; add; begin_token(:INT_LIT)
    when ' '; # ignore
    when "\n"; @line_no += 1
    when '+'; begin_token(:START); complete_token(:OP_PLUS)
    else; error
    end
  end
end

lexer = Lexer.new(<<SRC)
  aa+ 12312__bEQWJEOIb1234  1234 cceqweqweq
  qweqwe++
  qweqwe
SRC

lexer.lex_all
lexer.dump_tokens



