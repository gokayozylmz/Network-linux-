#!/usr/bin/env python3
"""
Local VTT Transcript Processor
Processes local VTT files and creates clean, timestamped transcripts.
This version works with local files when YouTube access is restricted.
"""

import os
import re
import html
import glob
import sys
from typing import Optional


def clean_transcript_with_timestamps(vtt_file: str = None) -> Optional[str]:
    """
    Clean VTT file and create timestamped transcript.
    
    Args:
        vtt_file: Path to VTT file. If None, searches for VTT files in current directory
    
    Returns:
        Cleaned transcript text or None if no VTT file found
    """
    if vtt_file:
        vtt_files = [vtt_file] if os.path.exists(vtt_file) else []
    else:
        vtt_files = glob.glob("*.vtt")
    
    if not vtt_files:
        print("❌ VTT dosyası bulunamadı.")
        return None

    file = vtt_files[0]
    print(f"✅ VTT dosyası bulundu: {file}")

    transcript = []
    last_entry = ""
    current_time = ""

    try:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # Skip WEBVTT header
                if line.startswith("WEBVTT"):
                    continue

                # Extract timestamp
                if "-->" in line:
                    current_time = line.replace(".", ",")  # More compatible time format
                    continue

                # Skip empty lines and line numbers
                if not line or line.isdigit():
                    continue

                # Clean HTML tags and decode entities
                text = re.sub(r"<.*?>", "", line)
                text = html.unescape(text)
                text = re.sub(r"^>>\s*", "", text)  # Remove speaker indicators

                # Add timestamped entry
                if current_time and text:
                    entry = f"[{current_time}] {text}"
                    if entry != last_entry:  # Avoid duplicates
                        transcript.append(entry)
                        last_entry = entry
                    current_time = ""

        # Save to file
        output_file = "timestamped_transcript.txt"
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("\n".join(transcript))

        print(f"💾 '{output_file}' dosyasına kaydedildi.")
        return "\n".join(transcript)
    
    except Exception as e:
        print(f"❌ Transkript işleme hatası: {e}")
        return None


def process_transcript(vtt_file: str = None) -> None:
    """
    Process VTT file and display results.
    
    Args:
        vtt_file: Path to VTT file. If None, searches for VTT files in current directory
    """
    print("🔄 VTT dosyası işleniyor...")
    print("-" * 50)
    
    result = clean_transcript_with_timestamps(vtt_file)
    
    if result:
        print("\n🕒 Transkript (zamanlı ve temiz):\n")
        print(result)
        print(f"\n📊 Toplam karakter sayısı: {len(result)}")
        print("📁 Tam transkript 'timestamped_transcript.txt' dosyasında.")
    else:
        print("❌ Transkript oluşturulamadı.")


def main():
    """Main function for command line usage."""
    if len(sys.argv) > 1:
        vtt_file = sys.argv[1]
        if not os.path.exists(vtt_file):
            print(f"❌ Dosya bulunamadı: {vtt_file}")
            sys.exit(1)
        process_transcript(vtt_file)
    else:
        print("Kullanım:")
        print("  python local_transcript_processor.py <vtt_file>")
        print("  python local_transcript_processor.py  # (mevcut dizindeki VTT dosyalarını arar)")
        print()
        print("📁 Mevcut dizinde VTT dosyası aranıyor...")
        process_transcript()


if __name__ == "__main__":
    print("🚀 Yerel VTT Transkript İşleyici")
    print("=" * 50)
    main()