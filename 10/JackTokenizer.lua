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

    function process(filename)
        --read file line by line
        local contents = file.read(filename)
        --strip single line comments
        contents = string.gsub(contents, "//.-\n", "")
        contents = string.gsub(contents, "/%*.-%*/", "")
        --tabs and newlines to spaces
        contents = string.gsub(contents, "%s", " ")
        local input_stream = contents
        
        print(contents)
        --and token by token

        while(hasMoreTokens(input_stream)) do
            token, input_stream = getNextDelimitedWord(input_stream)
            print("Next token: " .. token)
            print("Type:" .. tokenType())
        end
        print('end!')
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

    function keyword_map()
        keywords = {}
        for i,v in ipairs(keyword_list()) do 
            keywords[v] = string.upper(v)
        end
        return keywords
    end

    -- returns boolean
    function hasMoreTokens(input_stream)
        return input_stream ~= nil
    end

    -- should be called only if hasMoreTokens is true
    function advance()
        token = getNextDelimitedWord
    end

    -- returns the type of the current token
    function tokenType()
        if keyword_map()[token] ~= nil then
            token_value = keyword_map()[token]
            return TOKENTYPE_KEYWORD
        end
        if tablex.find(symbol_list(), token) ~= nil then
            token_value = symbol_list()[token]
            return TOKENTYPE_SYMBOL
        end
        --integer constant - 
        local numValue = tonumber(token)
        if(numValue ~= nil and numValue >= 0 and numValue <= 32767) then
            token_value = numValue
            return TOKENTYPE_INT_CONST
        end
        --string constant
        --???
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

jackTokenizer("ArrayTest/MainMini.jack")