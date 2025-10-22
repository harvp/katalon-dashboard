from src.parser.parse_junit import parse_folder
import os

if __name__ == "__main__":
    raw_path = os.path.join("data", "raw_reports")
    output_path = os.path.join("data", "processed", "katalon_results.csv")

    print(f"🚀 Parsing XML reports from: {raw_path}")
    df = parse_folder(raw_path)

    if not df.empty:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ Saved parsed results to {output_path}")
        print(df.head())
    else:
        print("⚠️ No XML reports found or parsed.")
