import hashlib
from pathlib import Path
from datetime import datetime

# 1 Solicitar al usuario la ruta de la carpeta a organizar
RUTA = Path(input("Ingresa la ruta completa de tu carpeta de Descargas (ejemplo: C:/Users/TuUsuario/Downloads): ")) 

CATEGORIAS = {
    # Documentos
    '.pdf': 'Documentos', '.docx': 'Documentos', '.txt': 'Documentos', '.csv': 'Documentos',
    # Imágenes
    '.jpg': 'Imágenes', '.jpeg': 'Imágenes', '.png': 'Imágenes', '.gif': 'Imágenes',
    # Programas/Comprimidos
    '.exe': 'Programas', '.msi': 'Programas', '.dmg': 'Programas', 
    '.zip': 'Comprimidos', '.rar': 'Comprimidos',
    # Videos
    '.mp4': 'Videos', '.mov': 'Videos', '.avi': 'Videos', '.mkv': 'Videos',
    # Música
    '.mp3': 'Música'
}
# Funcion para calcular hash SHA-256 del archivo
def calcular_hash_sha256(ruta_archivo):
    """Calcula el hash SHA-256 de un archivo dado su ruta."""
    sha256_hash = hashlib.sha256()
    with ruta_archivo.open("rb") as f:
        # Leer y actualizar el hash en bloques de 4K
        for byte_block in iter(lambda: f.read(4096), b""): # lee el archivo en bloques de 4096 bytes
            sha256_hash.update(byte_block) # actualiza el hash con el bloque leido 
    return sha256_hash.hexdigest() # devuelve el hash en formato hexadecimal

#  Inicializar un diccionario para rastrear archivos vistos
archivos_vistos = {}
#  Recorrer la carpeta 
for item in RUTA.iterdir():
    # Verificar si es un archivo
   if item.is_file():
        try:
            # 1. CALCULAR HASH Y OBTENER FECHA
            hash_archivo = calcular_hash_sha256(item)
            timestamp_modificacion = item.stat().st_mtime
            fecha_modificacion = datetime.fromtimestamp(timestamp_modificacion)
            
            # 2. Verificar si el archivo es un duplicado
            if hash_archivo in archivos_vistos:
            
                # Recuperar la info del archivo original
                nombre_original, fecha_original = archivos_vistos[hash_archivo]

                if fecha_modificacion > fecha_original:
                    # si el archivo actual (iterando) es mas nuevo, eliminamos el original
                    print(f'¡Duplicado encontrado!, Eliminando: {nombre_original}')
                    item.unlink()
                    
                else:
                    # si el archivo actual es igual o mas viejo, eliminamos el actual
                    print(f'Duplicado eliminado: {item.name}. Se conserva la versión original: {nombre_original}')
                    item.unlink()

                continue # Pasa al siguiente elemento

            else:
                # 3. Archivo nuevo: Registrar y renombrar
                
                # Registrar el archivo único (hash: (nombre, fecha_modificacion))
                archivos_vistos[hash_archivo] = (item.name, fecha_modificacion)
                
                # Obtener partes para el nuevo nombre
                extension = item.suffix.lower()
                nombre_base = item.name
                
                # Quitamos sufijos comunes de copia/descarga
                patrones_a_eliminar = [' (_copia_)', '(copia)', ' - copia', ' - Copy', '(1)', '(2)', '(3)', ' - (1)', ' - (2)', ' - (3)']
                
                for patron in patrones_a_eliminar:
                    nombre_base = nombre_base.replace(patron, '')
                    
                nombre_base = nombre_base.strip() # Limpia espacios al inicio/final

        
        except Exception as e:
            # Manejo de errores por si no se puede leer un archivo
            print(f'⚠️ Error al procesar {item.name}: {e}')
            continue
        
        # Obtener la extensión del archivo
        extension = item.suffix.lower()
        
        #  Determinar la categoría del archivo
        if extension in CATEGORIAS:
            categoria = CATEGORIAS[extension]

            # Crear la carpeta de categoría si no existe
            carpeta_destino = RUTA / categoria
            
            if not carpeta_destino.exists():
                carpeta_destino.mkdir()
            
            # Mover el archivo a la carpeta correspondiente
            destino = carpeta_destino / nombre_base
            item.rename(destino)
            print(f'Movido: {item.name} --> {categoria}/')
   else:
    print(f'Saltando carpeta: {item.name}') 
print("Organización completada.")
            


