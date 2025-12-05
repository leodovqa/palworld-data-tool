#!/usr/bin/env python3
"""
Russian IPTV Playlist Organizer
Organizes Russian M3U playlists with proper grouping
Uses #EXTGRP tags for better IPTV app navigation
"""

import re
import os

class RussianIPTVOrganizer:
    def __init__(self):
        # Define how to map Russian group-titles to EXTGRP categories
        self.group_mapping = {
            'Russia & Belarus': 'Live Russia - General',
            'Russia': 'Live Russia - General',
            '': 'Live Russia - General'
        }
        
    def parse_channel(self, line):
        if not line.startswith('#EXTINF:'):
            return None
            
        name_match = re.search(r'tvg-name="([^"]+)"', line)
        if not name_match:
            return None
            
        name = name_match.group(1)
        
        group_match = re.search(r'group-title="([^"]*)"', line)
        group = group_match.group(1) if group_match else ""
        
        id_match = re.search(r'tvg-ID="([^"]*)"', line)
        tvg_id = id_match.group(1) if id_match else ""
        
        logo_match = re.search(r'tvg-logo="([^"]*)"', line)
        logo = logo_match.group(1) if logo_match else ""
        
        return {
            'name': name,
            'group': group,
            'tvg_id': tvg_id,
            'tvg_logo': logo
        }
    
    def generate_tvg_id(self, channel):
        name = channel['name'].lower()
        
        if name.startswith('rus:'):
            channel_info = name.replace('rus:', '').strip()
            # Extract channel number if available
            num_match = re.search(r'(\d+)', channel_info)
            if num_match:
                channel_num = num_match.group(1)
                if 'perviy kanal' in channel_info or 'first channel' in channel_info:
                    return f"perviy-kanal-{channel_num}"
                elif 'russia' in channel_info:
                    return f"russia-{channel_num}"
                elif 'match' in channel_info:
                    return f"match-{channel_num}"
                elif 'sport' in channel_info:
                    return f"sport-{channel_num}"
                else:
                    return f"rus-{channel_num}"
            return re.sub(r'[^a-z0-9]', '-', channel_info)[:30]
        
        if name.startswith('by:'):
            channel_info = name.replace('by:', '').strip()
            num_match = re.search(r'(\d+)', channel_info)
            if num_match:
                return f"belarus-{num_match.group(1)}"
            return f"belarus-{re.sub(r'[^a-z0-9]', '-', channel_info)[:20]}"
        
        if 'russia' in name.lower():
            return 'russia-separator'
        
        return re.sub(r'[^a-z0-9]', '-', name.lower())[:30]
    
    def get_extgrp_tag(self, group):
        return self.group_mapping.get(group, f'Live Russia - {group}')
    
    def generate_logo_url(self, channel):
        name = channel['name'].lower()
        
        if name.startswith('rus:'):
            if 'perviy kanal' in name or 'first channel' in name:
                return 'https://example.com/perviy-kanal.png'
            elif 'russia' in name:
                return 'https://example.com/russia.png'
            elif 'match' in name:
                return 'https://example.com/match.png'
            elif 'sport' in name:
                return 'https://example.com/sport.png'
            elif 'discovery' in name:
                return 'https://example.com/discovery.png'
            elif 'national geographic' in name:
                return 'https://example.com/natgeo.png'
            elif 'fox' in name:
                return 'https://example.com/fox.png'
            elif 'mtv' in name:
                return 'https://example.com/mtv.png'
            elif 'cnn' in name:
                return 'https://example.com/cnn.png'
        
        if name.startswith('by:'):
            return 'https://example.com/belarus.png'
        
        if channel['tvg_logo'] and channel['tvg_logo'] != '[':
            return channel['tvg_logo']
        
        return 'https://example.com/default.png'
    
    def organize_playlist(self, input_file, output_file):
        print(f"Organizing Russian IPTV playlist: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        organized_lines = []
        channel_count = 0
        current_group = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if line.startswith('#EXTINF:'):
                channel = self.parse_channel(line)
                if channel:
                    original_group = channel['group'].strip()
                    if not original_group:
                        original_group = 'Russia & Belarus'
                    
                    channel['group'] = original_group
                    channel['tvg_id'] = self.generate_tvg_id(channel)
                    channel['tvg_logo'] = self.generate_logo_url(channel)
                    
                    if channel['group'] != current_group:
                        current_group = channel['group']
                        extgrp_tag = self.get_extgrp_tag(current_group)
                        organized_lines.append(f'#EXTGRP:{extgrp_tag}')
                        print(f"Added group: {extgrp_tag}")
                    
                    new_line = f'#EXTINF:-1 tvg-ID="{channel["tvg_id"]}" tvg-name="{channel["name"]}" tvg-logo="{channel["tvg_logo"]}" group-title="{channel["group"]}",{channel["name"]}'
                    organized_lines.append(new_line)
                    channel_count += 1
                    
                    if i + 1 < len(lines) and not lines[i + 1].startswith('#'):
                        organized_lines.append(lines[i + 1].strip())
            elif line.startswith('#') and not line.startswith('#EXTINF:'):
                organized_lines.append(line)
            elif line and not line.startswith('#'):
                continue
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            f.write(f'# Organized Russian IPTV Playlist with EXTGRP Tags\n')
            f.write(f'# Total Channels: {channel_count}\n')
            f.write(f'# Organized by Russian IPTV Organizer\n')
            f.write(f'# Uses #EXTGRP tags for better IPTV app navigation\n\n')
            
            for line in organized_lines:
                f.write(line + '\n')
        
        print(f"Organized playlist saved to: {output_file}")
        print(f"Total channels processed: {channel_count}")
        print(f"EXTGRP tags added for better IPTV app navigation")

def main():
    organizer = RussianIPTVOrganizer()
    
    input_file = 'US_IPTV_2025.m3u'
    output_file = 'RU_IPTV_2025_ORGANIZED.m3u'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    try:
        organizer.organize_playlist(input_file, output_file)
        print("Russian IPTV playlist organization completed successfully!")
        print("Your playlist now includes #EXTGRP tags for better navigation!")
    except Exception as e:
        print(f"Error organizing playlist: {e}")

if __name__ == "__main__":
    main() 