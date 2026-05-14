<div align="center">

# 🐍 → 🅲 &nbsp; Python to C Converter

### A source-to-source compiler that translates Python programs into equivalent C code

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

</div>

---

## 📖 What is This Project?

> **If you have never heard of a compiler before — read this first.**

When you write code in Python, your computer does not actually understand Python. It uses a special program called an **interpreter** or **compiler** to translate your Python into something the machine can run.

**This project is a mini-compiler** — it takes a Python program you write and automatically converts it into an equivalent program written in the **C programming language**.

**Why would you want Python converted to C?**
- C runs much faster than Python (it's closer to machine code)
- C is used in embedded systems, operating systems, and hardware programming
- It's a great learning tool to understand what Python is doing "under the hood"

**Example — you write this Python:**

```python
n = int(input("Enter a number: "))
if n > 10:
    print("Big number")
else:
    print("Small number")
```

**This project instantly produces this C:**

```c
#include <stdio.h>

int main() {
    int n;
    printf("Enter a number: ");
    scanf("%d", &n);
    if(n > 10) {
        printf("Big number");
    }
    else {
        printf("Small number");
    }
    return 0;
}
```

No manual work. No knowledge of C required. Just click **Convert**.

---

### What each file does in plain English

| File | Think of it as... | What it actually does |
|---|---|---|
| `app.py` | Runs the website you interact with. Has the upload button, text box, and Convert button. |
| `main.py` | Calls transformer + generator in the right order. Also lets you run from the command line. |
| `transformer.py` | Reads each Python line and rewrites it in C syntax. The most complex file. |
| `generator.py` | Takes all the translated pieces and glues them into one valid C file with the right headers. |

---

## ✅ What Python Code Can It Convert?

The converter handles the most common Python constructs:

| Python | C Output | Example |
|---|---|---|
| `int(input("..."))` | `scanf("%d", &var)` | Taking number input |
| `float(input("..."))` | `scanf("%f", &var)` | Taking decimal input |
| `input("...")` | `scanf("%s", var)` | Taking text input |
| `print(x)` | `printf("%d\n", x)` | Printing a variable |
| `print(f"val={x}")` | `printf("val=%d\n", x)` | f-string printing |
| `a = 10` | `int a = 10;` | Variable assignment |
| `b = 3.14` | `float b = 3.14;` | Float assignment |
| `a += 1` | `a += 1;` | Compound operator |
| `a // b` | `(int)(a / b)` | Floor division |
| `a / b` | `(float)a / b` | True division |
| `if x > 0:` | `if(x > 0) {` | Conditionals |
| `elif x == 0:` | `else if(x == 0) {` | Else-if |
| `else:` | `else {` | Else |
| `while i < n:` | `while(i < n) {` | While loop |
| `for i in range(n):` | `for(int i=0; i<n; i+=1) {` | For loop |
| `for i in range(a,b,s):` | `for(int i=a; i<b; i+=s) {` | For with step |
| `for x in arr:` | `for(int i=0; i<sizeof(arr)/sizeof(arr[0]); i++) {` | List iteration |
| `arr = [1,2,3]` | `int arr[3] = {1,2,3};` | Array / list |
| `def func(a, b):` | `int func(int a, int b) {` | Function |
| `return value` | `return value;` | Return statement |
| `break` | `break;` | Break |
| `continue` | `continue;` | Continue |
| `pass` | *(skipped)* | Pass statement |
| `# comment` | `// comment` | Single-line comment |
| `"""docstring"""` | `/* docstring */` | Multi-line comment |
| `True` / `False` | `1` / `0` | Boolean literals |

---

## ⚙️ Requirements

You only need **two things** installed:

### 1. Python 3.8 or higher

Check if you have it by opening a terminal and running:

```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from: https://www.python.org/downloads/

### 2. Streamlit (the web interface library)

Install it by running this **one command** in your terminal:

```bash
pip install streamlit
```

**That's it.** No other libraries needed. Everything else (`re`, `os`, `sys`) is built into Python already.

---

## 🚀 Installation — Step by Step

### Step 1 — Get the project

**Option A: Download ZIP from GitHub**
1. Go to the GitHub repository page
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract (unzip) the downloaded file
5. You will see a folder called `Python_to_C_Converter`

**Option B: Clone with Git** (if you have Git installed)

```bash
git clone https://github.com/your-username/Python_to_C_Converter.git
```

---

### Step 2 — Open a terminal inside the project folder

**On Windows:**
- Open the extracted folder
- Click the address bar at the top of the File Explorer window
- Type `cmd` and press Enter
- A command prompt opens inside that folder

**On Mac / Linux:**

```bash
cd path/to/Python_to_C_Converter
```

> Replace `path/to/` with the actual location where you extracted the folder.

---

### Step 3 — Install Streamlit

```bash
pip install streamlit
```

> If `pip` does not work, try `pip3 install streamlit`

---

### Step 4 — Run the application

```bash
streamlit run app.py
```

After a second or two, your browser will automatically open to:

```
http://localhost:8501
```

You will see the **Python to C Converter** web interface — ready to use.

---

## 🖥️ How to Use the Web Interface

The interface has four sections:

### Section 1 — Upload a Python file *(optional)*
- Click **"Browse files"** or drag and drop a `.py` file
- The file's contents will appear automatically in the text editor below

### Section 2 — Edit or type Python code
- A large text box shows your code
- You can type directly here even without uploading a file
- Try pasting this quick example:

```python
n = int(input("Enter a number: "))
for i in range(n):
    print(i)
```

### Section 3 — Set output filename *(optional)*
- Type a name for the output `.c` file (for example: `my_program`)
- If you leave it empty, it uses the uploaded filename or `manual_input` as the default

### Section 4 — Convert!
- Click the **Convert** button
- The page splits into two columns:
  - **Left column** — your original Python code with a Download button
  - **Right column** — the generated C code with a Download button

---

## 💻 Command Line Usage *(Alternative to the Web UI)*

You can also run the converter directly from the terminal.

**Convert a Python file:**

```bash
python main.py "test codes/even_odd.py"
```

**Type code interactively:**

```bash
python main.py
```

Paste your Python code line by line. When done, type `END` on a new line and press Enter. The generated C file is saved automatically in the `outputs/` folder.

---

## 🔄 Control Flow — How the Project Works Internally

> This section explains exactly what happens from the moment you click **Convert** to when C code appears on screen. Even if you have never read source code before, the diagrams below will make it clear.

### The Big Picture

```
You type / upload Python code
           │
           ▼
    ┌─────────────┐
    │   app.py    │  ← You click "Convert" here
    │  (Web UI)   │
    └──────┬──────┘
           │  calls run_compiler(code, filename)
           ▼
    ┌─────────────┐
    │   main.py   │  ← Manages the whole process
    └──────┬──────┘
           │  calls compile_python_to_c(code)
           ▼
    ┌──────────────────┐
    │  transformer.py  │  ← Reads Python line by line
    │  transform_to_c()│     and converts each line to C
    └──────┬───────────┘
           │  returns prototypes[], functions[], main_code[], include_math
           ▼
    ┌──────────────────┐
    │   generator.py   │  ← Assembles all C pieces into
    │ generate_c_code()│     one complete, valid C file
    └──────┬───────────┘
           │  returns final C code string
           ▼
    ┌─────────────┐
    │   main.py   │  ← Saves .c file to outputs/ folder
    └──────┬──────┘
           │  returns (c_code, file_path) to app.py
           ▼
    ┌─────────────┐
    │   app.py    │  ← Shows C code on screen + download button
    └─────────────┘
```

---

### Inside transformer.py — Line by Line Processing

This is the most important file. For every single line of your Python code, it works through this decision tree in order:

```
For EACH LINE in your Python code:
│
├─ Blank line or comment (#)?          → Skip it / convert # to //
│
├─ Did indentation DECREASE?           → Close open C blocks with  }
│   (e.g. after an if-block ends)         using the indent stack
│
├─ Starts with  def  ?                 → Start a C function definition
│                                          store index for return-type fix
│
├─ Starts with  return  ?              → Emit  return value;
│                                          flag float return for type patch
│
├─ Has  =  and a function call on RHS? → Variable assigned from function call
│
├─ Contains  input(  ?                 → int / float / char input → scanf
│
├─ Has  [  ]  (list literal)?          → C array declaration
│
├─ Matches  for x in arr  ?            → sizeof-based C for-loop
│
├─ Starts with  while  ?               → C while loop
│
├─ Starts with  for  ?                 → range()-based C for-loop
│
├─ Starts with  if / elif / else  ?    → C if / else if / else block
│
├─ Starts with  print  ?               → printf with correct format specifier
│
├─ Contains  +=  ?                     → Compound assignment  a += val;
│
├─ Is  pass  ?                         → Skip (no C equivalent needed)
│
├─ Is  break  ?                        → Emit  break;
│
├─ Is  continue  ?                     → Emit  continue;
│
└─ Contains  =  ?                      → Variable assignment
                                           typed on first use, plain after
```

---

### Key Mechanism — The Indent Stack

Python uses spaces (indentation) to define code blocks. C uses `{` and `}`. The transformer tracks a **stack of indent levels** that tells it exactly when to open and close braces:

```
Python code:              What indent_stack looks like:
──────────────────        ──────────────────────────────────────────────
def foo(n):               [0, 4]    ← pushed 4 when def was found
    if n > 0:             [0, 4, 8] ← pushed 8 when if was found
        print(n)          [0, 4, 8] ← no change, still inside if
    return n              back to 4 → pop 8 → emit "    }" (closes if)
                          back to 0 → pop 4 → emit "}"    (closes def)
```

Every time indentation decreases, one or more `}` braces are emitted. This is exactly how Python's invisible indentation becomes C's explicit block braces.

---

### Inside generator.py — Assembling the Final C File

After transformation, four lists are returned:

| List | Contains |
|---|---|
| `prototypes[]` | Function signatures like `int add(int a, int b);` |
| `functions[]` | Full function body definitions |
| `main_code[]` | All top-level statements (not inside any function) |
| `include_math` | `True` if the `**` power operator was used |

The generator assembles them in this exact order:

```c
#include <stdio.h>           ← always added

#include <math.h>            ← only if ** (power) was used in Python

int add(int a, int b);       ← function prototypes (forward declarations)

int main() {                 ← main_code[] wrapped inside main()
    ...
    return 0;
}

int add(int a, int b) {      ← full function bodies placed after main
    ...
}
```

> **Why does the function body appear AFTER main?**
>
> Prototypes are placed **before** `main()` so C knows about the function before it is called. The actual body is placed **after** — this is standard, valid C practice.

---

## 🧪 Testing with Sample Files

The `test codes/` folder contains ready-to-use Python programs. Each one tests different features:

| File | What it tests |
|---|---|
| `even_odd.py` | Function with return value, if/else, input |
| `prime_no_check.py` | Function, for loop, nested if, input |
| `prime_no_n.py` | For loop, function, multiple returns |
| `integer_division.py` | Floor division `//` and true division `/` |
| `test_multi_param.py` | Function with multiple parameters |
| `test_void.py` | Function with no return (void function) |
| `master_test.py` | Everything combined — functions calling functions, nested loops, lists, booleans, comments, floor division |

**To test from the web UI:**
1. Click **Browse files**
2. Navigate to the `test codes/` folder
3. Select any `.py` file and click **Convert**

**To test from the command line:**

```bash
python main.py "test codes/master_test.py"
```

---

## 📝 Quick Examples

### Example 1 — Simple Calculator

**Python input:**

```python
a = int(input("Enter a: "))
b = int(input("Enter b: "))
result = a + b
print(result)
```

**Generated C:**

```c
#include <stdio.h>

int main() {
    int a;
    printf("Enter a: ");
    scanf("%d", &a);
    int b;
    printf("Enter b: ");
    scanf("%d", &b);
    int result = a + b;
    printf("%d\n", result);
    return 0;
}
```

---

### Example 2 — Function with Return Value

**Python input:**

```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

num = int(input("Enter n: "))
result = factorial(num)
print(result)
```

**Generated C:**

```c
#include <stdio.h>

int factorial(int n);

int main() {
    int num;
    printf("Enter n: ");
    scanf("%d", &num);
    int result = factorial(num);
    printf("%d\n", result);
    return 0;
}

int factorial(int n) {
    if(n == 0 or n == 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
```

---

### Example 3 — Floor Division and True Division

**Python input:**

```python
a = 15
b = 4
floor_result = a // b
true_result = a / b
print(floor_result)
print(true_result)
```

**Generated C:**

```c
#include <stdio.h>

int main() {
    int a = 15;
    int b = 4;
    int floor_result = (int)(a / b);
    float true_result = (float)a / b;
    printf("%d\n", floor_result);
    printf("%f\n", true_result);
    return 0;
}
```

---

## 📂 Output Files

Every time you convert, a `.c` file is saved in the `outputs/` folder:

```
outputs/
├── manual_input.c       ← saved when you type code manually
├── even_odd.c           ← saved when you upload even_odd.py
└── your_filename.c      ← saved with whatever name you chose
```

You can compile and run these C files using GCC:

```bash
gcc outputs/even_odd.c -o even_odd
./even_odd
```

If the program uses the power operator `**`, add `-lm`:

```bash
gcc outputs/program.c -o program -lm
./program
```

---

## ⚠️ Known Limitations

The converter handles the most common Python patterns. A few things are not yet supported:

| Not Supported | Workaround |
|---|---|
| `and` / `or` / `not` in conditions | Use equivalent C expressions manually |
| `**` (power operator) — `math.h` not auto-included | Add `#include <math.h>` manually to the output |
| Negative step in range: `range(5, 0, -1)` | Use a while loop instead |
| Dictionaries `{}` | No direct C equivalent |
| Classes and objects | C has no class system |
| List comprehensions | Use an explicit for loop |
| `try` / `except` | Not supported |
| Multi-line statements with `\` | Put each statement on its own line |
| String methods like `split`, `join` | Not supported |

---

## 🛠️ Troubleshooting

### `streamlit: command not found`

```bash
# Try pip3 instead of pip:
pip3 install streamlit

# Or use python -m:
python -m streamlit run app.py
```

### `No module named streamlit`

```bash
# Make sure you install into the correct Python version:
python -m pip install streamlit
```

### Port already in use

```bash
# Run on a different port:
streamlit run app.py --server.port 8502
```

### The browser did not open automatically

Manually go to:

```
http://localhost:8501
```

### `Compilation error: ...` shown in the app

Your Python code may contain a construct the converter does not support yet. Check the **Known Limitations** section above and try simplifying the code.

---

## 🗂️ Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Language | Python 3.8+ | Everything is written in Python |
| Web UI | Streamlit | Creates the browser interface — no HTML or CSS needed |
| Pattern matching | `re` (regex) | Detects Python constructs in each source line |
| File handling | `os`, `sys` | Creates output folders and handles file paths |
| C assembler | Custom `generator.py` | Puts all translated pieces into one complete C program |

---

## 📜 License

This project was developed as an academic lab project for **Compiler Design**.
Feel free to use, modify, and share it for educational purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Commit: `git commit -m "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Open a Pull Request

---

<div align="center">

**Made with 🐍 Python &nbsp;·&nbsp; Powered by Streamlit**

*If this project helped you understand compilers, give it a ⭐ on GitHub!*

</div>
