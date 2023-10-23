import WindPy as wapi
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


def update_benchmark_return(exe_date: str, benchmark_id: str, benchmark_chs_name: str):
    exe_date_L10 = f"{exe_date[0:4]}-{exe_date[4:6]}-{exe_date[6:8]}"
    # w.wsd("NH0100.NHF", "pct_chg", "2023-10-20", "2023-10-20", "")
    benchmark_ret = wapi.w.wsd(benchmark_id, "pct_chg", exe_date_L10, exe_date_L10, "").Data[0][0]
    with open("paragraph_benchmark_ret.tex", "w+", encoding="utf-8") as f:
        f.write(f"{exe_date_L10}日，{benchmark_chs_name}当日收益率{benchmark_ret:.4}\%。")


if __name__ == "__main__":
    import sys

    wapi.w.start()

    calendar_path = r"E:\Deploy\Data\Calendar\cne_calendar.csv"
    exe_date = sys.argv[1]
    benchmark_id, benchmark_chs_name = "NH0100.NHF", "南华商品指数"
    update_sig_date(exe_date, calendar_path)
    update_benchmark_return(exe_date, benchmark_id, benchmark_chs_name)
