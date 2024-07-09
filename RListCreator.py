import pandas as pd
import os
import re


def format_utc_offset(offset):
    offset = int(offset)
    return f"{offset:+03}:00"


def process_csv(file_path, group_no, group_name, utc_offset, name_choice):
    df = pd.read_csv(file_path)

    # Identify the column that matches the pattern for 'Output Freq'
    output_freq_col = [col for col in df.columns if re.match(r'^\d+Output Freq$', col)][0]

    df['Mode'] = df['Mode'].str.strip()
    df.loc[df['Mode'].str.contains('analog', case=False), 'Mode'] = 'analog'

    df = df[df['Mode'].isin(['analog', 'DSTR'])]

    if name_choice == 'Location':
        df['Name'] = df['Location']
    else:
        df['Name'] = df[output_freq_col]

    df['Dup'] = df['Offset'].apply(lambda x: 'DUP-' if x == '-' else 'DUP+')

    df['Offset'] = (df[output_freq_col] - df['Input Freq']).abs().round(1)

    # Determine TONE and Repeater Tone
    def determine_tone(row):
        if pd.notnull(row['Tone']) and pd.isnull(row['TSQ']):
            tone = f"{row['Tone']}"
            if '.' not in tone:
                tone += '.0'
            return 'Tone', f"{tone}Hz"
        elif pd.notnull(row['Tone']) and pd.notnull(row['TSQ']):
            tsq = f"{row['TSQ']}"
            if '.' not in tsq:
                tsq += '.0'
            return 'TSQL', f"{tsq}Hz"
        elif row['Mode'] == 'DSTR':
            return 'OFF', '82.5Hz'
        else:
            return '', ''

    df[['TONE', 'Repeater Tone']] = df.apply(determine_tone, axis=1, result_type="expand")

    # Determine Repeater Call and Gateway Call
    def determine_callsign(row):
        if row['Mode'] == 'analog':
            return row['Call'], ''
        else:
            band = float(row[output_freq_col])
            padded_call = row['Call'].ljust(7)
            if 144 <= band <= 148:
                return f"{padded_call}C", f"{padded_call}G"
            elif 420 <= band <= 450:
                return f"{padded_call}B", f"{padded_call}G"
            else:
                return row['Call'], f"{padded_call}G"

    df[['Repeater Call', 'Gateway Call']] = df.apply(determine_callsign, axis=1, result_type="expand")

    df['Mode'] = df['Mode'].apply(lambda x: 'FM' if x == 'analog' else 'DV')

    final_df = pd.DataFrame({
        'Group No': group_no,
        'Group Name': group_name,
        'Name': df['Name'],
        'Sub Name': '',
        'Repeater Call Sign': df['Repeater Call'],
        'Gateway Call Sign': df['Gateway Call'],
        'Frequency': df[output_freq_col],
        'Dup': df['Dup'],
        'Offset': df['Offset'],
        'Mode': df['Mode'],
        'TONE': df['TONE'],
        'Repeater Tone': df['Repeater Tone'],
        'RPT1USE': 'Yes',
        'Position': 'Approximate',
        'Latitude': df['lat'],
        'Longitude': df['long'],
        'UTC Offset': format_utc_offset(utc_offset)
    })

    return final_df


def main():
    input_dir = input("Please enter the path to the directory containing the CSV files: ").strip()
    output_filename = input("Please enter the output repeater list filename: ").strip()

    if '.' in output_filename and not output_filename.endswith('.csv'):
        print("Error: Filename entry must either have no extension or end with '.csv'.")
        return

    if not output_filename.endswith('.csv'):
        output_filename += '.csv'
    output_file = output_filename

    if not os.path.isdir(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist.")
        return

    all_dfs = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            print(f"\nProcessing file: {filename}")

            group_no = input(f"Enter group number for {filename}: ").strip()
            group_name = input(f"Enter group name for {filename}: ").strip()
            utc_offset = input(f"Enter UTC offset for {filename} (e.g., -6): ").strip()

            df = pd.read_csv(file_path)
            print(f"\nFirst few values from Location column of {filename}:")
            print(df['Location'].head())

            # Identify the column that matches the pattern for 'Output Freq'
            output_freq_col = [col for col in df.columns if re.match(r'^\d+Output Freq$', col)][0]
            print(f"\nFirst few values from {output_freq_col} column of {filename}:")
            print(df[output_freq_col].head())

            while True:
                name_choice = input(
                    f"Enter column to use for Name (Location or {output_freq_col}) for {filename}: ").strip()
                if name_choice in ['Location', output_freq_col]:
                    break
                else:
                    print(f"Invalid choice. Please enter 'Location' or '{output_freq_col}'.")

            processed_df = process_csv(file_path, group_no, group_name, utc_offset, name_choice)
            all_dfs.append(processed_df)

    final_df = pd.concat(all_dfs, ignore_index=True).sort_values(by=['Group No', 'Frequency'])

    # Save to CSV
    final_df.to_csv(output_file, index=False)
    print(f"\nOutput CSV saved to {output_file}")


if __name__ == "__main__":
    main()
