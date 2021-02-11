--[[
    Removes all comments and white space from the input stream
    and breaks it into Jack language tokens,
    as specified by Jack grammar

    suggested structure:
    advance - get next token

    It should produce a list of tokens such as 
    <keyword> class </keyword>
    <identifier> Main </identifier>
    <symbol> { </symbol>
    <keyword> function </keyword>
    <keyword> void </keyword>
]]
if os.getenv("LOCAL_LUA_DEBUGGER_VSCODE") == "1" then
    require("lldebugger").start()
end

require 'pl'

function jackTokenizer(filename)

    local TOKENTYPE_KEYWORD = "keyword"
    local TOKENTYPE_SYMBOL = "symbol"
    local TOKENTYPE_IDENTIFIER = "identifier"
    local TOKENTYPE_INT_CONST = "integerConstant"
    local TOKENTYPE_STRING_CONST = "stringConstant"
    local TOKENTYPE_INVALID = "invalid"

    local token
    local token_value
    local token_was_string

    local symbols
    local keywords

    function process(filename)
        symbols = symbol_map()
        keywords = keyword_map()

        --read file line by line
        local contents = file.read(filename)
        --strip single line comments
        contents = string.gsub(contents, "//.-\n", "")
        contents = string.gsub(contents, "/%*.-%*/", "")
        --tabs and newlines to spaces
        contents = string.gsub(contents, "%s", " ")
        local input_stream = contents
        
        --and token by token

        print("<tokens>")
        while(hasMoreTokens(input_stream)) do
            token, input_stream = advance(input_stream)
            local type = tokenType()
            utils.printf("<%s> %s </%s>\n",type, token_value, type)
        end
        print("</tokens>")
    end

    function getNextDelimitedWord (input_stream)
        --trim leading spaces
        local input_stream = stringx.lstrip(input_stream)
        --find everything until the next delimiter
        local start_index, end_index = string.find(input_stream, ".-%s")
        --if no whitespace found, return everything
        if start_index == nil then
            local token = input_stream
            input_stream = ""
            return token, nil
        end
        local token = string.sub(input_stream, start_index, end_index)
        token = stringx.strip(token)
        input_stream = string.sub(input_stream, end_index)
        return token, input_stream
    end

    function keyword_list()
        return {"class","constructor", "function", "method","field", "static",
        "var", "int","char","boolean","void","true","false","null","this","let","do",
        "if","else","while","return"}
    end

    function symbol_list()
        return { "{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"}
    end

    function symbol_map()
        local symbols = {}
        for i,v in ipairs(symbol_list()) do
            if v == "<" then
                symbols[v] = "&lt;" 
            elseif v == ">" then
                symbols[v] = "&gt;"
            elseif v == "&" then
                symbols[v] = "&amp;"
            else
                symbols[v] = v
            end
        end
        return symbols
    end

    function keyword_map()
        local keywords = {}
        for i,v in ipairs(keyword_list()) do 
            keywords[v] = string.upper(v)
        end
        return keywords
    end

    -- returns boolean
    function hasMoreTokens(input_stream)
        if(input_stream == nil) then
            return false
        end
        local trimmed = stringx.lstrip(input_stream)
        return string.len(trimmed) > 0
    end 

    -- should be called only if hasMoreTokens is true
    function advance(input_stream)
        --trim leading spaces
        token_was_string = false
        local input_stream = stringx.lstrip(input_stream)
        local current_token = ""
        --special case - the first character is a symbol
        local firstchar = string.sub(input_stream,1,1)
        if symbols[firstchar] ~= nil then
            --consume just one character
            return firstchar, string.sub(input_stream, 2)
        end
        if firstchar == '"' then
            --look forward to the matching "
            local next_quote = string.find(input_stream,'"', 2)
            current_token = string.sub(input_stream, 2,next_quote-1)
            token_was_string = true
            return current_token, string.sub(input_stream, next_quote+1)
        end

        --consume character by character until we get to one of the terminators (symbol or whitespace)
        --example foo+3;
        repeat
            if(string.len(input_stream) == 0) then
                print("NO INPUT!!")
                return nil,nil
            end
            local char = string.sub(input_stream,1,1)
            if char == " " or symbols[char] ~= nil then
                --end the current token
                return current_token, input_stream
            end
            current_token = current_token .. char
            input_stream = string.sub(input_stream,2)
        until false;

        --go up to next space
        return getNextDelimitedWord(input_stream)

    end

    -- returns the type of the current token
    function tokenType()
        --string constant
        if token_was_string then
            token_value = token
            return TOKENTYPE_STRING_CONST
        end
        if keywords[token] ~= nil then
            token_value = token
            return TOKENTYPE_KEYWORD
        end
        if symbols[token] ~= nil then
            token_value = symbols[token]
            return TOKENTYPE_SYMBOL
        end
        --integer constant - 
        local numValue = tonumber(token)
        if(numValue ~= nil and numValue >= 0 and numValue <= 32767) then
            token_value = numValue
            return TOKENTYPE_INT_CONST
        end
        --identifier [A-Za-z_][A-Za-z_0-9]*
        local match_start, match_end = string.find(token, "[A-Za-z_][A-Za-z0-9_]*")
        if match_start == 1 and match_end == string.len(token) then
            token_value = token
            return TOKENTYPE_IDENTIFIER
        end
        return TOKENTYPE_INVALID
    end

    -- only call when tokenType is keyword
    function keyWord()
        return 
    end

    -- returns character that's the current token
    function symbol()

    end

    -- identifier that's the current token
    function identifier()

    end

    -- returns the integer value of the current token
    function intVal()
    end

    -- returns the string value of the current token
    function stringVal()

    end

    return process(filename)
end

jackTokenizer("ArrayTest/Main.jack")