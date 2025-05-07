import os
import argparse
from pydub import AudioSegment

def trim_trailing_audio(input_dir, output_dir, seconds_to_trim=10):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".wav"):
            audio_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file)

            audio = AudioSegment.from_wav(audio_path)
            duration = len(audio)
            trimmed = audio[:max(0, duration - seconds_to_trim * 1000)]
            trimmed.export(output_path, format="wav")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--trim_secs", type=int, default=10)
    args = parser.parse_args()

    trim_trailing_audio(args.input_dir, args.output_dir, args.trim_secs)
    print(f"Trimmed audio files saved to {args.output_dir}")