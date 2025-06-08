# download_model.py
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- Configuración de la descarga ---
# Define el nombre del modelo de Hugging Face Hub que quieres descargar.
# Usaremos GPT-Neo-1.3B, que es un buen equilibrio entre tamaño y capacidad para empezar.
# Asegúrate de tener suficiente RAM/VRAM (aproximadamente 5-8GB).
model_name = "EleutherAI/gpt-neo-1.3B"

# Define el directorio donde se guardará el modelo.
# Se creará (o se usará) una carpeta llamada 'modelo_neo' en la misma ubicación que este script.
save_directory = "modelo_neo"

# --- Proceso de descarga y guardado ---
print(f"Iniciando descarga y guardado del modelo '{model_name}'...")

# Crear el directorio si no existe
if not os.path.exists(save_directory):
    os.makedirs(save_directory)
    print(f"Directorio '{save_directory}' creado.")
else:
    print(f"Directorio '{save_directory}' ya existe. Se sobrescribirán los archivos existentes.")

try:
    print(f"Descargando tokenizer para '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(save_directory)
    print("Tokenizer descargado y guardado correctamente.")

    print(f"Descargando modelo para '{model_name}'...")
    # Si tienes GPU, Transformers usará CUDA automáticamente si está disponible y PyTorch lo soporta.
    # Para forzar CPU: model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32).to('cpu')
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.save_pretrained(save_directory)
    print("Modelo descargado y guardado correctamente.")

    print(f"\n¡Descarga y guardado completado en '{save_directory}'!")
    print("Ahora puedes ejecutar 'app.py' sin problemas de carga del modelo.")

except Exception as e:
    print(f"\nError durante la descarga o el guardado del modelo: {e}")
    print("Por favor, asegúrate de tener una conexión a internet estable, suficiente espacio en disco,")
    print("y que tu entorno 'bot_env' esté activado con las librerías 'transformers' y 'torch' instaladas.")