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

    # Current time in minutes since midnight
    now = time.localtime()
    now_minutes = now.tm_hour * 60 + now.tm_min

    # If time between clock-in and now is more than 6 hours, deduct 30 minutes
    worked_time = now_minutes - clock_in_minutes
    if worked_time > 6 * 60:
        print("More than 6 hours since clock-in: 30 minutes break deducted.")
        work_duration += 30

    # Clock-out time in minutes
    clock_out_minutes = clock_in_minutes + work_duration

    # Convert back to HH:MM
    out_h = (clock_out_minutes // 60) % 24
    out_m = clock_out_minutes % 60

    print(f"Clock out time: {out_h:02d}:{out_m:02d}")

    # --- Check overtime ---
    def to_decimal_hour(h, m):
        return f"{h},{int(m/60*100):02d}"  # e.g., 1h 12m -> 1,20

    if now_minutes > clock_out_minutes:
        overtime = now_minutes - clock_out_minutes
        oh, om = divmod(overtime, 60)
        print(f"⚠️ You are already overworking by {to_decimal_hour(oh, om)} hours.")
    else:
        remaining = clock_out_minutes - now_minutes
        rh, rm = divmod(remaining, 60)
        print(f"⏳ Remaining work time: {to_decimal_hour(rh, rm)} hours.")

if __name__ == "__main__":
    main()
