#!/usr/bin/env python3
"""
IPTV Playlist Organizer
Organizes M3U playlists for better searchability and structure
Uses #EXTGRP tags for better IPTV app navigation
"""

import re
import os
from typing import Dict, List, Tuple

class IPTVOrganizer:
    def __init__(self):
        self.network_patterns = {
            'ABC': r'US:\s*ABC\s+(\d+)\s+([^(]+?)\s+([A-Z]{2})\s*\(?([A-Z]+)\)?',
            'CBS': r'US:\s*CBS\s+(\d+)\s+([^(]+?)\s+([A-Z]{2})\s*\(?([A-Z]+)\)?',
            'NBC': r'US:\s*NBC\s+(\d+)\s+([^(]+?)\s+([A-Z]{2})\s*\(?([A-Z]+)\)?',
            'PBS': r'US:\s*PBS\s+(\d+)\s+([^(]+?)\s+([A-Z]{2})\s*\(?([A-Z]+)\)?',
            'FOX': r'US:\s*FOX\s+(\d+)\s+([^(]+?)\s+([A-Z]{2})\s*\(?([A-Z]+)\)?'
        }
        
        self.sports_patterns = {
            'ESPN': r'US:\s*ESPN\s+(\w+)',
            'FOX_SPORTS': r'US:\s*FOX\s+SPORTS\s+(\w+)',
            'TENNIS': r'US:\s*TENNIS\s+PLUS\s+(\d+)',
            'MLB': r'US:\s*MLB\s+(\w+)',
            'NBA': r'US:\s*NBA\s+(\w+)',
            'NFL': r'US:\s*NFL\s+(\w+)'
        }
        
        self.quality_indicators = ['HD', 'FHD', 'UHD', '4K']
        
        # Define EXTGRP categories based on original group-title
        self.extgrp_categories = {
            'USA - ABC Network': 'Live USA - ABC Network',
            'USA - CBS Network': 'Live USA - CBS Network',
            'USA - NBC Network': 'Live USA - NBC Network',
            'USA - PBS Network': 'Live USA - PBS Network',
            'USA - FOX Network': 'Live USA - FOX Network',
            'USA - Sport': 'Live USA - Sports Networks',
            'USA - Sports': 'Live USA - Sports Networks',
            'USA - Other Sports': 'Live USA - Other Sports',
            'USA - MLB': 'Live USA - MLB',
            'USA - NBA': 'Live USA - NBA',
            'USA - NFL': 'Live USA - NFL',
            'USA - NHL': 'Live USA - NHL',
            'USA - ESPN+': 'Live USA - ESPN Plus',
            'USA - Tennis Plus': 'Live USA - Tennis Plus',
            'USA - Peacock': 'Live USA - Peacock',
            'USA - News': 'Live USA - News Networks',
            'USA - Entertainment': 'Live USA - Entertainment Networks',
            'USA - Premium': 'Live USA - Premium Networks',
            'USA - Kids': 'Live USA - Kids Networks',
            'USA - California Local': 'Live USA - California Local',
            'USA - New York Local': 'Live USA - New York Local',
            'USA - Texas Local': 'Live USA - Texas Local',
            'USA - Florida Local': 'Live USA - Florida Local',
            'USA': 'Live USA - General'
        }
        
    def parse_channel(self, line: str) -> Dict:
        """Parse a channel line and extract information"""
        if not line.startswith('#EXTINF:'):
            return None
            
        # Extract tvg-name
        name_match = re.search(r'tvg-name="([^"]+)"', line)
        if not name_match:
            return None
            
        name = name_match.group(1)
        
        # Extract group-title
        group_match = re.search(r'group-title="([^"]+)"', line)
        group = group_match.group(1) if group_match else ""
        
        # Extract tvg-ID
        id_match = re.search(r'tvg-ID="([^"]+)"', line)
        tvg_id = id_match.group(1) if id_match else ""
        
        # Extract tvg-logo
        logo_match = re.search(r'tvg-logo="([^"]+)"', line)
        logo = logo_match.group(1) if logo_match else ""
        
        return {
            'name': name,
            'group': group,
            'tvg_id': tvg_id,
            'tvg_logo': logo,
            'original_line': line
        }
    
    def standardize_name(self, channel: Dict) -> str:
        """Standardize channel name format"""
        name = channel['name']
        
        # Check if it's a major network affiliate
        for network, pattern in self.network_patterns.items():
            match = re.search(pattern, name, re.IGNORECASE)
            if match:
                channel_num = match.group(1)
                city = match.group(2).strip()
                state = match.group(3)
                call_letters = match.group(4) if len(match.groups()) > 3 else ""
                
                if call_letters:
                    return f"US: {network} {channel_num} {city} {state} ({call_letters})"
                else:
                    return f"US: {network} {channel_num} {city} {state}"
        
        # Check if it's a sports channel
        for sport, pattern in self.sports_patterns.items():
            match = re.search(pattern, name, re.IGNORECASE)
            if match:
                identifier = match.group(1)
                return f"US: {sport.replace('_', ' ')} {identifier}"
        
        # Return original name if no pattern matches
        return name
    
    def generate_tvg_id(self, channel: Dict) -> str:
        """Generate a unique tvg-ID"""
        name = channel['name'].lower()
        
        # Extract network and channel number
        network_match = re.search(r'us:\s*(\w+)\s+(\d+)', name)
        if network_match:
            network = network_match.group(1)
            channel_num = network_match.group(2)
            return f"{network}-{channel_num}"
        
        # For sports channels
        if 'espn' in name:
            return 'espn-main'
        elif 'fox sports' in name:
            return 'fox-sports'
        elif 'tennis plus' in name:
            num_match = re.search(r'(\d+)', name)
            if num_match:
                return f"tennis-plus-{num_match.group(1).zfill(2)}"
        
        # Generate generic ID
        return re.sub(r'[^a-z0-9]', '-', name.lower())[:30]
    
    def determine_group(self, channel: Dict) -> str:
        """Determine the appropriate group for a channel based on original group-title"""
        original_group = channel['group'].strip()
        
        # If we have an original group, use it
        if original_group:
            return original_group
        
        # Fallback: determine group from channel name
        name = channel['name'].lower()
        
        # Major networks
        if any(network in name for network in ['abc', 'cbs', 'nbc', 'pbs', 'fox']):
            if 'abc' in name:
                return 'USA - ABC Network'
            elif 'cbs' in name:
                return 'USA - CBS Network'
            elif 'nbc' in name:
                return 'USA - NBC Network'
            elif 'pbs' in name:
                return 'USA - PBS Network'
            elif 'fox' in name:
                return 'USA - FOX Network'
        
        # Sports networks
        if any(sport in name for sport in ['espn', 'fox sports', 'tennis', 'mlb', 'nba', 'nfl', 'nhl']):
            if 'tennis plus' in name:
                return 'USA - Tennis Plus'
            elif 'espn plus' in name:
                return 'USA - ESPN+'
            elif 'mlb' in name:
                return 'USA - MLB'
            elif 'nba' in name:
                return 'USA - NBA'
            elif 'nfl' in name:
                return 'USA - NFL'
            elif 'nhl' in name:
                return 'USA - NHL'
            else:
                return 'USA - Sport'
        
        # News networks
        if any(news in name for news in ['cnn', 'fox news', 'msnbc', 'abc news', 'cbs news']):
            return 'USA - News'
        
        # Premium networks
        if any(premium in name for premium in ['hbo', 'showtime', 'cinemax', 'starz']):
            return 'USA - Premium'
        
        # Entertainment networks
        if any(ent in name for ent in ['mtv', 'vh1', 'comedy central', 'tbs', 'tnt']):
            return 'USA - Entertainment'
        
        # Kids networks
        if any(kids in name for kids in ['disney', 'nickelodeon', 'cartoon network', 'nick']):
            return 'USA - Kids'
        
        return 'USA'
    
    def get_extgrp_tag(self, group: str) -> str:
        """Get the EXTGRP tag for a group"""
        return self.extgrp_categories.get(group, f'Live USA - {group.replace("USA - ", "")}')
    
    def generate_logo_url(self, channel: Dict) -> str:
        """Generate a logo URL for the channel"""
        name = channel['name'].lower()
        
        # Major networks
        if 'abc' in name:
            return 'https://example.com/abc.png'
        elif 'cbs' in name:
            return 'https://example.com/cbs.png'
        elif 'nbc' in name:
            return 'https://example.com/nbc.png'
        elif 'pbs' in name:
            return 'https://example.com/pbs.png'
        elif 'fox' in name:
            return 'https://example.com/fox.png'
        elif 'espn' in name:
            return 'https://example.com/espn.png'
        elif 'cnn' in name:
            return 'https://example.com/cnn.png'
        elif 'hbo' in name:
            return 'https://example.com/hbo.png'
        
        return 'https://example.com/default.png'
    
    def organize_playlist(self, input_file: str, output_file: str):
        """Organize the entire playlist with EXTGRP tags"""
        print(f"Organizing playlist: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        organized_lines = []
        channel_count = 0
        current_group = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if line.startswith('#EXTINF:'):
                # Parse channel information
                channel = self.parse_channel(line)
                if channel:
                    # Standardize the channel
                    channel['name'] = self.standardize_name(channel)
                    channel['group'] = self.determine_group(channel)
                    channel['tvg_id'] = self.generate_tvg_id(channel)
                    channel['tvg_logo'] = self.generate_logo_url(channel)
                    
                    # Add EXTGRP tag if group changed
                    if channel['group'] != current_group:
                        current_group = channel['group']
                        extgrp_tag = self.get_extgrp_tag(current_group)
                        organized_lines.append(f'#EXTGRP:{extgrp_tag}')
                    
                    # Create new organized line
                    new_line = f'#EXTINF:-1 tvg-ID="{channel["tvg_id"]}" tvg-name="{channel["name"]}" tvg-logo="{channel["tvg_logo"]}" group-title="{channel["group"]}",{channel["name"]}'
                    organized_lines.append(new_line)
                    channel_count += 1
                    
                    # Add the URL line (next line)
                    if i + 1 < len(lines) and not lines[i + 1].startswith('#'):
                        organized_lines.append(lines[i + 1].strip())
            elif line.startswith('#') and not line.startswith('#EXTINF:'):
                # Keep other comment lines
                organized_lines.append(line)
            elif line and not line.startswith('#'):
                # Skip URL lines (they're handled above)
                continue
        
        # Write organized playlist
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            f.write(f'# Organized IPTV Playlist with EXTGRP Tags\n')
            f.write(f'# Total Channels: {channel_count}\n')
            f.write(f'# Organized by IPTV Organizer\n')
            f.write(f'# Uses #EXTGRP tags for better IPTV app navigation\n\n')
            
            for line in organized_lines:
                f.write(line + '\n')
        
        print(f"Organized playlist saved to: {output_file}")
        print(f"Total channels processed: {channel_count}")
        print(f"EXTGRP tags added for better IPTV app navigation")

def main():
    organizer = IPTVOrganizer()
    
    input_file = 'US_IPTV_2025.m3u'
    output_file = 'US_IPTV_2025_ORGANIZED.m3u'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    try:
        organizer.organize_playlist(input_file, output_file)
        print("Playlist organization completed successfully!")
        print("Your playlist now includes #EXTGRP tags for better navigation!")
    except Exception as e:
        print(f"Error organizing playlist: {e}")

if __name__ == "__main__":
    main() 