import threading

class Menu:
    def __init__(self, effects, effect_chain, on_quit_callback):
        self.effects = effects
        self.effect_chain = effect_chain
        self.current_effect_idx = 0
        self.running = True
        self.on_quit = on_quit_callback
        self.chain_mode = False  # Toggle between single and chain mode
    
    def get_current_effect(self):
        if self.chain_mode:
            return self.effect_chain
        return self.effects[self.current_effect_idx]
    
    def display_menu(self):
        print("\n" + "="*50)
        print(" Guitar FX Menu")
        print("="*50)
        
        if not self.chain_mode:
            print("\n[SINGLE EFFECT MODE]")
            print("\nEffects:")
            for i, effect in enumerate(self.effects, 1):
                marker = "→" if i-1 == self.current_effect_idx else " "
                print(f"  {marker} {i}. {effect.name}")
            print("\nCommands:")
            print("  1-9  : Select effect")
            print("  c    : Switch to Chain Mode")
        else:
            print("\n[CHAIN MODE - Multiple Effects]")
            print("\nEffect Chain:")
            print(self.effect_chain.get_status_display())
            print("\nCommands:")
            print("  1-9  : Toggle effect on/off")
            print("  s    : Switch to Single Mode")
            print("  r    : Reset all effects")
        
        print("  q    : Quit")
        print("="*50)
    
    def run(self):
        self.display_menu()
        
        while self.running:
            choice = input("> ").strip().lower()
            
            if choice.isdigit():
                idx = int(choice) - 1
                
                if not self.chain_mode:
                    # Single effect mode - select effect
                    if 0 <= idx < len(self.effects):
                        self.current_effect_idx = idx
                        self.display_menu()
                        print(f"\n✓ {self.effects[idx].name} enabled")
                    else:
                        print("Invalid effect number")
                else:
                    # Chain mode - toggle effect
                    if self.effect_chain.toggle_effect(idx):
                        self.display_menu()
                        status = "ON" if self.effect_chain.is_active(idx) else "OFF"
                        print(f"\n✓ {self.effect_chain.effects[idx].name} toggled {status}")
                    else:
                        print("Invalid effect number")
            
            elif choice == "c" and not self.chain_mode:
                self.chain_mode = True
                self.display_menu()
                print("\n✓ Switched to Chain Mode")
            
            elif choice == "s" and self.chain_mode:
                self.chain_mode = False
                self.display_menu()
                print("\n✓ Switched to Single Effect Mode")
            
            elif choice == "r" and self.chain_mode:
                self.effect_chain.reset()
                print("\n✓ All effects reset")
            
            elif choice == "q":
                print("\nExiting…")
                self.running = False
                self.on_quit()
                break
            
            else:
                print("Unknown command")
    
    def start_thread(self):
        threading.Thread(target=self.run, daemon=True).start()