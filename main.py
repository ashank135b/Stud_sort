import tkinter as tk
from tkinter.font import Font
import pickle

"""Student Class"""


class Student:
    def __init__(self, first_name, last_name, roll_number, rank):
        self.first_name = first_name
        self.last_name = last_name
        self.roll_number = roll_number
        self.rank = rank


"""Object of this class is responsible for changing frames in our App"""


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    """Destroys current frame and replaces it with a new one."""

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


"""Object of this class changes the frame to home window"""


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("App")
        self.master.geometry('250x190')

        myfont = Font(family="Times", size=10)

        """Creating labels, entries and buttons"""

        roll_number = tk.Label(self, text="Roll Number:", font=myfont)
        entry_roll_number = tk.Entry(self, font=myfont)
        name = tk.Label(self, text="Name:", font=myfont)
        entry_name = tk.Entry(self, font=myfont)
        rank = tk.Label(self, text="Rank:", font=myfont)
        entry_rank = tk.Entry(self, font=myfont)

        """On clicking view_button changes the window to PageTwo where all the data is displayed"""

        view_button = tk.Button(self, text="View all data", font=myfont,
                                command=lambda: master.switch_frame(PageTwo))

        """On clicking submit_button calls the function submit and gives it the values of all the entries"""

        submit_button = tk.Button(self, text="Submit", font=myfont,
                                  command=lambda: self.submit(entry_roll_number.get(), entry_name.get(),
                                                              entry_rank.get(), master))

        """Packing all the labels, entries and buttons"""

        roll_number.pack(side="top", fill="x")
        entry_roll_number.pack(side="top", fill="x")
        name.pack(side="top", fill="x")
        entry_name.pack(side="top", fill="x")
        rank.pack(side="top", fill="x")
        entry_rank.pack(side="top", fill="x")
        view_button.pack(side="top", fill="x")
        submit_button.pack(side="top", fill="x")

    """
    This function checks if the values of all the entries are filled.
    If not then displays the error message otherwise changes the frame to PageOne
    """

    def submit(self, roll_number, name, rank, master):

        """Adding new student to the file if non of the fields are empty and are appropriate"""

        if roll_number != "" and name != "" and rank != "" and roll_number.isalnum() and rank.isdigit() and all(x == " " or x.isalpha() for x in name) and int(rank) > 0:
            try:
                with open("data.txt", "rb") as rfp:
                    data = pickle.load(rfp)
            except EOFError:
                data = []
            if " " not in name:
                first_name = name
                last_name = ""
            else:
                first_name, last_name = name.split(" ")
            new_student = Student(first_name, last_name, roll_number, rank)
            data.append(new_student)

            with open("data.txt", "wb") as wfp:
                pickle.dump(data, wfp)

            master.switch_frame(PageOne)
        else:
            i = tk.Label(self, text='Fields incorrectly filled!!!!')
            i.pack()


"""Object of this class shows the window when data is saved and provides a back button"""


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("App")
        self.master.geometry('250x190')

        myfont = Font(family="Times New Roman", size=10)

        label = tk.Label(self, text="Data Saved!!", font=myfont)
        label.pack(side="bottom", fill="x", pady=10)

        back = tk.Button(self, text="Back", font=myfont,
                         command=lambda: master.switch_frame(StartPage))
        back.pack(side="bottom", fill="x", pady=20)


"""Object of this class shows the window with all the sorted data"""


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("App")
        self.master.geometry('500x500')

        myfont = Font(family="Times New Roman", size=10)

        with open("data.txt", "rb") as rfp:
            data = pickle.load(rfp)

        students = []

        for student in data:
            students.append(student)

        """calling mergesort"""

        self.mergesort(students, 0, len(students) - 1)

        """Displaying the sorted data in tabular form"""

        tk.Label(self, text="Roll Number", borderwidth=2, font=myfont).grid(row=0, column=0)
        tk.Label(self, text="Name", borderwidth=2, font=myfont).grid(row=0, column=1)
        tk.Label(self, text="Rank", borderwidth=2, font=myfont).grid(row=0, column=2)

        for i in range(len(students)):
            name = students[i].first_name + " " + students[i].last_name
            tk.Label(self, font=myfont, text=students[i].roll_number, borderwidth=1).grid(row=i + 1, column=0)
            tk.Label(self, font=myfont, text=name, borderwidth=1).grid(row=i + 1, column=1)
            tk.Label(self, font=myfont, text=students[i].rank, borderwidth=1).grid(row=i + 1, column=2)

        """Back button to go back to initial page"""

        tk.Button(self, text="Back", font=myfont,
                  command=lambda: master.switch_frame(StartPage)).grid(row=len(students) + 2, column=1)

    def merge(self, students, l, mid, r):
        n1 = mid - l + 1
        n2 = r - mid
        left = []
        right = []

        for i in range(0, n1):
            left.append(students[l + i])
        for j in range(0, n2):
            right.append(students[mid + 1 + j])

        i = 0
        j = 0
        k = l

        """
        While merging the lists the list is sorted according to first name then last name then rank and in the end
        according to roll number
        """

        while i < n1 and j < n2:
            if left[i].first_name.lower() == right[j].first_name.lower():
                if left[i].last_name.lower() == right[j].last_name.lower():
                    if int(left[i].rank.lower()) == int(right[j].rank.lower()):
                        if left[i].roll_number.lower() <= right[j].roll_number.lower():
                            students[k] = left[i]
                            i += 1
                        else:
                            students[k] = right[j]
                            j += 1
                    elif int(left[i].rank.lower()) < int(right[j].rank.lower()):
                        students[k] = left[i]
                        i += 1
                    else:
                        students[k] = right[j]
                        j += 1

                elif left[i].last_name.lower() < right[j].last_name.lower():
                    students[k] = left[i]
                    i += 1
                else:
                    students[k] = right[j]
                    j += 1
            elif left[i].first_name.lower() < right[j].first_name.lower():
                students[k] = left[i]
                i += 1
            else:
                students[k] = right[j]
                j += 1
            k += 1

        while i < n1:
            students[k] = left[i]
            i += 1
            k += 1

        while j < n2:
            students[k] = right[j]
            j += 1
            k += 1

    """Function for mergesort"""

    def mergesort(self, students, l, r):
        if l < r:
            mid = (l + (r - 1)) // 2
            self.mergesort(students, l, mid)
            self.mergesort(students, mid + 1, r)
            self.merge(students, l, mid, r)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
