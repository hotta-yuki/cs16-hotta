import os
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

def create_html_animation(input_dir, output_file):
    # Get all png files in the directory
    files = [f for f in os.listdir(input_dir) if f.endswith('.png')]
    
    # Function to extract the width value from the filename
    def extract_width(filename):
        match = re.search(r'width(\d+)', filename)
        return int(match.group(1)) if match else 0

    # Sort files numerically by width
    files.sort(key=extract_width)
    
    if not files:
        print(f"No images found in {input_dir}")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.axis('off')

    # Load first image to get dimensions
    first_img = Image.open(os.path.join(input_dir, files[0]))
    im = ax.imshow(first_img, animated=True)

    def update(frame_file):
        img = Image.open(os.path.join(input_dir, frame_file))
        im.set_array(img)
        return [im]

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=files, interval=200, blit=True)

    # Save as HTML
    html_content = ani.to_jshtml()
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    plt.close()
    print(f"Animation created successfully: {output_file}")

if __name__ == "__main__":
    # FFT Animation
    fft_input_directory = r'tmp_output\plots_simulation_fft'
    fft_output_html_path = r'tmp_output\simulation_fft_animation.html'
    create_html_animation(fft_input_directory, fft_output_html_path)

    # Waveform Animation
    wave_input_directory = r'tmp_output\plots_simulation_waveform'
    wave_output_html_path = r'tmp_output\simulation_waveform_animation.html'
    create_html_animation(wave_input_directory, wave_output_html_path)
