import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import pyttsx3

# Увоз на нашите модули
from text_generator import TextGenerator
from image_generator import AIImageGenerator
from vtuber_avatar import VTuberAvatar
from emotion_detector import SimpleEmotionDetector

class AIVTuberApp:
    def __init__(self, root):
        # Поставки на главниот прозорец
        self.root = root
        self.root.title("AI VTuber - Generative AI Project")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
        
        print("Initializing AI VTuber Application...")
        
        # Иницијализација на текст генератор (GPT-2 модел)
        try:
            print("Loading text generator...")
            self.text_gen = TextGenerator()
            print("Text generator loaded!")
        except Exception as e:
            print(f"Error loading text generator: {e}")
            messagebox.showerror("Error", f"Failed to load text generator: {e}")
            root.destroy()
            return
        
        # Иницијализација на слика генератор (AI модел за слики)
        try:
            print("Loading image generator...")
            self.image_gen = AIImageGenerator()
            print("Image generator loaded!")
        except Exception as e:
            print(f"Error loading image generator: {e}")
            self.image_gen = None
        
        # Иницијализација на емоција детектор (анализа на сентимент)
        try:
            print("Loading emotion detector...")
            self.emotion_detector = SimpleEmotionDetector()
            print("Emotion detector loaded!")
        except Exception as e:
            print(f"Error loading emotion detector: {e}")
            self.emotion_detector = None
        
        # Иницијализација на text-to-speech систем
        try:
            print("Initializing voice system...")
            self.tts_engine = pyttsx3.init()
            
            # Конфигурација на гласот (се обидува да постави женски глас)
            voices = self.tts_engine.getProperty('voices')
            if len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)
            
            # Поставки на брзина и јачина на гласот
            self.tts_engine.setProperty('rate', 160)
            self.tts_engine.setProperty('volume', 0.9)
            print("Voice system ready!")
        except Exception as e:
            print(f"Voice initialization error: {e}")
            self.tts_engine = None
        
        # VTuber аватарот (ќе се креира подоцна)
        self.avatar = None
        
        print("Building user interface...")
        self.setup_ui()
        print("Application ready!")
        
    def setup_ui(self):
        # Наслов на апликацијата
        title = tk.Label(
            self.root, 
            text="AI VTuber Generator - Pikto", 
            font=("Arial", 20, "bold"),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        title.pack(pady=10)
        
        # Рамка за избор на режим (текст или слика)
        mode_frame = tk.Frame(self.root, bg='#2b2b2b')
        mode_frame.pack(pady=5)
        
        tk.Label(
            mode_frame, 
            text="Select Mode:", 
            font=("Arial", 12),
            bg='#2b2b2b',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=5)
        
        # Променлива за чување на избраниот режим
        self.mode_var = tk.StringVar(value="text")
        
        # Радио копчиња за избор
        tk.Radiobutton(
            mode_frame, 
            text="Create Story", 
            variable=self.mode_var, 
            value="text",
            bg='#2b2b2b',
            fg='#ffffff',
            selectcolor='#404040',
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(
            mode_frame, 
            text="Generate Image", 
            variable=self.mode_var, 
            value="image",
            bg='#2b2b2b',
            fg='#ffffff',
            selectcolor='#404040',
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        # Рамка за поле за внес на промпт
        input_frame = tk.Frame(self.root, bg='#2b2b2b')
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            input_frame, 
            text="Your Prompt:", 
            font=("Arial", 11),
            bg='#2b2b2b',
            fg='#ffffff'
        ).pack(anchor=tk.W)
        
        # Текстуално поле со можност за скролање
        self.input_text = scrolledtext.ScrolledText(
            input_frame, 
            height=4, 
            font=("Arial", 10),
            bg='#404040',
            fg='#ffffff',
            insertbackground='#ffffff'
        )
        self.input_text.pack(fill=tk.X, pady=5)
        
        # Рамка за копчињата
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=5)
        
        # Копче за генерирање (главно копче)
        self.generate_btn = tk.Button(
            button_frame,
            text="Generate",
            command=self.generate,
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='#ffffff',
            padx=20,
            pady=5,
            cursor="hand2"
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Копче за прикажување на VTuber аватарот
        tk.Button(
            button_frame,
            text="Show Pikto",
            command=self.show_avatar,
            font=("Arial", 12),
            bg='#2196F3',
            fg='#ffffff',
            padx=20,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Копче за тестирање на гласот
        tk.Button(
            button_frame,
            text="Test Voice",
            command=self.test_voice,
            font=("Arial", 12),
            bg='#FF9800',
            fg='#ffffff',
            padx=20,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Копче за чистење на излезот
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_output,
            font=("Arial", 12),
            bg='#f44336',
            fg='#ffffff',
            padx=20,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Рамка за поле за излез (каде се прикажува генерираниот текст)
        output_frame = tk.Frame(self.root, bg='#2b2b2b')
        output_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            output_frame, 
            text="AI Response:", 
            font=("Arial", 11),
            bg='#2b2b2b',
            fg='#ffffff'
        ).pack(anchor=tk.W)
        
        # Текстуално поле за прикажување на резултатот
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=15,
            font=("Arial", 10),
            bg='#404040',
            fg='#00ff00',
            insertbackground='#ffffff',
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Статус линија на дното на прозорецот
        self.status_label = tk.Label(
            self.root,
            text="Ready - Click 'Show Pikto' to begin!",
            font=("Arial", 9),
            bg='#1a1a1a',
            fg='#00ff00',
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
    def show_avatar(self):
        # Прикажување на VTuber аватар во нов прозорец
        if self.avatar is None or not self.avatar.running:
            try:
                self.avatar = VTuberAvatar()
                # Стартување на аватарот во посебна нишка (thread)
                avatar_thread = threading.Thread(target=self.avatar.run, daemon=True)
                avatar_thread.start()
                self.update_status("Pikto avatar window opened!")
            except Exception as e:
                messagebox.showerror("Avatar Error", f"Could not open Pikto: {e}")
        else:
            messagebox.showinfo("Info", "Pikto is already active!")
    
    def generate(self):
        # Главна функција за генерирање (текст или слика)
        prompt = self.input_text.get("1.0", tk.END).strip()
        
        # Проверка дали е внесен промпт
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt!")
            return
        
        mode = self.mode_var.get()
        # Оневозможување на копчето додека генерира
        self.generate_btn.config(state=tk.DISABLED, text="Generating...")
        self.update_status(f"Generating {mode}...")
        
        # Стартување на анимација за размислување кај аватарот
        if self.avatar and self.avatar.running:
            self.avatar.start_thinking()
        
        # Стартување на генерирањето во посебна нишка (за да не се блокира GUI)
        thread = threading.Thread(
            target=self._generate_thread, 
            args=(prompt, mode),
            daemon=True
        )
        thread.start()
    
    def _generate_thread(self, prompt, mode):
        # Функција која работи во посебна нишка за генерирање
        try:
            if mode == "text":
                # Генерирање на текст
                result = self.text_gen.generate(prompt)
                self.root.after(0, self.display_result, result)
                
                # Детекција на емоција од генерираниот текст
                if self.emotion_detector:
                    emotion, confidence = self.emotion_detector.detect_emotion(result)
                    print(f"Detected emotion: {emotion} (confidence: {confidence:.2f})")
                    
                    # Поставување на емоцијата кај аватарот
                    if self.avatar and self.avatar.running:
                        self.avatar.set_emotion(emotion)
                    
                    # Добивање на параметри за гласот според емоцијата
                    rate, volume, _ = self.emotion_detector.get_voice_parameters(emotion)
                else:
                    rate, volume = 160, 0.9
                
                # Преминување од размислување во зборување
                self.root.after(0, self._start_talking)
                # Зборување на генерираниот текст
                self.speak(result, rate=rate, volume=volume)
                
            elif mode == "image":
                # Генерирање на слика
                if self.image_gen:
                    result = self.image_gen.generate(prompt)
                    self.root.after(0, self.display_result, result)
                    
                    # Поставување на среќна емоција за успешна генерација
                    if self.avatar and self.avatar.running:
                        self.avatar.set_emotion('happy')
                    
                    self.root.after(0, self._start_talking)
                    self.speak("Image has been generated successfully! Check the generated images folder.", rate=170, volume=0.95)
                else:
                    self.root.after(0, self.display_result, "Image generator not available")
                    
        except Exception as e:
            # Ракување со грешки
            error_msg = f"Error: {str(e)}"
            print(f"Generation error: {e}")
            self.root.after(0, self.display_result, error_msg)
            
            # Поставување на тажна емоција за грешка
            if self.avatar and self.avatar.running:
                self.avatar.set_emotion('sad')
            
            self.root.after(0, self._start_talking)
            self.speak("An error occurred during generation", rate=140, volume=0.7)
        finally:
            # Завршување на генерирањето
            self.root.after(0, self._generation_complete)
    
    def _start_talking(self):
        # Помошна функција за преминување во режим на зборување
        if self.avatar and self.avatar.running:
            self.avatar.stop_thinking()
            self.avatar.start_talking()
    
    def speak(self, text, rate=None, volume=None):
        # Функција за text-to-speech (зборување на текст)
        if not self.tts_engine:
            print("TTS not available")
            return
        
        try:
            # Поставување на параметри на гласот
            if rate:
                self.tts_engine.setProperty('rate', rate)
            if volume:
                self.tts_engine.setProperty('volume', volume)
            
            # Чистење на текстот (отстранување на нови линии)
            clean_text = text.replace('\n', ' ').strip()
            
            # Зборување на текстот (делење на парчиња ако е предолг)
            if len(clean_text) > 500:
                chunks = [clean_text[i:i+500] for i in range(0, len(clean_text), 500)]
                for chunk in chunks:
                    self.tts_engine.say(chunk)
                    self.tts_engine.runAndWait()
            else:
                self.tts_engine.say(clean_text)
                self.tts_engine.runAndWait()
            
            # Враќање на стандардни поставки
            self.tts_engine.setProperty('rate', 160)
            self.tts_engine.setProperty('volume', 0.9)
                
        except Exception as e:
            print(f"TTS error: {e}")
        finally:
            # Враќање на аватарот во idle состојба
            if self.avatar and self.avatar.running:
                self.avatar.stop_talking()
                self.avatar.stop_thinking()
    
    def test_voice(self):
        # Тестирање на гласовниот систем
        messages = [
            "Hello! I am Pikto, your AI assistant!",
            "My voice system is working correctly!",
            "I can generate stories and images!",
            "Ready to help with your project!"
        ]
        import random
        message = random.choice(messages)
        
        self.update_status("Testing voice...")
        
        # Стартување на анимација на зборување
        if self.avatar and self.avatar.running:
            self.avatar.start_talking()
        
        # Зборување во посебна нишка
        thread = threading.Thread(target=self._test_voice_speak, args=(message,), daemon=True)
        thread.start()
    
    def _test_voice_speak(self, message):
        # Помошна функција за тестирање на гласот
        try:
            if self.tts_engine:
                self.tts_engine.say(message)
                self.tts_engine.runAndWait()
        finally:
            if self.avatar and self.avatar.running:
                self.avatar.stop_talking()
            self.root.after(0, self.update_status, "Voice test complete!")
    
    def display_result(self, result):
        # Прикажување на резултатот во output полето
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)
        self.output_text.config(state=tk.DISABLED)
    
    def _generation_complete(self):
        # Завршување на генерирањето (враќање на копчето во нормална состојба)
        self.generate_btn.config(state=tk.NORMAL, text="Generate")
        self.update_status("Generation complete!")
        
        # Чистење на состојбата на аватарот
        if self.avatar and self.avatar.running:
            self.avatar.stop_thinking()
            self.avatar.stop_talking()
    
    def clear_output(self):
        # Чистење на input и output полињата
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.input_text.delete("1.0", tk.END)
        self.update_status("Cleared")
    
    def update_status(self, message):
        # Ажурирање на статус линијата
        self.status_label.config(text=message)

def main():
    # Главна функција за стартување на апликацијата
    print("=" * 60)
    print("AI VTuber - Generative AI Project - Pikto")
    print("=" * 60)
    
    root = tk.Tk()
    app = AIVTuberApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()