from openai import OpenAI
import subprocess
import os

client = OpenAI()

# model_name = "gpt-4-turbo-2024-04-09"
model_name = "gpt-3.5-turbo-0125"
system_content = """You are an expert software engineer specialized in Python and C programming.
Your task is to rewrite a given Python code in C. You will be provided with the original Python code and a unit test.
You need to write a C function and a main function that tests the C function in the same way as the unit test.
Only produce code that is complete and ready to compile and run.
"""
# parse yaml file with orig code test code includes and tcl; and top function
import yaml
# read config file from terminal argument
import sys
# read config file from terminal argument
if len(sys.argv) != 2:
    print("Please provide the config file")
    exit(1)

config_file = sys.argv[1]

with open(config_file, "r") as f:
    config = yaml.safe_load(f)

# read orig code from config
with open(config["orig_code"], "r") as f:
    orig_code = f.read()

orig_file = config["orig_code"] 

top_function = config["top_function"]

# out folder
out_folder = config["out_folder"]

# check if out_folder exists
if not os.path.exists(out_folder):
    os.makedirs(out_folder)


message_list=[
        {"role": "system", "content": system_content},
        {"role": "user", "content": f"""Help me rewrite the Python function '{top_function}' in C. 
         Make also a main function that tests {top_function} in the same way and produces the same output. \n\n {orig_code}\n"""}
    ]
# counter
total_gpt_runs =0
i= 0
error = True
while error != None:
    error = None
    print("iteration ", i)
    if i ==10:
        exit(1)
    i+=1
    # prompt
    print("Prompt: ", message_list[-1]["content"])
    completion = client.chat.completions.create(
        model=model_name,
        messages = message_list
    )
    total_gpt_runs+=1
    print( completion.choices[0].message.content)

    # get c copde and create a file with it
    c_code_dut = completion.choices[0].message.content.split("```c")[1].split("```")[0]

    # update message_list
    message_list.append(completion.choices[0].message)

    # new file
    file_name = f"{out_folder}/temp_dut.c"
    with open(file_name, "w") as f:
        # f.write(inlcudes)
        f.write(c_code_dut)
        # f.write(test_code_dut)

    # compile the file with gcc
    print("Compiling the code")
    log = subprocess.run(["g++", file_name, "-o", f"temp_dut"], capture_output=True)
    if "error" in log.stderr.decode():
        error = log.stderr.decode()
        #only keep the first 3 lines
        error = "\n".join(error.split("\n")[:3])
        # update message_list
        print("There is an error in the code: ", error)
        message_list.append({"role": "user", "content": "There is an error in the code: " + error + ", please try again"})
        continue

    

    
    # run the compiled files and check the outputs match
    out_dut = subprocess.run(["./temp_dut"], capture_output=True)
    out_ref = subprocess.run(["python3", orig_file], capture_output=True)

    # check the outputs match, ignore whitespaces and new lines
    if out_dut.stdout.decode().replace(" ", "").replace("\n", "").replace("[", "").replace("]", "") == out_ref.stdout.decode().replace(" ", "").replace("\n", "").replace("[", "").replace("]", ""):
        print("The code is correct")
        error = None
    else:
        print("The code is incorrect")
        # retry with same error
        error = True
        message_list.append({"role": "user", "content": "There is an error in the code, the result should be " +  out_ref.stdout.decode()  + " \n the output was instead: "+ out_dut.stdout.decode()+", please try again"})

    print(out_dut.stdout)
    print(out_ref.stdout)


# write final c 
with open(out_folder + f"{top_function}.c", "w") as f:
    f.write(c_code_dut)
print("The code is correct, number of gpt runs: ", total_gpt_runs)