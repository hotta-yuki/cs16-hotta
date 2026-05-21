import matplotlib.pyplot as plt
import numpy as np
import japanize_matplotlib
import os

def verify_matplotlib():
    print("--- Matplotlib Environment Verification ---")
    
    # 1. Create sample data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # 2. Setup Plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='正弦波 (Sine Wave)', color='tab:blue', linewidth=2)
    plt.scatter(x[::10], y[::10], color='tab:red', label='観測点 (Data Points)')
    
    # 3. Apply Styling
    plt.title('Matplotlib 環境構築確認 (Verification Plot)', fontsize=16)
    plt.xlabel('時間 (Time) [s]', fontsize=12)
    plt.ylabel('振幅 (Amplitude)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # 4. Save
    output_dir = 'tmp_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'matplotlib_verification.png')
    plt.savefig(output_path)
    print(f"Success: Plot saved to {output_path}")
    
    # 5. Show (if in interactive environment)
    # plt.show()

if __name__ == "__main__":
    verify_matplotlib()
