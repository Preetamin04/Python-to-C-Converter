import re

def transform_to_c(lines, symbol_table):
    # Stores translated C functions
    functions = []

    # Stores translated code for the main function
    main_code = []

    # Stores function prototypes
    prototypes = []

    # Tracks indentation levels for block management
    indent_stack = [0]

    # Flag to include math.h if power operator (**) is used
    include_math = False

    # Indicates whether we are inside a function definition
    inside_function = False

    # Keeps track of declared variables to avoid redeclaration
    declared_vars = set()

    # Default function return type
    function_return_type = "int"

    # Tracks function metadata
    current_function_index = None
    current_prototype_index = None
    has_return_statement = False

    #COMMENT FLAGS
    in_multiline_comment = False

    # Helper Function: Get datatype from symbol table
    def get_type(var_name):
        if var_name in symbol_table and "datatype" in symbol_table[var_name]:
            return symbol_table[var_name]["datatype"]
        return "int"

    def is_float_expr(expr):

        # Floor division result is integer
        if "floor(" in expr:
            return False

        return "/" in expr or "." in expr

    # Helper Function: Infer datatype for lists and tuples
    def infer_array_type(elements):
        cleaned = [e.strip() for e in elements if e.strip()]

        if not cleaned:
            return "int"

        is_string = any(
            e.startswith('"') or e.startswith("'") for e in cleaned
        )
        is_float = any("." in e for e in cleaned)

        if is_string:
            return "char"
        elif is_float:
            return "float"
        else:
            return "int"

    # FLOOR DIVISION HANDLER
    def handle_floor_div(expr):
        nonlocal include_math

        def repl(match):
            a = match.group(1).strip()
            b = match.group(2).strip()

            include_math = True

            return f"(int)floor((double)({a}) / ({b}))"

        return re.sub(r'([^/\s]+)\s*//\s*([^/\s]+)', repl, expr)

    # TRUE DIVISION HANDLER
    def handle_true_div(expr):

        # Skip if already converted floor division
        if "floor(" in expr:
            return expr

        def repl(match):
            a = match.group(1).strip()
            b = match.group(2).strip()

            type_a = get_type(a)
            type_b = get_type(b)

            if type_a == "int" and type_b == "int":
                return f"(float){a} / {b}"
            else:
                return f"{a} / {b}"

        return re.sub(r'(\w+)\s*/\s*(\w+)', repl, expr)

    def handle_boolean_literals(expr):
        expr = re.sub(r'\bTrue\b', '1', expr)
        expr = re.sub(r'\bFalse\b', '0', expr)
        return expr

    # Main Transformation Loop
    for line in lines:
        stripped = line.strip()

        # ================= COMMENT HANDLING =================

        # MULTI-LINE COMMENT START/END
        if stripped.startswith(("'''", '"""')):
            if not in_multiline_comment:
                in_multiline_comment = True
                main_code.append("/*")
            else:
                in_multiline_comment = False
                main_code.append("*/")
            continue

        # INSIDE MULTI-LINE COMMENT
        if in_multiline_comment:
            main_code.append(stripped)
            continue

        comment_line = None

        # SINGLE LINE COMMENT (# → //)
        if "#" in stripped:
            code_part, comment_part = stripped.split("#", 1)
            code_part = code_part.rstrip()

            if code_part:
                stripped = code_part
                comment_line = "// " + comment_part.strip()
            else:
                main_code.append("// " + comment_part.strip())
                continue

        # Skip empty lines
        if not stripped:
            continue

        # Calculate indentation level
        indent = len(line) - len(line.lstrip())

        # Close Blocks When Indentation Decreases
        while indent < indent_stack[-1]:
            indent_stack.pop()
            closing = "    " * len(indent_stack) + "}"

            if inside_function:
                if len(indent_stack) == 1 and current_function_index is not None:
                    if not has_return_statement:
                        functions[current_function_index] = functions[current_function_index].replace(
                            "int", "void", 1
                        )
                        prototypes[current_prototype_index] = prototypes[current_prototype_index].replace(
                            "int", "void", 1
                        )
                    elif function_return_type == "float":
                        functions[current_function_index] = functions[current_function_index].replace(
                            "int", "float", 1
                        )
                        prototypes[current_prototype_index] = prototypes[current_prototype_index].replace(
                            "int", "float", 1
                        )
                    current_function_index = None
                    current_prototype_index = None

                functions.append(closing)
            else:
                main_code.append(closing)

        # Exit function block when indentation resets
        if inside_function and len(indent_stack) == 1:
            inside_function = False

        pad = "    " * len(indent_stack)

        # FUNCTION DEFINITION
        if stripped.startswith("def"):
            inside_function = True

            name = stripped.split()[1].split("(")[0]
            params = stripped.split("(")[1].split(")")[0]

            param_list = []
            if params:
                for p in params.split(","):
                    p = p.strip()
                    p_type = get_type(p)
                    if p_type == "char":
                        param_list.append(f"char {p}[]")
                    else:
                        param_list.append(f"{p_type} {p}")

            current_function_index = len(functions)
            current_prototype_index = len(prototypes)
            has_return_statement = False
            function_return_type = "int"

            sig = f"int {name}({', '.join(param_list)})"
            functions.append(f"{sig} {{")
            prototypes.append(f"{sig};")
            indent_stack.append(indent + 4)

        # RETURN STATEMENT
        elif stripped.startswith("return"):
            ret_val = stripped.replace("return", "").strip()
            has_return_statement = True

            if ret_val == "True":
                ret_val = "1"
            elif ret_val == "False":
                ret_val = "0"

            if "." in ret_val:
                function_return_type = "float"

            stmt = f"{pad}return {ret_val};"
            if comment_line:
                stmt += "  " + comment_line
            functions.append(stmt)

        # FUNCTION CALL ASSIGNMENT
        elif "=" in stripped and "input(" not in stripped and re.search(r"\w+\s*\(.*\)", stripped.split("=", 1)[1]):
            var = stripped.split("=")[0].strip()
            rhs = stripped.split("=", 1)[1].strip()

            # Handle operators only on RHS
            rhs = handle_floor_div(rhs)
            rhs = handle_true_div(rhs)
            rhs = handle_boolean_literals(rhs)

            dtype = get_type(var)

            if var not in declared_vars:
                line_out = f"{pad}{dtype} {var} = {rhs};"
                declared_vars.add(var)
            else:
                line_out = f"{pad}{var} = {rhs};"

            if comment_line:
                line_out += "  " + comment_line

            if inside_function:
                functions.append(line_out)
            else:
                main_code.append(line_out)

        # INPUT STATEMENT
        elif "input(" in stripped:
            var = stripped.split("=")[0].strip()

            if "int(input" in stripped:
                dtype = "int"
                fmt = "%d"
            elif "float(input" in stripped:
                dtype = "float"
                fmt = "%f"
            else:
                dtype = "char"
                fmt = "%s"

            if var not in declared_vars:
                if dtype == "char":
                    line_out = f"{pad}char {var}[100];"
                else:
                    line_out = f"{pad}{dtype} {var};"
                declared_vars.add(var)

                if inside_function:
                    functions.append(line_out)
                else:
                    main_code.append(line_out)

            prompt_match = re.search(r'input\([\'"]?(.*?)[\'"]?\)', stripped)
            if prompt_match:
                prompt = prompt_match.group(1)
                if prompt:
                    stmt = f'{pad}printf("{prompt}");'
                    if inside_function:
                        functions.append(stmt)
                    else:
                        main_code.append(stmt)

            scan = f'{pad}scanf("{fmt}", {"&"+var if dtype!="char" else var});'
            if inside_function:
                functions.append(scan)
            else:
                main_code.append(scan)

        # LIST HANDLING
        elif "[" in stripped and "=" in stripped and stripped.endswith("]"):
            var = stripped.split("=")[0].strip()
            values = stripped.split("=", 1)[1].strip()

            elements = [e.strip() for e in values.strip("[]").split(",") if e.strip()]
            dtype = infer_array_type(elements)
            size = len(elements)
            formatted = ", ".join(elements)

            if dtype == "char":
                line_out = f"{pad}char *{var}[{size}] = {{{formatted}}};"
            else:
                line_out = f"{pad}{dtype} {var}[{size}] = {{{formatted}}};"

            declared_vars.add(var)

            if inside_function:
                functions.append(line_out)
            else:
                main_code.append(line_out)

        # FOR LOOP (list iteration)
        elif re.search(r"for\s+(\w+)\s+in\s+(\w+):", stripped):
            match = re.search(r"for\s+(\w+)\s+in\s+(\w+):", stripped)
            var = match.group(1)
            arr = match.group(2)

            line_out = (
                f"{pad}for(int i=0; i<sizeof({arr})/sizeof({arr}[0]); i++) {{\n"
                f"{pad}    int {var} = {arr}[i];"
            )

            if inside_function:
                functions.append(line_out)
            else:
                main_code.append(line_out)

            indent_stack.append(indent + 4)

        # WHILE LOOP
        elif stripped.startswith("while"):
            cond = stripped.replace("while", "").replace(":", "").strip()
            line_out = f"{pad}while({cond}) {{"

            if inside_function:
                functions.append(line_out)
            else:
                main_code.append(line_out)

            indent_stack.append(indent + 4)

        # FOR LOOP (range)
        elif stripped.startswith("for"):
            match = re.search(r"for\s+(\w+)\s+in\s+range\((.*?)\):", stripped)

            if match:
                var = match.group(1)
                args = match.group(2).split(",")

                if len(args) == 1:
                    start, end, step = "0", args[0], "1"
                elif len(args) == 2:
                    start, end = args
                    step = "1"
                else:
                    start, end, step = args

                line_out = (
                    f"{pad}for(int {var}={start.strip()}; "
                    f"{var}<{end.strip()}; {var}+={step.strip()}) {{"
                )

                if inside_function:
                    functions.append(line_out)
                else:
                    main_code.append(line_out)

                indent_stack.append(indent + 4)

        # IF / ELSE
        elif stripped.startswith(("if ", "elif ", "else")):
            if stripped.startswith("if "):
                cond = stripped[2:].replace(":", "").strip()
                line_out = f"{pad}if({cond}) {{"
            elif stripped.startswith("elif"):
                cond = stripped[4:].replace(":", "").strip()
                line_out = f"{pad}else if({cond}) {{"
            else:
                line_out = f"{pad}else {{"

            if inside_function:
                functions.append(line_out)
            else:
                main_code.append(line_out)

            indent_stack.append(indent + 4)

        # PRINT STATEMENT
        elif stripped.startswith("print"):
            content = stripped[6:-1]

            if content.startswith('f"') or content.startswith("f'"):
                content = content[1:].strip('"').strip("'")
                variables = re.findall(r"\{(.*?)\}", content)
                format_parts = []

                for var in variables:
                    dtype = get_type(var.strip())
                    format_parts.append("%f" if dtype == "float" else "%d")

                i = 0

                def repl(match):
                    nonlocal i
                    val = format_parts[i]
                    i += 1
                    return val

                format_str = re.sub(r"\{.*?\}", repl, content)
                stmt = f'{pad}printf("{format_str}\\n", {", ".join(variables)});'

            else:
                if "," not in content:
                    if content.startswith('"') or content.startswith("'"):
                        stmt = f'{pad}printf({content});'
                    else:
                        dtype = get_type(content)
                        fmt = "%f" if dtype == "float" else "%d"
                        stmt = f'{pad}printf("{fmt}\\n", {content});'
                else:
                    parts = content.split(",")
                    fmt = ""
                    vars_ = []

                    for p in parts:
                        p = p.strip()

                        if p.startswith('"') or p.startswith("'"):
                            fmt += p.strip('"').strip("'") + " "
                        else:
                            dtype = get_type(p)
                            fmt += "%f " if dtype == "float" else "%d "
                            vars_.append(p)

                    stmt = f'{pad}printf("{fmt.strip()}\\n", {", ".join(vars_)});'

            if comment_line:
                stmt += "  " + comment_line

            if inside_function:
                functions.append(stmt)
            else:
                main_code.append(stmt)

        # += OPERATOR
        elif "+=" in stripped:
            var, val = stripped.split("+=")
            var = var.strip()
            val = val.strip()

            stmt = f"{pad}{var} += {val};"

            if comment_line:
                stmt += "  " + comment_line

            if inside_function:
                functions.append(stmt)
            else:
                main_code.append(stmt)

        # PASS STATEMENT
        elif stripped == "pass":
            continue

        # BREAK STATEMENT
        elif stripped == "break":
            stmt = f"{pad}break;"

            if comment_line:
                stmt += "  " + comment_line

            if inside_function:
                functions.append(stmt)
            else:
                main_code.append(stmt)

        # CONTINUE STATEMENT
        elif stripped == "continue":
            stmt = f"{pad}continue;"

            if comment_line:
                stmt += "  " + comment_line

            if inside_function:
                functions.append(stmt)
            else:
                main_code.append(stmt)

        # VARIABLE ASSIGNMENT
        elif "=" in stripped:
            var = stripped.split("=")[0].strip()
            rhs = stripped.split("=", 1)[1].strip()

            # Handle operators only on RHS
            rhs = handle_floor_div(rhs)
            rhs = handle_true_div(rhs)
            rhs = handle_boolean_literals(rhs)

            dtype = get_type(var)

            if is_float_expr(rhs):
                dtype = "float"

            symbol_table[var] = {"datatype": dtype}

            if var not in declared_vars:
                line_out = f"{pad}{dtype} {var} = {rhs};"
                declared_vars.add(var)
            else:
                line_out = f"{pad}{var} = {rhs};"

            if comment_line:
                line_out += "  " + comment_line

            if inside_function:
                functions.append(line_out)
            else:
                main_code.append(line_out)

        # FUNCTION CALL
        elif "(" in stripped and ")" in stripped:
            stmt = f"{pad}{stripped};"

            if comment_line:
                stmt += "  " + comment_line

            if inside_function:
                functions.append(stmt)
            else:
                main_code.append(stmt)

    # Close Remaining Open Blocks
    while len(indent_stack) > 1:
        indent_stack.pop()
        closing = "    " * len(indent_stack) + "}"

        if inside_function:
            if current_function_index is not None:
                if not has_return_statement:
                    functions[current_function_index] = functions[current_function_index].replace(
                        "int", "void", 1
                    )
                    prototypes[current_prototype_index] = prototypes[current_prototype_index].replace(
                        "int", "void", 1
                    )
                elif function_return_type == "float":
                    functions[current_function_index] = functions[current_function_index].replace(
                        "int", "float", 1
                    )
                    prototypes[current_prototype_index] = prototypes[current_prototype_index].replace(
                        "int", "float", 1
                    )
                current_function_index = None
                current_prototype_index = None
            functions.append(closing)
        else:
            main_code.append(closing)

    return prototypes, functions, main_code, include_math