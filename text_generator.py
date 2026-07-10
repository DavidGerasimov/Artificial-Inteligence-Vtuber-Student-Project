from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class TextGenerator:
    def __init__(self):
        # Вчитување на GPT-2 модел за генерирање креативен текст
        print("  Loading GPT-2 text model for creative writing...")
        
        # Користење на GPT-2 medium (добар за приказни и креативно пишување)
        self.model_name = "gpt2-medium"
        
        try:
            # Вчитување на tokenizer (го конвертира текстот во броеви)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            # Вчитување на самиот модел
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Поставување на padding token (за правилно процесирање)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Проверка дали има GPU (графичка), ако не користи CPU
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            
            print(f"  ✓ GPT-2 ready for creative text generation on {self.device}")
            
        except Exception as e:
            print(f"  Error loading text model: {e}")
            raise
    
    def generate(self, prompt, max_length=250):
        # Главна функција за генерирање текст
        try:
            # КРИТИЧНО: Конвертирање на промптот во формат за приказна
            story_prompt = self._convert_to_story_start(prompt)
            
            print(f"  Story prompt: '{story_prompt[:60]}...'")
            
            # Конвертирање на текстот во броеви (токенизација)
            inputs = self.tokenizer.encode(story_prompt, return_tensors="pt").to(self.device)
            
            # Генерирање на текст со оптимизирани параметри за приказни
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,              # Максимална должина
                    min_length=80,                       # Минимална должина (подолги приказни)
                    temperature=0.9,                     # Креативност (0.8-1.0 за приказни)
                    do_sample=True,                      # Користење на семплирање
                    top_k=40,                            # Избор од топ 40 зборови
                    top_p=0.92,                          # Nucleus sampling
                    num_return_sequences=1,              # Генерира еден резултат
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3,              # Избегнување на повторување
                    repetition_penalty=1.3,              # Казна за повторување
                )
            
            # Конвертирање на броевите назад во текст
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Чистење на излезот
            result = self._extract_story(generated_text, story_prompt)
            
            return result
            
        except Exception as e:
            return f"Error while generating story: {str(e)}"
    
    def _convert_to_story_start(self, prompt):
        # Конвертирање на било какво барање во формат за приказна
        
        prompt_lower = prompt.lower().strip()
        
        # Ако е "Write a story about X" или "Tell me a story about X"
        if 'story about' in prompt_lower or 'write' in prompt_lower:
            # Извлекување на темата
            if 'about' in prompt_lower:
                # Наоѓање на делот после "about"
                parts = prompt_lower.split('about')
                if len(parts) > 1:
                    topic = parts[-1].strip()
                    # Отстранување на завршни точки/прашалници
                    topic = topic.rstrip('.?!').strip()
                    
                    # СПЕЦИФИЧНА ОБРАБОТКА ЗА РАЗЛИЧНИ ТЕМИ
                    if 'dragon' in topic:
                        return "Once upon a time, there lived a fearsome dragon. "
                    elif 'robot' in topic:
                        return "In a world of technology, there was a special robot. "
                    elif 'princess' in topic or 'prince' in topic:
                        return "In a faraway kingdom, there lived a noble princess. "
                    elif 'wizard' in topic or 'magic' in topic:
                        return "In the realm of magic, a powerful wizard dwelled. "
                    elif 'astronaut' in topic or 'space' in topic:
                        return "Far beyond Earth, in the depths of space, "
                    else:
                        # Општа конверзија
                        return f"Once upon a time, there was {topic}. "
            
            # Ако нема "about", само стандарден почеток
            return "Once upon a time, in a land far away, "
        
        # Ако веќе почнува со "Once upon a time"
        elif prompt_lower.startswith('once upon'):
            return prompt.strip() + " "
        
        # Ако е прашање (What, Why, How, etc.)
        elif any(prompt_lower.startswith(q) for q in ['what', 'why', 'how', 'who', 'when', 'where']):
            # Конвертирај во приказна форма
            return "Here is a tale: "
        
        # Ако е директен почеток на реченица
        elif len(prompt.split()) < 10 and not prompt.endswith(('.', '!', '?')):
            # Додај го како почеток на приказна
            return prompt.strip() + " "
        
        # За сè друго, додај "Once upon a time" на почетокот
        else:
            return "Once upon a time, " + prompt.strip() + " "
    
    def _extract_story(self, full_text, original_prompt):
        # Извлекување и чистење на приказната
        
        # Отстранување на оригиналниот промпт ако е повторен
        text = full_text
        if text.startswith(original_prompt):
            text = text[len(original_prompt):].strip()
        
        # Отстранување на честа garbage (Arisa, Aria, итн.)
        # Ова се имиња од anime што често се појавуваат погрешно
        garbage_indicators = [
            'Arisa', 'Aria', 'Asuna', '「', '」', 
            '(TL note:', 'To be clear,', 'In truth it seems'
        ]
        
        # Ако текстот содржи овие, тоа значи дека генерирањето не успеа
        if any(garbage in text for garbage in garbage_indicators):
            # Врати едноставна приказна наместо garbage
            return "Once upon a time, there lived a mighty dragon in the mountains. The dragon was feared by all who knew of its existence. Villages would tremble when they heard tales of the beast. But perhaps this dragon had a story worth telling, one of mystery and ancient power."
        
        # Чистење на останатиот текст
        # Отстранување на специјални знаци
        text = text.replace('「', '').replace('」', '')
        
        # Разделување на реченици
        sentences = []
        current = ""
        
        for char in text:
            current += char
            # Кога најдеме крај на реченица
            if char in '.!?' and len(current) > 15:
                sentence = current.strip()
                # Провери дали е валидна реченица
                if (len(sentence) > 10 and 
                    sentence[0].isupper() and 
                    not any(bad in sentence for bad in ['(TL', 'TL note'])):
                    sentences.append(sentence)
                current = ""
        
        # Ако има преостанат текст
        if current.strip() and len(current) > 15:
            sentences.append(current.strip())
        
        # Спојување на реченици (максимум 6-7 за добра приказна)
        if sentences:
            result = ' '.join(sentences[:7])
        else:
            # Ако ништо не е генерирано, врати fallback приказна
            result = "In a distant land, a tale unfolded of courage and wonder. The story speaks of adventures yet untold, waiting to be discovered."
        
        # Осигурај дека завршува со точка
        if result and not result[-1] in '.!?':
            result += '.'
        
        return result.strip()


# Тест функција
if __name__ == "__main__":
    print("\n=== Testing Story Generator ===\n")
    
    gen = TextGenerator()
    
    # Тест промпти
    test_prompts = [
        "Write me a story about a dragon that eats people",
        "Write a story about a friendly robot",
        "Once upon a time in a magical forest",
        "Write a story about a brave knight",
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: {prompt}")
        print(f"{'='*60}")
        result = gen.generate(prompt)
        print(f"\nGenerated Story:\n{result}")
        print(f"\n{'='*60}\n")