import os
import shutil

def get_folder_size(folder_path):
    """Пресметка на големината на папка во MB"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except Exception as e:
        print(f"Грешка: {e}")
    return total_size / (1024 * 1024)  # Конвертирај во MB

def cleanup_huggingface_cache():
    """Чистење на Hugging Face cache"""
    
    print("=" * 60)
    print("Hugging Face Cache Cleanup Tool")
    print("=" * 60)
    
    # Hugging Face cache локација
    cache_dir = os.path.expanduser("~/.cache/huggingface")
    
    # На Windows, понекогаш е на друга локација
    if os.name == 'nt':  # Windows
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface")
    
    if not os.path.exists(cache_dir):
        print(f"\n✓ Cache папката не постои: {cache_dir}")
        print("Нема ништо за чистење!")
        return
    
    # Прикажи големина
    cache_size = get_folder_size(cache_dir)
    print(f"\nCache локација: {cache_dir}")
    print(f"Тековна големина: {cache_size:.2f} MB")
    
    # Листа на модели во cache
    hub_dir = os.path.join(cache_dir, "hub")
    if os.path.exists(hub_dir):
        print(f"\nМодели во cache:")
        models = [d for d in os.listdir(hub_dir) if os.path.isdir(os.path.join(hub_dir, d))]
        for i, model in enumerate(models, 1):
            model_path = os.path.join(hub_dir, model)
            model_size = get_folder_size(model_path)
            print(f"  {i}. {model} ({model_size:.2f} MB)")
    
    # Прашај за потврда
    print(f"\n{'='*60}")
    print("ПРЕДУПРЕДУВАЊЕ: Ова ќе ги избрише сите кеширани модели!")
    print("Ќе треба да ги преземеш повторно кога ги користиш.")
    print(f"{'='*60}")
    
    choice = input("\nДали сакаш да продолжиш? (yes/no): ").lower().strip()
    
    if choice in ['yes', 'y', 'да']:
        try:
            # Бришење на целиот cache
            shutil.rmtree(cache_dir)
            print(f"\n✓ Cache е исчистен! Ослободени ~{cache_size:.2f} MB")
            print(f"✓ Папката {cache_dir} е избришана.")
        except Exception as e:
            print(f"\n✗ Грешка при бришење: {e}")
            print("\nПробај рачно да ја избришеш папката:")
            print(f"  {cache_dir}")
    else:
        print("\n✗ Откажано. Ништо не е избришано.")

def cleanup_specific_model(model_name):
    """Бришење на специфичен модел од cache"""
    
    cache_dir = os.path.expanduser("~/.cache/huggingface")
    if os.name == 'nt':
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface")
    
    hub_dir = os.path.join(cache_dir, "hub")
    
    if not os.path.exists(hub_dir):
        print("Cache не постои.")
        return
    
    # Најди го моделот
    models = [d for d in os.listdir(hub_dir) if model_name.lower() in d.lower()]
    
    if not models:
        print(f"Моделот '{model_name}' не е најден во cache.")
        return
    
    for model in models:
        model_path = os.path.join(hub_dir, model)
        model_size = get_folder_size(model_path)
        
        print(f"\nНајден: {model} ({model_size:.2f} MB)")
        choice = input("Избриши? (yes/no): ").lower().strip()
        
        if choice in ['yes', 'y', 'да']:
            try:
                shutil.rmtree(model_path)
                print(f"✓ Избришан! Ослободени {model_size:.2f} MB")
            except Exception as e:
                print(f"✗ Грешка: {e}")

def main():
    print("\n" + "=" * 60)
    print("ИЗБЕРИ ОПЦИЈА:")
    print("=" * 60)
    print("1. Исчисти го целиот Hugging Face cache")
    print("2. Избриши специфичен модел (GPT-2 Large)")
    print("3. Прикажи информации за cache (без бришење)")
    print("4. Излез")
    print("=" * 60)
    
    choice = input("\nИзбери (1-4): ").strip()
    
    if choice == "1":
        cleanup_huggingface_cache()
    elif choice == "2":
        print("\nКој модел сакаш да го избришеш?")
        print("Пример: gpt2-large, bloom, opt")
        model = input("Име на модел: ").strip()
        cleanup_specific_model(model)
    elif choice == "3":
        cache_dir = os.path.expanduser("~/.cache/huggingface")
        if os.name == 'nt':
            cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface")
        
        if os.path.exists(cache_dir):
            size = get_folder_size(cache_dir)
            print(f"\nCache локација: {cache_dir}")
            print(f"Вкупна големина: {size:.2f} MB ({size/1024:.2f} GB)")
        else:
            print("\nCache не постои.")
    else:
        print("\nИзлез.")

if __name__ == "__main__":
    main()