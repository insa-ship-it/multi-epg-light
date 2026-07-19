import os
import gzip
import re
import xml.etree.ElementTree as ET
import requests

# Settings
NAME = "light"
# Get URL from GitHub Secret
M3U_URL = os.getenv("M3U_URL")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "epgs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# We only define the .gz path to stay under GitHub's 100MB limit
OUTPUT_FILE_GZ = os.path.join(OUTPUT_DIR, f"{NAME}-epg.xml.gz")

URLS = [
    'https://epgshare01.online/epgshare01/epg_ripper_US2.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_CA2.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_UK1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_MX1.xml.gz', 
    'https://epgshare01.online/epgshare01/epg_ripper_ZA1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_SV1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_US_SPORTS1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_FANDUEL1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_TBNPLUS1.xml.gz', 
    'https://epgshare01.online/epgshare01/epg_ripper_WHALETVPLUS1.xml.gz', 
    'https://epgshare01.online/epgshare01/epg_ripper_DUMMY_CHANNELS.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_DISTROTV1.xml.gz', 
    'https://iptv-epg.org/files/epg-al.xml.gz', 
    'https://iptv-epg.org/files/epg-ar.xml.gz', 
    'https://iptv-epg.org/files/epg-am.xml.gz', 
    'https://iptv-epg.org/files/epg-au.xml.gz', 
    'https://iptv-epg.org/files/epg-at.xml.gz', 
    'https://iptv-epg.org/files/epg-bs.xml.gz', 
    'https://iptv-epg.org/files/epg-by.xml.gz', 
    'https://iptv-epg.org/files/epg-be.xml.gz', 
    'https://iptv-epg.org/files/epg-bo.xml.gz', 
    'https://iptv-epg.org/files/epg-ba.xml.gz', 
    'https://iptv-epg.org/files/epg-br.xml.gz', 
    'https://iptv-epg.org/files/epg-bg.xml.gz', 
    'https://iptv-epg.org/files/epg-ca.xml.gz', 
    'https://iptv-epg.org/files/epg-cl.xml.gz', 
    'https://iptv-epg.org/files/epg-co.xml.gz', 
    'https://iptv-epg.org/files/epg-cr.xml.gz', 
    'https://iptv-epg.org/files/epg-hr.xml.gz', 
    'https://iptv-epg.org/files/epg-cw.xml.gz', 
    'https://iptv-epg.org/files/epg-cz.xml.gz', 
    'https://iptv-epg.org/files/epg-dk.xml.gz', 
    'https://iptv-epg.org/files/epg-do.xml.gz', 
    'https://iptv-epg.org/files/epg-eg.xml.gz', 
    'https://iptv-epg.org/files/epg-sv.xml.gz', 
    'https://iptv-epg.org/files/epg-fi.xml.gz', 
    'https://iptv-epg.org/files/epg-fr.xml.gz', 
    'https://iptv-epg.org/files/epg-ge.xml.gz',
    'https://iptv-epg.org/files/epg-de.xml.gz', 
    'https://iptv-epg.org/files/epg-gh.xml.gz', 
    'https://iptv-epg.org/files/epg-gr.xml.gz', 
    'https://iptv-epg.org/files/epg-gt.xml.gz', 
    'https://iptv-epg.org/files/epg-hn.xml.gz', 
    'https://iptv-epg.org/files/epg-hk.xml.gz', 
    'https://iptv-epg.org/files/epg-hu.xml.gz', 
    'https://iptv-epg.org/files/epg-is.xml.gz', 
    'https://iptv-epg.org/files/epg-in.xml.gz', 
    'https://iptv-epg.org/files/epg-id.xml.gz', 
    'https://iptv-epg.org/files/epg-il.xml.gz', 
    'https://iptv-epg.org/files/epg-it.xml.gz', 
    'https://iptv-epg.org/files/epg-jm.xml.gz', 
    'https://iptv-epg.org/files/epg-lb.xml.gz', 
    'https://iptv-epg.org/files/epg-lt.xml.gz', 
    'https://iptv-epg.org/files/epg-lu.xml.gz', 
    'https://iptv-epg.org/files/epg-mk.xml.gz', 
    'https://iptv-epg.org/files/epg-my.xml.gz', 
    'https://iptv-epg.org/files/epg-mt.xml.gz', 
    'https://iptv-epg.org/files/epg-mx.xml.gz', 
    'https://iptv-epg.org/files/epg-me.xml.gz', 
    'https://iptv-epg.org/files/epg-nl.xml.gz', 
    'https://iptv-epg.org/files/epg-nz.xml.gz', 
    'https://iptv-epg.org/files/epg-ni.xml.gz', 
    'https://iptv-epg.org/files/epg-ng.xml.gz', 
    'https://iptv-epg.org/files/epg-no.xml.gz', 
    'https://iptv-epg.org/files/epg-pa.xml.gz', 
    'https://iptv-epg.org/files/epg-py.xml.gz', 
    'https://iptv-epg.org/files/epg-pe.xml.gz', 
    'https://iptv-epg.org/files/epg-ph.xml.gz', 
    'https://iptv-epg.org/files/epg-pl.xml.gz', 
    'https://iptv-epg.org/files/epg-pt.xml.gz', 
    'https://iptv-epg.org/files/epg-ro.xml.gz', 
    'https://iptv-epg.org/files/epg-ru.xml.gz', 
    'https://iptv-epg.org/files/epg-rs.xml.gz', 
    'https://iptv-epg.org/files/epg-sg.xml.gz', 
    'https://iptv-epg.org/files/epg-si.xml.gz', 
    'https://iptv-epg.org/files/epg-za.xml.gz', 
    'https://iptv-epg.org/files/epg-kr.xml.gz', 
    'https://iptv-epg.org/files/epg-es.xml.gz', 
    'https://iptv-epg.org/files/epg-se.xml.gz', 
    'https://iptv-epg.org/files/epg-ch.xml.gz', 
    'https://iptv-epg.org/files/epg-tw.xml.gz', 
    'https://iptv-epg.org/files/epg-th.xml.gz', 
    'https://iptv-epg.org/files/epg-tt.xml.gz', 
    'https://iptv-epg.org/files/epg-tr.xml.gz', 
    'https://iptv-epg.org/files/epg-ug.xml.gz', 
    'https://iptv-epg.org/files/epg-ua.xml.gz', 
    'https://iptv-epg.org/files/epg-ae.xml.gz', 
    'https://iptv-epg.org/files/epg-gb.xml.gz', 
    'https://iptv-epg.org/files/epg-us.xml.gz', 
    'https://iptv-epg.org/files/epg-uy.xml.gz', 
    'https://iptv-epg.org/files/epg-ve.xml.gz', 
    'https://iptv-epg.org/files/epg-zw.xml.gz', 
    'https://github.com/BuddyChewChew/tcl-playlist-generator/raw/refs/heads/main/tcl_epg.xml',
    'https://github.com/matthuisman/i.mjh.nz/raw/refs/heads/master/nzau/epg.xml.gz',
    'https://raw.githubusercontent.com/BuddyChewChew/localnow-playlist-generator/refs/heads/main/epg.xml',
    'https://github.com/matthuisman/i.mjh.nz/raw/master/Plex/all.xml.gz',
    'https://raw.githubusercontent.com/BuddyChewChew/dummy-epg-project/refs/heads/main/epg.xml',
    'https://github.com/matthuisman/i.mjh.nz/raw/master/Roku/all.xml',
    'https://epg.pw/api/epg.xml?lang=en&timezone=VVMvRWFzdGVybg%3D%3D&date=20260405&channel_id=464981',
    'https://github.com/BuddyChewChew/xumo-playlist-generator/raw/refs/heads/main/playlists/xumo_epg.xml.gz',
    'https://github.com/matthuisman/i.mjh.nz/raw/refs/heads/master/PlutoTV/all.xml.gz',
    'https://github.com/matthuisman/i.mjh.nz/raw/refs/heads/master/SamsungTVPlus/all.xml.gz', 
    'http://drewlive2423.duckdns.org:8045/DrewLive/DrewLive.xml.gz', 
    'https://github.com/insa-ship-it/tcl-playlist-generator/raw/refs/heads/main/tcl_epg.xml', 
    'http://mains.services/xmltv.php?username=tmo247line&password=65s4d64vgfdfbae4&type=m3u_plus', 
    'https://github.com/insa-ship-it/app-m3u-generator/raw/refs/heads/main/playlists/tubi_epg.xml', 
    
]

def get_tvg_ids_from_remote_m3u():
    """Downloads M3U from GitFlic and extracts tvg-id values."""
    tvg_ids = set()
    if not M3U_URL:
        print("CRITICAL: No M3U_URL secret found.")
        return None

    print(f"Downloading M3U from GitFlic...")
    try:
        response = requests.get(M3U_URL, timeout=30)
        if response.status_code != 200:
            print(f"Failed to download M3U: {response.status_code}")
            return None
        
        # Extract tvg-id="value"
        pattern = re.compile(r'tvg-id="([^"]+)"')
        matches = pattern.findall(response.text)
        for val in matches:
            tvg_ids.add(val)
            
        print(f"Successfully mapped {len(tvg_ids)} channels from your playlist.")
        return tvg_ids
    except Exception as e:
        print(f"Error fetching M3U: {e}")
        return None

def fetch_and_parse(url):
    try:
        print(f"Fetching EPG: {url.split('/')[-1]}")
        response = requests.get(url, timeout=60)
        if response.status_code != 200: return None
        content = response.content
        if url.endswith('.gz'):
            content = gzip.decompress(content)
        return ET.fromstring(content)
    except Exception as e:
        print(f"  ! Error: {e}")
        return None

def main():
    valid_ids = get_tvg_ids_from_remote_m3u()
    
    # SAFETY CHECK: Stop if M3U fails to prevent pulling ~400MB of data to GitHub
    if not valid_ids:
        print("Stopping process: M3U filter is required to stay under GitHub file size limits.")
        return

    master_root = ET.Element('tv', {"generator-info-name": "BuddyChewChew-Light-GZ-Only"})

    for url in URLS:
        epg_data = fetch_and_parse(url)
        if epg_data is None: continue

        for channel in epg_data.findall('channel'):
            if channel.get('id') in valid_ids:
                master_root.append(channel)

        for prog in epg_data.findall('programme'):
            if prog.get('channel') in valid_ids:
                title = prog.find('title')
                if title is not None and title.text in ['NHL Hockey', 'Live: NFL Football']:
                    sub = prog.find('sub-title')
                    if sub is not None and sub.text:
                        title.text = f"{title.text} {sub.text}"
                master_root.append(prog)

    # Write ONLY the .gz file to save space and stay under 100MB
    print(f"Saving compressed EPG to {OUTPUT_FILE_GZ}...")
    tree = ET.ElementTree(master_root)
    with gzip.open(OUTPUT_FILE_GZ, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
    
    print("M3U-Filtered EPG (.gz only) generation complete.")

if __name__ == "__main__":
    main()
