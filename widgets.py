import WindPy as wapi
import json
from skyrim.whiterun import CCalendar, SetFontYellow, SetFontGreen

def expand_date(d:str):
    return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"


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
    exe_date_L10 = expand_date(exe_date)
    # w.wsd("NH0100.NHF", "pct_chg", "2023-10-20", "2023-10-20", "")
    benchmark_ret = wapi.w.wsd(benchmark_id, "pct_chg", exe_date_L10, exe_date_L10, "").Data[0][0]
    with open("paragraph_benchmark_ret.tex", "w+", encoding="utf-8") as f:
        f.write(f"{exe_date_L10}日，{benchmark_chs_name}当日收益率{benchmark_ret:.4}\%。")
    return 0

def update_premium(sim_date:str, calendar_path:str, premium_path:str, strategy_id:str):
    def __get_premium(trade_date: str) -> float:
        for k, v in config_sig["premium"].items():
            if trade_date >= k:
                return v
        print(f"{SetFontYellow('Warning')}! No premium is found for {SetFontGreen(trade_date)}")
        return 0.0

    with open(premium_path, "r") as f:
        contents = f.read()
    config_strategy = json.loads(contents)
    config_sig = config_strategy[strategy_id]
    print(config_sig)

    calendar = CCalendar(calendar_path)
    exe_date = calendar.get_next_date(sim_date, -1)
    sig_date = calendar.get_next_date(sim_date, -2)
    premium = __get_premium(sig_date)

    sim_date_L10, exe_date_L10 = expand_date(sim_date), expand_date(exe_date)
    with open("paragraph_premium.tex", "w+", encoding="utf-8") as f:
        f.write(f"报告日{sim_date_L10}，当日头寸的建仓日为{exe_date_L10}，建仓市值{premium/1e4:.2f}万元。")
    return 0


if __name__ == "__main__":
    import sys

    wapi.w.start()

    calendar_path = r"E:\Deploy\Data\Calendar\cne_calendar.csv"
    config_strategy_path = r"E:\Deploy\Projects\Trade3\config_strategy.json"

    exe_date = sys.argv[1]
    benchmark_id, benchmark_chs_name = "NH0100.NHF", "南华商品指数"
    update_sig_date(exe_date, calendar_path)
    update_benchmark_return(exe_date, benchmark_id, benchmark_chs_name)
    update_premium(exe_date, calendar_path, config_strategy_path, strategy_id="SND")
