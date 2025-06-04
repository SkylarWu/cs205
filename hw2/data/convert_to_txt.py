import pandas as pd

def convert_transfusion_csv(input_file, output_file):
    df = pd.read_csv(input_file)

    label_col = df.columns[-1]
    feature_cols = df.columns[:-1]

    with open(output_file, 'w') as f:
        for _, row in df.iterrows():
            label = int(row[label_col])
            features = row[feature_cols].tolist()
            f.write(f"{label} {' '.join(str(x) for x in features)}\n")

if __name__ == '__main__':
    convert_transfusion_csv('transfusion.data', 'transfusion_formatted.txt')
