#!/usr/bin/env python3
"""
YouTube Transcript Extractor with Timestamps
Extracts subtitles from YouTube videos and creates clean, timestamped transcripts.
"""

import os
import re
import html
import glob
import sys
from typing import Optional

try:
    from yt_dlp import YoutubeDL
except ImportError:
    print("❌ yt-dlp not found. Installing...")
    os.system("pip install --break-system-packages -q yt-dlp")
    from yt_dlp import YoutubeDL


def download_subs(youtube_url: str, lang: str = "en", use_cookies: bool = False) -> None:
    """
    Download subtitles from YouTube video.
    
    Args:
        youtube_url: YouTube video URL
        lang: Language code for subtitles (default: "en")
        use_cookies: Whether to try using browser cookies for authentication
    """
    # Clean up any existing VTT files
    for f in glob.glob("*.vtt"):
        os.remove(f)
    
    print("🔽 Altyazı indiriliyor...")
    
    ydl_opts = {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": [lang],
        "skip_download": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        # Add user agent to avoid bot detection
        "http_headers": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
    
    # Try with cookies if requested
    if use_cookies:
        ydl_opts["cookiesfrombrowser"] = ("chrome",)
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        error_msg = str(e)
        if "Sign in to confirm" in error_msg or "bot" in error_msg:
            print("⚠️  YouTube bot koruması aktif. Farklı bir video deneyin veya cookies kullanın.")
            print("💡 Çözüm önerileri:")
            print("   1. Daha popüler/eski bir video deneyin")
            print("   2. --cookies parametresi ile browser cookies kullanın")
            print("   3. Farklı bir IP adresinden deneyin")
        else:
            print(f"❌ Altyazı indirme hatası: {error_msg}")
        sys.exit(1)


def clean_transcript_with_timestamps() -> Optional[str]:
    """
    Clean VTT file and create timestamped transcript.
    
    Returns:
        Cleaned transcript text or None if no VTT file found
    """
    vtt_files = glob.glob("*.vtt")
    if not vtt_files:
        print("❌ Altyazı bulunamadı.")
        return None

    file = vtt_files[0]
    print(f"✅ Altyazı bulundu: {file}")

    transcript = []
    last_entry = ""
    current_time = ""

    try:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

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


def generate_transcript_with_time(youtube_url: str, lang: str = "en", use_cookies: bool = False) -> None:
    """
    Complete process: download subtitles and generate timestamped transcript.
    
    Args:
        youtube_url: YouTube video URL
        lang: Language code for subtitles (default: "en")
        use_cookies: Whether to try using browser cookies for authentication
    """
    print(f"🎬 Video URL: {youtube_url}")
    print(f"🌐 Dil: {lang}")
    print("-" * 50)
    
    download_subs(youtube_url, lang, use_cookies)
    result = clean_transcript_with_timestamps()
    
    if result:
        print("\n🕒 Transkript (zamanlı ve temiz):\n")
        print(result[:1000] + "..." if len(result) > 1000 else result)
        print(f"\n📊 Toplam karakter sayısı: {len(result)}")
        print("📁 Tam transkript 'timestamped_transcript.txt' dosyasında.")
    else:
        print("❌ Transkript oluşturulamadı.")


def test_with_alternative_videos():
    """Test with some alternative videos that might not require authentication."""
    test_videos = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll - classic, older video
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Despacito - very popular
        "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",  # Bohemian Rhapsody - Queen
    ]
    
    print("🔄 Bot koruması nedeniyle alternatif videolar deneniyor...")
    
    for i, url in enumerate(test_videos, 1):
        print(f"\n📹 Test video {i}: {url}")
        try:
            generate_transcript_with_time(url)
            print("✅ Bu video ile başarılı!")
            return True
        except SystemExit:
            print(f"❌ Video {i} başarısız, bir sonrakini deniyoruz...")
            continue
    
    print("😞 Hiçbir test videosu çalışmadı. Manuel olarak farklı bir URL deneyin.")
    return False


def main():
    """Main function for command line usage."""
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  python youtube_transcript_extractor.py <YouTube_URL>")
        print("  python youtube_transcript_extractor.py <YouTube_URL> --cookies")
        print("  python youtube_transcript_extractor.py --test")
        print()
        print("Örnekler:")
        print("  python youtube_transcript_extractor.py 'https://www.youtube.com/watch?v=VIDEO_ID'")
        print("  python youtube_transcript_extractor.py 'https://www.youtube.com/watch?v=VIDEO_ID' --cookies")
        sys.exit(1)
    
    if sys.argv[1] == "--test":
        test_with_alternative_videos()
        return
    
    youtube_url = sys.argv[1]
    use_cookies = "--cookies" in sys.argv
    
    generate_transcript_with_time(youtube_url, use_cookies=use_cookies)


if __name__ == "__main__":
    print("🚀 YouTube Transkript Çıkarıcı")
    print("=" * 50)
    
    # You can either run with command line argument or use the example URL
    if len(sys.argv) > 1:
        main()
    else:
        print("⚠️  Orijinal video bot koruması nedeniyle erişilemiyor.")
        print("🔄 Alternatif videolar deneniyor...\n")
        success = test_with_alternative_videos()
        if not success:
            print("\n💡 Manuel kullanım:")
            print("python youtube_transcript_extractor.py '<YouTube_URL>'")
            print("python youtube_transcript_extractor.py '<YouTube_URL>' --cookies")