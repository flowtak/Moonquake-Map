"""
Fetch and plot Apollo PSE seismic data for a chosen station/year/day, then
rebuild the plot index (plots/plot_dict.json) that index.html reads.

This wraps the existing pse_fetch.py / pse_plot.py functions with a small
CLI so a GitHub Actions workflow (or you, locally) can request a specific
slice of data instead of "fetch literally everything".

Usage:
    python moonquake_fetch_and_plot.py --station s12 --year 1971 --day 100
    python moonquake_fetch_and_plot.py --station s12 --year 1971 --day all
    python moonquake_fetch_and_plot.py --station all --year 1971 --day 100

Any of --station/--year/--day may be omitted or set to "all" to fetch every
available value for that field (be careful: this can mean thousands of
requests and a very long run).
"""
import argparse

import pse_fetch
import pse_plot


def _norm(value):
    if value is None:
        return None
    if str(value).strip().lower() in ("", "all", "none"):
        return None
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--station", default=None, help="e.g. s12 (omit or 'all' for every station)")
    parser.add_argument("--year", default=None, help="e.g. 1971 (omit or 'all' for every year)")
    parser.add_argument("--day", default=None, help="day-of-year 1-366 (omit or 'all' for every day)")
    args = parser.parse_args()

    station = _norm(args.station)
    year = _norm(args.year)
    day = _norm(args.day)

    print(f"Fetching PSE data: station={station or 'all'} year={year or 'all'} day={day or 'all'}")
    pse_fetch.fetch_data(stations=station, years=year, days=day)

    print("Plotting fetched data...")
    pse_plot.plot_data(stations=station, years=year, days=day)

    print("Rebuilding plot dictionary (plots/plot_dict.json)...")
    pse_plot.make_plot_dictionary()

    print("Done.")


if __name__ == "__main__":
    main()
