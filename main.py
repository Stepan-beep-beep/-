import tkinter as tk
from gui import HomeInventoryGUI


def main():

    root = tk.Tk()

    try:
        root.iconbitmap('icon.ico')
    except:
        pass

    app = HomeInventoryGUI(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()