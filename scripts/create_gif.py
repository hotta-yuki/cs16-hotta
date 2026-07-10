import os
import re
from PIL import Image

def create_gif(input_dir, output_file, duration=200):
    # Get all png files in the directory
    files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    
    # Function to extract the width value from the filename
    def extract_width(filename):
        match = re.search(r'width(\d+)', filename)
        return int(match.group(1)) if match else 0

    # Sort files numerically by width
    files.sort(key=extract_width)
    
    # Load images
    images = []
    for filename in files:
        file_path = os.path.join(input_dir, filename)
        img = Image.open(file_path)
        images.append(img)
    
    if not images:
        print("No images found to create GIF.")
        return

    # Save as GIF
    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    print(f"GIF created successfully: {output_file}")

if __name__ == "__main__":
    # FFT GIF
    fft_input_directory = r'tmp_output\plots_simulation_fft'
    fft_output_gif_path = r'tmp_output\sim_fft.gif'
    create_gif(fft_input_directory, fft_output_gif_path)

    # Waveform GIF
    wave_input_directory = r'tmp_output\plots_simulation_waveform'
    wave_output_gif_path = r'tmp_output\sim_wave.gif'
    create_gif(wave_input_directory, wave_output_gif_path)
