import argparse
from uploader import BulkUploader

def main():
    parser = argparse.ArgumentParser(description='Cargador masivo de MercadoLibre')
    parser.add_argument('--batch-size', type=int, help='Cantidad de productos a procesar')
    parser.add_argument('--dry-run', action='store_true', help='Simular sin subir a MercadoLibre')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("MLUploader - Carga Masiva MercadoLibre")
    if args.dry_run:
        print("MODO SIMULACIÓN (DRY-RUN)")
    print("=" * 50)
    
    uploader = BulkUploader(dry_run=args.dry_run)
    results = uploader.process_batch()
    
    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)
    print(f"Total procesados: {results['total']}")
    print(f"✓ Exitosos: {results['success']}")
    print(f"✗ Fallidos: {results['failed']}")
    print(f"⊘ Saltados: {results['skipped']}")
    print("=" * 50)
    
    if args.dry_run:
        print("\nEste fue un DRY-RUN. Para subir realmente, ejecutá:")
        print("   python main.py")

if __name__ == "__main__":
    main()