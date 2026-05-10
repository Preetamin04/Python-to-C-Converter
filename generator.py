def generate_c_code(prototypes, functions, main_code, include_math=False):

    code = []
    code.append("#include <stdio.h>")

    if include_math:
        code.append("#include <math.h>")

    code.append("")

    # PROTOTYPES
    if prototypes:
        for p in prototypes:
            code.append(p)
        code.append("")

    #  MAIN FUNCTION
    code.append("int main() {")

    for line in main_code:
        code.append(line)

    code.append("    return 0;")
    code.append("}")

    code.append("")

    # FUNCTIONS (DEFINED AFTER MAIN)
    for line in functions:
        code.append(line)

    return code