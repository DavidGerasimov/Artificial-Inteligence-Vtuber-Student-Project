from PIL import Image, ImageDraw
import random
import os
from datetime import datetime

class SimpleImageGenerator:
    # Едноставен генератор на геометриска уметност (без AI модел)
    def __init__(self):
        print("  Using simple geometric image generator")
        # Креирање на папка за зачувување на слики
        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"  ✓ Images will be saved to: {self.output_dir}/")
    
    def generate(self, prompt):
        # Генерирање на шарена геометриска слика базирана на промптот
        try:
            # Креирање на нова слика (512x512 пиксели)
            img = Image.new('RGB', (512, 512), color='white')
            draw = ImageDraw.Draw(img)
            
            # Користење на промптот за seed на random генераторот
            # (истиот промпт = иста слика)
            hash_val = hash(prompt)
            random.seed(hash_val)
            
            # Избор на стил според клучни зборови во промптот
            prompt_lower = prompt.lower()
            
            if 'dark' in prompt_lower or 'night' in prompt_lower:
                bg_color = (20, 20, 40)  # Темна позадина
            elif 'sunset' in prompt_lower or 'orange' in prompt_lower:
                bg_color = (255, 180, 100)  # Портокалова позадина
            elif 'ocean' in prompt_lower or 'blue' in prompt_lower:
                bg_color = (150, 200, 255)  # Сина позадина
            else:
                bg_color = (240, 240, 250)  # Светла позадина
            
            # Пополнување на позадината
            draw.rectangle([0, 0, 512, 512], fill=bg_color)
            
            # Цртање на случајни шарени форми
            num_shapes = random.randint(15, 30)
            
            for _ in range(num_shapes):
                # Случајна позиција и големина
                x1 = random.randint(0, 512)
                y1 = random.randint(0, 512)
                size = random.randint(30, 150)
                x2 = x1 + size
                y2 = y1 + size
                
                # Случајна светла боја
                color = (
                    random.randint(50, 255),
                    random.randint(50, 255),
                    random.randint(50, 255)
                )
                
                # Случаен тип на форма
                shape_type = random.choice(['circle', 'rectangle', 'line'])
                
                if shape_type == 'circle':
                    # Цртање на круг
                    draw.ellipse([x1, y1, x2, y2], fill=color, outline=color)
                elif shape_type == 'rectangle':
                    # Цртање на правоаголник
                    draw.rectangle([x1, y1, x2, y2], fill=color, outline=color)
                else:
                    # Цртање на линија
                    draw.line([x1, y1, x2, y2], fill=color, width=random.randint(2, 8))
            
            # Зачувување на сликата
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath)
            
            return f"✓ Image generated successfully!\n\nSaved to: {filepath}\n\nPrompt: {prompt}\n\nNote: Using simple geometric generator (no AI model required)"
            
        except Exception as e:
            return f"Error generating image: {str(e)}"


# AI генератор на слики користејќи Tiny-SD (лесен AI модел)
class AIImageGenerator:
    def __init__(self):
        print("  Loading MinDALL-E AI image generator...")
        print("  (This may take 2-3 minutes on first run)")
        
        try:
            from diffusers import DiffusionPipeline
            import torch
            
            # Креирање на папка за слики
            self.output_dir = "generated_images"
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Користење на помал, побрз модел (SegMind Tiny SD - само 150MB!)
            model_id = "segmind/tiny-sd"
            
            print("  Downloading model (first time only, ~150MB)...")
            
            # Вчитување со оптимизации за CPU
            self.pipe = DiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Преместување на CPU (работи без GPU)
            self.pipe = self.pipe.to("cpu")
            
            print("  ✓ AI image generator loaded!")
            print("  Note: Generation takes 30-60 seconds on CPU")
            
            self.available = True
            
        except Exception as e:
            # Ако AI моделот не може да се вчита, користи едноставен генератор
            print(f"  Could not load AI model: {e}")
            print("  Falling back to simple generator")
            self.available = False
            self.simple_gen = SimpleImageGenerator()
    
    def generate(self, prompt):
        # Генерирање на слика користејќи AI или едноставен генератор
        
        # Ако AI не е достапен, користи едноставен генератор
        if not self.available:
            return self.simple_gen.generate(prompt)
        
        try:
            print(f"  Generating AI image for: '{prompt}'")
            print("  Please wait 30-60 seconds...")
            
            # Генерирање со ниски чекори за побрзо (помалку квалитет, повеќе брзина)
            image = self.pipe(
                prompt,
                num_inference_steps=20,  # Помалку = побрзо
                guidance_scale=7.5,
                height=512,
                width=512
            ).images[0]
            
            # Зачувување на сликата
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_img_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            image.save(filepath)
            
            return f"✓ AI Image generated successfully!\n\nSaved to: {filepath}\n\nPrompt: {prompt}\n\nModel: SegMind Tiny-SD (150MB lightweight AI)"
            
        except Exception as e:
            # Ако AI генерирањето не успее, користи едноставен генератор
            print(f"  AI generation failed: {e}")
            print("  Falling back to simple generator")
            return SimpleImageGenerator().generate(prompt)


# Тест функција
if __name__ == "__main__":
    print("\nImage Generator Test")
    print("=" * 50)
    print("\n1. Simple Geometric Generator (No AI)")
    print("2. AI Image Generator (Tiny-SD, 150MB)")
    
    choice = input("\nChoose (1 or 2): ").strip()
    
    if choice == "2":
        gen = AIImageGenerator()
    else:
        gen = SimpleImageGenerator()
    
    result = gen.generate("a beautiful sunset over mountains")
    print("\n" + result)