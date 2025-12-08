import threading

class Menu:
    def __init__(self, effects, on_quit_callback):
        self.effects = effects
        self.current_effect_idx = 0
        self.running = True
        self.on_quit = on_quit_callback
    
    def get_current_effect(self):
        return self.effects[self.current_effect_idx]
    
    def display_menu(self):
        print("\n Guitar pedal menu")
        for i, effect in enumerate(self.effects, 1):
            print(f"{i} = {effect.name}")
        print("q = Quit")
        print("-----------------------------------")
    
    def run(self):
        self.display_menu()
        
        while self.running:
            choice = input("> ").strip()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.effects):
                    self.current_effect_idx = idx
                    print(f"→ {self.effects[idx].name} enabled")
                else:
                    print("Unknown option")
            elif choice == "q":
                print("Exiting…")
                self.running = False
                self.on_quit()
                break
            else:
                print("Unknown option")
    
    def start_thread(self):
        threading.Thread(target=self.run, daemon=True).start()