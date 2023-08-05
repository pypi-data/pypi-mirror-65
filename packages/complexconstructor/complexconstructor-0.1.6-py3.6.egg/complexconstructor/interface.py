from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os
import re
import complexconstructor.helpText as helpText
import webbrowser

def initGui():
    cwd = os.getcwd()
    #initialize main window
    root = Tk()
    logo = Image("photo", file = os.path.dirname(os.path.realpath(__file__))+"/CB_icon.png")
    logo_sm = Image("photo", file = os.path.dirname(os.path.realpath(__file__))+"/CB_icon_sm.png")
    root.title("ComplexConstructor")
    root.call('wm','iconphoto',root._w, logo)
    root.configure(background = "#2da6e6")

    def simpleName(inputPath):
        """Returns the last element of a path to display just the input name"""
        justInput=re.search('([^/]+)/?$', inputPath)
        return justInput.group(0)

    def fastaSelection():
        """Opens window with *.fa files in the current directory to select the FASTA file"""
        filetext="Select"
        root.filename =  filedialog.askopenfilename(initialdir = cwd,title = "Select the FASTA file",
                                                    filetypes = (("FASTA files","*.fa"),
                                                                ("all files","*.*")))
        print (root.filename)
        bF["text"]= simpleName(root.filename) if root.filename else filetext
        return root.filename

    def pdbSelection():
        """Opens window with directories present in the current folder to select the the one
        with the pair interactions in PDB"""
        filetext="Select"
        root.directory = filedialog.askdirectory(title = "Select the directory with PDB files")
        print (root.directory)
        bP["text"]= simpleName(root.directory) if root.directory else filetext
        return root.directory

    def oSelection():
        """Stores the name introduced for the output file """
        filetext="Confirm"
        print (outputName.get())
        bO["text"]= simpleName(outputName.get()) if outputName.get() else filetext
        return outputName.get()

    def stSelection():
        """Opens window with files in the current directory to select the the stoichiometry file"""
        filetext="Select"
        root.filenameSt =  filedialog.askopenfilename(initialdir = cwd,title = "Select the stoichiometry file",
                                                    filetypes = (("Text files","*.txt"),
                                                                ("all files","*.*")))
        print (root.filenameSt)
        frameSt.pack(pady="15", padx="50",anchor=W, fill=X, expand=YES)
        bSt["text"]= simpleName(root.filenameSt) if root.filenameSt else filetext
        labelO["text"]="Output directory name:                       "
        labelSt.lift()
        labelSt.pack(side=LEFT )
        bSt.lift()
        bSt.pack()
        return root.filenameSt

    def checkVerbose():
        """Returns TRUE if the log checkbox if checked"""
        return verb.get()

    def showHelp():
        """Displays help of the ComplexConstructor in a new window"""
        t = Toplevel(root)
        t.wm_title("Help")
        l = Label(t, text=helpText.helpMessage,justify=LEFT)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def openTutorial():
        """Displays README file from gitHub"""
        webbrowser.open_new("https://github.com/Argonvi/SBI-PYT_Project/blob/master/README.md")

    def runCB():
        """Checks that all the mandatory inputs are defined and run the program"""
        if outputName.get()!='':
            try:
                print(root.filename)
                print(root.directory )
                root.destroy()
            except:
                messagebox.showerror("Ups!", "You should select the input FASTA file and the directory with the PDB interaction files.")

        else:
            messagebox.showerror("Ups!", "You should specify and confirm the name of the directory where the output files will be stored.")


    # Setting of the topmenu
    menubar = Menu(root, tearoff=0)
    filemenu = Menu(menubar)

    filemenu.add_command(label="Add stoichiometry", command=stSelection)
    #filemenu.add_command(label="Energy analysis", command=menu_action)
    #filemenu.add_command(label="Open log file", command=menu_action)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=root.quit)

    helpmenu = Menu(menubar)
    helpmenu.add_command(label="Help", command=showHelp)
    helpmenu.add_separator()
    helpmenu.add_command(label="About", command=openTutorial)

    menubar.add_cascade(label="Options", menu=filemenu)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)


    #Console frame
    frame = Frame(root)
    frame.pack(pady="10", padx="10")

    frameWll = Frame(frame)
    frameWll.pack(pady="10")

    #Initial text
    panel = Label(frameWll, image = logo_sm)
    panel.pack(side=LEFT, padx="9")
    wellcome = Label(frameWll, text="Introduce the FASTA file and the directory with the interactions in PDB:    ")
    wellcome.pack(side=TOP,pady="10")


    # FASTA widget
    frameFA = Frame(frame)
    frameFA.pack(pady="15", padx="50",side=TOP,anchor=W, fill=X, expand=YES)
    labelF = Label(frameFA, text="Sequence file:                                          ")
    labelF.pack( side=LEFT )
    bF = Button(frameFA, text="Select", command=fastaSelection) #Button FASTA file
    bF.pack( )


    #PDB widget
    framePDB = Frame(frame)
    framePDB.pack(pady="15", padx="50",anchor=W, fill=X, expand=YES)
    labelF = Label(framePDB, text="Interactions directory:                             ")
    labelF.pack( side=LEFT )
    bP = Button(framePDB, text="Select", command=pdbSelection)  #Button PDB dir
    bP.pack( )


    #Output widget
    frameO = Frame(frame)
    frameO.pack(pady="15", padx="50",anchor=W, fill=X, expand=YES)
    labelO = Label(frameO, text="Output directory name:    ")
    labelO.pack( side=LEFT )
    outputName = StringVar()  #textBox for output folder
    nameEntered = Entry(frameO, width = 15, textvariable = outputName)
    nameEntered.pack(side=LEFT, padx="5")
    bO = Button(frameO, text = "Confirm", command = oSelection)
    bO.pack(side=LEFT)


    #Verbose widget
    frameV = Frame(frame)
    frameV.pack(pady="15", padx="50",side=LEFT,anchor=W, fill=X, expand=YES)
    labelF = Label(frameV, text="Do you want to create a log file?")
    labelF.pack( side=LEFT )
    verb = BooleanVar()  #Checkbox verbose
    cV = Checkbutton(frameV, text="I do!", variable=verb, command=checkVerbose)
    cV.pack()

    #Stoichiometry widget
    frameSt = Frame(frame)
    frameSt.pack_forget()
    labelSt = Label(frameSt, text="Define a stoichiometry:  ")
    labelSt.lower()
    bSt = Button(frameSt, text = "Select", command = stSelection)
    bSt.lower()


    #Submit widget
    bEnter = Button(root, text="Build complex", command=runCB, bd="2",
                     relief="solid",padx="10", pady="10") #fg="red", bg="blue",
    bEnter.pack( side=BOTTOM ,pady="5")
    root.mainloop()


    #Parse inputs
    inputs=[]
    inputs.append(root.filename) # FASTA
    inputs.append(root.directory) # PDB dir
    inputs.append(checkVerbose()) # verbose T/F
    try: # stoichiometry None/file
        inputs.append( root.filenameSt)
    except:
        inputs.append(None)
    inputs.append(outputName.get()) #Output folder
    print(inputs)
    return inputs
