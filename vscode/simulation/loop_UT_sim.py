import UT_FlawVariation_Sim
import itertools
import os

def load_simdata(file_path):
    """
    simdata.csv からパラメータを読み込む。
    形式:
    f_width
    val1
    val2
    f_pitch
    val1
    ...
    """
    params = {
        'f_width': [],
        'f_pitch': [],
        'f_depth': []
    }
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return params

    current_key = None
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            if line in params:
                current_key = line
            elif current_key:
                try:
                    params[current_key].append(float(line))
                except ValueError:
                    print(f"Warning: Could not parse value '{line}' for {current_key}")
    
    return params

def main():
    csv_path = 'vscode\\simulation\\simdata.csv'
    params = load_simdata(csv_path)
    
    widths = params['f_width']
    pitches = params['f_pitch']
    depths = params['f_depth']
    
    print("Parameters loaded:")
    print(f"  f_width: {widths}")
    print(f"  f_pitch: {pitches}")
    print(f"  f_depth: {depths}")
    
    # 全組み合わせの生成
    combinations = list(itertools.product(widths, pitches, depths))
    total = len(combinations)
    print(f"\nTotal simulations to run: {total}")
    
    for i, (w, p, d) in enumerate(combinations):
        # ファイル名の生成と存在確認
        filename = f"sim_pitch{int(p * 1000000)}_depth{int(d * 1000000)}_width{int(w * 1000000)}.csv"
        check_paths = [
            os.path.join("tmp_output\\sim", filename),
            os.path.join("data_im     ", "simdata_out", filename)
        ]
        
        exists = False
        for path in check_paths:
            if os.path.exists(path):
                print(f"\n[{i+1}/{total}] Skipping: {filename} already exists in {os.path.dirname(path)}")
                exists = True
                break
        
        if exists:
            continue

        print(f"\n[{i+1}/{total}] Starting simulation...")
        UT_FlawVariation_Sim.run_simulation(f_width=w, f_pitch=p, f_depth=d)

if __name__ == "__main__":
    main()
