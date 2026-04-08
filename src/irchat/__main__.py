#!/usr/bin/env python3
"""
IRC Chat Client - UI Selector
Allows choosing between basic CLI and rich UI options
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='IRC Chat Client - Choose your UI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Available UI Options:
  basic    - Simple CLI interface (default, lightweight)
  modern   - Modern colored terminal UI (requires terminal support)
  rich     - Rich library UI with panels and tables (requires 'rich' package)

Examples:
  python run.py basic irc.libera.chat 6667 mynick #general
  python run.py modern irc.libera.chat 6667 mynick
  python run.py rich irc.libera.chat 6667 mynick #python
        '''
    )
    
    parser.add_argument('ui', nargs='?', default='basic',
                       choices=['basic', 'modern', 'rich'],
                       help='UI mode to use (default: basic)')
    parser.add_argument('server', help='IRC server address')
    parser.add_argument('port', type=int, help='IRC server port')
    parser.add_argument('nickname', help='Your nickname')
    parser.add_argument('channel', nargs='?', help='Channel to join')
    
    # Parse only first few args for UI selection
    args = sys.argv[1:]
    
    if not args:
        parser.print_help()
        sys.exit(1)
    
    ui_mode = args[0] if args[0] in ['basic', 'modern', 'rich'] else 'basic'
    remaining_args = args if args[0] not in ['basic', 'modern', 'rich'] else args[1:]
    
    if not remaining_args or len(remaining_args) < 3:
        parser.print_help()
        sys.exit(1)
    
    server = remaining_args[0]
    try:
        port = int(remaining_args[1])
    except ValueError:
        print("Error: port must be an integer")
        sys.exit(1)
    
    nickname = remaining_args[2]
    channel = remaining_args[3] if len(remaining_args) > 3 else ""
    
    if channel and not channel.startswith('#'):
        channel = '#' + channel
    
    # Route to appropriate UI
    if ui_mode == 'basic':
        from .irc_chat import IRCInterface
        interface = IRCInterface()
        interface.run(server, port, nickname, channel)
    elif ui_mode == 'modern':
        print("Note: Modern UI requires manual setup. Use 'irc_modern.py' directly.")
        from .irc_chat import IRCInterface
        interface = IRCInterface()
        interface.run(server, port, nickname, channel)
    elif ui_mode == 'rich':
        print("Note: Rich UI requires 'rich' package. Use 'irc_rich.py' directly.")
        from .irc_chat import IRCInterface
        interface = IRCInterface()
        interface.run(server, port, nickname, channel)

if __name__ == '__main__':
    main()
