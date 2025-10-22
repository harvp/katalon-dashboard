import os
import xml.etree.ElementTree as ET
import pandas as pd


def parse_junit_xml(file_path: str) -> list[dict]:
    """
    Parses a single Katalon JUnit XML file and extracts suite/test data.
    Returns a list of dictionaries (rows).
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"⚠️  Could not parse {file_path}: {e}")
        return []

    rows = []
    for suite in root.findall("testsuite"):
        suite_name = suite.get("name")
        suite_time = suite.get("time")
        suite_timestamp = suite.get("timestamp")

        for case in suite.findall("testcase"):
            test_name = case.get("name").split("/")[-1]
            status = case.get("status", "UNKNOWN")
            time = float(case.get("time", 0))
            system_err = (case.find("system-err").text or "").strip() if case.find("system-err") is not None else ""
            system_out = (case.find("system-out").text or "").strip() if case.find("system-out") is not None else ""

            rows.append({
                "Date": suite_timestamp.split("T")[0] if suite_timestamp else "",
                "Suite": suite_name,
                "Test Case": test_name,
                "Status": status,
                "Duration (s)": round(time, 2),
                "Error Message": system_err or ("Failed" if status == "FAILED" else ""),
                "Details": system_out[:300],  # truncate long logs for readability
                "File": file_path
            })
    return rows


def parse_folder(root_folder: str) -> pd.DataFrame:
    """
    Walks through all subfolders of root_folder, parses JUnit XMLs,
    and returns a DataFrame with aggregated results.
    """
    all_rows = []
    for dirpath, _, filenames in os.walk(root_folder):
        for file in filenames:
            if file.endswith(".xml") and "JUnit_Report" in file:
                file_path = os.path.join(dirpath, file)
                print(f"📄 Parsing: {file_path}")
                all_rows.extend(parse_junit_xml(file_path))

    df = pd.DataFrame(all_rows)
    return df
