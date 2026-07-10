class SimpleEmotionDetector:
    # Едноставен детектор на емоции базиран на клучни зборови
    
    def __init__(self):
        print("  Using keyword-based emotion detector")
        
        # Речник на клучни зборови за секоја емоција
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'great', 'wonderful', 'awesome', 'love', 'amazing', 'fantastic', 'good', 'nice'],
            'sad': ['sad', 'sorry', 'unfortunately', 'bad', 'terrible', 'awful', 'wrong', 'error', 'failed', 'lost'],
            'excited': ['exciting', 'wow', 'incredible', 'outstanding', 'brilliant', '!!!', 'awesome'],
            'confused': ['confused', 'unclear', 'what', 'how', '??', 'understand', 'confusing'],
            'curious': ['why', 'how', 'what', 'when', 'where', 'curious', 'wonder', 'interesting'],
        }
        
        print("  ✓ Emotion detector ready")
    
    def detect_emotion(self, text):
        # Детектирање на емоција од клучни зборови во текстот
        if not text:
            return 'neutral', 0.5
        
        # Конвертирање на текстот во мали букви
        text_lower = text.lower()
        
        # Бројање на индикатори за емоција
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            # Броење колку пати се појавува секој клучен збор
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Наоѓање на доминантната емоција
        max_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[max_emotion]
        
        # Ако нема најдени клучни зборови, врати neutral
        if max_score == 0:
            return 'neutral', 0.5
        
        # Пресметка на доверба (confidence) - максимум 1.0
        confidence = min(max_score / 5.0, 1.0)
        return max_emotion, confidence
    
    def get_voice_parameters(self, emotion):
        # Добивање на параметри за гласот според емоцијата
        # Формат: (брзина, јачина, висина)
        
        emotion_params = {
            'happy': (170, 0.95, 1.1),      # Побрзо, погласно, повисоко
            'excited': (180, 1.0, 1.2),     # Многу брзо, многу гласно, високо
            'sad': (140, 0.7, 0.9),         # Полека, тивко, ниско
            'neutral': (160, 0.9, 1.0),     # Нормално
            'confused': (150, 0.85, 1.05),  # Малку полека
            'curious': (165, 0.9, 1.1),     # Нормално-брзо, малку повисоко
        }
        
        # Враќање на параметри или стандардни ако емоцијата не постои
        return emotion_params.get(emotion, (160, 0.9, 1.0))


# Тест функција
if __name__ == "__main__":
    # Креирање на детектор
    detector = SimpleEmotionDetector()
    
    # Тест реченици
    tests = [
        "I'm so happy to help you!",
        "Unfortunately, there was an error.",
        "What is artificial intelligence?",
        "This is absolutely incredible!!!",
    ]
    
    # Тестирање на секоја реченица
    for text in tests:
        emotion, conf = detector.detect_emotion(text)
        print(f"{text[:30]}... → {emotion} ({conf:.2f})")