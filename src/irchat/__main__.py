#!/usr/bin/env python3
"""
IRC Chat Client - Modern Terminal UI
Professional-grade IRC client with Gemini CLI-inspired interface
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='💬 IRChat - Modern Terminal IRC Client',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Available UI Modes:
  modern   - Modern, professional CLI (default) ⭐
  basic    - Simple, lightweight CLI
  rich     - Rich library UI with advanced features

Examples:
  python -m irchat modern irc.libera.chat 6667 mynick #general
  python -m irchat irc.libera.chat 6667 mynick #general  (uses modern by default)
  python -m irchat basic irc.libera.chat 6667 mynick #python
        '''
    )
    
    parser.add_argument('ui_or_server', 
                       help='UI mode (modern/basic/rich) or IRC server address')
    parser.add_argument('server_or_port', nargs='?',
                       help='IRC server address (if ui specified) or port number')
    parser.add_argument('port_or_nick', nargs='?',
                       help='Port number (if ui specified) or nickname')
    parser.add_argument('nick_or_channel', nargs='?',
                       help='Nickname (if ui specified) or channel to join')
    parser.add_argument('channel', nargs='?',
                       help='Channel to join (if ui specified)')
    
    args = parser.parse_args()
    
    # Parse arguments - determine if first arg is UI mode or server
    ui_mode = 'modern'  # Default
    
    if args.ui_or_server in ['basic', 'modern', 'rich']:
        # First arg is UI mode
        ui_mode = args.ui_or_server
        server = args.server_or_port
        port_str = args.port_or_nick
        nickname = args.nick_or_channel
        channel = args.channel
    else:
        # First arg is server
        server = args.ui_or_server
        port_str = args.server_or_port
        nickname = args.port_or_nick
        channel = args.nick_or_channel
    
    # Validate arguments
    if not server or not port_str or not nickname:
        parser.print_help()
        sys.exit(1)
    
    try:
        port = int(port_str)
    except (ValueError, TypeError):
        print("Error: port must be an integer")
        sys.exit(1)
    
    # Normalize channel
    channels = []
    if channel:
        if not channel.startswith('#'):
            channel = '#' + channel
        channels = [channel]
    
    # Route to appropriate UI
    try:
        if ui_mode == 'modern':
            from .irc_chat_modern import ModernIRCInterface
            interface = ModernIRCInterface()
            interface.run(server, port, nickname, channels)
        elif ui_mode == 'basic':
            from .irc_chat import IRCInterface
            interface = IRCInterface()
            interface.run(server, port, nickname, channel if channel else "")
        elif ui_mode == 'rich':
            from .irc_rich import IRCClient as RichIRCClient
            client = RichIRCClient(server, port)
            client.run_interface(nickname, channels)
    except ImportError as e:
        print(f"Error: Failed to load UI mode '{ui_mode}': {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
