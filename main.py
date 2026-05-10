import os
import sys

from transformer import transform_to_c
from generator import generate_c_code


def compile_python_to_c(python_code):
    lines = python_code.splitlines()
    functions, main_code, include_math = transform_to_c(lines, {})
    c_lines = generate_c_code(functions, main_code, include_math)
    return "\n".join(c_lines)


def run_compiler(python_code, filename="output"):
    try:
        c_source = compile_python_to_c(python_code)

        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, f"{filename}.c")
        with open(output_path, "w") as f:
            f.write(c_source)

        return c_source, output_path

    except Exception as e:
        return f"Compilation error: {str(e)}", None


def main():
    print("=" * 50)
    print("      Python -> C Converter  (Console Mode)")
    print("=" * 50)

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if not os.path.isfile(input_path):
            print(f"[ERROR] File not found: {input_path}")
            sys.exit(1)

        with open(input_path, "r") as f:
            python_code = f.read()

        filename = os.path.splitext(os.path.basename(input_path))[0]
        print(f"[INFO] Reading from file: {input_path}\n")

    else:
        print("Paste your Python code below.")
        print("When done, type 'END' on a new line and press Enter.\n")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip() == "END":
                break
            lines.append(line)

        python_code = "\n".join(lines)
        filename = "output"

    if not python_code.strip():
        print("[ERROR] No code provided.")
        sys.exit(1)

    result, path = run_compiler(python_code, filename)

    if path is None:
        print(f"\n[ERROR] {result}")
        sys.exit(1)

    print("\n" + "-" * 50)
    print("Generated C Code:")
    print("-" * 50)
    print(result)
    print("-" * 50)
    print(f"\n[SUCCESS] C file saved to: {path}")


if __name__ == "__main__":
    main()