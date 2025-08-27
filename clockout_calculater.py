import time

def parse_time(clock_in_str):
    """Parses input like '08:12' or '0812' into hours and minutes."""
    if ":" in clock_in_str:
        h, m = map(int, clock_in_str.split(":"))
    else:
        # Assume last two digits are minutes
        clock_in_str = clock_in_str.zfill(4)  # e.g., "812" -> "0812"
        h, m = int(clock_in_str[:-2]), int(clock_in_str[-2:])
    return h, m

def main():
    # Ask user for clock-in time
    clock_in_str = input("Clock-in time: ")
    h, m = parse_time(clock_in_str)
    clock_in_minutes = h * 60 + m

    # Work duration in minutes (7.7 hours = 462 minutes)
    work_duration = 7 * 60 + 42

    # If continuous work >= 6 hours, subtract 30 min
    if work_duration > 6 * 60:
        work_duration -= 30

    # Clock-out time in minutes
    clock_out_minutes = clock_in_minutes + work_duration

    # Convert back to HH:MM
    out_h = (clock_out_minutes // 60) % 24
    out_m = clock_out_minutes % 60

    print(f"Clock out time: {out_h:02d}:{out_m:02d}")

    # --- Check overtime ---
    # Current time in minutes since midnight
    now = time.localtime()
    now_minutes = now.tm_hour * 60 + now.tm_min08

    if now_minutes > clock_out_minutes:
        overtime = now_minutes - clock_out_minutes
        oh, om = divmod(overtime, 60)
        #om = om / 60
        print(f"⚠️ You are already overworking by {oh}h {om}m.")
    else:
        remaining = clock_out_minutes - now_minutes
        rh, rm = divmod(remaining, 60)
        print(f"⏳ Remaining work time: {rh}h {rm}m.")

if __name__ == "__main__":
    main()
