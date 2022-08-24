import os
import sys
import tkinter as tk
from clusterer import do_clustering
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from VectorModelBuilder import VectorModelBuilder

VMB_ARGS = (
    ("Dataset", ""), 
    ("Count Method", "ngram"), 
    ("Weighting", "ppmi"), 
    ("Output Directory", "../vector_data/"), 
    ("Output File Name", "<default name>"), 
    ("Value of N", "3")
)
CLUSTERER_ARGS = (
    ("Input Data File", ""), 
    ("Output File Directory", "../found_classes/"), 
    ("Output File Name", "classes.txt"), 
    ("V Scalar", "1"), 
    ("Constrain Partition", "True"), 
    ("Constrain PCS", "True")
)
LABELS = ["  Run  ","Browse..."]
BOOL_LABELS = ["True", "False"]
FILE_TYPE = (
    ("All Files", "*.*"), 
    ("Text Files", "*.txt"),
    ("Data Files", "*.data")
)
COUNT_METHODS = ["ngram"]
WEIGHT_METHODS = ["ppmi", "probability", "conditional_probability", "pmi", "none"]

# Setting up the root of the window, intended to take up a quarter of the screen
HEIGHT = 500
WIDTH = 960
window = tk.Tk()
window.title("Distributional Learning")
canvas = tk.Canvas(window, height=HEIGHT, width=WIDTH)
canvas.grid()

################### Vector Model Builder ################
vmb_frame = tk.Frame(master=window)
vmb_frame.place(x=10, y=10, relx=0, rely=0, relwidth=0.6)
vector_model_builder = tk.Label(master=vmb_frame, text="Vector Model Builder")
vector_model_builder.grid(row=0, column=0, sticky="w")
# looping to populate labels
for i, text in enumerate(VMB_ARGS):
    label = tk.Label(master=vmb_frame, text=VMB_ARGS[i][0])
    label.grid(row=i+1, column=0, sticky="e")

# Argument 1 Dataset
def open_dataset_browse():
    """Open a file."""
    filepath = askopenfilename(
        filetypes=FILE_TYPE
    )
    if not filepath:
        return
    dataset_path_ent.delete("0", tk.END)
    dataset_path_ent.insert(tk.END, filepath)

dataset_path_ent = tk.Entry(master=vmb_frame, width=60)
dataset_path_ent.grid(row=1, column=1, sticky="w")
dataset_path_ent.insert(0, VMB_ARGS[0][1])
dataset_browse = tk.Button(
    master=vmb_frame, text="Browse...", command=open_dataset_browse
)
dataset_browse.grid(row=1, column=2, sticky="e")

# Argument 2 Count Method
method_ent = tk.StringVar(vmb_frame)
method_ent.set(VMB_ARGS[1][1])
method_menu = tk.OptionMenu(
    vmb_frame, method_ent, *COUNT_METHODS
)
method_menu.grid(row=2, column=1, sticky="w")

# Argument 3 Weighting
weight_var = tk.StringVar(vmb_frame)
weight_var.set(VMB_ARGS[2][1])
weight_menu = tk.OptionMenu(vmb_frame, weight_var, *WEIGHT_METHODS)
weight_menu.grid(row=3, column=1, sticky="w")

# Argument 4 Output directory
def open_outdir_browse():
    """Open a directory."""
    dirpath = askdirectory()
    if not dirpath:
        return
    outdir_ent.delete("0", tk.END)
    outdir_ent.insert(tk.END, dirpath)

outdir_ent = tk.Entry(master=vmb_frame, width=60)
outdir_ent.grid(row=4, column=1, sticky="w")
outdir_ent.insert(0, VMB_ARGS[3][1])
outdir_browse = tk.Button(
    master=vmb_frame, text="Browse...", command=open_outdir_browse
)
outdir_browse.grid(row=4, column=2, sticky="e")

# Argument 5 Output File Name
outf_name_ent = tk.Entry(master=vmb_frame)
outf_name_ent.grid(row=5, column=1, sticky="w")
outf_name_ent.insert(0,VMB_ARGS[4][1])

# Argument 6 value of N "-n"
n_ent = tk.Entry(master=vmb_frame)
n_ent.grid(row=6, column=1, sticky="w")
n_ent.insert(0, VMB_ARGS[5][1])

# A dataset is required to run
def run_vector_model_builder():
    # returns an error message if first argument is blank
    if not dataset_path_ent.get():
        return messagebox.showwarning(
            title="Error...", message="Missing Required Argument"
        )

    n_val = n_ent.get()        
    outfile_arg = outf_name_ent.get()
    # Check for the default case of None for output file name
    if outfile_arg == "<default name>":
        outfile_arg = None
    # Convert value of n from string to int or set the default to 3 if blank
    if not n_val:
        n_val = 3
    else:
        n_val = int(n_val)

    Vector_tk = VectorModelBuilder(
        dataset_path_ent.get(), method_ent.get(), weight_var.get(), 
        outdir_ent.get(),outfile_arg,n_val
    )
    Vector_tk.create_vector_model()
    Vector_tk.save_vector_model()

run_VectorModelBuilder = tk.Button(
    master=vmb_frame, command=run_vector_model_builder, text=LABELS[0]
)
run_VectorModelBuilder.grid(row=7, column=0, sticky="w")
#########################################################################
################################## Clusterer ############################
clusterer_frame = tk.Frame(master=window)
clusterer_frame.place(x=10, y=10, relx=0, rely=0.5, relwidth=0.6)

clusterer = tk.Label(master=clusterer_frame, text="Clusterer")
clusterer.grid(row=0, column=0, sticky="w")
# Looping to populate the labels
for i, text in enumerate(CLUSTERER_ARGS):
    label = tk.Label(master=clusterer_frame, text=CLUSTERER_ARGS[i][0])
    label.grid(row=i+1, column=0, sticky="e")

# Argument 1
def open_file_name():
    """Open a file."""
    filepath = askopenfilename(
        filetypes=FILE_TYPE
    )
    if not filepath:
        return
    filepath = filepath.rsplit('.', 1)
    file_name_ent.delete("0", tk.END)
    file_name_ent.insert(tk.END, filepath[0])

file_name_ent = tk.Entry(master=clusterer_frame, width=60)
file_name_ent.grid(row=1, column=1, sticky="w")
file_name_ent.insert(0, CLUSTERER_ARGS[0][1])
file_name_btn = tk.Button(
    master=clusterer_frame, text=LABELS[1], command=open_file_name
)
file_name_btn.grid(row=1, column=2, sticky="w")

# Argument 2 Output File Directory
def output_file_browse():
    """Open a file."""
    dirpath = askdirectory()
    if not dirpath:
        return
    output_dir_ent.delete("0", tk.END)
    output_dir_ent.insert(tk.END, dirpath)

output_dir_ent = tk.Entry(master=clusterer_frame, width=60)
output_dir_ent.grid(row=2, column=1, sticky="w")
output_dir_ent.insert(0, CLUSTERER_ARGS[1][1])
output_dir_browse = tk.Button(
    master=clusterer_frame, text="Browse...", command=output_file_browse
)
output_dir_browse.grid(row=2, column=2, sticky="w")

# Argument 3 Output File Name
output_name_ent = tk.Entry(
    master=clusterer_frame, text=CLUSTERER_ARGS[2], width=60
)
output_name_ent.grid(row=3, column=1, sticky="w")
output_name_ent.insert(0, CLUSTERER_ARGS[2][1])

# Argument 4 v_scalar
v_scalar_ent = tk.Entry(master=clusterer_frame)
v_scalar_ent.grid(row=4, column=1, sticky="w")
v_scalar_ent.insert(0, CLUSTERER_ARGS[3][1])

# Argument 5
constrain_partition_var = tk.StringVar(clusterer_frame)
constrain_partition_var.set(CLUSTERER_ARGS[4][1])
constrain_partition_menu  = tk.OptionMenu(
    clusterer_frame, constrain_partition_var, *BOOL_LABELS
)
constrain_partition_menu.grid(row=5, column=1, sticky="w")

# Argument 6
constrain_pcs_var = tk.StringVar(clusterer_frame)
constrain_pcs_var.set(CLUSTERER_ARGS[5][1])
constrain_pcs_menu  = tk.OptionMenu(
    clusterer_frame, constrain_pcs_var, *BOOL_LABELS
)
constrain_pcs_menu.grid(row=6, column=1, sticky="w")

def run_clusterer():
    # returns an error message if first argument is blank
    if not file_name_ent.get():
        return messagebox.showwarning(
            title="Error...", message="Missing Required Argument"
        )

    output = os.path.join(output_dir_ent.get(), output_name_ent.get())
    v_scalar = int(v_scalar_ent.get())
    constrain_partition = bool(constrain_partition_var.get())
    constrain_pcs = bool(constrain_pcs_var.get())

    do_clustering(
        file_name_ent.get(), output, v_scalar, constrain_partition, 
        constrain_pcs
    )

run_clusterer_btn = tk.Button(
    master=clusterer_frame, command=run_clusterer, text=LABELS[0]
)
run_clusterer_btn.grid(row=7, column=0, sticky="w")
########################################################################
###################### stdout & stderr implementation ##################

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("0.0", str, (self.tag,))
        self.widget.configure(state="disabled")

text = tk.Text(master=window)
text.place(y=10, x=10, relx=0.6, rely=0, relwidth=0.4, relheight=1)
text.insert("end", "\nThis box is for stdout and stderr only.\nNo user input required.")
text.tag_configure("stderr", foreground="#b22222")
sys.stdout = TextRedirector(text, "stdout")
sys.stderr = TextRedirector(text, "stderr")

window.mainloop()


python generate_vowel_harmony_corpus.py --corpus_size 8000 --outfile output_train.txt 

python code\\generate_vowel_harmony_corpus.py --corpus_size 2000 --outfile output_dev.txt
