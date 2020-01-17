def run(filepath:str, line_from:int, line_to:int):
    script = open(filepath)
    script_text = script.read()
    lines = [l for l in script_text.split('\n')]
    print(lines)
    for n in range(line_from - 1, line_to, 1):
        print(lines[n])
        exec(lines[n])
