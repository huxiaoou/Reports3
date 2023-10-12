from skyrim.whiterun import CCalendar


def update_sig_date(exe_date: str, calendar_path: str):
    calendar = CCalendar(calendar_path)
    sig_date = calendar.get_next_date(exe_date, -1)
    with open("set_sig_exe_date.tex", "w+") as f:
        f.write("\\newcommand{{\exeYear}}{{{0}}}\n".format(exe_date[0:4]))
        f.write("\\newcommand{{\exeDate}}{{{0}}}\n".format(exe_date))
        f.write("\\newcommand{{\sigYear}}{{{0}}}\n".format(sig_date[0:4]))
        f.write("\\newcommand{{\sigDate}}{{{0}}}\n".format(sig_date))
        f.write("\\newcommand{{\displayDate}}{{{0}}}\n".format(exe_date[0:4] + "-" + exe_date[4:6] + "-" + exe_date[6:8]))
    return 0


if __name__ == "__main__":
    import sys
    calendar_path = r"E:\Deploy\Data\Calendar\cne_calendar.csv"
    update_sig_date(sys.argv[1], calendar_path)
