#! /usr/bin/env ruby

$input = "abcd    897312++ wqewqew"
$state = :START

$keywords = {
  'while' => :KW_WHILE,
}

def begin_token(new_state)
  $token_start = $offset
  $state = new_state
end

def complete_token(token_type, advance = true)
  if !advance
    $offset -= 1
  end

  token_value = $input[$token_start..$offset]
  puts 'complete token: %s: %s' % [token_type, token_value]
  $state = :START
end

def error
  raise 'lexer error %s' % [$curr_char]
end

def lex_all(input)
  $offset = 0
  while $offset < input.size
    $curr_char = input[$offset]
    lex_char
    $offset += 1
  end

  $curr_char = 'EOF'
  lex_char
end

def lex_char
  case $state
  when :IDENT; lex_ident
  when :LIT_INT; lex_lit_int
  when :START; lex_start
  else; raise "bad"
  end
end

def lex_ident
  if $curr_char >= 'a' && $curr_char <= 'z'
    # pass
  else
    complete_token(:IDENT, false)
  end
end

def lex_lit_int
  if $curr_char >= '0' && $curr_char <= '9'
    # pass
  else
    complete_token(:LIT_INT, false)
  end
end

def lex_start
  case $curr_char
  when 'a'..'z'; begin_token(:IDENT)
  when '0'..'9'; begin_token(:LIT_INT)
  when '+'; $token_start = $offset; complete_token(:OP_PLUS)
  when ' ';
  when "\n";
  when 'EOF';
  else; error
  end
end

lex_all($input)

